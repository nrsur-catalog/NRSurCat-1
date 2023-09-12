from tqdm.auto import tqdm
import imageio
import os
import glob

try:
    from pygifsicle import optimize
except ImportError:
    print("pygifsicle not installed, skipping gif optimization")
    optimize = lambda x: None


def mp4_to_gif(mp4_file, gif_file):
    reader = imageio.get_reader(mp4_file)
    fps = reader.get_meta_data().get("fps", 15)
    writer = imageio.get_writer(gif_file, fps=fps)
    for i, frame in enumerate(reader):
        writer.append_data(frame)
    writer.close()
    optimize(gif_file)


def get_filesize_in_mb(fn):
    return os.stat(fn).st_size / 1024 / 1024


def main(mp4_regex, outdir):
    os.makedirs(outdir, exist_ok=True)
    pbar = tqdm(glob.glob(mp4_regex))

    for mp4_file in pbar:
        gif_file = os.path.join(outdir, os.path.basename(mp4_file).replace(".mp4", ".gif"))
        mp4_to_gif(mp4_file, gif_file)
        orig_size = get_filesize_in_mb(mp4_file)
        new_size = get_filesize_in_mb(gif_file)
        pbar.set_description(f"({orig_size:.2f} MB -> {new_size:.2f} MB)")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("mp4_regex")
    parser.add_argument("--outdir", default="out_gif")
    args = parser.parse_args()
    main(args.mp4_regex, args.outdir)
