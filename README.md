# Claude Code 跨平台配置同步指南

> **适用系统**：Windows、macOS、Linux
> **Python 要求**：3.6 或更高版本
> **支持功能**：MCP 服务器、Skills、Agents、Commands、Rules、Contexts 等所有配置

---

## 📋 概述

本指南帮助您在不同操作系统（Windows、macOS、Linux）的电脑之间同步 Claude Code 配置，包括所有自定义的技能、智能代理、命令、MCP 服务器等。

### 备份内容

- ✅ `agents/` - 智能代理配置
- ✅ `commands/` - 自定义斜杠命令
- ✅ `rules/` - 项目规则文件
- ✅ `contexts/` - 上下文配置
- ✅ `skills/` - 技能库
- ✅ `settings.json` - Claude 全局设置
- ✅ `.claude.json` - Claude 配置文件（含 MCP 服务器）
- ✅ `CLAUDE.md` - 项目级配置
- ✅ `config.json` - 插件配置
- ✅ `plugins/` - 插件相关配置

---

## 🚀 快速开始

### 第一步：在源电脑上备份

#### Windows
```powershell
# 使用默认备份位置（C:\Users\你的用户名\claude-config-backup）
python backup-claude-config-universal.py

# 或者指定自定义路径
python backup-claude-config-universal.py "D:\my-backups\claude-config"
```

#### macOS/Linux
```bash
# 使用默认备份位置（~/claude-config-backup）
python3 backup-claude-config-universal.py

# 或者指定自定义路径
python3 backup-claude-config-universal.py ~/backups/claude-config
```

### 第二步：传输备份

选择以下任一方式：

#### 方式 A：U 盘或移动硬盘
```bash
# 复制备份目录到 U 盘
# Windows
xcopy C:\Users\你的用户名\claude-config-backup E:\claude-config-backup /E /I

# macOS/Linux
cp -r ~/claude-config-backup /Volumes/YourUSBDrive/
```

#### 方式 B：网盘（OneDrive、Google Drive、百度网盘等）
```bash
# 直接将备份目录移动到网盘同步文件夹即可
```

#### 方式 C：局域网共享
```bash
# Windows：右键文件夹 -> 属性 -> 共享
# macOS：系统偏好设置 -> 共享 -> 文件共享
# Linux：配置 Samba 或 NFS
```

#### 方式 D：云存储服务
```bash
# 上传到云存储（Dropbox、Box 等）
# 在目标电脑下载
```

### 第三步：在目标电脑上恢复

#### Windows
```powershell
# 如果备份在默认位置
python restore-claude-config-universal.py

# 如果备份在其他位置
python restore-claude-config-universal.py "D:\backups\claude-config-backup"
```

#### macOS/Linux
```bash
# 如果备份在默认位置
python3 restore-claude-config-universal.py

# 如果备份在其他位置
python3 restore-claude-config-universal.py ~/backups/claude-config-backup
```

### 第四步：重新配置敏感信息

#### MCP 服务器 API 密钥

由于 MCP 配置可能包含 API 密钥等敏感信息，需要重新配置：

**方法 1：使用环境变量（推荐）**

```powershell
# Windows PowerShell
[Environment]::SetEnvironmentVariable("OPENAI_API_KEY", "your-api-key", "User")
[Environment]::SetEnvironmentVariable("ANTHROPIC_API_KEY", "your-api-key", "User")

# 重新启动终端使环境变量生效
```

```bash
# macOS/Linux
# 编辑 ~/.bashrc 或 ~/.zshrc
echo 'export OPENAI_API_KEY="your-api-key"' >> ~/.bashrc
echo 'export ANTHROPIC_API_KEY="your-api-key"' >> ~/.bashrc

# 重新加载配置
source ~/.bashrc
```

**方法 2：直接编辑配置文件**

```bash
# 编辑 ~/.claude.json
# 将环境变量占位符替换为实际的 API 密钥
```

### 第五步：重启 Claude Code

完全关闭并重新启动 Claude Code 以加载新配置。

---

## 🔧 高级功能

### 自定义备份路径

```bash
# 备份到自定义位置
python3 backup-claude-config-universal.py /path/to/custom/backup

# 从自定义位置恢复
python3 restore-claude-config-universal.py /path/to/custom/backup
```

### 自动备份当前配置

恢复脚本会自动备份现有的配置，避免数据丢失：

```bash
# 恢复前会自动创建备份
# 备份位置：~/.claude.backup.YYYYMMDD_HHMMSS
```

### 查看备份信息

```bash
# 恢复脚本会显示备份的详细信息：
# - 备份时间
# - 源系统信息
# - 计算机名
# - 用户名
# - 成功/失败项目数
```

---

## 🌍 跨平台注意事项

### 路径分隔符

脚本自动处理不同操作系统的路径分隔符：
- Windows: `\`
- macOS/Linux: `/`

### 文件权限

- **macOS/Linux**：确保脚本有执行权限
  ```bash
  chmod +x backup-claude-config-universal.py
  chmod +x restore-claude-config-universal.py
  ```

- **Windows**：Python 脚本无需特殊权限

### 符号链接

如果您的技能使用符号链接，需要在目标系统上重新创建：

```bash
# macOS/Linux
ln -s /path/to/original/skill ~/.claude/skills/skill-name

# Windows（需要管理员权限）
# 以管理员身份运行 PowerShell
New-Item -ItemType SymbolicLink -Path "$env:USERPROFILE\.claude\skills\skill-name" -Target "D:\path\to\skill"
```

### MCP 服务器路径

检查 MCP 服务器配置中的路径是否适用于目标系统：

```json
{
  "mcpServers": {
    "my-server": {
      "command": "python",
      "args": ["/path/to/server.py"]  // 确保路径在目标系统上有效
    }
  }
}
```

---

## 📦 不同操作系统间的传输

### Windows → macOS

```bash
# 1. 在 Windows 上备份
python backup-claude-config-universal.py

# 2. 使用网络共享或云存储传输
# 3. 在 macOS 上恢复
python3 restore-claude-config-universal.py
```

### macOS → Windows

```bash
# 1. 在 macOS 上备份
python3 backup-claude-config-universal.py

# 2. 使用网络共享或云存储传输
# 3. 在 Windows 上恢复
python restore-claude-config-universal.py
```

### Linux → macOS

```bash
# 1. 在 Linux 上备份
python3 backup-claude-config-universal.py

# 2. 使用 scp 或 rsync 传输
scp -r ~/claude-config-backup user@macos-host:~/

# 3. 在 macOS 上恢复
python3 restore-claude-config-universal.py
```

### Windows → Linux

```bash
# 1. 在 Windows 上备份
python backup-claude-config-universal.py

# 2. 使用 WinSCP 或 Samba 传输
# 3. 在 Linux 上恢复
python3 restore-claude-config-universal.py
```

---

## 🔄 自动化同步方案

### 方案 1：Git 版本控制（推荐）

**优点**：版本控制、可回滚、多设备同步、免费

**设置步骤**：

```bash
# 1. 初始化 Git 仓库
cd ~/.claude
git init

# 2. 创建 .gitignore
cat > .gitignore << EOF
*.log
cache/
backup-info.json
.env
*.key
*.pem
EOF

# 3. 提交配置
git add .
git commit -m "Initial commit"

# 4. 推送到远程仓库
git remote add origin https://github.com/yourusername/claude-config.git
git branch -M main
git push -u origin main
```

**在其他设备上克隆**：

```bash
# 备份现有配置
mv ~/.claude ~/.claude.backup

# 克隆配置
git clone https://github.com/yourusername/claude-config.git ~/.claude

# 重新配置 API 密钥
# 然后重启 Claude Code
```

### 方案 2：Syncthing 实时同步

**优点**：自动实时同步、无需云存储、跨平台、加密传输

**设置步骤**：

1. 在所有设备上安装 Syncthing
2. 在源设备上添加 `~/.claude` 文件夹
3. 在目标设备上接受共享
4. 配置同步路径

**官网**：https://syncthing.net/

### 方案 3：OneDrive/Google Drive 自动同步

**优点**：完全自动化、无需额外软件

**设置步骤**：

```bash
# 1. 将 .claude 目录移动到网盘同步文件夹
mv ~/.claude ~/OneDrive/.claude

# 2. 创建符号链接
# macOS/Linux
ln -s ~/OneDrive/.claude ~/.claude

# Windows（需要管理员权限）
# 以管理员身份运行 PowerShell
New-Item -ItemType SymbolicLink -Path "$env:USERPROFILE\.claude" -Target "$env:USERPROFILE\OneDrive\.claude"
```

---

## ⚠️ 常见问题

### 问题 1：备份时提示权限错误

**解决方案**：

```bash
# macOS/Linux
sudo python3 backup-claude-config-universal.py

# Windows
# 以管理员身份运行 PowerShell
python backup-claude-config-universal.py
```

### 问题 2：恢复后配置不生效

**解决方案**：

```bash
# 1. 清除 Claude Code 缓存
rm -rf ~/.claude/cache  # macOS/Linux
Remove-Item -Path "$env:USERPROFILE\.claude\cache" -Recurse -Force  # Windows

# 2. 重启 Claude Code
```

### 问题 3：MCP 服务器连接失败

**解决方案**：

```bash
# 1. 检查环境变量
echo $OPENAI_API_KEY  # macOS/Linux
echo $env:OPENAI_API_KEY  # Windows PowerShell

# 2. 检查 MCP 服务器配置
cat ~/.claude.json  # macOS/Linux
type $env:USERPROFILE\.claude.json  # Windows

# 3. 重新配置 API 密钥
```

### 问题 4：技能无法加载

**解决方案**：

```bash
# 1. 检查技能目录结构
ls -la ~/.claude/skills/  # macOS/Linux
Get-ChildItem "$env:USERPROFILE\.claude\skills"  # Windows

# 2. 检查 SKILL.md 文件是否存在
cat ~/.claude/skills/your-skill/SKILL.md

# 3. 查看 Claude Code 错误日志
```

### 问题 5：Python 版本不兼容

**解决方案**：

```bash
# 检查 Python 版本
python --version  # Windows
python3 --version  # macOS/Linux

# 如果版本低于 3.6，需要升级
# macOS: brew install python3
# Linux: sudo apt install python3
# Windows: 从 https://python.org 下载安装
```

---

## 📝 最佳实践

### 1. 定期备份

建议每周或每次重要更改后备份：

```bash
# 设置定时任务
# Windows: 任务计划程序
# macOS: launchd
# Linux: cron
```

### 2. 敏感信息管理

- ❌ 不要在配置文件中直接存储 API 密钥
- ✅ 使用环境变量或加密配置文件
- ✅ 将 `.claude.json` 中的敏感信息替换为 `${VARIABLE_NAME}`

### 3. 版本控制

- ✅ 使用 Git 管理配置
- ✅ 定期提交重要更改
- ✅ 使用分支管理不同环境配置

### 4. 测试恢复

定期测试恢复流程，确保备份有效：

```bash
# 在测试环境或虚拟机中测试恢复
python3 restore-claude-config-universal.py
```

### 5. 文档记录

记录自定义配置和修改：

```bash
# 创建配置说明文档
cat > ~/.claude/CONFIG_NOTES.md << EOF
# Claude Code 配置说明

## MCP 服务器
- openai: 需要设置 OPENAI_API_KEY 环境变量
- anthropic: 需要设置 ANTHROPIC_API_KEY 环境变量

## 自定义技能
- xiaohongshu-automation: 小红书自动化技能
  - 路径: D:\www\idea\xhs_auto\workflow\.codebuddy\skills\xiaohongshu-automation
  - 符号链接: ~/.claude/skills/xiaohongshu-automation

## 自定义命令
- /custom: 自定义命令说明
EOF
```

---

## 🎯 使用场景

### 场景 1：工作电脑 ↔ 家用电脑

```bash
# 使用 Git 方案，定期同步
cd ~/.claude
git add .
git commit -m "Update config"
git push

# 在另一台电脑上
cd ~/.claude
git pull
```

### 场景 2：Windows 开发环境 ↔ macOS 生产环境

```bash
# 使用备份/恢复脚本
# 注意路径差异和符号链接
```

### 场景 3：团队协作共享配置

```bash
# 使用 Git + 分支管理
git checkout -b feature/new-skill
# 添加新技能
git add .
git commit -m "Add new skill"
git push origin feature/new-skill
```

### 场景 4：定期备份以防数据丢失

```bash
# 使用定时任务定期备份
# Windows: 任务计划程序
# macOS: launchd
# Linux: cron
```

---

## 📚 相关资源

- [Claude Code 官方文档](https://docs.anthropic.com/claude/code)
- [MCP 协议文档](https://modelcontextprotocol.io/)
- [Python 官方网站](https://www.python.org/)
- [Syncthing 官网](https://syncthing.net/)

---

## 🆘 获取帮助

如果遇到问题：

1. 查看本文档的"常见问题"部分
2. 检查脚本的错误输出
3. 确认 Python 版本是否 >= 3.6
4. 验证文件权限是否正确
5. 在 Claude Code 中查看错误日志

---

## 📄 许可证

本指南和脚本为开源项目，可自由使用和修改。

---

**最后更新**：2026-01-29
**版本**：1.0.0
**作者**：Claude Code 跨平台配置同步工具