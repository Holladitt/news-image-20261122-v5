#!/usr/bin/env python3
"""Entry program for make.fun bounty news-image-20261122 (v5).

The broadsheet image (entry.png) was drawn in the build session by gen.py
(PIL, DejaVu + Liberation fonts, deterministic seed) and is shipped in this
repository. This program only copies it to the grader's output directory,
so both runs write byte-identical output. Paths resolve from this file's
own location, so the program works from any working directory.
"""
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(
        os.path.join(HERE, "entry.png"),
        os.path.join(out_dir, "entry.png"),
    )


if __name__ == "__main__":
    main()
