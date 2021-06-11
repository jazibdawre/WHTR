import os
import sys
import glob
import argparse
import subprocess

from path import Path

from utils.split_images import split_lines


def main(image_name: str):
    base_file = os.path.join(sys.path[0], "images", image_name)
    split_lines(base_file)

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
