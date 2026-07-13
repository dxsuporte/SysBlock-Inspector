#!/usr/bin/env bash

# ==============================================================================
# PROGRAMMER: High-efficiency Automated Compiler Script for SysBlock-Inspector Binary.
# Automatically cleans residual caches, invokes PyInstaller, and bundles assets.
# Integrated with python3 -m wrappers to ensure cross-environment binary deployments.
# ==============================================================================

# Exit immediately if any command inside the script fails
set -e

echo "========================================================"
echo "⚡ INICIANDO O COMPILADOR AUTOMÁTICO DO SysBlock-Inspector ⚡"
echo "========================================================"

# 1. CLEANING LAYER: Uses administrative sudo to bypass root-owned __pycache__ permissions locks
echo "🧹 Fazendo a faxina administrativa de caches e binários antigos..."
sudo rm -rf build/ dist/ __pycache__ gui/__pycache__ *.spec

# 2. COMPILATION LAYER: Invokes PyInstaller via Python module to bypass PATH binary drift locks
echo "📦 Empacotando e compilando em arquivo único executável..."
python3 -m PyInstaller --clean --onefile --windowed \
  --add-data "gui:gui" \
  --add-data "icon.png:." \
  --name "SysBlock-Inspector" \
  main.py

# 3. CHMOD PERMISSIONS LAYER: Ensures the final binary has execution rights for double-click
if [ -f "dist/SysBlock-Inspector" ]; then
    echo "🔒 Aplicando permissões de execução no binário final..."
    chmod +x dist/SysBlock-Inspector
    
    echo "========================================================"
    echo "🎉 SUCESSO TOTAL MÁXIMO ABSOLUTO!"
    echo "📦 O seu arquivo único portátil está pronto na pasta: dist/SysBlock-Inspector"
    echo "========================================================"
else
    echo "❌ Erro: O arquivo binário final não foi encontrado na pasta dist."
    exit 1
fi
