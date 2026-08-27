# Blogger 博客模板 - 中国优化版

这是一个专门为在中国访问优化的 Blogger 博客模板。

## 功能特点

- ✅ 完全中文界面
- ✅ 国内字体优化（不用 Google Fonts）
- ✅ 响应式设计，支持移动端
- ✅ 快速加载（无外部依赖）
- ✅ 现代简洁的卡片式布局
- ✅ SEO 友好结构

## 安装步骤

1. 登录 Blogger 后台
2. 进入「主题」→「编辑 HTML」
3. 复制 index.html 内容粘贴
4. 替换 {blog-title} 和 {blog-description} 为你的博客信息
5. 点击「保存」

## 文件说明

- index.html - 主模板文件（Blogger XML 格式）
- style.css - 样式表
- script.js - 交互脚本
- README.md - 本说明文件

## 自定义建议

### 修改颜色主题
在 style.css 中修改 CSS 变量：
`css
:root {
    --primary-color: #2c3e50;
    --accent-color: #3498db;
}
`

### 添加文章封面图
在 Blogger 文章编辑器中添加图片，或者在模板中添加：
`xml
<b:if cond="data:post.firstImageUrl">
    <img expr:src="data:post.firstImageUrl" class="post-image"/>
</b:if>
`

## 注意事项

- 本模板不含 Google Fonts，避免国内访问慢的问题
- 所有 CSS/JS 均为内联，无需额外请求
- 模板已针对移动设备优化

## 许可

MIT License - 可自由修改和使用
