# 🎉 Blog Hugo - Setup Completado

## ✅ Estado actual

- ✅ Repositorio creado en: https://github.com/karpoke/hugo.github.io
- ✅ Push inicial realizado exitosamente
- ✅ Tema PaperMod instalado
- ✅ 3 artículos de ejemplo creados
- ✅ Configuración de URLs legacy: `/YYYY/MM/DD/slug/`
- ✅ GitHub Actions configurado
- ✅ Búsqueda integrada habilitada

## 📋 Próximos pasos

### 1. Activar GitHub Pages

Ve a tu repositorio en GitHub:
https://github.com/karpoke/hugo.github.io/settings/pages

Configuración:
- **Source**: GitHub Actions
- Espera a que se complete el primer deploy (verás el workflow en Actions)
- Una vez completado, el sitio estará en: https://karpoke.github.io/hugo.github.io/

### 2. Configurar dominio personalizado (opcional)

Si quieres usar `blog.ignaciocano.com`:

1. En tu proveedor DNS, añade un registro CNAME:
   ```
   blog.ignaciocano.com -> karpoke.github.io
   ```

2. Actualiza el CNAME en tu repo:
   ```bash
   echo "blog.ignaciocano.com" > static/CNAME
   ```

3. Actualiza `hugo.toml`:
   ```toml
   baseURL = 'https://blog.ignaciocano.com/'
   ```

4. Commit y push:
   ```bash
   git add static/CNAME hugo.toml
   git commit -m "Update domain to blog.ignaciocano.com"
   git push
   ```

5. En GitHub Pages settings, añade el custom domain: `blog.ignaciocano.com`

### 3. Probar el sitio localmente

```bash
cd /home/hbxuser/karpoke/hugo.github.io
make server
# O directamente:
hugo server -D
```

Visita: http://localhost:1313

### 4. Verificar URLs legacy

Una vez desplegado, verifica que las URLs funcionan:
- https://karpoke.github.io/hugo.github.io/2024/01/15/bienvenido-al-blog/
- https://karpoke.github.io/hugo.github.io/2024/02/10/optimizando-consultas-sql/
- https://karpoke.github.io/hugo.github.io/2024/03/05/docker-compose-desarrollo/

### 5. Migrar contenido de Pelican

Cuando estés listo para migrar tus artículos de Pelican, necesitarás:

1. **Script de conversión** para el frontmatter:
   ```python
   # Convertir de:
   Title: Mi Post
   Date: 2024-01-15 10:30
   Tags: python, web
   Slug: mi-post
   
   # A:
   title: "Mi Post"
   date: 2024-01-15T10:30:00+01:00
   tags: ["python", "web"]
   slug: mi-post
   draft: false
   ```

2. **Mover los archivos** a `content/posts/`

3. **Verificar** que las URLs se mantienen igual

¿Necesitas ayuda con el script de migración?

## 🛠️ Comandos útiles

```bash
# Desarrollo
make server          # Iniciar servidor local
make build           # Generar sitio estático
make clean           # Limpiar archivos generados

# Contenido
make new-post TITLE="Mi Nuevo Post"  # Crear post

# Git
git add .
git commit -m "mensaje"
git push

# Actualizar tema
make update-theme
```

## 🔍 Características del blog

- **Búsqueda**: Disponible en `/search/`
- **Tags**: Organizados en `/tags/`
- **RSS**: Feed en `/index.xml`
- **Responsive**: Mobile-friendly
- **Syntax Highlighting**: Para bloques de código
- **Copy button**: En todos los bloques de código

## 📁 Estructura de archivos

```
hugo.github.io/
├── .github/workflows/  # GitHub Actions
├── content/
│   ├── posts/         # Tus artículos aquí
│   └── search.md      # Página de búsqueda
├── static/
│   └── CNAME          # Dominio personalizado
├── themes/PaperMod/   # Tema (submódulo)
├── hugo.toml          # Configuración principal
├── Makefile           # Comandos útiles
└── README.md          # Documentación
```

## 🚀 Deploy automático

Cada vez que hagas `git push` a la rama `main`:
1. GitHub Actions se ejecuta automáticamente
2. Genera el sitio con Hugo
3. Despliega a GitHub Pages
4. El sitio se actualiza en ~1-2 minutos

## 📝 Crear un nuevo post

```bash
# Opción 1: Con make
make new-post TITLE="Mi Post"

# Opción 2: Manual
hugo new posts/mi-post.md
```

Luego edita el archivo en `content/posts/mi-post.md`:

```markdown
---
title: "Mi Post"
date: 2024-02-19T10:00:00+01:00
draft: false
tags: ["tag1", "tag2"]
slug: mi-post
description: "Descripción breve"
---

## Contenido

Tu contenido aquí...
```

## ❓ Problemas comunes

### El sitio no se despliega
- Verifica que GitHub Pages esté activado con "GitHub Actions" como source
- Revisa los logs en la pestaña "Actions" del repositorio

### Las URLs no funcionan como esperado
- Verifica que `permalinks` esté configurado en `hugo.toml`
- Asegúrate de que cada post tenga el campo `slug` en el frontmatter

### La búsqueda no funciona
- Verifica que `content/search.md` exista
- Asegúrate de que `outputs` incluya `["HTML", "RSS", "JSON"]` en `hugo.toml`

## 📞 Siguiente paso

Visita https://github.com/karpoke/hugo.github.io/actions para ver el progreso del deploy inicial.

Una vez completado, tu blog estará disponible en:
**https://karpoke.github.io/hugo.github.io/**
