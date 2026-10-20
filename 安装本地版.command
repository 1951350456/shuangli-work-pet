#!/bin/zsh
set -eu
project_dir="$(cd -- "$(dirname -- "$0")" && pwd)"
print '说明：当前客户端已实测会将本地条目自动迁移上云。此工具部署本地文件，不保证永久离线。'
python3 "$project_dir/scripts/install_local.py" install
print '\n本地文件已安装。请在设置 → Pets 刷新后选择「霜璃（本地版）」。'
print '若条目自动消失或又出现云端加载延迟，请查看 docs/local-install.md 的客户端迁移说明。'
print '此脚本不会修改应用程序、云端宠物、当前选择或系统缓存。'
read -r '?按回车关闭窗口。'
