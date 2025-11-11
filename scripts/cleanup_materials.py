#!/usr/bin/env python3
"""
Source Materials Cleanup Tool

清理 ~/skill-materials/ 中的临时材料

Usage:
    # 交互式清理（列出所有材料，询问是否删除）
    cleanup_materials.py

    # 清理特定项目
    cleanup_materials.py awesome-tool

    # 清理所有材料（危险！会先确认）
    cleanup_materials.py --all

    # 列出所有材料（不删除）
    cleanup_materials.py --list

    # 强制删除（无确认）
    cleanup_materials.py awesome-tool --force
"""

import os
import sys
import argparse
import shutil
from pathlib import Path


def find_project_root(start_path=None):
    """
    查找项目根目录（包含 .git 或 .claude/ 的目录）

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

    # 向上查找，直到根目录
    while current != current.parent:
        # 检查是否有 .git 或 .claude
        if (current / '.git').exists() or (current / '.claude').exists():
            return current
        current = current.parent

    return None


def get_materials_dirs():
    """
    获取材料目录路径（支持两种模式）

    Returns:
        List of (path, mode_name) tuples
    """
    dirs = []

    # 检查项目模式
    project_root = find_project_root()
    if project_root:
        project_materials = project_root / '.claude' / 'temp-materials'
        if project_materials.exists():
            dirs.append((project_materials, 'project'))

    # 检查全局模式
    global_materials = Path.home() / 'skill-materials'
    if global_materials.exists():
        dirs.append((global_materials, 'global'))

    return dirs


def get_materials_dir():
    """获取材料目录路径（兼容旧版，优先返回项目模式）"""
    dirs = get_materials_dirs()
    if dirs:
        return dirs[0][0]  # 返回第一个可用的

    # 如果都不存在，返回智能默认值
    project_root = find_project_root()
    if project_root:
        return project_root / '.claude' / 'temp-materials'
    else:
        return Path.home() / 'skill-materials'


def get_dir_size(path):
    """计算目录大小（字节）"""
    total = 0
    try:
        for entry in os.scandir(path):
            if entry.is_file(follow_symlinks=False):
                total += entry.stat().st_size
            elif entry.is_dir(follow_symlinks=False):
                total += get_dir_size(entry.path)
    except PermissionError:
        pass
    return total


def format_size(bytes_size):
    """格式化文件大小"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes_size < 1024.0:
            return f"{bytes_size:.1f} {unit}"
        bytes_size /= 1024.0
    return f"{bytes_size:.1f} TB"


def list_materials():
    """列出所有材料及其大小（支持两个位置）"""
    dirs = get_materials_dirs()

    if not dirs:
        print(f"\n📂 No materials directories found")
        print(f"   Checked:")
        project_root = find_project_root()
        if project_root:
            print(f"   - {project_root}/.claude/temp-materials/ (project mode)")
        print(f"   - ~/skill-materials/ (global mode)")
        return []

    materials = []

    for materials_dir, mode in dirs:
        for item in sorted(materials_dir.iterdir()):
            if item.is_dir() and not item.name.startswith('.'):
                size = get_dir_size(item)
                materials.append({
                    'name': item.name,
                    'path': item,
                    'size': size,
                    'size_str': format_size(size),
                    'mode': mode
                })

    return materials


def print_materials_list(materials):
    """打印材料列表"""
    if not materials:
        print("\n✅ No materials found")
        return

    # 按模式分组
    project_materials = [m for m in materials if m['mode'] == 'project']
    global_materials = [m for m in materials if m['mode'] == 'global']

    print(f"\n📂 Source materials:\n")

    index = 1
    total_size = 0

    # 项目模式材料
    if project_materials:
        project_root = find_project_root()
        print(f"  📍 Project mode ({project_root}/.claude/temp-materials/):")
        for mat in project_materials:
            print(f"     {index}. {mat['name']:<28} {mat['size_str']:>10}")
            total_size += mat['size']
            index += 1
        print()

    # 全局模式材料
    if global_materials:
        print(f"  🌍 Global mode (~/skill-materials/):")
        for mat in global_materials:
            print(f"     {index}. {mat['name']:<28} {mat['size_str']:>10}")
            total_size += mat['size']
            index += 1
        print()

    print(f"  Total: {len(materials)} projects, {format_size(total_size)}")


def confirm_deletion(name, size_str):
    """确认删除操作"""
    print(f"\n⚠️  About to delete: {name} ({size_str})")
    response = input("   Confirm deletion? (y/n): ").strip().lower()
    return response == 'y'


def delete_material(material, force=False):
    """删除单个材料"""
    if not force:
        if not confirm_deletion(material['name'], material['size_str']):
            print("   Skipped")
            return False

    try:
        shutil.rmtree(material['path'])
        print(f"   ✅ Deleted: {material['name']} ({material['size_str']})")
        return True
    except Exception as e:
        print(f"   ❌ Error deleting {material['name']}: {e}")
        return False


def interactive_cleanup():
    """交互式清理"""
    materials = list_materials()

    if not materials:
        return

    print_materials_list(materials)

    print("\n💡 Options:")
    print("   1-N: Delete specific project")
    print("   'all': Delete all materials")
    print("   'quit': Exit without deleting")

    while True:
        response = input("\nYour choice: ").strip().lower()

        if response == 'quit':
            print("\nExiting without changes")
            break

        if response == 'all':
            print(f"\n⚠️  WARNING: This will delete ALL {len(materials)} materials!")
            confirm = input("   Type 'DELETE ALL' to confirm: ").strip()
            if confirm == 'DELETE ALL':
                deleted_count = 0
                for mat in materials:
                    if delete_material(mat, force=False):
                        deleted_count += 1
                print(f"\n✅ Deleted {deleted_count}/{len(materials)} materials")
            else:
                print("   Cancelled")
            break

        # 尝试解析为数字
        try:
            index = int(response) - 1
            if 0 <= index < len(materials):
                delete_material(materials[index], force=False)
            else:
                print(f"   Invalid index. Choose 1-{len(materials)}")
        except ValueError:
            print("   Invalid input. Try again or type 'quit'")


def cleanup_specific(name, force=False):
    """清理特定材料（在两个位置搜索）"""
    dirs = get_materials_dirs()

    if not dirs:
        # 如果没有现有目录，尝试智能默认位置
        dirs = [(get_materials_dir(), 'auto')]

    target_path = None
    mode = None

    # 在所有可能的位置搜索
    for materials_dir, dir_mode in dirs:
        candidate = materials_dir / name
        if candidate.exists():
            target_path = candidate
            mode = dir_mode
            break

    if not target_path:
        print(f"\n❌ Material not found: {name}")
        print(f"   Searched in:")
        for materials_dir, dir_mode in dirs:
            print(f"   - {materials_dir} ({dir_mode} mode)")
        return False

    size = get_dir_size(target_path)
    size_str = format_size(size)

    material = {
        'name': name,
        'path': target_path,
        'size': size,
        'size_str': size_str,
        'mode': mode
    }

    print(f"   Found in: {mode} mode - {target_path.parent}")

    return delete_material(material, force=force)


def cleanup_all(force=False):
    """清理所有材料"""
    materials = list_materials()

    if not materials:
        return

    print_materials_list(materials)

    if not force:
        print(f"\n⚠️  WARNING: This will delete ALL {len(materials)} materials!")
        confirm = input("   Type 'DELETE ALL' to confirm: ").strip()
        if confirm != 'DELETE ALL':
            print("   Cancelled")
            return

    deleted_count = 0
    for mat in materials:
        try:
            shutil.rmtree(mat['path'])
            deleted_count += 1
            print(f"   ✅ Deleted: {mat['name']} ({mat['size_str']})")
        except Exception as e:
            print(f"   ❌ Error deleting {mat['name']}: {e}")

    print(f"\n✅ Deleted {deleted_count}/{len(materials)} materials")


def main():
    parser = argparse.ArgumentParser(
        description='Clean up source materials from ~/skill-materials/',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Interactive cleanup (list and choose what to delete)
  %(prog)s

  # Delete specific material
  %(prog)s awesome-tool

  # List all materials without deleting
  %(prog)s --list

  # Delete all materials (with confirmation)
  %(prog)s --all

  # Force delete without confirmation (dangerous!)
  %(prog)s awesome-tool --force
        """
    )

    parser.add_argument('name', nargs='?',
                       help='Specific material name to delete')
    parser.add_argument('--list', '-l', action='store_true',
                       help='List all materials without deleting')
    parser.add_argument('--all', '-a', action='store_true',
                       help='Delete all materials')
    parser.add_argument('--force', '-f', action='store_true',
                       help='Force delete without confirmation')

    args = parser.parse_args()

    print("\n" + "="*60)
    print("SOURCE MATERIALS CLEANUP")
    print("="*60)

    # List mode
    if args.list:
        materials = list_materials()
        print_materials_list(materials)
        return

    # Delete all mode
    if args.all:
        cleanup_all(force=args.force)
        return

    # Delete specific material
    if args.name:
        cleanup_specific(args.name, force=args.force)
        return

    # Interactive mode (default)
    interactive_cleanup()


if __name__ == '__main__':
    main()
