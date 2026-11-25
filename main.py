# news-image-20261125 — acct2 entrypoint.
# Writes the day's newspaper image to /output/entry.png. Deterministic, no network.
import os

from build import build


def main():
    out = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out, exist_ok=True)
    build(os.path.join(out, "entry.png"))


if __name__ == "__main__":
    main()
