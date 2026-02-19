# Blog de Nacho Cano

Blog técnico construido con [Hugo](https://gohugo.io/) y el tema [PaperMod](https://github.com/adityatelange/hugo-PaperMod).

Migrado desde Pelican manteniendo URLs legacy para compatibilidad SEO.

## 🚀 Desarrollo Local

### Requisitos
- Hugo (extended version)
- Git
- Make (opcional, para comandos simplificados)

### Clonar el repositorio

```bash
git clone https://github.com/USUARIO/hugo.github.io.git
cd hugo.github.io
git submodule update --init --recursive
make install-hooks  # Instalar git hooks (recomendado)
```

### Ejecutar servidor local

Con Make:
```bash
make server
```

Sin Make:
```bash
hugo server -D
```

El sitio estará disponible en `http://localhost:1313`

## 📝 Crear nuevo post

Con Make:
```bash
make new-post TITLE="Mi Nuevo Post"
```

Sin Make:
```bash
hugo new posts/mi-nuevo-post.md
```

## 🏗️ Build

```bash
make build
# o
hugo --minify
```

El sitio generado estará en `./public/`

## 📦 Deploy

El deploy a GitHub Pages se realiza automáticamente mediante GitHub Actions cuando se hace push a la rama `main`.

### Configuración en GitHub

1. Ve a Settings > Pages
2. Source: GitHub Actions
3. El dominio personalizado `blog.ignaciocano.com` ya está configurado en `static/CNAME`

## 📁 Estructura del proyecto

```
.
├── .github/workflows/  # GitHub Actions
├── content/
│   ├── posts/         # Artículos del blog
│   └── search.md      # Página de búsqueda
├── static/            # Archivos estáticos (CNAME, etc.)
├── themes/PaperMod/   # Tema (submódulo)
├── hugo.toml          # Configuración de Hugo
└── Makefile           # Comandos útiles
```

## 🔗 URLs Legacy

Las URLs mantienen el formato de Pelican para compatibilidad SEO:
```
/YYYY/MM/DD/slug/
```

Ejemplo: `/2026/02/19/migracion-pelican-a-hugo/`

## ⚙️ Comandos Make disponibles

```bash
make help           # Mostrar ayuda
make server         # Servidor de desarrollo
make build          # Generar sitio estático
make clean          # Limpiar archivos generados
make deploy         # Build para producción
make new-post       # Crear nuevo post
make update-theme   # Actualizar tema PaperMod
make install-hooks  # Instalar git hooks
```

## 🎣 Git Hooks

El proyecto incluye un hook pre-commit que valida que Hugo puede generar el sitio antes de cada commit.

### Instalación
```bash
make install-hooks
```

### ¿Qué hace?
- Ejecuta `hugo --minify` antes de cada commit
- Valida que no hay errores de build
- Limpia automáticamente los archivos generados
- Previene commits con errores de sintaxis o configuración

### Saltar el hook (emergencia)
Si necesitas hacer un commit urgente sin validación:
```bash
git commit --no-verify -m "mensaje"
```

## 🔍 Características

- ✅ Búsqueda integrada con Fuse.js
- ✅ URLs legacy de Pelican
- ✅ Diseño responsivo
- ✅ Syntax highlighting
- ✅ RSS feed
- ✅ Tags y categorías
- ✅ Deploy automático con GitHub Actions
- ✅ Dominio personalizado

## 📄 Licencia

Contenido: Todos los derechos reservados © Nacho Cano
