from tqdm.auto import trange
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

    files = glob.glob(mp4_regex)
    src_dir = os.path.dirname(files[0])
    gifs = [os.path.join(outdir, os.path.basename(mp4_file).replace(".mp4", ".gif")) for mp4_file in files]
    gifs = [f for f in gifs if not os.path.exists(f)]
    mp4s = [os.path.join(src_dir, os.path.basename(f).replace(".gif", ".mp4")) for f in gifs]

    pbar = trange(len(mp4s))
    for i in pbar:
        mp4_file = mp4s[i]
        gif_file = gifs[i]
        pbar.set_description(os.path.basename(mp4_file))
        if not os.path.exists(gif_file):
            attempt = 0
            while attempt < 5:
                try:
                    mp4_to_gif(mp4_file, gif_file)
                    orig_size = get_filesize_in_mb(mp4_file)
                    new_size = get_filesize_in_mb(gif_file)
                    print(f"({orig_size:.2f} MB -> {new_size:.2f} MB)")
                    break
                except Exception as e:
                    print("Error:", e)
                    if os.path.exists(gif_file):
                        os.remove(gif_file)
                    attempt += 1

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("mp4_regex")
    parser.add_argument("--outdir", default="out_gif")
    args = parser.parse_args()
    main(args.mp4_regex, args.outdir)
