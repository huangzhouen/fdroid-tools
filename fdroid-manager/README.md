# F-Droid 仓库管理器

图形化管理界面，用于管理本地 F-Droid 仓库。

## 功能
- 添加/删除 APK 文件
- 自动生成 repos.xml
- 启动/停止 HTTP 服务器
- 查看应用列表

## 使用方法
1. 双击 `start.bat` 启动管理界面
2. 点击"添加 APK"选择要加入仓库的应用
3. 点击"启动服务器"开始提供服务
4. 在 F-Droid App 中添加仓库地址: `http://localhost:8000`

## 依赖
- Python 3.11+
- tkinter (通常随 Python 安装)
