#!/bin/bash
# Script para instalar git hooks del proyecto

echo "📦 Instalando git hooks..."

# Crear directorio de hooks si no existe
mkdir -p .git/hooks

# Copiar pre-commit hook
if [ -f "scripts/pre-commit" ]; then
    cp scripts/pre-commit .git/hooks/pre-commit
    chmod +x .git/hooks/pre-commit
    echo "✅ Pre-commit hook instalado"
else
    echo "❌ Error: No se encontró scripts/pre-commit"
    exit 1
fi

echo ""
echo "🎉 Git hooks instalados correctamente"
echo ""
echo "El hook pre-commit validará que Hugo puede generar el sitio antes de cada commit."
echo "Si necesitas saltarte la validación en algún commit, usa: git commit --no-verify"
