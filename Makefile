PYTHON := python3

.PHONY = lint test run build_macos build_windows remove-build-files

lint:
	@echo "Linting..."
	@${PYTHON} -m flake8 lento
	@echo "Done!"

test:
	@echo "Testing..."
	@${PYTHON} -m pytest tests
	@echo "Done!"

run: test lint
	@${PYTHON} app.py

build-macos: test lint
	@pyinstaller --name="Lento" \
		--add-data "macos-style.qss:." \
		--add-data "fonts/*.ttf:fonts/" \
		--icon assets/Lento.icns \
		--windowed --onefile app.py
		@#--add-data ".env:." \
		@# --osx-bundle-identifier io.github.lentoapp.lento

build-windows: test lint
	@${PYTHON} -m PyInstaller --name="Lento" \
		--add-data "windows-style.qss;." \
		--add-data "fonts/*.ttf;fonts/" \
		--add-data "assets/lento-icon.png;." \
		--icon assets/lento-icon.ico \
		--windowed --onefile app.py

remove-build-files:
	@rm -rf Lento.spec build dist

iconset:
	@echo "Generating macOS iconset..."
	@mv assets/lento-icon.png .
	@mkdir Lento.iconset
	@sips -z 16 16     lento-icon.png --out Lento.iconset/icon_16x16.png
	@sips -z 32 32     lento-icon.png --out Lento.iconset/icon_16x16@2x.png
	@sips -z 32 32     lento-icon.png --out Lento.iconset/icon_32x32.png
	@sips -z 64 64     lento-icon.png --out Lento.iconset/icon_32x32@2x.png
	@sips -z 128 128   lento-icon.png --out Lento.iconset/icon_128x128.png
	@sips -z 256 256   lento-icon.png --out Lento.iconset/icon_128x128@2x.png
	@sips -z 256 256   lento-icon.png --out Lento.iconset/icon_256x256.png
	@sips -z 512 512   lento-icon.png --out Lento.iconset/icon_256x256@2x.png
	@sips -z 512 512   lento-icon.png --out Lento.iconset/icon_512x512.png
	@cp lento-icon.png Lento.iconset/icon_512x512@2x.png
	@iconutil -c icns Lento.iconset
	@rm -R Lento.iconset
	@mv lento-icon.png Lento.icns assets/
	@echo "Iconset generation complete!"
