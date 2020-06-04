import click

import glob
import os
import random
from shutil import copy
from multiprocessing import Pool
from tqdm import tqdm


def save_subset(subset):
    copy(subset[0], subset[1])

@click.command()
@click.option('--ffhq_folder', default='../ffhq')
@click.option('--save_folder', default='../datasets')
@click.option('--n_images', default=5000)
@click.option('--val_ratio', default=0.3)
def main(ffhq_folder, save_folder, n_images, val_ratio):
    save_train = os.path.join(save_folder, 'ffhq')
    save_val = os.path.join(save_folder, 'ffhq_val')
    os.makedirs(save_train, exist_ok=True)
    os.makedirs(save_val, exist_ok=True)
    images = glob.glob(f'{ffhq_folder}/*/*.*g')
    images = random.sample(images, n_images)
    n_val = int(n_images * val_ratio)
    train_images = images[n_val:]
    val_images = images[:n_val]
    for subset, save_path in zip([train_images, val_images], [save_train, save_val]):
        save_path = [save_path] * len(subset)
        subset = list(zip(subset, save_path))
        with Pool(8) as pool:
            list(tqdm(pool.imap(save_subset, subset), total=len(subset)))


if __name__ == '__main__':
    main()
