# Tutorial: Analyzing Sound with Arrp

## Getting Started

The goal of this tutorial is to create a sound analyzer detecting onsets of sounds. As an example, we will use a short sound clip ([claps.wav](claps.wav)). This is the beginning of the disco song Car Wash by Rose Royce. The clip contains several classic disco claps. Our program will detect these claps and output a stream of numbers: a value of 1 at the beginning of each clap, and 0 at all other instants.

The file `onsets.arrp` contains the initial code. The code represents a first attempt at the goal, simply outputting 1 whenever the amplitude of the input signal is larger than a threshold.

You can test the program using the following steps:

- Compile the code into a program named `onsets`:

        arrp onsets.arrp -x onsets

- Run the program and with the file `claps.wav` as input and writing the output into `onsets.txt`. The input file is read using `ffmpeg`:

        ffmpeg -i claps.wav -ar 44.1k -f f64le pipe:1 | ./onsets x=pipe:raw > onsets.txt

- The above two steps are defined in the provided Makefile, so if you have `make` installed, you can simply run `make onsets` instead of the first step and `make onsets-output` instead of both steps.

## Strategy

There are two issues with the initial code:

- The output stream has one element for each input element (audio sample). This output rate is much higher then normally required for audio analysis.

- The output stream contains many ones for each clap because each clap consists of many oscillations and the code outputs a 1 whenever the signal oscillates above a threshold.

Both the above problems are usually solved using the *overlapped window* approach: sound is segmented into overlapping blocks of samples called *windows* and a single value is output for each window. In our case, an output value will represent the loudness of a window. We will detect the onset of a clap as the moment when this loudness suddenly increases.

## Reducing Output Rate

First, we want to reduce the output rate so that we output one value for each window. The spacing between windows is usually called a *hop*, so we want to produce one output value for every *hop* input samples.

This code defines a hop size `H = 10` and then uses `H` to define a stream `energy` containing each 10th input sample:

    H = 10;
    energy[n] = x[H*n];

**Challenge:**

- Modify the hop size `H` so that `energy` contains about 40 elements per second, considering the sampling rate named `sr`. The stream `energy` should then contain about 180 elements.

Note: You can output `energy` instead of `y` by changing the line `output y ...` to `output energy ...`.


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

    y[n] = energy[n+1] - energy[n];

**Challenge:**

- Define `y` so that it contains a value of 1 when the energy increases significantly and 0 otherwise.
- You may notice that `y` still contains multiple consecutive 1s for each clap. Try modifying the code to only output the first out of a group of 1s for each clap, and 0 otherwise.
