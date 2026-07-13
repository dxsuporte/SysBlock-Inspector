#!/usr/bin/env bash

# ==============================================================================
# PROGRAMMER: Native Fedora RPM Package Builder for GitHub Clones.
# Executes PyInstaller and uses native rpmbuild toolchains to build installers.
# Calibrated with full image file extensions to guarantee icon display on Fedora.
# TARGET OUTPUT: Packages the final .rpm inside the dist/ directory context.
# ==============================================================================

set -e

echo "========================================================"
echo "⚙️ COMPILANDO E GERANDO PACOTE NATIVO FEDORA (.RPM) ⚙️"
echo "========================================================"

# Check if the Fedora environment has the rpmbuild toolkit active
if ! command -v rpmbuild &> /dev/null; then
    echo "⚠️  Ferramenta 'rpmbuild' não detectada no seu Fedora."
    echo "🛠️ Instale executando: sudo dnf install rpm-build -y"
    exit 1
fi

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
RPM_ROOT="/tmp/SysBlock-Inspector-rpm-build"
rm -rf "$RPM_ROOT"
mkdir -p "$RPM_ROOT"/{BUILD,RPMS,SOURCES,SPECS,SRPMS}
mkdir -p "$RPM_ROOT"/BUILDROOT/SysBlock-Inspector-1.0-1.x86_64/usr/bin
mkdir -p "$RPM_ROOT"/BUILDROOT/SysBlock-Inspector-1.0-1.x86_64/usr/share/applications
mkdir -p "$RPM_ROOT"/BUILDROOT/SysBlock-Inspector-1.0-1.x86_64/usr/share/pixmaps

# Copy files directly into their buildroot destinations
cp dist/SysBlock-Inspector "$RPM_ROOT"/BUILDROOT/SysBlock-Inspector-1.0-1.x86_64/usr/bin/SysBlock-Inspector
cp icon.png "$RPM_ROOT"/BUILDROOT/SysBlock-Inspector-1.0-1.x86_64/usr/share/pixmaps/SysBlock-Inspector.png

# 3. Create the native dynamic desktop application launcher icon (FIXED ICON EXTENSION)
cat << 'EOF' > "$RPM_ROOT"/BUILDROOT/SysBlock-Inspector-1.0-1.x86_64/usr/share/applications/SysBlock-Inspector.desktop
[Desktop Entry]
Version=1.0
Type=Application
Name=SysBlock-Inspector
Comment=Monitor de Hardware e Diagnóstico de Bancada
Exec=SysBlock-Inspector
Icon=SysBlock-Inspector.png
Terminal=false
Categories=System;Monitor;
EOF

# 4. Create the strict building block specifications file for Fedora (.spec)
cat << 'EOF' > "$RPM_ROOT"/SPECS/SysBlock-Inspector.spec
Name:           SysBlock-Inspector
Version:        1.0
Release:        1%{?dist}
Summary:        Monitor de Hardware e Diagnóstico de Bancada Premium
License:        GPL
URL:            https://github.com
BuildArch:      x86_64

%description
Monitor de Hardware e Diagnóstico de Bancada Premium Industrial.

%files
/usr/bin/SysBlock-Inspector
/usr/share/applications/SysBlock-Inspector.desktop
/usr/share/pixmaps/SysBlock-Inspector.png

%changelog
* Sun Jul 12 2026 Danilo <danilo@dx-desk> - 1.0-1
- Initial release build pipeline mapping framework.
EOF

# 5. Invoke the core system packager tool
echo "📦 Executando compilação do pacote RPM no Fedora e salvando em dist/..."
# Ensure the target directory exists and prune any matching stale rpm packages inside it
mkdir -p dist
rm -f dist/*.rpm

# Run the native Fedora compiler
rpmbuild --define "_topdir $RPM_ROOT" -bb "$RPM_ROOT"/SPECS/SysBlock-Inspector.spec

# PROG: FIXED! Redirects the output package stream straight into the local dist/ folder
mv "$RPM_ROOT"/RPMS/x86_64/*.rpm dist/

# Clean temporary folders
rm -rf "$RPM_ROOT"

echo "========================================================"
echo "🎉 INSTALADOR FEDORA/RPM GERADO COM SUCESSO!"
echo "📄 Arquivo pronto: $(ls dist/*.rpm)"
echo "========================================================"
