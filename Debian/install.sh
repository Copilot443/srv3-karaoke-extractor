#!/bin/bash
set -e

echo "==============================="
echo " srv3 / YTSubExtractor Installer"
echo "==============================="

# Must be run as root
if [ "$EUID" -ne 0 ]; then
    echo "Please run this installer with sudo:"
    echo "  sudo ./install.sh"
    exit 1
fi

# Detect original user (for HOME paths)
REAL_USER="${SUDO_USER:-$USER}"
REAL_HOME=$(eval echo "~$REAL_USER")

echo "Installing dependencies (forced)..."

# ----------------------------------------
# System packages (reinstall)
# ----------------------------------------
apt update
apt install --reinstall -y \
    curl \
    wget \
    ffmpeg \
    ca-certificates \
    gnupg \
    software-properties-common \
    yt-dlp \
    micro

# ----------------------------------------
# yt-dlp (APT + overwrite with latest binary)
# ----------------------------------------
echo "Installing yt-dlp (APT + latest binary override)..."

# Ensure apt version is installed
apt install --reinstall -y yt-dlp

# Overwrite with latest upstream binary
wget -q https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp \
    -O /usr/local/bin/yt-dlp
chmod +x /usr/local/bin/yt-dlp

# ----------------------------------------
# .NET 8 Runtime (forced)
# ----------------------------------------
echo "Installing .NET 8 runtime (forced)..."
wget -q https://packages.microsoft.com/config/ubuntu/$(lsb_release -rs)/packages-microsoft-prod.deb \
    -O /tmp/microsoft-prod.deb

dpkg -i /tmp/microsoft-prod.deb || true
apt update
apt install --reinstall -y dotnet-runtime-8.0

# ----------------------------------------
# YTSubConverter (.deb)
# ----------------------------------------
if [ ! -f "./YTSubConverter-Linux.deb" ]; then
    echo "ERROR: YTSubConverter-Linux.deb not found!"
    echo "Put it in the same directory as install.sh"
    exit 1
fi

echo "Installing YTSubConverter (forced)..."
apt install --reinstall -y ./YTSubConverter-Linux.deb

# ----------------------------------------
# Create ytsubconverter CLI wrapper (overwrite)
# ----------------------------------------
echo "Creating ytsubconverter CLI..."

cat << 'EOF' > /usr/local/bin/ytsubconverter
#!/bin/bash
exec dotnet /opt/ytsubconverter/ytsubconverter.dll "$@"
EOF

chmod +x /usr/local/bin/ytsubconverter

# ----------------------------------------
# Install srv3 script globally (overwrite)
# ----------------------------------------
if [ ! -f "./srv3" ]; then
    echo "ERROR: srv3 script not found!"
    echo "Put your srv3 script in the same directory as install.sh"
    exit 1
fi

echo "Installing srv3 command..."
install -m 755 -o root -g root ./srv3 /usr/local/bin/srv3

# ----------------------------------------
# Ensure Videos directory exists
# ----------------------------------------
mkdir -p "$REAL_HOME/Videos"
chown "$REAL_USER":"$REAL_USER" "$REAL_HOME/Videos"

# ----------------------------------------
# Final checks
# ----------------------------------------
echo
echo "Verifying installation..."

yt-dlp --version

echo
echo "==============================="
echo " INSTALLATION COMPLETE ✅"
echo "==============================="
echo
echo "You can now run from ANY directory:"
echo "  srv3 \"https://youtube.com/...\""
echo
