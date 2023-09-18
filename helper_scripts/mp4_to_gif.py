from tqdm.auto import tqdm
import os
import glob

from moviepy.editor import VideoFileClip


def mp4_to_gif(mp4_file, gif_file, fps=5):
    clip = VideoFileClip(mp4_file, audio=False)
    clip = clip.resize(0.4)
    clip = clip.speedx(1.5)
    clip.write_gif(gif_file, fps=fps, colors=128)
    return True


def get_filesize_in_mb(fn):
    return os.stat(fn).st_size / 1024 / 1024


def main(mp4_regex, outdir):
    os.makedirs(outdir, exist_ok=True)
    pbar = tqdm(glob.glob(mp4_regex))

    for mp4_file in pbar:
        pbar.set_description(os.path.basename(mp4_file))
        gif_file = os.path.join(outdir, os.path.basename(mp4_file).replace(".mp4", ".gif"))
        if not os.path.exists(gif_file):
            attempt = 0
            while attempt < 5:
                try:
                    mp4_to_gif(mp4_file, gif_file)
                    break
                except:
                    attempt += 1
            orig_size = get_filesize_in_mb(mp4_file)
            new_size = get_filesize_in_mb(gif_file)
            print(f"({orig_size:.2f} MB -> {new_size:.2f} MB)")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("mp4_regex")
    parser.add_argument("--outdir", default="out_gif")
    args = parser.parse_args()
    main(args.mp4_regex, args.outdir)
