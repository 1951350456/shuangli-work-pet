# 本地文件安装与离线验证

本安装方式将同一张已验收的 Q 版精灵图安装到桌面客户端的本地宠物目录。安装器只使用 Python 3.9+ 标准库，不联网，不需要 Pillow、API Key 或管理员权限。

**2026-10-20 的实际使用反馈：** 用户在同一台 Mac 上选择「霜璃（本地版）」后，对照原云端版测试：本地版目前没有再出现透明，原云端版仍有此问题。这是用户报告的实际改善，尚未记录测试时长、重启或断网复测结果。

同时，账号内出现了对应的云端宠物记录，说明客户端执行过云端创建/迁移流程。**云端记录存在不能单独证明当前选中条目的渲染图片来自云端，也不能据此否定本地安装的改善；永久离线仍未验证。** 安装器不会禁用迁移、修改客户端程序、改写隐藏设置或替换现有云端宠物。

## 在 Mac 上安装

下载完整仓库并解压，双击根目录的 `安装本地版.command`。也可以在仓库目录运行：

```bash
python3 scripts/install_local.py install
python3 scripts/install_local.py status
```

默认目录是 `$CODEX_HOME/pets/shuangli-local`；未设置 `CODEX_HOME` 时使用 `~/.codex/pets/shuangli-local`。目录内包含：

```text
pet.json
spritesheet.png
```

本地条目名为「霜璃（本地版）」，原生本地 ID 为 `custom:shuangli-local`。它与账号内的云端霜璃是不同条目；安装器保留云端记录和当前选择。

1. 打开桌面客户端「设置 → Pets」，选择 Refresh／刷新。
2. 选择「霜璃（本地版）」。仅看到同名卡片不能证明它仍使用本地图片，因为迁移可能保留显示名称。
3. 关闭设置后重新打开，并在几分钟后再次检查首次显示及动作切换。如果条目消失、被合并或再次等待云端图像加载，应继续检查客户端迁移和运行时请求，不能宣称离线修复成功。

安装会先核对精灵图校验和、格式和尺寸，再暂存完整文件并发布本地目录。重复安装相同文件不会改写文件；目标目录内容不同时直接报错，要求先显式备份，不覆盖用户修改。

## 构建可搬运文件包

```bash
python3 scripts/install_local.py bundle
```

文件输出到 `build/shuangli-local/`。这只是可搬运的原生文件对，尚未安装到客户端。

## 验证范围

- 本仓库测试验证：本地安装后的字节与已验收 PNG 完全一致，清单只引用同目录 `spritesheet.png`；没有运行时网络依赖写入这个本地包。
- 用户对照反馈验证：本地版目前未再出现透明，原云端版仍出现。该结果支持继续使用本地版，但不单独确定缓存根因或长期修复结论。
- 本安装器不操作客户端的选择界面，不读取账号令牌，不修改自动云迁移状态。`runtime_selection_verified` 和 `permanent_offline_verified` 保持 `false`，由实际客户端观察另行确认。
- 本机检查的桌面客户端版本：26.1013.40934。其本地读取器支持 `pet.json`、`spriteVersionNumber: 2` 和本地图片转内嵌图像，同时存在自动云迁移逻辑。这属于当前实现兼容性，不是永久公共 API 保证。
- [官方 Pets 文档](https://learn.chatgpt.com/docs/pets)说明桌面创建的自定义宠物可保存在本地，但未说明当前云迁移和缓存淘汰的全部行为。

Python API 文档基线：Context7 `/python/cpython/v3.9.22`，参考 [Path.rename](https://docs.python.org/3.9/library/pathlib.html#pathlib.Path.rename) 与 [TemporaryDirectory](https://docs.python.org/3.9/library/tempfile.html#tempfile.TemporaryDirectory)。
