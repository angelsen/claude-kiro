.PHONY: help version-patch version-minor version-major format-docs build publish clean

help:
	@echo "Claude Kiro - Development Commands"
	@echo ""
	@echo "Version bumping:"
	@echo "  make version-patch    Bump patch version (0.0.X)"
	@echo "  make version-minor    Bump minor version (0.X.0)"
	@echo "  make version-major    Bump major version (X.0.0)"
	@echo ""
	@echo "Formatting:"
	@echo "  make format-docs      Format HTML/CSS/JS with prettier"
	@echo ""
	@echo "Build & publish:"
	@echo "  make build            Build source distribution and wheel"
	@echo "  make publish          Publish to PyPI (requires pass: pypi/uv-publish)"
	@echo "  make clean            Remove build artifacts"

version-patch:
	uv version --bump patch

version-minor:
	uv version --bump minor

version-major:
	uv version --bump major

format-docs:
	prettier --write "docs/**/*.{html,css,js}"

build:
	uv build

publish:
	uv publish --token "$$(pass show pypi/uv-publish)"

clean:
	rm -rf dist/ *.egg-info
