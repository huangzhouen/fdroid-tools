# F-Droid 仓库管理器

一个功能完整的 F-Droid 应用仓库管理工具，支持图形化界面操作。

## 项目简介

本项目提供了一套完整的 F-Droid 自建仓库解决方案，包括图形化管理界面、自动化构建和完整的文档支持。

## 功能特性

### 核心功能
- 添加/删除 APK 应用
- 自动生成仓库元数据
- HTTP 服务器托管
- 实时监控日志

### 管理界面
- 全中文图形界面
- 实时状态显示
- 应用列表管理
- 配置参数设置

## 目录结构

```
fdroid-manager/
├── app.py              # 主程序（中文GUI）
├── server.py           # HTTP 服务器
├── start.bat           # Windows 启动脚本
├── README.md           # 本文档
├── apps/               # APK 文件目录
└── repo/               # 仓库数据
```

## 使用方法

1. 运行 `start.bat` 启动界面
2. 点击"添加 APK"选择应用
3. 点击"启动服务器"
4. 在 F-Droid App 中添加仓库地址

## 系统要求

- Python 3.11+
- tkinter 模块
- Windows 10+ / macOS / Linux

## 许可证

MIT License