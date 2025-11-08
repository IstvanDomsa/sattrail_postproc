import matplotlib.pyplot as plt
import os

from logger import get_logger

import matplotlib
matplotlib.use('Agg')


def plot_mask_file(mask, plot_directory, maskfile):
    mask_name = get_filename_without_extension(maskfile)
    output_file = f"{plot_directory}/{mask_name}_mask.png"
    get_logger().debug(f"Plotting mask to {output_file}")

    plt.imshow(mask, cmap='gray', vmin=0, vmax=1)
    plt.title('Mask')
    plt.savefig(output_file)
    plt.close()


def plot_skeletonized_mask_file(mask, plot_directory, maskfile):
    mask_name = get_filename_without_extension(maskfile)
    output_file = f"{plot_directory}/{mask_name}_skeletonized.png"
    get_logger().debug(f"Plotting skeletonized mask to {output_file}")

    plt.imshow(mask, cmap='gray', vmin=0, vmax=1)
    plt.title('Skeletonized Mask')
    plt.savefig(output_file)
    plt.close()


def get_filename_without_extension(file_path):
    return os.path.splitext(os.path.basename(file_path))[0]
