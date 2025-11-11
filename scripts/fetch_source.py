#!/usr/bin/env python3
"""
Source Material Fetcher for Skill Forge

统一获取创建 skill 所需的源材料（Git 仓库、在线文档、PDF、Office 文档等）

Usage:
    # 从 GitHub 克隆仓库
    fetch_source.py --git https://github.com/user/repo
    fetch_source.py --git https://github.com/user/repo --output ~/my-materials/repo-name
    fetch_source.py --git https://github.com/user/repo --depth 1 --branch main

    # 从在线文档抓取（使用 markitdown）
    fetch_source.py --docs https://docs.example.com --name example-docs

    # PDF 文档（URL 或本地文件）
    fetch_source.py --docs https://example.com/manual.pdf --name manual
    fetch_source.py --docs /path/to/document.pdf --name doc

    # Office 文档（DOCX, PPTX, XLSX）
    fetch_source.py --docs /path/to/spec.docx --name spec

    # 混合模式：同时克隆仓库和抓取文档
    fetch_source.py --git https://github.com/user/repo --docs https://docs.example.com --name combo

Requirements:
    - git (for --git)
    - markitdown (for --docs): pip install 'markitdown[all]'
        Supports: HTML, PDF, DOCX, PPTX, XLSX

Options:
    --git URL               Git 仓库 URL
    --docs URL/PATH         文档 URL 或本地文件路径（HTML/PDF/DOCX/PPTX/XLSX）
    --name NAME             项目名称（用于 docs 模式）
    --output PATH           输出目录（默认：智能选择）
    --depth N               Git 克隆深度（默认：完整历史）
    --branch NAME           指定分支（默认：默认分支）
    --single-branch         只克隆单个分支
    --clean                 如果目标目录存在，先清理
"""

import os
import sys
import argparse
import subprocess
import shutil
from pathlib import Path
from urllib.parse import urlparse

# 尝试导入 llms.txt 检测器（如果在同目录下）
try:
    script_dir = Path(__file__).parent
    sys.path.insert(0, str(script_dir))
    from detect_llms_txt import detect_llms_txt, download_llms_txt
    LLMS_TXT_AVAILABLE = True
except ImportError:
    LLMS_TXT_AVAILABLE = False


def find_project_root(start_path=None):
    """
    查找项目根目录（包含 .git 或 .claude/ 的目录）

    排除 skill-forge 工具目录本身

    Args:
        start_path: 开始搜索的路径（默认当前目录）

    Returns:
        Path object 或 None
    """
    if start_path is None:
        start_path = Path.cwd()
    else:
        start_path = Path(start_path)

    current = start_path.resolve()

    # 检测 skill-forge 工具目录（通过检查是否有 SKILL.md 且名称为 skill-forge）
    script_dir = Path(__file__).parent.parent.resolve()  # skill-forge/
    is_skill_forge_dir = (script_dir / 'SKILL.md').exists() and script_dir.name == 'skill-forge'

    # 向上查找，直到根目录
    while current != current.parent:
        # 检查是否有 .git 或 .claude
        if (current / '.git').exists() or (current / '.claude').exists():
            # 排除 skill-forge 工具目录本身
            if is_skill_forge_dir and current == script_dir:
                current = current.parent
                continue
            return current
        current = current.parent

    return None


def get_smart_materials_dir(project_name):
    """
    智能选择材料目录

    - 如果在项目中：<项目根>/.claude/temp-materials/
    - 如果全局环境：~/skill-materials/

    Returns:
        (materials_base_dir, is_project_mode)
    """
    project_root = find_project_root()

    if project_root:
        # 项目模式
        materials_base = project_root / '.claude' / 'temp-materials'
        return materials_base, True
    else:
        # 全局模式
        materials_base = Path.home() / 'skill-materials'
        return materials_base, False


def get_repo_name(git_url):
    """从 Git URL 提取仓库名称"""
    # https://github.com/user/repo.git -> repo
    # https://github.com/user/repo -> repo
    path = urlparse(git_url).path
    name = path.rstrip('/').split('/')[-1]
    if name.endswith('.git'):
        name = name[:-4]
    return name


def clone_repository(git_url, output_dir, depth=None, branch=None, single_branch=False):
    """克隆 Git 仓库"""
    print(f"\n{'='*60}")
    print(f"CLONING REPOSITORY")
    print(f"{'='*60}")
    print(f"URL: {git_url}")
    print(f"Output: {output_dir}")

    cmd = ['git', 'clone']

    # 添加选项
    if depth:
        cmd.extend(['--depth', str(depth)])
    if branch:
        cmd.extend(['--branch', branch])
    if single_branch:
        cmd.append('--single-branch')

    cmd.extend([git_url, str(output_dir)])

    print(f"\nCommand: {' '.join(cmd)}\n")

    try:
        subprocess.run(cmd, check=True)
        print(f"\n✅ Clone successful: {output_dir}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Clone failed: {e}")
        return False
    except FileNotFoundError:
        print("\n❌ Error: 'git' command not found")
        print("   Please install git first")
        return False


def get_directory_stats(directory):
    """统计目录信息"""
    stats = {
        'total_files': 0,
        'py_files': 0,
        'md_files': 0,
        'js_files': 0,
        'json_files': 0,
        'total_size': 0
    }

    for root, dirs, files in os.walk(directory):
        # 跳过 .git 目录
        if '.git' in root:
            continue

        for file in files:
            stats['total_files'] += 1
            filepath = os.path.join(root, file)

            try:
                stats['total_size'] += os.path.getsize(filepath)
            except OSError:
                pass

            if file.endswith('.py'):
                stats['py_files'] += 1
            elif file.endswith('.md'):
                stats['md_files'] += 1
            elif file.endswith('.js') or file.endswith('.jsx') or file.endswith('.ts') or file.endswith('.tsx'):
                stats['js_files'] += 1
            elif file.endswith('.json'):
                stats['json_files'] += 1

    return stats


def check_markitdown():
    """检查 markitdown 是否已安装"""
    try:
        from markitdown import MarkItDown
        return True
    except ImportError:
        return False


def fetch_documentation(docs_url, name, output_dir):
    """使用 markitdown 抓取在线文档"""
    print(f"\n{'='*60}")
    print(f"FETCHING DOCUMENTATION")
    print(f"{'='*60}")
    print(f"URL: {docs_url}")
    print(f"Name: {name}")

    # 🆕 检测 llms.txt（如果可用且不是直接的 llms.txt URL）
    if LLMS_TXT_AVAILABLE and not docs_url.endswith(('.txt', 'llms.txt')):
        print(f"\n🔍 Checking for llms.txt...")
        llms_result = detect_llms_txt(docs_url)

        if llms_result:
            print(f"✅ Found: {llms_result['url']} ({llms_result['variant']})")
            print(f"\n💡 llms.txt is 10x faster than full scraping!")
            print(f"   Recommended: Use the llms.txt URL instead:")
            print(f"   python scripts/fetch_source.py --docs {llms_result['url']} --name {name}")
            print(f"\n   Continuing with regular scrape...")
        else:
            print(f"❌ No llms.txt found, using regular scrape")

    # 检查 markitdown 是否安装
    if not check_markitdown():
        print(f"\n❌ MarkItDown not installed")
        print(f"\n💡 Install it with:")
        print(f"   pip install 'markitdown[all]'")
        print(f"\n   This enables conversion from:")
        print(f"   - HTML/documentation websites")
        print(f"   - PDF files (text-based PDFs work best)")
        print(f"   - Office documents (DOCX, PPTX, XLSX)")
        print(f"\n   Note: Scanned PDFs can be processed visually by AI")
        return False

    try:
        from markitdown import MarkItDown

        print(f"\n📥 Fetching documentation using MarkItDown...")

        # 创建 MarkItDown 实例
        md = MarkItDown()

        # 转换 URL
        result = md.convert(docs_url)

        # 保存到文件
        output_file = output_dir / f"{name}.md"
        output_file.write_text(result.text_content, encoding='utf-8')

        print(f"\n✅ Documentation fetched successfully")
        print(f"   Saved to: {output_file}")

        return True

    except Exception as e:
        print(f"\n❌ Documentation fetch failed: {e}")
        print(f"\n💡 You can manually save the documentation and use it as local files.")
        return False


def print_next_steps(output_dir, has_git, has_docs):
    """打印下一步操作提示"""
    print(f"\n{'='*60}")
    print("NEXT STEPS")
    print(f"{'='*60}\n")

    print("📂 Source materials are ready at:")
    print(f"   {output_dir}\n")

    # 统计信息
    stats = get_directory_stats(output_dir)
    print("📊 Directory contents:")
    print(f"   Total files: {stats['total_files']}")
    if stats['py_files'] > 0:
        print(f"   Python files: {stats['py_files']}")
    if stats['md_files'] > 0:
        print(f"   Markdown files: {stats['md_files']}")
    if stats['js_files'] > 0:
        print(f"   JavaScript/TypeScript files: {stats['js_files']}")
    if stats['json_files'] > 0:
        print(f"   JSON files: {stats['json_files']}")

    size_mb = stats['total_size'] / (1024 * 1024)
    print(f"   Total size: {size_mb:.2f} MB\n")

    print("🚀 To create a skill from these materials, tell Claude:\n")
    print(f'   "Create a skill from the materials in {output_dir}"')
    print("\n   Or be more specific:\n")
    print(f'   "Create a [skill name] skill from {output_dir}')
    print('    Focus on [specific aspect]')
    print('    Use [these files] for the main functionality"\n')

    print("💡 Claude will automatically:")
    print("   1. Analyze the directory structure")
    print("   2. Identify useful scripts, docs, and assets")
    print("   3. Organize them into scripts/, references/, assets/")
    print("   4. Generate SKILL.md with usage instructions")
    print("   5. Package the skill for distribution")


def main():
    parser = argparse.ArgumentParser(
        description='Fetch source materials for skill creation',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Clone a repository
  %(prog)s --git https://github.com/user/awesome-tool

  # Clone with shallow history (faster)
  %(prog)s --git https://github.com/user/repo --depth 1

  # Clone specific branch
  %(prog)s --git https://github.com/user/repo --branch develop

  # Scrape documentation
  %(prog)s --docs https://docs.example.com --name example

  # Both: clone repo + scrape docs
  %(prog)s --git https://github.com/user/repo --docs https://docs.example.com --name combo
        """
    )

    parser.add_argument('--git', type=str, metavar='URL',
                       help='Git repository URL to clone')
    parser.add_argument('--docs', type=str, metavar='URL',
                       help='Documentation URL to scrape')
    parser.add_argument('--name', type=str,
                       help='Project name (required for --docs)')
    parser.add_argument('--output', '-o', type=str, metavar='PATH',
                       help='Output directory (default: ~/skill-materials/<name>)')
    parser.add_argument('--depth', type=int, metavar='N',
                       help='Git clone depth (default: full history)')
    parser.add_argument('--branch', '-b', type=str,
                       help='Git branch to clone (default: default branch)')
    parser.add_argument('--single-branch', action='store_true',
                       help='Clone only a single branch')
    parser.add_argument('--clean', action='store_true',
                       help='Clean output directory if it exists')

    args = parser.parse_args()

    # 验证参数
    if not args.git and not args.docs:
        parser.error("At least one of --git or --docs is required")

    if args.docs and not args.name:
        parser.error("--name is required when using --docs")

    # 确定项目名称
    if args.git:
        project_name = get_repo_name(args.git)
    elif args.name:
        project_name = args.name
    else:
        parser.error("Cannot determine project name")

    # 确定输出目录
    if args.output:
        output_dir = Path(args.output).expanduser()
        is_project_mode = False  # 用户指定路径，视为手动模式
    else:
        # 智能路径选择
        materials_base, is_project_mode = get_smart_materials_dir(project_name)
        output_dir = materials_base / project_name

        # 显示模式信息
        if is_project_mode:
            project_root = find_project_root()
            print(f"\n📍 Project mode detected")
            print(f"   Project root: {project_root}")
            print(f"   Materials will be saved in project: .claude/temp-materials/")
        else:
            print(f"\n📍 Global mode")
            print(f"   Materials will be saved in: ~/skill-materials/")

    # 处理已存在的目录
    if output_dir.exists():
        if args.clean:
            print(f"\n🧹 Cleaning existing directory: {output_dir}")
            shutil.rmtree(output_dir)
        else:
            print(f"\n⚠️  Output directory already exists: {output_dir}")
            response = input("   Continue anyway? (y/n): ").strip().lower()
            if response != 'y':
                print("   Aborted")
                sys.exit(0)

    # 创建输出目录
    output_dir.mkdir(parents=True, exist_ok=True)

    success_git = False
    success_docs = False

    # 克隆 Git 仓库
    if args.git:
        success_git = clone_repository(
            args.git,
            output_dir,
            depth=args.depth,
            branch=args.branch,
            single_branch=args.single_branch
        )

        if not success_git:
            print("\n❌ Failed to clone repository")
            sys.exit(1)

    # 抓取文档
    if args.docs:
        docs_output = output_dir / 'docs_fetched'
        docs_output.mkdir(exist_ok=True)
        success_docs = fetch_documentation(args.docs, args.name, docs_output)

        if not success_docs:
            if args.git:
                print("\n⚠️  Documentation fetch failed, but repository was cloned")
            else:
                print("\n❌ Documentation fetch failed")
                sys.exit(1)

    # 打印下一步
    print_next_steps(output_dir, success_git, success_docs)


if __name__ == '__main__':
    main()
