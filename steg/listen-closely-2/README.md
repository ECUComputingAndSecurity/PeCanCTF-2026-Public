# Listen Closely / Look Closely

## Flags

- Part A (`listen-closely-1`): `pecan{N0T_G0NN4}`
- Part B (`listen-closely-2`): `pecan{L00K_CL0S3LY}`

## Writeup

The audio is "Never Gonna Give You Up" with two independent Morse code sequences overlaid starting at 5s — one at ~800Hz and another at ~18000Hz.

### Part A — Listen Closely (800Hz)

Transcribe the audible Morse beeps at ~800Hz:

```
.--. . -.-. .- -. -.--. -. ----- - ..--.- --. ----- -. -. ....- -.--.-
```

Decode to get: `PECAN{N0T_G0NN4}`

### Part B — Look Closely (18000Hz)

Open the same MP3 in an online spectrogram viewer like [Academo](https://academo.org/demos/spectrum-analyzer/). The high-frequency Morse at ~18000Hz is clearly visible:

```
.--. . -.-. .- -. -.--. .-.. ----- ----- -.- ..--.- -.-. .-.. ----- ... ...-- .-.. -.-- -.--.-
```

Decode to get: `PECAN{L00K_CL0S3LY}`

### Morse Decode Tables

| A: 800Hz |      | B: 18000Hz |      |
|----------|------|-----------|------|
| `.--.`   | P    | `.--.`    | P    |
| `.`      | E    | `.`       | E    |
| `-.-.`   | C    | `-.-.`    | C    |
| `.-`     | A    | `.-`      | A    |
| `-.`     | N    | `-.`      | N    |
| `-.--.`  | {    | `-.--.`   | {    |
| `-.`     | N    | `.-..`    | L    |
| `-----`  | 0    | `-----`   | 0    |
| `-`      | T    | `-----`   | 0    |
| `..--.-` | _    | `-.-`     | K    |
| `--.`    | G    | `..--.-`  | _    |
| `-----`  | 0    | `-.-.`    | C    |
| `-.`     | N    | `.-..`    | L    |
| `-.`     | N    | `-----`   | 0    |
| `....-`  | 4    | `...`     | S    |
| `-.--.-` | }    | `...--`   | 3    |
|          |      | `.-..`    | L    |
|          |      | `-.--`    | Y    |
|          |      | `-.--.-`  | }    |

## Resources

- [International Morse Code](https://upload.wikimedia.org/wikipedia/commons/b/b5/International_Morse_Code.svg)
- [Spectrum Analyzer](https://academo.org/demos/spectrum-analyzer/)
