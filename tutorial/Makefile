
synth: synth.arrp
	arrp synth.arrp -x synth

synth-output: synth
	./synth -f raw | ffmpeg -y -t 2.0 -ac 1 -ar 44.1k -f f64le -i pipe:0 file:output.wav

onsets: onsets.arrp
	arrp onsets.arrp -x onsets

onsets-output: onsets
	ffmpeg -i claps.wav -ar 44.1k -f f64le pipe:1 | ./onsets x=pipe:raw > output.txt

onsets-solution: onsets-solution.arrp
	arrp onsets-solution.arrp -x onsets-solution

onsets-solution-output: onsets-solution
	ffmpeg -i claps.wav -ar 44.1k -f f64le pipe:1 | ./onsets-solution x=pipe:raw > output.txt


.PHONY: tutorial
tutorial: synth.html onsets.html

synth.html: synth.md
	pandoc synth.md -s --mathjax -o synth.html

onsets.html: onsets.md
	pandoc onsets.md -s --mathjax -o onsets.html
