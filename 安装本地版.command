#!/bin/zsh
set -eu
project_dir="$(cd -- "$(dirname -- "$0")" && pwd)"
print '说明：最新复测本地版仍会加载失败；当前条目已迁移为云端选择。此工具不保证永久离线，也未修复透明故障。'
python3 "$project_dir/scripts/install_local.py" install
print '\n本地文件已安装。请在设置 → Pets 刷新后选择「霜璃（本地版）」。'
print '若条目自动消失或又出现云端加载延迟，请查看 docs/local-install.md 的客户端迁移说明。'
print '此脚本不会修改应用程序、云端宠物、当前选择或系统缓存。'
read -r '?按回车关闭窗口。'
