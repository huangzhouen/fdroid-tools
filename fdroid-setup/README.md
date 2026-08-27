# F-Droid 自建仓库搭建指南

## 文件说明

| 文件 | 用途 |
|------|------|
| install-fdroid.sh | 一键安装脚本 |
| add-app.sh | 添加应用到仓库 |
| update-repo.sh | 更新仓库元数据 |
| backup.sh | 备份仓库数据 |

## 快速开始

### 1. 准备工作

确保你有：
- Linux 服务器（Ubuntu 20.04+ / Debian 11+）
- Root 或 sudo 权限
- 域名 + HTTPS 证书
- 至少 100GB 磁盘空间

### 2. 上传脚本到服务器

\\\ash
# 方式一：使用 scp
scp -r fdroid-setup/ user@your-server:/opt/

# 方式二：使用 git
git clone https://your-repo.com/fdroid-setup.git /opt/fdroid-setup
\\\

### 3. 执行安装

\\\ash
# 设置环境变量（可选）
export REPO_NAME="我的 F-Droid 源"
export REPO_URL="https://fdroid.yourdomain.com"
export DOMAIN="fdroid.yourdomain.com"

# 执行安装
cd /opt/fdroid-setup
chmod +x *.sh
sudo ./install-fdroid.sh
\\\

### 4. 添加应用

\\\ash
# 复制 APK 到服务器
scp app.apk user@your-server:/tmp/

# 添加应用
sudo ./add-app.sh com.example.app /tmp/app.apk

# 更新仓库
sudo ./update-repo.sh
\\\

## 常用命令

\\\ash
# 查看仓库状态
fdroid list

# 更新应用元数据
fdroid update -a

# 构建应用
fdroid build -p com.example.app

# 备份仓库
./backup.sh
\\\

## 参考链接

- [F-Droid 官方文档](https://f-droid.org/docs/)
- [F-Droid Server GitLab](https://gitlab.com/fdroid/fdroidserver)
