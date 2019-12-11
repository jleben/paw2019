
.PHONY: all
all: figures slides

.PHONY: slides
slides: build/slides.pdf

build/slides.pdf: presentation/slides.tex figures
	cd build && xelatex -halt-on-error -shell-escape ../presentation/slides.tex

.PHONY: figures
figures: \
	build/parallel-scaling-max-filter-slide.pdf \
	build/downsample-sched-simple1.svg \
	build/stencil-basic.pdf \
	build/stencil-tiled1.pdf \
	build/periodic-tiling.svg \
	build/buf-mode-storage.tex

build/parallel-scaling-max-filter-slide.pdf: figures/parallel-scaling.py
	cd build && python3 ../figures/parallel-scaling.py --for-slides ../

build/downsample-sched-simple1.svg: figures/downsample.py
	cd build && python3 ../figures/downsample.py

build/stencil-basic.pdf: figures/stencil.py
	cd build && python3 ../figures/stencil.py

build/stencil-tiled1.pdf: figures/stencil-tiled.py
	cd build && python3 ../figures/stencil-tiled.py

build/periodic-tiling.svg: figures/periodic-tiling.py
	cd build && python3 ../figures/periodic-tiling.py

build/buf-mode-storage.tex: figures/buf-mode-storage.py
	cd build && python3 ../figures/buf-mode-storage.py


.PHONY: tutorial
tutorial: \
	build/tutorial/tutorial.html \
	build/tutorial/synth.html \
	build/tutorial/onsets.html \
	build/tutorial/realtime.html \
	tutorial/Makefile \
	tutorial/synth.arrp \
	tutorial/synth-solution.arrp \
	tutorial/onsets.arrp \
	tutorial/onsets-solution.arrp \
	tutorial/run-onsets-realtime.sh \
	tutorial/onsets-rt-host.cpp \
	build/tutorial/claps.wav \
	build/tutorial/synth-solution.wav \
	| build/tutorial

	cp -u tutorial/Makefile build/tutorial/
	cp -u tutorial/*.arrp build/tutorial/
	cp -u tutorial/run-onsets-realtime.sh build/tutorial/
	cp -u tutorial/onsets-rt-host.cpp build/tutorial/

build/tutorial:
	mkdir -p build/tutorial

build/tutorial/%.html: tutorial/%.md | build/tutorial
	pandoc $< -s --mathjax -o $@

build/tutorial/%.pdf: tutorial/%.md | build/tutorial
	pandoc $< -o $@

build/tutorial/claps.wav:
	cd build/tutorial && wget https://jakob-leben.s3-us-west-2.amazonaws.com/paw2019/claps.wav

build/tutorial/synth-solution.wav:
	cd build/tutorial && wget https://jakob-leben.s3-us-west-2.amazonaws.com/paw2019/synth-solution.wav

build/tutorial/mac/ffmpeg:
	mkdir -p build/tutorial/mac
	cd build && wget https://evermeet.cx/ffmpeg/ffmpeg-4.2.1.zip
	unzip build/ffmpeg-4.2.1.zip -d build/tutorial/mac/

build/tutorial/mac/arrp/bin/arrp:
	cd build && wget https://github.com/jleben/arrp/releases/download/version-1.0.0-beta2/arrp_1.0.0_macos.zip
	cd build && unzip arrp_1.0.0_macos.zip
	mkdir -p build/tutorial/mac/arrp
	cp -r build/arrp_1.0.0_macos/* build/tutorial/mac/arrp/

build/tutorial/linux/arrp_1.0.0_amd64.deb:
	mkdir -p build/tutorial/linux
	cd build/tutorial/linux && wget https://github.com/jleben/arrp/releases/download/version-1.0.0-beta2/arrp_1.0.0_amd64.deb

.PHONY: tutorial-package
tutorial-package: tutorial \
	tutorial/mac/setup.sh \
	build/tutorial/linux/arrp_1.0.0_amd64.deb \
	build/tutorial/mac/ffmpeg \
	build/tutorial/mac/arrp/bin/arrp

	cp -u tutorial/mac/setup.sh build/tutorial/mac/
	cd build && rm -f tutorial.zip && zip -r tutorial.zip tutorial
