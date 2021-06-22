import os
import sys
import glob
import argparse
import subprocess

from path import Path
from autocorrect import Speller

from utils.split_images import split_lines


def main(image_name: str):
    # Config
    base_file = os.path.join(sys.path[0], "images", image_name)
    spell = Speller(only_replacements=True)

    # Split Lines
    split_lines(base_file)

    # OCR
    for line_img in glob.glob(os.path.join(os.path.splitext(base_file)[0], "*.png")):
        p = subprocess.run(
            [
                "python",
                "main.py",
                f"--img_file={line_img}",
            ],
            cwd="src",
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
        )

        if p.returncode != 0:
            print(p.stderr)

    # Autocorrect
    with open(os.path.splitext(base_file)[0] + ".txt", "w") as f:
        for line_text_file in glob.glob(
            os.path.join(os.path.splitext(base_file)[0], "*.txt")
        ):
            with open(line_text_file, "r") as line_text:
                f.write(spell(line_text.read()) + "\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--img_file",
        help="Image to be transcribed",
        type=Path,
        default="line.png",
    )
    args = parser.parse_args()

    main(args.img_file)
