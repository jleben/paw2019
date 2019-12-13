# Tutorial: Analyzing Sound with Arrp

## Getting Started

The goal of this tutorial is to create a sound analyzer detecting onsets of sounds. As an example, we will use a short sound clip ([claps.wav](claps.wav)). This is the beginning of the disco song Car Wash by Rose Royce. The clip contains several classic disco claps. Our program will detect these claps and output a stream of boolean values: true at the beginning of each clap, and false at all other instants.

The file [onsets.arrp](onsets.arrp) contains the initial code. The code represents a first attempt at the goal, simply outputting true whenever the amplitude of the input signal is larger than a threshold.

You can run the program using the following steps:

- Compile the code into a program named `onsets`:

        arrp onsets.arrp -x onsets

- Run the program using the file `claps.wav` as input and writing the output into `onsets.txt`. The input file is read using `ffmpeg`:

        ffmpeg -i claps.wav -ar 44.1k -f f64le pipe:1 | ./onsets x=pipe:raw > onsets.txt

- The above two steps are defined in the provided Makefile, so if you have `make` installed, you can simply run `make onsets` instead of the first step and `make onsets-output` instead of both steps.

Alternatively, if you are using the online [Playground](http://arrp-lang.info/play), you can use as input a shorter clip containing only the last 5 of the claps, downsampled to 8 kHz ([claps_8khz.wav](claps_8khz.wav)) and converted to text ([claps_8khz.txt](claps_8khz.txt)):

- Copy the contents of [claps_8khz.txt](claps_8khz.txt) into the Input box in the Playground.
- Copy the code from [onsets.arrp](onsets.arrp) into the Code box and modify the definition of `sr` to `sr = 8000;`.

Note that the Playground outputs only the first 1000 output elements.

## Strategy

There are two issues with the initial code:

- The output stream has one element for each input element (audio sample). This output rate is much higher then normally required for audio analysis.

- The output stream contains many true values for each clap because each clap consists of many oscillations and the code outputs true whenever the signal oscillates above a threshold.

Both the above problems are usually solved using the *overlapped window* approach: sound is segmented into overlapping blocks of samples called *windows* and a single value is output for each window. In our case, an output value will represent the loudness of a window. We will detect the onset of a clap as the moment when this loudness suddenly increases.

## Reducing Output Rate

First, we want to reduce the output rate so that we output one value for each window. The spacing between windows is usually called a *hop*, so we want to produce one output value for every *hop* input samples.

This code defines a hop size `H = 10` and then uses `H` to define a stream `energy` containing each 10th input sample:

    H = 10;
    energy[n] = x[H*n];

**Challenge:**

- Modify the hop size `H` so that `energy` contains about 40 elements per second, considering the sampling rate named `sr`. You may need to use integer division with the syntax `a//b`. With this hop size, the stream `energy` should contain only about 180 elements for the full-length clip at 44.1 kHz.

Note: You can output `energy` instead of `y` by changing the line `output y : [~]bool;` to `output energy : [~]real64;`.


## Computing Energy of Input Windows

Next, instead of just selecting elements out of `x`, let's estimate the loudness of windows beginning at those elements.

If we consider an array 'a' with size W, the following equation defines the energy of the array which is a rough estimate of loudness:

$$
  \sum_{i=0}^{W-1} a[i]^2
$$

The following code is an Arrp implementation of the above equation. It applies the provided function `sum` to a temporary array (*lambda* array) which contains the first `W` samples from `x`, squared:

    sum([i:W] -> x[i]^2)

**Challenge:**

- Set the window size `W` to be twice your hop size `H`.
- Change the stream `energy` so that each element at `n` equals the energy of `W` elements of `x` starting at `H*n`.


## Detecting Sudden Increase in Energy

Finally, we can detect the onset of a clap by detecting a sudden increase in energy.

For example, the following computes the difference between consecutive elements of `energy`:

    energy_dif[n] = energy[n+1] - energy[n];

**Challenge:**

- Define `y` so that it is true when the energy increases significantly and false otherwise.
- You may notice that `y` still contains multiple consecutive true values for each clap. Try modifying the code to convert the true values other than the first within a group to false.
