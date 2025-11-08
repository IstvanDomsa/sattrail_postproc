from logger import get_logger, create_logger, DEBUG
import numpy as np
import pandas as pd
from astropy.io import fits
from skimage.morphology import skeletonize
import json
from typing import cast

from plotter import plot_mask_file, plot_skeletonized_mask_file
from hough import phl, progressive_phl


def process_mask(
        subfitsfile,
        maskfile,
        outputfile=None,
        skeleton=False,
        progressive=False,
        plot_directory=None,
        line_length=10,
        line_gap=50,
        threshold=10,
        initial_threshold=200,
    ):
    # setup logger
    create_logger(level=DEBUG)
    get_logger().info(
        f"Processing {subfitsfile} FITS file and {maskfile} mask file.")

    # load mask, return if empty
    mask_pixels = open_maskfile(maskfile)
    if mask_pixels is None or mask_pixels.size == 0:
        get_logger().info("Mask is empty.")
        if outputfile:
            create_empty_outputfile(outputfile)
        return None

    get_logger().debug(f"Number of pixels in mask: {len(mask_pixels)}")

    # load FITS image
    image = cast(np.ndarray, fits.getdata(subfitsfile))
    if image is None:
        get_logger().error(f"Failed to load FITS file: {subfitsfile}")
        return None
    get_logger().debug(f"FITS image shape: {image.shape}")

    # convert mask from pixel array to image
    mask = np.zeros(image.shape, dtype=np.uint8)
    mask[mask_pixels[:, 1], mask_pixels[:, 0]] = 1

    # plot mask if requested
    if plot_directory:
        plot_mask_file(mask, plot_directory, maskfile)

    # skeletonize mask (and plot it) if requested
    if skeleton:
        mask = skeletonize(mask.astype(np.uint8)).astype('>f4')
        get_logger().debug(
            f"Number of pixels in mask after skeletonization: {mask.sum():.0f}")
        if plot_directory:
            plot_skeletonized_mask_file(mask, plot_directory, maskfile)

    # Hough transform to detect lines
    if progressive:
        lines = progressive_phl(
            mask,
            min_line_length=line_length,
            min_threshold=threshold,
            initial_threshold=initial_threshold,
            initial_gap=line_gap
        )
    else:
        lines = phl(mask, threshold=threshold, line_length=line_length, line_gap=line_gap)

    return None


def open_maskfile(maskfile):
    with open(maskfile, 'r') as f:
        data = json.load(f)
        return np.array(data['mask'])


def create_empty_outputfile(outputfile):
    get_logger().debug(f"Creating empty output file: {outputfile}")
    dat = pd.DataFrame([0], columns=['numlines'])
    dat.to_hdf(outputfile, key='numlines')
