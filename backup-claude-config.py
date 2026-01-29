#!/usr/bin/env python3
"""
Claude Code 配置备份工具
跨平台通用：Windows、macOS、Linux
支持 Python 3.6+
"""

import os
import sys
import shutil
import json
import platform
from datetime import datetime

# =============================================================================
# 全局配置
# =============================================================================

# Claude 配置路径（跨平台自动检测）
def get_claude_config_path():
    """获取 Claude 配置目录路径"""
    home = os.path.expanduser('~')
    return os.path.join(home, '.claude')

CLAUDE_CONFIG_PATH = get_claude_config_path()

# 默认备份路径
DEFAULT_BACKUP_PATH = os.path.join(os.path.expanduser('~'), 'claude-config-backup')

# 需要备份的项目
BACKUP_ITEMS = [
    {'source': 'agents', 'dest': 'agents'},
    {'source': 'commands', 'dest': 'commands'},
    {'source': 'rules', 'dest': 'rules'},
    {'source': 'contexts', 'dest': 'contexts'},
    {'source': 'skills', 'dest': 'skills'},
    {'source': 'settings.json', 'dest': 'settings.json'},
    {'source': '.claude.json', 'dest': 'claude.json'},
    {'source': 'CLAUDE.md', 'dest': 'CLAUDE.md'},
    {'source': 'config.json', 'dest': 'config.json'},
    {'source': 'plugins/known_marketplaces.json', 'dest': 'plugins/known_marketplaces.json'},
    {'source': 'plugins/installed_plugins.json', 'dest': 'plugins/installed_plugins.json'}
]

# 颜色输出（跨平台）
class Colors:
    """终端颜色类"""
    HEADER = '\033[95m' if sys.stdout.isatty() else ''
    OKBLUE = '\033[94m' if sys.stdout.isatty() else ''
    OKGREEN = '\033[92m' if sys.stdout.isatty() else ''
    WARNING = '\033[93m' if sys.stdout.isatty() else ''
    FAIL = '\033[91m' if sys.stdout.isatty() else ''
    ENDC = '\033[0m' if sys.stdout.isatty() else ''
    BOLD = '\033[1m' if sys.stdout.isatty() else ''
    UNDERLINE = '\033[4m' if sys.stdout.isatty() else ''

# =============================================================================
# 工具函数
# =============================================================================

def print_header():
    """打印头部信息"""
    print(Colors.HEADER + "=" * 60 + Colors.ENDC)
    print(Colors.BOLD + "Claude Code 配置备份工具" + Colors.ENDC)
    print(f"跨平台支持：Windows、macOS、Linux")
    print(f"当前系统：{platform.system()} {platform.release()}")
    print(f"Python 版本：{sys.version.split()[0]}")
    print(Colors.HEADER + "=" * 60 + Colors.ENDC)
    print()

def get_backup_path():
    """获取备份路径"""
    if len(sys.argv) > 1:
        backup_path = sys.argv[1]
    else:
        backup_path = DEFAULT_BACKUP_PATH

    return os.path.abspath(backup_path)

def create_backup_dir(backup_path):
    """创建备份目录"""
    if os.path.exists(backup_path):
        print(f"{Colors.WARNING}备份目录已存在: {backup_path}{Colors.ENDC}")
        try:
            choice = input("是否删除旧备份并重新备份？(y/n): ").strip().lower()
            if choice == 'y':
                shutil.rmtree(backup_path)
                print(f"{Colors.OKGREEN}已删除旧备份{Colors.ENDC}")
            else:
                print("备份已取消")
                sys.exit(0)
        except KeyboardInterrupt:
            print("\n操作已取消")
            sys.exit(0)

    try:
        os.makedirs(backup_path, exist_ok=True)
        print(f"{Colors.OKGREEN}创建备份目录: {backup_path}{Colors.ENDC}")
        print()
    except Exception as e:
        print(f"{Colors.FAIL}创建备份目录失败: {e}{Colors.ENDC}")
        sys.exit(1)

def backup_item(source, dest, backup_path):
    """备份单个项目"""
    source_path = os.path.join(CLAUDE_CONFIG_PATH, source)
    dest_path = os.path.join(backup_path, dest)

    print(f"正在备份: {source}")

    if not os.path.exists(source_path):
        print(f"  {Colors.WARNING}⚠ 不存在，跳过{Colors.ENDC}")
        return False

    try:
        # 确保目标目录存在
        dest_dir = os.path.dirname(dest_path)
        if dest_dir:
            os.makedirs(dest_dir, exist_ok=True)

        if os.path.isdir(source_path):
            # 备份目录
            shutil.copytree(source_path, dest_path, dirs_exist_ok=True)
        else:
            # 备份文件
            shutil.copy2(source_path, dest_path)

        print(f"  {Colors.OKGREEN}✓ 成功{Colors.ENDC}")
        return True
    except Exception as e:
        print(f"  {Colors.FAIL}✗ 失败: {e}{Colors.ENDC}")
        return False

def create_backup_info(backup_path, success_count, fail_count):
    """创建备份信息文件"""
    # 获取系统信息
    system_info = {
        'system': platform.system(),
        'release': platform.release(),
        'version': platform.version(),
        'machine': platform.machine(),
        'processor': platform.processor()
    }

    backup_info = {
        'backup_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'system_info': system_info,
        'computer_name': os.environ.get('COMPUTERNAME', os.environ.get('HOSTNAME', 'unknown')),
        'user_name': os.environ.get('USERNAME', os.environ.get('USER', 'unknown')),
        'success_count': success_count,
        'fail_count': fail_count,
        'backup_path': backup_path,
        'claude_config_path': CLAUDE_CONFIG_PATH,
        'platform_info': platform.platform()
    }

    info_path = os.path.join(backup_path, 'backup-info.json')
    try:
        with open(info_path, 'w', encoding='utf-8') as f:
            json.dump(backup_info, f, indent=2, ensure_ascii=False)
        return backup_info
    except Exception as e:
        print(f"{Colors.WARNING}创建备份信息文件失败: {e}{Colors.ENDC}")
        return backup_info

def check_dependencies():
    """检查依赖"""
    required_modules = ['os', 'sys', 'shutil', 'json', 'platform', 'datetime']
    missing = []

    for module in required_modules:
        try:
            __import__(module)
        except ImportError:
            missing.append(module)

    if missing:
        print(f"{Colors.FAIL}缺少必需的模块: {', '.join(missing)}{Colors.ENDC}")
        print("请安装 Python 3.6 或更高版本")
        sys.exit(1)

def print_success_message(backup_info):
    """打印成功消息"""
    print()
    print(Colors.OKGREEN + "=" * 60 + Colors.ENDC)
    print(Colors.BOLD + "备份完成！" + Colors.ENDC)
    print(Colors.OKGREEN + "=" * 60 + Colors.ENDC)
    print()
    print(f"备份位置: {backup_info['backup_path']}")
    print(f"备份时间: {backup_info['backup_date']}")
    print(f"系统信息: {backup_info['system_info']['system']} {backup_info['system_info']['release']}")
    print(f"计算机名: {backup_info['computer_name']}")
    print(f"用户名: {backup_info['user_name']}")
    print(f"成功项目: {backup_info['success_count']}")
    print(f"失败项目: {backup_info['fail_count']}")
    print()
    print(Colors.OKBLUE + "下一步：" + Colors.ENDC)
    print("1. 将备份目录传输到目标电脑")
    print("2. 在目标电脑上执行: python restore-claude-config-universal.py")
    print("3. 如果备份在自定义位置，使用: python restore-claude-config-universal.py <backup_path>")
    print()

# =============================================================================
# 主函数
# =============================================================================

def main():
    """主函数"""
    try:
        print_header()

        # 检查依赖
        check_dependencies()

        # 检查 Claude 配置目录
        if not os.path.exists(CLAUDE_CONFIG_PATH):
            print(f"{Colors.FAIL}错误: Claude 配置目录不存在: {CLAUDE_CONFIG_PATH}{Colors.ENDC}")
            print("请确保已安装 Claude Code")
            sys.exit(1)

        # 获取备份路径
        backup_path = get_backup_path()

        # 创建备份目录
        create_backup_dir(backup_path)

        # 开始备份
        success_count = 0
        fail_count = 0

        for item in BACKUP_ITEMS:
            if backup_item(item['source'], item['dest'], backup_path):
                success_count += 1
            else:
                fail_count += 1

        # 创建备份信息
        backup_info = create_backup_info(backup_path, success_count, fail_count)

        # 显示结果
        print_success_message(backup_info)

    except KeyboardInterrupt:
        print("\n\n操作已取消")
        sys.exit(0)
    except Exception as e:
        print(f"\n{Colors.FAIL}发生错误: {e}{Colors.ENDC}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()