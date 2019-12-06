# Synthesizing Sound

## Getting Started

The goal of this tutorial is to implement a synthesizer generating a repeating percussion-like sound ("pew pew pew").

The file `synth.arrp` contains initial code. It generates a pure sinusoidal tone at 500 Hz, assuming a sampling rate of 44.1 kHz.

You can test it using the following steps:

- Compile the code into a program named `synth`:

        arrp synth.arrp -x synth

- Run the program and pass its output through `ffmpeg` to generate a 2 seconds long audio file `output.wav`:

        ./synth -f raw | ffmpeg -y -t 2.0 -ac 1 -ar 44.1k -f f64le -i pipe:0 file:output.wav

- The above two steps are defined in the provided Makefile, so if you have `make` installed, you can simply run `make synth` instead of the first step and `make synth-output` instead of both steps.

- You can also print the output of the `synth` program in the console. For example, the following prints the first 100 samples:

        ./synth | head -n 100


## Creating a trigger

First, we need to generate a trigger signal - a signal indicating when in time an instance of the sound should be started. This signal will have boolean values: true when the sound should start, and false otherwise.

Here is an example where the first signal sample is true, and all the rest are false:

    trigger[n] = if n == 0 then true else false;

You can test this signal in the online Playground by combining it with the following line that defines an output:

    output trigger : [~]bool;

Challenge: Modify `trigger` so that it is true whenever `n` is a multiple of the desired number of samples. You can use the function `sec` defined in `synth.arrp` to convert a duration in seconds to samples.

## Creating a control signal

To control the parameters of the desired sound, we will create a signal that gradually descends from 1 to 0 within a given duration, restarting from 1 whenever the `trigger` signal is `true`.

Here is a simpler function that generates a signal starting at 1 and descending infinitely by 0.01 at each sample. The function takes a trigger as argument and restarts at 1 when trigger is `true`:

    ramp(trigger) = y where {
      y[0] = 1.0;
      y[n] = if trigger[n] then 1.0 else y[n-1] - 0.01;
    };

Challenge: Modify `ramp` as follows:

- Add an argument `duration`.
- Adjust the rate at which the signal descends so that it reaches 0 after `duration` samples.
- Make the signal descend no further than 0 and stop there until the next trigger.
- Make sure the signal starts at 0 unless the trigger starts with `true`.


## Controlling sound

We will use the function `ramp(trigger, duration)` implemented in the previous step to control various parameters of the sound.

In the following example, `sound` is modified so that its amplitude descends from 1 to 0 in 0.2 seconds on each trigger:

    sound = osc(hz(500)) * 0.2 * ramp(trigger, sec(0.2));

Challenges:

- Modify `sound` so that its frequency descends from 600 Hz to 200 Hz together with the amplitude.
- What other parameters of the sound can you control? Suggestion: try generating a sum of sinusoids at different frequencies and control their relative amplitude.
- Can you make a more complex control signal instead of the simple descending line?
