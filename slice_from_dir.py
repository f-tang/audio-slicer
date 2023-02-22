import os
import shutil
from pathlib import Path
from argparse import ArgumentParser

import librosa
import soundfile
from slicer2 import Slicer

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--path', type=str, help="Root directory of ouput and clean_vocals folder.")
    args = parser.parse_args()
    path = args.path
    if path is None or not os.path.isdir(path):
        print("Please specify --path as the root directory")
        exit(0)

    output_path = os.path.join(path, "clips")
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    for file in os.listdir(path):
        src = os.path.join(path, file)
        if os.path.isfile(src):
            stem, ext = os.path.splitext(file)
            audio, sr = librosa.load(src, sr=None, mono=False)  # Load an audio file with librosa.
            slicer = Slicer(
                sr=sr,
                threshold=-30,
                min_length=5000,
                min_interval=1000,
                hop_size=10,
                max_sil_kept=1000
            )
            chunks = slicer.slice(audio)
            for i, chunk in enumerate(chunks):
                if len(chunk.shape) > 1:
                    chunk = chunk.T  # Swap axes if the audio is stereo.
                dst = os.path.join(output_path, stem + '_' + str(i) + ext)
                print(dst)
                soundfile.write(dst, chunk, sr)  # Save sliced audio files with soundfile.
