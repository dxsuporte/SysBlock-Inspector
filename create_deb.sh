#!/usr/bin/env bash

# ==============================================================================
# PROGRAMMER: Native Debian Package Builder for GitHub Clones.
# Executes PyInstaller and uses native dpkg-deb toolchains to build installers.
# Calibrated with rigid absolute lowercase pixmap paths to guarantee Mint icons.
# TARGET OUTPUT: Packages the final .deb inside the dist/ directory context.
# ==============================================================================

set -e

echo "========================================================"
echo "🧬 COMPILANDO E GERANDO PACOTE NATIVO DEBIAN (.DEB) 🧬"
echo "========================================================"

# 1. Trigger the master core PyInstaller compilation
if [ -f "./build.sh" ]; then
    echo "⚡ Chamando o motor de compilação do executável..."
    ./build.sh
else
    echo "❌ Erro: Script ./build.sh não encontrado na raiz."
    exit 1
fi

# 2. Build temporary structure mapping paths strings tokens
echo "🏗️ Estruturando diretórios temporários do pacote..."
TEMP_DIR="/tmp/sysblock-inspector-deb-build"
rm -rf "$TEMP_DIR"
mkdir -p "$TEMP_DIR/usr/bin"
mkdir -p "$TEMP_DIR/usr/share/applications"
mkdir -p "$TEMP_DIR/usr/share/pixmaps"
mkdir -p "$TEMP_DIR/DEBIAN"

# PROG: FIXED! Copies the binary and the icon using unified secure lowercase registers
cp dist/SysBlock-Inspector "$TEMP_DIR/usr/bin/sysblock-inspector"
cp icon.png "$TEMP_DIR/usr/share/pixmaps/sysblock-inspector.png"

# 3. Create the administrative metadata control file
cat << 'EOF' > "$TEMP_DIR/DEBIAN/control"
Package: sysblock-inspector
Version: 1.0
Section: utils
Priority: optional
Architecture: amd64
Maintainer: Danilo Assistência Técnica
Description: Monitor de Hardware e Diagnóstico de Bancada Premium.
 Utilitário portátil industrial para auditoria de silício e firmware.
EOF

# 4. Create the native dynamic desktop application launcher icon (FIXED ABSOLUTE PATH)
cat << 'EOF' > "$TEMP_DIR/usr/share/applications/sysblock-inspector.desktop"
[Desktop Entry]
Version=1.0
Type=Application
Name=SysBlock-Inspector
Comment=Monitor de Hardware e Diagnóstico de Bancada
Exec=sysblock-inspector
Icon=/usr/share/pixmaps/sysblock-inspector.png
Terminal=false
Categories=System;Monitor;
EOF

# 5. Invoke the core system packager tool
echo "📦 Compactando em arquivo .deb final e salvando em dist/..."
mkdir -p dist
rm -f dist/sysblock-inspector*.deb

# Redirects the output package stream straight into the local dist/ folder
dpkg-deb --build "$TEMP_DIR" dist/

# Clean temporary folders
rm -rf "$TEMP_DIR"

echo "========================================================"
echo "🎉 INSTALADOR DEBIAN/MINT GERADO COM SUCESSO!"
echo "📄 Arquivo pronto: $(ls dist/sysblock-inspector*.deb)"
echo "========================================================"
