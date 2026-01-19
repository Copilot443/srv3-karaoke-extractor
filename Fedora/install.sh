#!/bin/bash
set -e

echo "==============================="
echo " srv3 / YTSubExtractor Installer"
echo " Fedora Edition"
echo "==============================="

# Must be run as root
if [ "$EUID" -ne 0 ]; then
    echo "Please run this installer with sudo:"
    echo "  sudo ./install-fedora.sh"
    exit 1
fi

REAL_USER="${SUDO_USER:-$USER}"
REAL_HOME=$(eval echo "~$REAL_USER")

# ----------------------------------------
# Enable RPM Fusion (required for ffmpeg)
# ----------------------------------------
if ! rpm -q rpmfusion-free-release >/dev/null 2>&1; then
    echo "Enabling RPM Fusion..."
    dnf install -y \
        https://download1.rpmfusion.org/free/fedora/rpmfusion-free-release-$(rpm -E %fedora).noarch.rpm
fi

# ----------------------------------------
# System packages
# ----------------------------------------
dnf install -y \
    curl \
    wget \
    ffmpeg \
    ca-certificates \
    gnupg2 \
    yt-dlp \
    micro \
    xz

# ----------------------------------------
# Install latest yt-dlp binary
# ----------------------------------------
echo "Installing latest yt-dlp..."
wget -q https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp \
    -O /usr/local/bin/yt-dlp
chmod +x /usr/local/bin/yt-dlp

# ----------------------------------------
# Install .NET 8 runtime
# ----------------------------------------
echo "Installing .NET 8 runtime..."

rpm --import https://packages.microsoft.com/keys/microsoft.asc
wget -q https://packages.microsoft.com/config/fedora/$(rpm -E %fedora)/packages-microsoft-prod.rpm \
    -O /tmp/microsoft-prod.rpm

rpm -Uvh /tmp/microsoft-prod.rpm || true
dnf install -y dotnet-runtime-8.0

# ----------------------------------------
# Install YTSubConverter (.tar.xz)
# ----------------------------------------
echo "Installing YTSubConverter..."

if [ ! -f "./YTSubConverter-Linux.tar.xz" ]; then
    echo "ERROR: YTSubConverter-Linux.tar.xz not found!"
    exit 1
fi

rm -rf /opt/ytsubconverter
mkdir -p /opt/ytsubconverter

# IMPORTANT: no --strip-components (your archive has no top-level dir)
tar -xJf ./YTSubConverter-Linux.tar.xz -C /opt/ytsubconverter

# ----------------------------------------
# Create ytsubconverter CLI wrapper (kept)
# ----------------------------------------
cat << 'EOF' > /usr/local/bin/ytsubconverter
#!/bin/bash
exec dotnet /opt/ytsubconverter/ytsubconverter.dll "$@"
EOF

chmod +x /usr/local/bin/ytsubconverter

# ----------------------------------------
# Install srv3
# ----------------------------------------
if [ ! -f "./srv3" ]; then
    echo "ERROR: srv3 script not found!"
    exit 1
fi

install -m 755 -o root -g root ./srv3 /usr/local/bin/srv3

# ----------------------------------------
# Ensure Videos directory exists
# ----------------------------------------
mkdir -p "$REAL_HOME/Videos"
chown "$REAL_USER":"$REAL_USER" "$REAL_HOME/Videos"

# ----------------------------------------
# Final verification
# ----------------------------------------
echo
echo "yt-dlp version:"
yt-dlp --version
echo
echo "ytsubconverter test:"
ytsubconverter --help || true
echo
echo "==============================="
echo " INSTALLATION COMPLETE ✅"
echo "==============================="
echo
echo "Run from anywhere:"
echo "  srv3 \"https://youtube.com/...\""
echo
