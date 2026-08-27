#!/bin/bash
# 添加应用到 F-Droid 仓库脚本
# 使用方法: ./add-app.sh <包名> <APK路径>

set -e

REPO_DIR="/opt/fdroid/repo"
FDROID_SERVER_DIR="/opt/fdroid/fdroidserver"
FDROID_USER="fdroid"

PACKAGE_NAME="${1:?用法: $0 <包名> <APK路径>}"
APK_PATH="${2:?用法: $0 <包名> <APK路径>}"

if [[ ! -f "$APK_PATH" ]]; then
    echo "错误: APK 文件不存在: $APK_PATH"
    exit 1
fi

echo "添加应用: $PACKAGE_NAME"
echo "APK 文件: $APK_PATH"

# 创建目录结构
APP_DIR="$REPO_DIR/apps/$PACKAGE_NAME/metadata"
mkdir -p "$APP_DIR"

# 复制 APK
cp "$APK_PATH" "$REPO_DIR/app/$PACKAGE_NAME.apk"

# 生成 metadata
cat > "$APP_DIR/$PACKAGE_NAME.yml" << EOF
Name: $(basename "$PACKAGE_NAME")
Summary: 从 F-Droid 源添加的应用
Description: |
  这是一个从用户自定义源安装的应用。
SourceCode: https://github.com/example/$PACKAGE_NAME
IssueTracker: https://github.com/example/$PACKAGE_NAME/issues
Website: https://example.com
Contact: admin@example.com
License: Apache-2.0
AntiFeatures:
  - Ads
  - Tracking
Categories:
  - Entertainment
build: 1.0.0
subdir: build
gradle:
  - yes
scanme:
  - false
EOF

echo "✅ 应用已添加到: $APP_DIR"
echo "📱 APK 已复制到: $REPO_DIR/app/"
echo ""
echo "下一步："
echo "1. 编辑 metadata 文件完善信息"
echo "2. 运行: cd $REPO_DIR && sudo -u $FDROID_USER bash -c 'cd $FDROID_SERVER_DIR && source venv/bin/activate && fdroid update -a'"
echo "3. 如果需要构建源码版本: sudo -u $FDROID_USER bash -c 'cd $FDROID_SERVER_DIR && source venv/bin/activate && fdroid build -p $PACKAGE_NAME'"