#!/usr/bin/env python3
import wave
import struct
import math
import subprocess
import os
import sys
import tempfile
import urllib.request

FLAG_A = "PECAN{N0T_G0NN4}"
FLAG_B = "PECAN{L00K_CL0S3LY}"
OUTPUT = "listen_closely.mp3"
RICK_VIDEO = "Rick Roll.mp4"
RICK_URL = "https://archive.org/download/rick-roll/Rick%20Roll.mp4"

MORSE = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.',
    'G': '--.', 'H': '....', 'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..',
    'M': '--', 'N': '-.', 'O': '---', 'P': '.--.', 'Q': '--.-', 'R': '.-.',
    'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-',
    'Y': '-.--', 'Z': '--..',
    '0': '-----', '1': '.----', '2': '..---', '3': '...--', '4': '....-',
    '5': '.....', '6': '-....', '7': '--...', '8': '---..', '9': '----.',
    '{': '-.--.', '}': '-.--.-', '_': '..--.-',
}

SAMPLE_RATE = 44100
DOT = 0.12
DASH = 0.30
SYM_GAP = 0.08
CHAR_GAP = 0.30
FREQ_A = 800
FREQ_B = 18000
VOL_A = 0.35
VOL_B = 0.50
START_DELAY = 5.0
FADE = 0.005


def text_to_morse(text):
    result = []
    for c in text.upper():
        if c == ' ':
            result.append(' ')
        else:
            result.append(MORSE.get(c, ''))
    return result


def generate_samples(freq, duration, volume):
    n = int(SAMPLE_RATE * duration)
    fade_n = int(SAMPLE_RATE * FADE)
    samples = []
    for i in range(n):
        t = i / SAMPLE_RATE
        val = math.sin(2 * math.pi * freq * t)
        if i < fade_n:
            val *= i / fade_n
        elif i > n - fade_n:
            val *= (n - i) / fade_n
        samples.append(int(32767 * volume * val))
    return samples


def generate_silence(duration):
    n = int(SAMPLE_RATE * duration)
    return [0] * n


def generate_morse_sequence(text, freq, volume):
    result = generate_silence(START_DELAY)
    morse_chars = text_to_morse(text)
    for ci, morse in enumerate(morse_chars):
        if morse == ' ':
            result.extend(generate_silence(SYM_GAP))
            continue
        for si, symbol in enumerate(morse):
            if si > 0:
                result.extend(generate_silence(SYM_GAP))
            dur = DOT if symbol == '.' else DASH
            samples = generate_samples(freq, dur, volume)
            result.extend(samples)
        if ci < len(morse_chars) - 1:
            result.extend(generate_silence(CHAR_GAP))
    result.extend(generate_silence(1.0))
    return result


def find_rickroll():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    local_file = os.path.join(script_dir, RICK_VIDEO)
    if os.path.exists(local_file):
        return local_file
    return None


def download_rickroll():
    url = RICK_URL
    script_dir = os.path.dirname(os.path.abspath(__file__))
    dest = os.path.join(script_dir, RICK_VIDEO)
    print(f"Downloading from {url}...")
    urllib.request.urlretrieve(url, dest)
    print("Done.")
    return dest


def pad_to(audio, target_len):
    if len(audio) < target_len:
        audio.extend([0] * (target_len - len(audio)))
    return audio


def main():
    rick_path = find_rickroll()
    if rick_path is None:
        print(f"Rick Roll video not found at:")
        print(f"  {os.path.join(os.path.dirname(os.path.abspath(__file__)), RICK_VIDEO)}")
        ans = input("Download from archive.org? (y/n) ").strip().lower()
        if ans in ('y', 'yes'):
            rick_path = download_rickroll()
        else:
            sys.exit(1)

    script_dir = os.path.dirname(os.path.abspath(__file__))
    mp3_path = os.path.join(script_dir, OUTPUT)

    seq_a = generate_morse_sequence(FLAG_A, FREQ_A, VOL_A)
    seq_b = generate_morse_sequence(FLAG_B, FREQ_B, VOL_B)

    max_len = max(len(seq_a), len(seq_b))
    pad_to(seq_a, max_len)
    pad_to(seq_b, max_len)

    audio = [min(32767, max(-32767, a + b)) for a, b in zip(seq_a, seq_b)]

    with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as f:
        beep_wav = f.name

    with wave.open(beep_wav, 'w') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(SAMPLE_RATE)
        wf.writeframes(struct.pack(f'<{len(audio)}h', *audio))

    beep_duration = len(audio) / SAMPLE_RATE

    subprocess.run([
        'ffmpeg', '-y',
        '-i', rick_path,
        '-i', beep_wav,
        '-filter_complex',
        '[1:a]adelay=0|0[beeps];[0:a][beeps]amix=inputs=2:duration=first:weights=1 0.7[aout]',
        '-map', '[aout]',
        '-codec:a', 'libmp3lame', '-q:a', '2',
            mp3_path
    ], check=True)

    os.remove(beep_wav)

    morse_a = text_to_morse(FLAG_A)
    morse_b = text_to_morse(FLAG_B)

    print(f"Part A ({FREQ_A}Hz): {FLAG_A}")
    print(f"  Morse: {' '.join(morse_a)}")
    print(f"Part B ({FREQ_B}Hz): {FLAG_B}")
    print(f"  Morse: {' '.join(morse_b)}")
    print(f"Output: {OUTPUT}")
    print(f"Duration: {beep_duration:.1f}s (beeps start at {START_DELAY}s)")


if __name__ == '__main__':
    main()
