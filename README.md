# gpt龙娘 · D 清晰版

用户选定的 D 版白发龙娘：粗紫色轮廓、简洁白裙、大色块与清楚的紫色眼睛。保留双龙角、淡紫龙翼、卷尾和结形发饰，跳跃改为微笑着张开双臂、迎向你的抱抱。

![动作预览](assets/preview.gif)

## 预览与使用

下载完整仓库后双击 `index.html`，无需联网或 Node.js。鼠标移到角色上会播放一次“抱抱跳”，落地后回到之前的动作；也可用动作按钮、背景、尺寸和跟随注视控件查看。桌面 Pets 的互动触发时机由宿主控制，本项目更新对应动画素材。

Mac 本地文件安装入口为 `安装本地版.command`，步骤见 [安装说明](local-install.html)。已有目标文件不同会明确报错，请先显式备份；安装器不会静默覆盖。原生目录沿用 `shuangli-local`，保留已有条目身份。

## 清晰度与尺寸

![D 主形象](assets/portrait.png)

Pets 每帧固定 192 × 208。本版通过加粗轮廓、简化细碎纹样，并在完整动作外沿约束下增加有效占比来优化观感。九行动作采用共同站立参考高度 183 px、共同基线 203 px，跳跃保留真实位移；不逐帧拉伸或填满画格。

完整透明图集为 1536 × 2288，8 列 × 11 行，73 个有效帧和 15 个透明空单元。九种状态为待机、右移、左移、挥手、抱抱跳、失落、等待、思考、检查；另有十六方向注视。

![四帧示例](assets/motion-stills.png)

本次只更新美术和网页互动。客户端程序、网络和缓存没有改动。原有加载失败／下半身透明故障仍未确认修复，本地文件也不保证当前客户端保持永久离线加载。[既有故障记录](docs/display-troubleshooting.md)。

## 校验与导出

开发需要 Python 3.12+ 和 Pillow 12.3.0；本地安装器只需 Python 3.9+ 标准库。

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python scripts/validate.py
python scripts/render.py
python -m unittest discover -s tests -v
```

预览导出到 `build/`。MP4 可选：将 FFmpeg 加入 PATH 后运行 `python scripts/render.py --mp4`。图像生成具有随机性，仓库提供从最终图集重新导出预览的工具，没有打包专有生成插件。

[制作说明](docs/creation.md) · [验收摘要](docs/qa.json) · [素材来源](ASSETS.md)。代码采用 [MIT](LICENSE)，视觉素材使用边界见 ASSETS；该拟人形象不是 OpenAI 官方角色。
