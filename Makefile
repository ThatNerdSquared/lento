PYTHON := python3

.PHONY = lint test run build_macos build_windows remove-build-files
DAEMON_DIRS = $(shell find ./daemon/ -type d)
DAEMON_FILES = $(shell find ./daemon/ -type f -name '*')
APP_DIRS = $(shell find ./lento/ -type d)
APP_FILES = $(shell find ./lento/ -type f -name '*')

lint:
	@echo Linting...
	@${PYTHON} -m flake8 ./app.py lento daemon tests --exclude="tests/helpers.py"
	@echo Done!

test:
	@echo Testing...
	@${PYTHON} -m pytest tests
	@echo Done!

vtest:
	@echo Testing...
	@${PYTHON} -m pytest -vv tests
	@echo Done!

run: test lint
	@${PYTHON} app.py

run-daemon: test lint
	@${PYTHON} -m daemon

build-daemon: $(DAEMON_DIRS) $(DAEMON_FILES)
	make test
	make lint
	@${PYTHON} -m nuitka daemon/__main__.py \
		--onefile --standalone
	@mv __main__.bin lentodaemon

build-daemon-windows: test lint daemon/
	@${PYTHON} -m nuitka daemon/__main__.py \
		--onefile --standalone
	@mv __main__.exe lentodaemon.lento.exe


build-macos: build-daemon $(APP_DIRS) $(APP_FILES)
	make test
	make lint
	@pyinstaller --name="Lento" \
		--add-data "lento.qss:." \
		--add-data "fonts/*.ttf:fonts/" \
		--add-data "lentodaemon:." \
		--add-data ".venv/lib/python3.10/site-packages/fleep/data.json:fleep/." \
		--add-data "assets/toggle-unfolded.svg:assets/." \
		--add-data "assets/toggle-folded.svg:assets/." \
		--add-data "assets/arrow-left.svg:assets/." \
		--add-data "assets/arrow-right.svg:assets/." \
		--add-data "assets/add-twemoji.svg:assets/." \
		--add-data "assets/delete-twemoji.svg:assets/." \
		--icon assets/Lento.icns \
		--windowed app.py
		@#--add-data ".env:." \
		@# --osx-bundle-identifier io.github.lentoapp.lento

build-windows: test lint build-daemon-windows
	@${PYTHON} -m PyInstaller --name="Lento" \
		--add-data "lento.qss;." \
		--add-data "fonts/*.ttf;fonts/" \
		--add-data "lentodaemon;." \
		--add-data ".venv/Lib/site-packages/fleep/data.json;fleep/." \
		--add-data "assets/toggle-unfolded.svg;assets/." \
		--add-data "assets/toggle-folded.svg;assets/." \
		--add-data "assets/arrow-left.svg;assets/." \
		--add-data "assets/arrow-right.svg;assets/." \
		--add-data "assets/add-twemoji.svg;assets/." \
		--add-data "assets/delete-twemoji.svg;assets/." \
		--add-data "assets/lento-icon.png;." \
		--icon assets/lento-icon.ico \
		--windowed --onefile app.py

remove-build-files:
	@rm -rf Lento.spec build dist lentodaemon.spec __main__.bin __main__.build __main__.dist __main__.onefile-build/ lentodaemon

remove-build-files-win:
	@rm -Force Lento.spec, build, dist, lentodaemon.spec, __main__.bin, __main__.build, __main__.dist, __main__.onefile-build, app.build, app.dist, lentodaemon.exe


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
