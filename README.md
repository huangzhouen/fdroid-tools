# F-Droid Tools - F-Droid 仓库管理工具集

一个完整的 F-Droid 自建仓库解决方案，包含图形化管理界面、Blogger 模板和服务器安装脚本。

## 项目简介

本项目提供了一套完整的工具集，帮助你快速搭建和管理 F-Droid 应用仓库：

- **图形化管理界面** - 全中文 GUI，操作简单直观
- **Blogger 中文模板** - 支持联网搜索的博客模板
- **服务器安装脚本** - 一键部署 F-Droid 服务器
- **轻量级服务器** - 无需 Docker，纯 Python 运行

## 功能特性

### F-Droid 管理器 (fdroid-manager)
- 图形化添加/删除 APK
- 自动生成仓库元数据
- 内置 HTTP 服务器
- 实时监控日志
- 全中文界面

### Blogger 模板 (blogger-template-cn)
- 响应式设计
- 联网搜索功能
- 简洁美观的界面
- 易于定制

### 服务器脚本 (fdroid-setup)
- 一键安装脚本
- 自动配置 Nginx
- SSL 证书管理
- 定期备份功能

## 目录结构

```
fdroid-tools/
├── blogger-template-cn/      # Blogger 中文模板
│   ├── template.xml          # 主模板
│   ├── index.html            # 主页
│   ├── search.html           # 搜索页面
│   ├── style.css             # 样式表
│   └── script.js             # 交互脚本
├── fdroid-manager/           # 图形化管理界面
│   ├── app.py                # 主程序（中文GUI）
│   ├── server.py             # HTTP 服务器
│   └── start.bat             # Windows 启动脚本
├── fdroid-setup/             # 服务器安装脚本
│   ├── install-fdroid.sh     # 一键安装
│   ├── add-app.sh            # 添加应用
│   └── update-repo.sh        # 更新仓库
└── fdroid-simple/            # 简化版服务器
    ├── server.py             # 轻量服务器
    └── run.bat               # 启动脚本
```

## 快速开始

### 方式一：图形化管理界面（推荐）

```bash
# 进入管理器目录
cd fdroid-manager

# 启动图形界面
python app.py
```

然后：
1. 点击"添加 APK"选择应用
2. 点击"启动服务器"
3. 在 F-Droid App 中添加仓库地址

### 方式二：使用简化版服务器

```bash
# 进入简化版目录
cd fdroid-simple

# 启动服务器
python server.py
```

### 方式三：部署完整服务器

```bash
# 上传到 Linux 服务器
scp -r fdroid-setup/ user@server:/opt/

# 执行安装
cd /opt/fdroid-setup
chmod +x *.sh
sudo ./install-fdroid.sh
```

## 系统要求

### 图形化管理界面
- Python 3.11 或更高版本
- tkinter 模块
- Windows 10+ / macOS / Linux

### 服务器部署
- Ubuntu 20.04+ / Debian 11+
- Root 权限
- 100GB+ 磁盘空间
- 域名 + HTTPS 证书

## 详细文档

- [Blogger 模板说明](blogger-template-cn/README.md)
- [F-Droid 管理器说明](fdroid-manager/README.md)
- [服务器安装说明](fdroid-setup/README.md)

## 许可证

MIT License

## 作者

huangzhouen

## 更新日志

### v1.0.0 (2026-08-27)
- 初始版本发布
- 添加图形化管理界面
- 添加 Blogger 中文模板
- 添加服务器安装脚本