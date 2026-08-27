#!/bin/bash
set -e
REPO_NAME="${REPO_NAME:-My F-Droid Repo}"
REPO_URL="${REPO_URL:-https://fdroid.example.com}"
REPO_DIR="/opt/fdroid/repo"
FDROID_SERVER_DIR="/opt/fdroid/fdroidserver"
FDROID_USER="fdroid"

echo "F-Droid 服务器安装脚本 v1.0"
echo "[1/8] 安装系统依赖..."
apt update && apt install -y git python3-pip python3-venv openjdk-17-jdk-headless zlib1g-dev libsqlite3-dev libssl-dev chrony nginx certbot python3-certbot-nginx gpg

echo "[2/8] 创建用户和目录..."
adduser --system --shell /bin/bash --group $FDROID_USER 2>/dev/null || true
mkdir -p $REPO_DIR/app $FDROID_SERVER_DIR
chown -R $FDROID_USER:$FDROID_USER $REPO_DIR $FDROID_SERVER_DIR

echo "[3/8] 克隆 F-Droid 代码..."
git clone https://gitlab.com/fdroid/fdroidserver.git $FDROID_SERVER_DIR --depth=1
chown -R $FDROID_USER:$FDROID_USER $FDROID_SERVER_DIR

echo "[4/8] 配置 Python 环境..."
cd $FDROID_SERVER_DIR
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install -r server/requirements.txt

echo "[5/8] 生成 GPG 密钥..."
GPG_KEY_ID=$(gpg --list-secret-keys --keyid-format long 2>/dev/null | grep "sec" | head -1 | awk '{print $2}' | cut -d'/' -f2)
if [[ -z "$GPG_KEY_ID" ]]; then
    echo "请运行 'gpg --full-generate-key' 生成密钥"
    read -p "请输入 GPG 密钥 ID: " GPG_KEY_ID
fi

echo "[6/8] 创建配置文件..."
cat > $REPO_DIR/fdroidserver.cfg << EOF
[repo]
name = $REPO_NAME
url = $REPO_URL
icon = icon.png
versioncode = 1
[signing]
key = $GPG_KEY_ID
file = 
algo = SHA256
EOF

echo "[7/8] 配置 Nginx..."
cat > /etc/nginx/sites-available/fdroid << 'EOF'
server {
    listen 80;
    server_name _;
    root /var/www/html;
    location / { try_files $uri $uri/ =404; }
}
EOF
mkdir -p /var/www/html
echo "<h1>F-Droid Repository</h1>" > /var/www/html/index.html
ln -sf /etc/nginx/sites-available/fdroid /etc/nginx/sites-enabled/
nginx -t && systemctl reload nginx

echo "[8/8] 初始化仓库..."
cd $REPO_DIR
sudo -u $FDROID_USER bash -c "cd $FDROID_SERVER_DIR && source venv/bin/activate && export PATH=\$PATH:$FDROID_SERVER_DIR && fdroid init"

echo ""
echo "✅ 安装完成！"
echo "仓库目录: $REPO_DIR"
echo "下一步: sudo ./add-app.sh <包名> <APK路径>"