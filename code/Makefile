

synth: synth.arrp
	arrp synth.arrp -x synth

run-synth: synth
	./synth -f raw | ffmpeg -y -t 2.0 -ac 1 -ar 44.1k -f f64le -i pipe:0 file:output.wav
