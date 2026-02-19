# Git Pre-Commit Hook - Documentación

## 🎯 Objetivo

El hook pre-commit valida automáticamente que Hugo puede generar el sitio antes de cada commit, previniendo errores de sintaxis o configuración que rompan el build.

## 📁 Archivos creados

### 1. `.git/hooks/pre-commit` (local, no se sube)
El hook activo que git ejecuta antes de cada commit.

### 2. `scripts/pre-commit` (se sube al repo)
Versión compartible del hook que otros desarrolladores pueden instalar.

### 3. `scripts/install-hooks.sh`
Script de instalación para facilitar el setup del hook.

## 🔧 Instalación

Para nuevos desarrolladores que clonen el repositorio:

```bash
make install-hooks
```

O manualmente:
```bash
bash scripts/install-hooks.sh
```

## ✅ ¿Qué valida el hook?

1. **Hugo está instalado**: Verifica que el comando `hugo` esté disponible
2. **Build exitoso**: Ejecuta `hugo --quiet --minify` 
3. **Sin errores**: Si hay errores de sintaxis, configuración o contenido, el commit es rechazado
4. **Limpieza automática**: Elimina `public/` y `resources/` después de la validación

## 🚀 Flujo de trabajo

```bash
# 1. Modificas archivos
vim content/posts/mi-post.md

# 2. Añades al staging
git add content/posts/mi-post.md

# 3. Intentas hacer commit
git commit -m "Add new post"

# 4. El hook se ejecuta automáticamente:
#    🔍 Pre-commit hook: Validando build de Hugo...
#    ✅ Build de Hugo exitoso
#    [main abc1234] Add new post

# 5. Si hay errores:
#    ❌ Error: El build de Hugo falló
#    [muestra los errores]
#    Commit rechazado
```

## 🆘 Saltar el hook (emergencias)

En casos excepcionales donde necesitas hacer commit aunque el build falle:

```bash
git commit --no-verify -m "WIP: trabajo en progreso"
```

**⚠️ Advertencia**: Solo usar en emergencias, ya que puede romper el deploy automático.

## 🧪 Probar el hook manualmente

```bash
# Ejecutar el hook sin hacer commit
bash .git/hooks/pre-commit

# O ejecutar el script fuente
bash scripts/pre-commit
```

## 📊 Ejemplo de salida

### Build exitoso:
```
🔍 Pre-commit hook: Validando build de Hugo...
✅ Build de Hugo exitoso
```

### Build con errores:
```
🔍 Pre-commit hook: Validando build de Hugo...
❌ Error: El build de Hugo falló

Errores encontrados:
ERROR the "date" front matter field is not a parsable date: see /path/to/post.md
ERROR render of "page" failed: template error

Por favor, corrige los errores antes de hacer commit.
Puedes ejecutar 'hugo --verbose' para más detalles.
```

## 🔄 Actualizar el hook

Si el hook se actualiza en el repositorio:

```bash
make install-hooks  # Reinstalar la última versión
```

## 🛠️ Personalización

Para modificar el hook, edita `scripts/pre-commit` y luego ejecuta:

```bash
make install-hooks
```

## 📝 Beneficios

- ✅ **Prevención temprana**: Detecta errores antes de hacer commit
- ✅ **CI/CD más rápido**: Evita pushes que fallarían en GitHub Actions
- ✅ **Consistencia**: Todos los desarrolladores usan la misma validación
- ✅ **Feedback inmediato**: Errores reportados en segundos, no minutos

## ❓ Troubleshooting

### El hook no se ejecuta
```bash
# Verificar que existe y es ejecutable
ls -la .git/hooks/pre-commit

# Si no existe, reinstalar
make install-hooks
```

### Hugo no encontrado
```bash
# Instalar Hugo
# Ver: https://gohugo.io/installation/
```

### Quiero deshabilitar el hook permanentemente
```bash
# Renombrar el hook
mv .git/hooks/pre-commit .git/hooks/pre-commit.disabled
```

---

**Nota**: Los archivos en `.git/hooks/` son locales y no se suben al repositorio. Por eso incluimos `scripts/pre-commit` y `scripts/install-hooks.sh` en el repo para que otros puedan instalarlo fácilmente.
