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

# Copiar pre-push hook
if [ -f "scripts/pre-push" ]; then
    cp scripts/pre-push .git/hooks/pre-push
    chmod +x .git/hooks/pre-push
    echo "✅ Pre-push hook instalado"
else
    echo "❌ Error: No se encontró scripts/pre-push"
    exit 1
fi

echo ""
echo "🎉 Git hooks instalados correctamente"
echo ""
echo "El hook pre-commit validará que Hugo puede generar el sitio antes de cada commit."
echo "El hook pre-push comprobará si hay una nueva versión de Hugo disponible."
echo "Si necesitas saltarte la validación, usa: git commit --no-verify / git push --no-verify"
