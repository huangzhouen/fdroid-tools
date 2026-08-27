#!/bin/bash
# 更新 F-Droid 仓库脚本
set -e

REPO_DIR="/opt/fdroid/repo"
FDROID_SERVER_DIR="/opt/fdroid/fdroidserver"
FDROID_USER="fdroid"

echo "🔄 更新 F-Droid 仓库..."

cd "$REPO_DIR"
su - "$FDROID_USER" -c "
    cd $FDROID_SERVER_DIR
    source venv/bin/activate
    export PATH=\$PATH:$FDROID_SERVER_DIR
    echo '更新配置...'
    fdroid update -c
    echo '扫描新应用...'
    fdroid update -a
    echo '更新索引...'
    fdroid update -r
    echo '签名仓库...'
    fdroid signrepo
    echo '✅ 仓库更新完成'
"

echo ""
echo "📊 当前仓库状态："
su - "$FDROID_USER" -c "
    cd $FDROID_SERVER_DIR
    source venv/bin/activate
    export PATH=\$PATH:$FDROID_SERVER_DIR
    fdroid list | head -20
"