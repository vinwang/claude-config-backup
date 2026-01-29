#!/usr/bin/env python3
"""
Claude Code 配置恢复工具
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
    print(Colors.BOLD + "Claude Code 配置恢复工具" + Colors.ENDC)
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

def read_backup_info(backup_path):
    """读取备份信息"""
    info_path = os.path.join(backup_path, 'backup-info.json')
    if os.path.exists(info_path):
        try:
            with open(info_path, 'r', encoding='utf-8') as f:
                backup_info = json.load(f)

            print("备份信息:")
            print(f"  备份时间: {backup_info.get('backup_date', 'N/A')}")
            print(f"  源系统: {backup_info.get('system_info', {}).get('system', 'N/A')} {backup_info.get('system_info', {}).get('release', 'N/A')}")
            print(f"  计算机名: {backup_info.get('computer_name', 'N/A')}")
            print(f"  用户名: {backup_info.get('user_name', 'N/A')}")
            print(f"  成功项目: {backup_info.get('success_count', 0)}")
            print(f"  失败项目: {backup_info.get('fail_count', 0)}")
            print()
            return backup_info
        except Exception as e:
            print(f"{Colors.WARNING}读取备份信息失败: {e}{Colors.ENDC}")
            return None
    else:
        print(f"{Colors.WARNING}警告：未找到备份信息文件{Colors.ENDC}")
        return None

def confirm_restore():
    """确认恢复"""
    print(Colors.WARNING + "警告：此操作将覆盖现有的 Claude Code 配置！" + Colors.ENDC)
    print(Colors.WARNING + "建议在恢复前先备份当前配置。" + Colors.ENDC)
    try:
        choice = input("是否继续？: ").strip().lower()
        if choice != 'y':
            print("恢复已取消")
            sys.exit(0)
        print()
        print("开始恢复配置...")
        print()
    except KeyboardInterrupt:
        print("\n操作已取消")
        sys.exit(0)

def restore_item(source, dest):
    """恢复单个项目"""
    item_name = os.path.basename(source)
    print(f"正在恢复: {item_name}")

    try:
        if os.path.isdir(source):
            # 恢复目录
            if os.path.exists(dest):
                shutil.rmtree(dest)
            shutil.copytree(source, dest)
        else:
            # 恢复文件
            dest_dir = os.path.dirname(dest)
            if dest_dir and not os.path.exists(dest_dir):
                os.makedirs(dest_dir, exist_ok=True)
            shutil.copy2(source, dest)

        print(f"  {Colors.OKGREEN}✓ 成功{Colors.ENDC}")
        return True
    except Exception as e:
        print(f"  {Colors.FAIL}✗ 失败: {e}{Colors.ENDC}")
        return False

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

def backup_current_config():
    """备份当前配置"""
    if os.path.exists(CLAUDE_CONFIG_PATH):
        print(f"{Colors.WARNING}检测到现有配置，正在备份...{Colors.ENDC}")
        backup_dir = CLAUDE_CONFIG_PATH + '.backup.' + datetime.now().strftime('%Y%m%d_%H%M%S')
        try:
            shutil.copytree(CLAUDE_CONFIG_PATH, backup_dir)
            print(f"{Colors.OKGREEN}当前配置已备份到: {backup_dir}{Colors.ENDC}")
            print()
        except Exception as e:
            print(f"{Colors.WARNING}备份当前配置失败: {e}{Colors.ENDC}")
            print()
    else:
        print(f"{Colors.OKBLUE}未检测到现有配置，将创建新配置{Colors.ENDC}")
        print()

def print_success_message(success_count, fail_count):
    """打印成功消息"""
    print()
    print(Colors.OKGREEN + "=" * 60 + Colors.ENDC)
    print(Colors.BOLD + "恢复完成！" + Colors.ENDC)
    print(Colors.OKGREEN + "=" * 60 + Colors.ENDC)
    print()
    print(f"成功项目: {success_count}")
    print(f"失败项目: {fail_count}")
    print()
    print(Colors.OKBLUE + "建议操作：" + Colors.ENDC)
    print("1. 重启 Claude Code 以加载新配置")
    print("2. 检查 MCP 服务器是否需要重新配置 API 密钥")
    print("3. 测试技能和命令是否正常工作")
    print()
    print(Colors.WARNING + "重要提示：" + Colors.ENDC)
    print("- 如果 MCP 服务器使用环境变量，请在目标系统上设置相应的环境变量")
    print("- 如果技能使用符号链接，需要重新创建符号链接")
    print("- 检查并更新任何路径相关的配置")
    print()

def print_restore_instructions():
    """打印恢复说明"""
    print(Colors.OKBLUE + "使用说明：" + Colors.ENDC)
    print()
    print("基本用法:")
    print("  python restore-claude-config-universal.py")
    print()
    print("指定备份路径:")
    print("  python restore-claude-config-universal.py <backup_path>")
    print()
    print("示例:")
    print("  # Windows")
    print("  python restore-claude-config-universal.py D:\\backups\\claude-config-backup")
    print()
    print("  # macOS/Linux")
    print("  python restore-claude-config-universal.py ~/backups/claude-config-backup")
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

        # 检查是否为帮助请求
        if len(sys.argv) > 1 and sys.argv[1] in ['-h', '--help', 'help']:
            print_restore_instructions()
            sys.exit(0)

        # 获取备份路径
        backup_path = get_backup_path()

        # 检查备份目录是否存在
        if not os.path.exists(backup_path):
            print(f"{Colors.FAIL}错误：备份目录不存在: {backup_path}{Colors.ENDC}")
            print()
            print("请检查:")
            print("1. 备份路径是否正确")
            print("2. 备份目录是否已传输到本机")
            print()
            print_restore_instructions()
            sys.exit(1)

        # 读取备份信息
        backup_info = read_backup_info(backup_path)

        # 确认恢复
        confirm_restore()

        # 备份当前配置
        backup_current_config()

        # 开始恢复
        success_count = 0
        fail_count = 0

        # 获取备份目录中的所有项目
        items = os.listdir(backup_path)
        backup_info_file = 'backup-info.json'

        if backup_info_file in items:
            items.remove(backup_info_file)

        if not items:
            print(f"{Colors.WARNING}备份目录为空，没有可恢复的项目{Colors.ENDC}")
            sys.exit(0)

        for item in items:
            source_path = os.path.join(backup_path, item)
            dest_path = os.path.join(CLAUDE_CONFIG_PATH, item)

            if restore_item(source_path, dest_path):
                success_count += 1
            else:
                fail_count += 1

        # 显示结果
        print_success_message(success_count, fail_count)

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