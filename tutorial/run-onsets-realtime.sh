#! /bin/bash

# This runs the onsets analysis program (./onsets-solution by default or the first argument) and prints its output in the console.
# NOTE: Adjust Arrp code to slow down analysis rate to ~10Hz so output does not fly by too fast.
# NOTE: This requires the programs 'arecord' and 'ffmpeg'.

onsets_program=$1
if [[ -z "$onsets_program" ]]; then
  onsets_program=./onsets-solution
fi

if [[ ! -x "$onsets_program" ]]; then
  echo "'$onsets_program' does not exist or is not an executable program.";
  exit 1;
fi

arecord -D default -r 44100 -f S16_LE --buffer-size=512 | ffmpeg -i pipe:0 -f f64le pipe:1 -v 0 | $onsets_program x=pipe:raw -b 512
