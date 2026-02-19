# Instrucciones para GitHub Copilot

Este documento contiene las directrices y contexto para que GitHub Copilot ayude eficientemente en el desarrollo de este blog.

## 📋 Contexto del Proyecto

### Tecnologías
- **Framework**: Hugo (Static Site Generator)
- **Versión Hugo**: 0.139.3 (extended)
- **Tema**: PaperMod (submódulo git)
- **Deploy**: GitHub Pages con GitHub Actions
- **Lenguaje**: Markdown para contenido, TOML para configuración

### Estructura del Blog
```
hugo.github.io/
├── content/posts/          # Artículos del blog
├── static/                 # Archivos estáticos (CNAME, imágenes, etc.)
├── themes/PaperMod/        # Tema (submódulo)
├── .github/workflows/      # CI/CD
├── hugo.toml              # Configuración principal
└── Makefile               # Comandos útiles
```

## 🎯 Objetivos del Proyecto

1. **Blog técnico**: Contenido sobre programación, DevOps, bases de datos, desarrollo web
2. **SEO crítico**: Mantener URLs legacy de Pelican (`/YYYY/MM/DD/slug/`)
3. **Búsqueda**: Integrada con Fuse.js en el frontend
4. **Deploy automático**: Push a `main` → GitHub Actions → GitHub Pages

## 🔧 Convenciones de Código

### Formato de Posts
Todos los artículos deben seguir este frontmatter:

```markdown
---
title: "Título del Post"
date: YYYY-MM-DDTHH:MM:SS+01:00
draft: false
tags: ["tag1", "tag2", "tag3"]
slug: url-amigable-del-post
description: "Descripción breve para SEO"
---

## Contenido aquí...
```

### Comandos Comunes
- `make server` - Servidor de desarrollo local
- `make build` - Generar sitio estático
- `make new-post TITLE="Título"` - Crear nuevo post
- `make clean` - Limpiar archivos generados

### URLs Legacy (CRÍTICO)
Las URLs DEBEN mantener este formato exacto para SEO:
```
/YYYY/MM/DD/slug/
```

Configurado en `hugo.toml`:
```toml
[permalinks]
  posts = '/:year/:month/:day/:slug/'
```

## 📝 Al Crear Contenido

### Posts de Blog
- **Idioma**: Español
- **Tono**: Técnico pero accesible
- **Código**: Incluir ejemplos prácticos con syntax highlighting
- **SEO**: Siempre incluir `description` en frontmatter
- **Tags**: Usar tags relevantes y consistentes

### Ejemplos de Código
Usar bloques de código con el lenguaje especificado:

````markdown
```python
def ejemplo():
    return "Código con syntax highlighting"
```
````

### Imágenes
Colocar en `static/images/` y referenciar como:
```markdown
![Descripción](/images/nombre-imagen.png)
```

## 🚫 Restricciones y Cuidados

### NO incluir:
- ❌ Credenciales reales (contraseñas, tokens, API keys)
- ❌ Rutas locales del sistema (`/home/user/...`)
- ❌ Información personal sensible
- ❌ Claves SSH o certificados

### NO modificar sin confirmar:
- ⚠️ Formato de permalinks (URLs legacy)
- ⚠️ Configuración de GitHub Actions
- ⚠️ Submódulo del tema PaperMod

### Siempre verificar:
- ✅ Formato de fechas en frontmatter (ISO 8601)
- ✅ Field `slug` presente en cada post
- ✅ Tags entre comillas y como array
- ✅ Draft: false para posts publicados

## 🔍 Búsqueda y Navegación

### Configuración de Búsqueda
El sitio usa Fuse.js para búsqueda en el frontend:
- Archivo especial: `content/search.md`
- Output JSON configurado en `hugo.toml`
- Índice en: `public/index.json`

### Menú Principal
Configurado en `hugo.toml` bajo `[menu.main]`:
- Posts
- Tags
- Buscar

## 🛠️ Tareas Comunes

### Crear un nuevo post
```bash
make new-post TITLE="Mi Post"
# Editar: content/posts/mi-post.md
# Verificar: make server
# Commit y push
```

### Actualizar tema PaperMod
```bash
make update-theme
# Verificar cambios
git commit -am "Update PaperMod theme"
git push
```

### Debugging
```bash
# Ver errores de build
hugo --verbose

# Limpiar y rebuild
make clean && make build

# Ver logs de GitHub Actions
# Ir a: https://github.com/karpoke/hugo.github.io/actions
```

## 📦 Deploy

### Proceso Automático
1. Push a rama `main`
2. GitHub Actions ejecuta workflow
3. Hugo genera sitio estático
4. Deploy a GitHub Pages
5. Sitio actualizado en ~1-2 minutos

### Workflow
- Archivo: `.github/workflows/hugo.yml`
- Hugo version: 0.139.3
- Incluye: Dart Sass, optimizaciones, minify

## 🎨 Personalización del Tema

### Configuración PaperMod
En `hugo.toml` bajo `[params]`:
- Búsqueda habilitada
- Botones de compartir
- Código con botón copiar
- TOC (tabla de contenidos)
- Lectura estimada
- Breadcrumbs

### Overrides
Para personalizar el tema, crear archivos en:
- `layouts/` - Para templates
- `assets/` - Para CSS/JS custom
- `static/` - Para archivos estáticos

## 📚 Recursos

### Documentación
- [Hugo Docs](https://gohugo.io/documentation/)
- [PaperMod Wiki](https://github.com/adityatelange/hugo-PaperMod/wiki)
- [Hugo Permalinks](https://gohugo.io/content-management/urls/)

### Comandos Hugo Útiles
```bash
hugo --help
hugo server --help
hugo new --help
hugo config
```

## 🧪 Testing

### Local
```bash
# Servidor con drafts
make server

# Build de producción
make build

# Verificar enlaces rotos
hugo --printPathWarnings
```

### Pre-Deploy Checklist
- [ ] ✅ Links internos funcionan
- [ ] ✅ Imágenes cargan correctamente
- [ ] ✅ URLs siguen formato legacy
- [ ] ✅ Búsqueda funciona
- [ ] ✅ Sin errores en `hugo --verbose`
- [ ] ✅ Tags correctos
- [ ] ✅ Fecha en formato ISO

## 🔐 Seguridad

### Información Sensible
**NUNCA incluir en código/commits**:
- Contraseñas reales
- Tokens de API
- Claves privadas SSH
- Variables de entorno con secretos

### Ejemplos de Código
Los ejemplos en artículos **PUEDEN** incluir:
- Contraseñas de ejemplo (`dev_password_123`)
- URLs de ejemplo (`ejemplo.com`)
- Datos ficticios para tutoriales

### .gitignore
Verificar que incluye:
- `public/`
- `resources/`
- `.env`
- `*.log`
- Archivos IDE (`.idea/`, `.vscode/`)

## 💡 Sugerencias para Copilot

### Al generar contenido de blog:
1. Usar español técnico pero claro
2. Incluir ejemplos de código reales
3. Añadir tablas cuando sea útil
4. Usar emojis con moderación (solo en títulos)
5. Crear listas para mejor legibilidad

### Al modificar configuración:
1. Comentar cambios importantes
2. Mantener formato TOML limpio
3. Documentar nuevas features
4. Verificar compatibilidad con PaperMod

### Al crear comandos Make:
1. Añadir comentario de ayuda (`## descripción`)
2. Usar `.PHONY` para targets
3. Manejar errores apropiadamente

## 🎓 Patrones del Proyecto

### Naming Conventions
- **Archivos**: kebab-case (`mi-post.md`)
- **Slugs**: kebab-case sin acentos (`optimizando-consultas-sql`)
- **Tags**: lowercase, español (`python`, `bases-de-datos`)
- **Ramas git**: kebab-case (`feature/nueva-funcionalidad`)

### Commits
Usar mensajes descriptivos:
```
Add: Nueva funcionalidad
Update: Cambio en existente
Fix: Corrección de bug
Docs: Documentación
```

## 🚀 Roadmap Futuro

Posibles mejoras a considerar:
- [ ] Migración de contenido desde Pelican
- [ ] Analytics (Google Analytics o alternativa)
- [ ] Comentarios (Disqus, Utterances)
- [ ] Newsletter
- [ ] Categorías adicionales
- [ ] Series de posts relacionados
- [ ] Modo oscuro automático

---

**Última actualización**: Febrero 2026  
**Mantenedor**: Ignacio Cano (@karpoke)  
**Repositorio**: https://github.com/karpoke/hugo.github.io
