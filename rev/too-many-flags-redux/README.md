# Writeup: SemiPRand (PRNG Redux)

## Step 1 — Identify RNG Algorithm

Participants must identify the PRNG in use by comparing the given outputs to the output of given algorithms. A hint is provided in the name of the Python class `SemiPRand`.
This name has been selected as to reduce the triviality of identification via an LLM prompt. Participants must research RNG algorithms and identify the use of a "Semi Prime (SemiP)" algorithm, "Blum-Blum-Shub".

## Step 2 - Extract Modulus

After identifying the algorithm in use, participants can extract the modulus in use by getting the greatest common divisor of the differences between each consecutive value, defined as `gcd(x_i^2 - x_i+1)`.

## Step 3 - Reverse Flag Scrambling

The solution to unscrambling the flags is almost identical to the previous "Too Many Flags" challenge, though an extra step has been added to use an extra 2 random ints for each scramble step.

An example solution script has been included in `solution.py`.