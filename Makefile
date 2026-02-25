.PHONY: help server build clean deploy new-post new-micropost update-theme init-submodules install-hooks

help: ## Show this help
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

server: ## Run local development server
	hugo server -D --bind 0.0.0.0 --baseURL http://localhost

build: ## Generate static site into ./public
	hugo --minify

clean: ## Remove generated files
	rm -rf public/ resources/

deploy: build ## Build and prepare for deploy
	@echo "Site generated in ./public - ready for GitHub Pages"

new-post: ## Create a new post (usage: make new-post TITLE="My Post")
	@if [ -z "$(TITLE)" ]; then \
		echo "Error: TITLE is required. Example: make new-post TITLE=\"My Post\""; \
		exit 1; \
	fi; \
	hugo new posts/$(shell echo "$(TITLE)" | sed 's/ /-/g' | tr '[:upper:]' '[:lower:]').md

new-micropost: ## Create a micropost from a URL (usage: make new-micropost URL="https://...")
	@if [ -z "$(URL)" ]; then \
		echo "Error: URL is required. Example: make new-micropost URL=\"https://example.com\""; \
		exit 1; \
	fi; \
	python3 scripts/new-micropost.py "$(URL)" $(if $(DRAFT),--draft,)

update-theme: ## Update PaperMod theme
	git submodule update --remote --merge

init-submodules: ## Initialize submodules (useful after cloning)
	git submodule update --init --recursive

install-hooks: ## Install project git hooks
	@bash scripts/install-hooks.sh
