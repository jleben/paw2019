
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
	build/tutorial/tutorial.pdf \
	build/tutorial/synth.pdf \
	build/tutorial/onsets.pdf \
	tutorial/Makefile \
	tutorial/synth.arrp \
	tutorial/synth-solution.arrp \
	tutorial/onsets.arrp \
	tutorial/onsets-solution.arrp \
	build/tutorial/claps.wav \
	build/tutorial/synth-solution.wav \
	| build/tutorial

	cp -u tutorial/Makefile build/tutorial/
	cp -u tutorial/*.arrp build/tutorial/

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


.PHONY: tutorial-package
tutorial-package: tutorial
	cd build && rm -f tutorial.zip && zip -r tutorial.zip tutorial
