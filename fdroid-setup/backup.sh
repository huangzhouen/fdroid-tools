#!/bin/bash
# F-Droid 仓库备份脚本
set -e

REPO_DIR="/opt/fdroid/repo"
BACKUP_DIR="/opt/fdroid/backups"
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="$BACKUP_DIR/fdroid-backup-$DATE.tar.gz"

echo "📦 开始备份 F-Droid 仓库..."

# 创建备份目录
mkdir -p "$BACKUP_DIR"

# 创建备份
tar -czf "$BACKUP_FILE" \
    --exclude='*.apk' \
    --exclude='venv' \
    --exclude='.git' \
    -C /opt fdroid/

echo "✅ 备份完成: $BACKUP_FILE"
echo "📊 备份大小: $(du -sh "$BACKUP_FILE" | cut -f1)"
echo ""
echo "恢复命令:"
echo "  tar -xzf $BACKUP_FILE -C /"
echo ""
echo "旧备份清理（保留最近 7 天）:"
find "$BACKUP_DIR" -name "fdroid-backup-*.tar.gz" -mtime +7 -delete