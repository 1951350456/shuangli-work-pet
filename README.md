# 霜璃 · Shuangli Work Pet

一只白发、淡紫瞳、大头短身的 Q 版小龙娘，作为 ChatGPT Work / Pets 的自定义动画形象。包含九种状态动画、十六方向注视和可直接打开的离线预览。

![霜璃动作预览](assets/preview.gif)

## 预览与使用

1. 下载或克隆本仓库，直接双击 `index.html`；预览无需网络、API Key 或 Node.js。
2. 点击动作按钮，切换浅色、深色或透明网格背景；开启“跟随注视”后在角色周围移动鼠标。显示宽度可模拟 Pets 的 80–224 px 范围；“连续切换动作”穿插待机检查转换。
3. Mac 本地安装：双击根目录的 `安装本地版.command`，随后在「设置 → Pets」刷新并选择「霜璃（本地版）」。[图文入口](local-install.html) · [完整说明](docs/local-install.md)。
4. 通过 Pets 插件上传 `assets/spritesheet.png` 则创建账号内的云端宠物，这是另一条加载路径。账号内宠物 ID 与启用状态不会随仓库分发。

也可以在仓库目录运行 `python3 -m http.server 8000`，打开 `http://localhost:8000`。

**这是一套精灵素材与预览工具，不是 macOS 常驻应用。** 实际窗口、缩放、交互及运行性能由 Pets 宿主控制。形象属于用户选择的 ChatGPT 拟人创作，并非 OpenAI 官方角色。

本地安装器使用 Python 3.9+ 标准库，将已验收图片和原生清单写入 `CODEX_HOME/pets/shuangli-local`（默认 `~/.codex/pets/shuangli-local`），不联网。**本次实机测试中，客户端已把「霜璃（本地版）」自动迁移成云端记录，因此该工具尚未实现当前 Work Pets 的永久离线加载，也未证实修复透明消失故障。** 安装器不改写客户端的迁移开关，也不修改当前选择；本次保留 Work Pets 方式和此安装工具，并明确记录限制。

## Q 版变化

![同一画格下的旧版与 Q 版](assets/comparison.png)

大头、短身、粗轮廓与简化裙装，优先保证小尺寸下能看清表情。实际大小仍在 Pets 设置中调整。拖动、挥手、跳跃时下半身透明消失的问题尚未在宿主中复现，不能宣称换图已根治；检查结果与对照方法见 [显示异常说明](docs/display-troubleshooting.md)。

## 动画规格

| 项目 | 规格 |
| --- | --- |
| 精灵图 | 透明 RGBA PNG，1536 × 2288 |
| 网格 | 8 列 × 11 行，单格 192 × 208 |
| 必需帧 | 73 帧，15 个未用单元保持透明 |
| 基础动作 | 待机、向右移动、向左移动、挥手、跳跃、失落、等待、思考、检查 |
| 注视 | 从正上方起，顺时针每隔 22.5°，共 16 个姿势 |

![四个实际动画帧](assets/motion-stills.png)

## 校验与导出预览

需要 Python 3.12+。开发依赖固定为 Pillow 12.3.0。

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python scripts/validate.py
python scripts/render.py
python -m unittest discover -s tests -v
```

Windows 激活虚拟环境可使用 `.venv\Scripts\activate`。

预览导出到 `build/`；不会修改原始精灵图。若需要 MP4，先将 FFmpeg 加入 PATH，再运行 `python scripts/render.py --mp4`。静态资源和示例预览已随仓库提供。

校验器检查尺寸、帧占用、透明留白、校验和、跳跃位移和本地资源链接。**几何指标采用 A > 16 的可见边界，未用单元仍要求完全透明；它不判断表情、肢体或注视语义**；这些需要人工检查。修改精灵图后，需同步更新 `pet.json` 中的 SHA-256，并重新检查所有动作。

## 制作与验收

- 本次图像通过内置图像生成工具逐行制作，再进行确定性裁切、注册和合成。
- 已完成逐行动作检查、四个方向锚点检查、十六方向连续性检查、三位独立检查员的方向盲测和 Pets 服务端格式校验。
- Q 版减少纹样并放大五官。成品跳跃离地 20 像素，落地偏差 1 像素；实际指标和已复查的过渡警告见公开验收摘要。
- [制作说明](docs/creation.md)、[公开验收摘要](docs/qa.json)、[素材与参考来源](ASSETS.md)。

图像生成具有随机性；本仓库可以从已提交的精灵图重新导出预览，不承诺仅凭提示词逐像素重现原始生成结果。制作时使用的专有插件脚本和账号状态未打包。

## 许可

本仓库自编程序与文档采用 [MIT License](LICENSE)。**MIT 不适用于视觉素材**；美术的来源、使用边界及第三方权利说明见 [ASSETS.md](ASSETS.md)。
