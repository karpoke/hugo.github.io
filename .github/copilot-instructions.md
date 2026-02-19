# Instrucciones para GitHub Copilot

Este documento contiene las directrices y contexto para que GitHub Copilot ayude eficientemente en el desarrollo de este blog.

## 📋 Contexto del Proyecto

### Tecnologías
- **Framework**: Hugo (Static Site Generator)
- **Versión Hugo**: 0.156.0 (extended)
- **Tema**: PaperMod (submódulo git)
- **Deploy**: GitHub Pages con GitHub Actions
- **Lenguaje**: Markdown para contenido, TOML para configuración
- **Título del sitio**: Karpoke - Just Another Hugo Blog
- **Dominio**: hugo.github.io (temporal), blog.ignaciocano.com (final)
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
- Hugo version: 0.156.0
- Incluye: Dart Sass, optimizaciones, minify

## 🎨 Personalización del Tema

### Configuración PaperMod
En `hugo.toml` bajo `[params]`:
- Búsqueda habilitada con Fuse.js
- Botones de compartir en posts (X/Twitter, LinkedIn, Reddit, Facebook, WhatsApp, Telegram, HackerNews)
- Código con botón copiar
- TOC (tabla de contenidos)
- Lectura estimada
- Breadcrumbs
- Icono social de GitHub en header apuntando a `https://github.com/karpoke/`
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

## ⚙️ Configuración de Git

### Pager desactivado
El proyecto está configurado para NO usar pager en git (útil para scripting y CI/CD):

```bash
# Configuración aplicada en .git/config:
core.pager = cat
pager.branch = false
pager.log = false
pager.diff = false
```

Esto significa que comandos como `git log`, `git diff`, `git branch` mostrarán la salida directamente sin usar `less` o similar.

### SSH personalizado
El repositorio usa una clave SSH específica:
```bash
core.sshCommand = ssh -i /home/hbxuser/karpoke/ssh/id_rsa -o IdentitiesOnly=yes
```

**Nota**: Esta configuración es local y no se sube al repositorio.

### Git Hooks
El proyecto incluye un hook pre-commit que valida el build de Hugo:

```bash
# Instalar hooks
make install-hooks

# Ubicación del hook
.git/hooks/pre-commit  # Hook activo (no se sube al repo)
scripts/pre-commit     # Script fuente (se sube al repo)
```

**Qué hace el pre-commit hook:**
- ✅ Valida que Hugo puede generar el sitio sin errores
- ✅ Ejecuta `hugo --quiet --minify`
- ✅ Limpia archivos generados automáticamente
- ✅ Previene commits con errores de sintaxis

**Saltar el hook (solo emergencias):**
```bash
git commit --no-verify -m "mensaje"
```

## 🎯 Reglas de Automatización

### Comandos sin Confirmación
Los siguientes comandos NO requieren confirmación previa, incluso si se ejecutan encadenados con `&&`:
- `cd` - Cambiar de directorio
- `git add` - Añadir archivos al staging
- `git diff` - Ver diferencias en archivos
- `git log` - Ver historial de commits
- `git status` - Ver estado del repositorio
- `git check-ignore` - Verificar si archivos están ignorados
- `git show` - Mostrar commits
- `git reflog` - Ver historial de referencias

Ejemplos que NO requieren confirmación:
```bash
cd /ruta && git add archivo.txt
git diff archivo.txt
git status
```

### Compilación de Hugo y Servidor Local
**IMPORTANTE**: Antes de ejecutar `hugo` para compilar el sitio:
1. Verificar si el servidor local está en ejecución (`make server`)
2. Si el servidor está activo, **NO ejecutar `hugo`** directamente
3. Si el servidor está en ejecución, los cambios ya están compilados automáticamente en memoria
4. Solo ejecutar `hugo` directamente cuando el servidor local NO esté corriendo

**Comandos relacionados:**
```bash
# Verificar si el servidor está corriendo
lsof -i :1313
ps aux | grep "hugo server"

# Si el servidor está corriendo, los cambios ya están compilados
# Si necesitas generar el sitio estático, primero detén el servidor:
# Ctrl+C en la ventana del servidor
# Luego ejecuta: hugo
```

### Comandos que Requieren Autorización Explícita del Usuario
- `git commit` - NO hacer commit hasta que el usuario lo pida explícitamente
- `git push` - NUNCA hacer push sin confirmación explícita del usuario
- `git push --force` - Comando peligroso, requiere confirmación
- `git reset --hard` - Comando destructivo, requiere confirmación
- `git rebase` - Comando que reescribe historia
- `git force-push` - Variante de push --force

**Importante**: Aunque los archivos estén en staging con `git add`, NO ejecutar `git commit` hasta que el usuario lo solicite específicamente.

### Actualización Automática de Instrucciones
Cuando se detecten nuevas reglas o convenciones durante el trabajo:
- Actualizar este archivo automáticamente
- Incluir en el mismo commit donde se aplique la regla
- Documentar el cambio en la sección apropiada

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
Usar semantic commit messages siguiendo el formato: `type(scope): description`

**Tipos de commits permitidos:**
- `feat:` - Nueva funcionalidad
- `fix:` - Corrección de bug
- `docs:` - Cambios en documentación
- `style:` - Cambios de formato (espacios, comillas, etc.) sin afectar código
- `refactor:` - Refactorización de código sin cambiar funcionalidad
- `perf:` - Mejoras de performance
- `test:` - Añadir o modificar tests
- `chore:` - Cambios en herramientas de build, dependencias, etc.
- `ci:` - Cambios en configuración de CI/CD

**Scope (opcional pero recomendado):**
- `hugo` - Configuración de Hugo
- `post` - Artículos del blog
- `theme` - Cambios en tema PaperMod
- `hooks` - Git hooks
- `workflow` - GitHub Actions

**Ejemplos correctos:**
```
feat(post): add new article about Docker Compose
fix(hugo): correct date format in frontmatter
docs(copilot-instructions): clarify semantic commit rules
feat(theme): add custom CSS for syntax highlighting
chore(deps): update PaperMod to latest version
ci(workflow): update Hugo version to 0.156.0
```

**Formato completo:**
```
type(scope): description

[cuerpo opcional - detalles adicionales si es necesario]

[footer opcional - referencias a issues, breaking changes, etc.]
```


---

**Última actualización**: Febrero 2026  
**Mantenedor**: Nacho Cano (@karpoke)  
**Repositorio**: https://github.com/karpoke/hugo.github.io
