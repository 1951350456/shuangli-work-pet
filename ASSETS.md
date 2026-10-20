# 视觉素材与参考来源

## 本仓库的视觉素材

`assets/` 中的图片、GIF 与视频为本次工作流生成、裁切或导出的展示素材。它们不包含在代码的 MIT 许可中，本仓库未将它们授权为可自由再分发的开源美术资源，也不授予任何第三方角色设计、商标或上游美术的权利。

图像生成工具：OpenAI 内置图像生成工具。主题为用户选择的白发、淡紫瞳、龙角、薄翼、卷尾及白紫裙装的 ChatGPT 拟人龙娘。它不是 OpenAI 官方角色或官方品牌素材。

## 上游参考

- 参考项目：[Konata147/DragonDeskPet](https://github.com/Konata147/DragonDeskPet)
- 上游美术规则：[ASSET_LICENSE.md](https://github.com/Konata147/DragonDeskPet/blob/main/ASSET_LICENSE.md)

上游源代码的 MIT 许可不覆盖其角色美术。其美术许可限制独立提取、再分发、其他项目使用及衍生素材制作。本项目不声称已获得上游美术再授权。

本仓库未包含上游原始角色图片、原始动画帧、程序图标或参考原图。展示的生成结果受到上述参考形象的影响；如需复用、再发布或商业使用相关角色形象，请先向相关权利方核对并取得适用授权。

## 程序与第三方依赖

预览页面、校验器及预览导出脚本为本项目自编代码，未复制上游 Windows 程序源码或专有 Pets 插件脚本。

- Pillow：固定使用 12.3.0；Context7 文档 ID `/python-pillow/pillow/12.3.0`。
- Pillow 官方文档：https://pillow.readthedocs.io/en/stable/
- GIF 保存参考：https://github.com/python-pillow/Pillow/blob/12.3.0/docs/handbook/image-file-formats.rst
- 可选 MP4 导出工具 FFmpeg：https://ffmpeg.org/ffmpeg-all.html 。制作时使用 7.1；本仓库不捆绑其二进制。

## 本轮选定设计

用户提供了白发龙娘参考图，并明确选定生成的第一张详细 Q 版，要求保留 OpenAI 结形发饰及服装装饰。本仓库发布生成图集、生成主形象与预览，不包含用户提供的原始参考图。结形标志作为用户要求的角色装饰使用，不表示官方角色或背书。

## D 清晰版

D 概念与动作行由内置 image_gen 生成，以用户明确选定的 D 图为主形象。粗轮廓和简化色块用于小尺寸辨识度优化；跳跃为用户指定的微笑张臂抱抱。第三方参考与标志的权利边界沿用上文，不包含用户提供的原始参考图。
