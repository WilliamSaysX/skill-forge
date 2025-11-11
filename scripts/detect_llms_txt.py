#!/usr/bin/env python3
"""
llms.txt Detector - 检测文档站点的 llms.txt 文件

llms.txt 是一个新兴标准，让文档网站提供 LLM 友好的内容索引。
详见: https://llmstxt.org/

支持的变体:
- llms-full.txt: 完整版（包含所有内容）
- llms.txt: 标准版（核心内容）
- llms-small.txt: 精简版（快速概览）

Usage:
    # 检测单个 URL
    python scripts/detect_llms_txt.py https://react.dev/

    # 检测所有变体
    python scripts/detect_llms_txt.py https://react.dev/ --all

    # 作为模块使用
    from detect_llms_txt import detect_llms_txt
    result = detect_llms_txt("https://react.dev/")
"""

import sys
import requests
from urllib.parse import urlparse
from typing import Optional, Dict, List


# 支持的 llms.txt 变体（按优先级排序）
LLMS_TXT_VARIANTS = [
    ('llms-full.txt', 'full'),      # 完整版 - 最优先
    ('llms.txt', 'standard'),        # 标准版
    ('llms-small.txt', 'small')      # 精简版
]


def detect_llms_txt(base_url: str, timeout: int = 5) -> Optional[Dict[str, str]]:
    """
    检测可用的 llms.txt 变体（返回第一个找到的）

    Args:
        base_url: 文档网站 URL
        timeout: 请求超时时间（秒）

    Returns:
        Dict with 'url' and 'variant' keys, or None if not found

    Example:
        >>> result = detect_llms_txt("https://react.dev/")
        >>> print(result)
        {'url': 'https://react.dev/llms-full.txt', 'variant': 'full'}
    """
    parsed = urlparse(base_url)
    root_url = f"{parsed.scheme}://{parsed.netloc}"

    for filename, variant in LLMS_TXT_VARIANTS:
        url = f"{root_url}/{filename}"

        if _check_url_exists(url, timeout):
            return {
                'url': url,
                'variant': variant,
                'filename': filename
            }

    return None


def detect_all_variants(base_url: str, timeout: int = 5) -> List[Dict[str, str]]:
    """
    检测所有可用的 llms.txt 变体

    Args:
        base_url: 文档网站 URL
        timeout: 请求超时时间（秒）

    Returns:
        List of dicts with 'url' and 'variant' keys for each found variant

    Example:
        >>> results = detect_all_variants("https://react.dev/")
        >>> for r in results:
        ...     print(f"{r['variant']}: {r['url']}")
    """
    parsed = urlparse(base_url)
    root_url = f"{parsed.scheme}://{parsed.netloc}"

    found_variants = []

    for filename, variant in LLMS_TXT_VARIANTS:
        url = f"{root_url}/{filename}"

        if _check_url_exists(url, timeout):
            found_variants.append({
                'url': url,
                'variant': variant,
                'filename': filename
            })

    return found_variants


def download_llms_txt(url: str, output_path: str, timeout: int = 10) -> bool:
    """
    下载 llms.txt 文件内容

    Args:
        url: llms.txt 文件 URL
        output_path: 保存路径
        timeout: 请求超时时间（秒）

    Returns:
        True if successful, False otherwise
    """
    try:
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(response.text)

        return True
    except Exception as e:
        print(f"Download failed: {e}")
        return False


def _check_url_exists(url: str, timeout: int) -> bool:
    """
    检查 URL 是否存在（返回 200 状态码）

    使用 HEAD 请求以提高效率
    """
    try:
        response = requests.head(url, timeout=timeout, allow_redirects=True)
        return response.status_code == 200
    except requests.RequestException:
        return False


def main():
    """命令行接口"""
    if len(sys.argv) < 2:
        print(__doc__)
        print("\nExamples:")
        print("  python scripts/detect_llms_txt.py https://react.dev/")
        print("  python scripts/detect_llms_txt.py https://fastapi.tiangolo.com/ --all")
        sys.exit(1)

    base_url = sys.argv[1]
    detect_all = '--all' in sys.argv

    print(f"🔍 Detecting llms.txt at: {base_url}\n")

    if detect_all:
        results = detect_all_variants(base_url)

        if results:
            print(f"✅ Found {len(results)} variant(s):\n")
            for r in results:
                print(f"  {r['variant']:8} → {r['url']}")
        else:
            print("❌ No llms.txt variants found")
            print("\n💡 This site may not support the llms.txt standard.")
            print("   Learn more: https://llmstxt.org/")
    else:
        result = detect_llms_txt(base_url)

        if result:
            print(f"✅ Found: {result['url']}")
            print(f"   Variant: {result['variant']}")
            print(f"\n💡 Use this URL for faster documentation extraction:")
            print(f"   python scripts/fetch_source.py --docs {result['url']} --name myskill")
        else:
            print("❌ No llms.txt found")
            print("\n💡 This site may not support the llms.txt standard.")
            print("   You can still scrape it normally with fetch_source.py")


if __name__ == '__main__':
    main()
