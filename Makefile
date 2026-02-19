.PHONY: help server build clean deploy new-post update-theme init-submodules install-hooks

help: ## Mostrar esta ayuda
	@echo "Comandos disponibles:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

server: ## Ejecutar servidor local de desarrollo
	hugo server -D --bind 0.0.0.0 --baseURL http://localhost

build: ## Generar sitio estático en ./public
	hugo --minify

clean: ## Limpiar archivos generados
	rm -rf public/ resources/

deploy: build ## Build y preparar para deploy
	@echo "Sitio generado en ./public - listo para GitHub Pages"

new-post: ## Crear nuevo post (uso: make new-post TITLE="Mi Post")
	@if [ -z "$(TITLE)" ]; then \
		echo "Error: Debes especificar TITLE. Ejemplo: make new-post TITLE=\"Mi Post\""; \
		exit 1; \
	fi; \
	hugo new posts/$(shell echo "$(TITLE)" | sed 's/ /-/g' | tr '[:upper:]' '[:lower:]').md

update-theme: ## Actualizar tema PaperMod
	git submodule update --remote --merge

init-submodules: ## Inicializar submódulos (útil después de clonar)
	git submodule update --init --recursive

install-hooks: ## Instalar git hooks del proyecto
	@bash scripts/install-hooks.sh
