
default: synth onsets

synth: synth.arrp
	arrp synth.arrp -x synth

synth-output: synth
	./synth -f raw | ffmpeg -y -t 2.0 -ac 1 -ar 44.1k -f f64le -i pipe:0 file:synth.wav

synth-solution: synth-solution.arrp
	arrp synth-solution.arrp -x synth-solution

.PHONY: synth-solution-output
synth-solution-output: synth-solution
	./synth-solution -f raw | ffmpeg -y -t 2.0 -ac 1 -ar 44.1k -f f64le -i pipe:0 file:synth-solution.wav


onsets: onsets.arrp
	arrp onsets.arrp -x onsets

onsets-output: onsets
	ffmpeg -i claps.wav -ar 44.1k -f f64le pipe:1 | ./onsets x=pipe:raw > onsets.txt

onsets-solution: onsets-solution.arrp
	arrp onsets-solution.arrp -x onsets-solution

.PHONY: onsets-solution-output
onsets-solution-output: onsets-solution
	ffmpeg -i claps.wav -ar 44.1k -f f64le pipe:1 | ./onsets-solution x=pipe:raw > onsets-solution.txt

onsets.cpp: onsets-solution.arrp
	arrp onsets-solution.arrp --cpp onsets.cpp

onsets-rt: onsets.cpp onsets-rt-host.cpp
	g++ onsets-rt-host.cpp -o onsets-rt -lrtaudio -lpthread
