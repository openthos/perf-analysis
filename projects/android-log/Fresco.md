## Fresco的介绍
Fresco是FaceBook开发的一个开源的图片加载组件，使用之后不需要管图片加载和显示的问题

## Fresco的特性
 - 内存管理：Android中解压的图片都使用Bitmap，这样占用很大的内存，当长时间之后就会OOM，从而引发频繁的GC。在Fresco中将图片放在特定的内存区域，在图片不使用之后就自动释放
 - 图片加载：Fresco支持多种的图片加载方式
 - 图片绘制：可以自定义居中焦点；可以实现圆角图；下载失败之后可以点击重新下载
 - 图片的呈现：Android不支持图片的渐近式呈现，但是Fresco可以支持

## 参考文献：[Fresco官网](https://www.fresco-cn.org/docs/index.html)
