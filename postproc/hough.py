from skimage.transform import probabilistic_hough_line
from skimage.draw import line

from logger import get_logger


def phl(edges, threshold=10, line_length=10, line_gap=50):
    """
    Wrapper for skimage's probabilistic Hough line transform.
    """
    lines = probabilistic_hough_line(
        edges,
        threshold=threshold,
        line_length=line_length,
        line_gap=line_gap
    )
    get_logger().debug(
        f'phl: Detected {len(lines)} lines with threshold {threshold}, line_length {line_length}, line_gap {line_gap}')
    return lines


def progressive_phl(edges, min_line_length=10, min_threshold=10, initial_threshold=100, initial_gap=50):
    """
    Progressively detect lines, removing them from consideration to allow detection of weaker lines.
    """
    edges_copy = edges.copy()
    all_lines = []
    threshold = initial_threshold
    lgap = initial_gap

    get_logger().debug(
        f'progressive_phl: Starting with threshold {threshold} and gap {lgap}')

    while (threshold > min_threshold) & (len(edges_copy[edges_copy > 0]) > 0):
        # Detect lines with current threshold
        lines = phl(
            edges_copy,
            threshold=threshold,
            line_length=min_line_length,
            line_gap=lgap
        )

        get_logger().debug(
            f'progressive_phl: Detected {len(lines)} lines at threshold {threshold} with gap {lgap}')

        if len(lines) == 0:
            # Lower threshold if no lines found
            threshold = max(min_threshold, int(threshold * 0.5))
            get_logger().debug(
                f'progressive_phl: no lines: lowering threshold to {threshold}')
            continue

        # Add detected lines
        all_lines.extend(lines)

        # Remove detected lines from edge image
        for L in lines:
            (p0, p1) = L
            # Draw line to remove these edges
            rr, cc = line(p0[1], p0[0], p1[1], p1[0])
            # Dilate slightly to remove nearby edges
            for r, c in zip(rr, cc):
                buffer = 1
                y_min = max(0, r - buffer)
                y_max = min(edges_copy.shape[0], r + buffer + 1)
                x_min = max(0, c - buffer)
                x_max = min(edges_copy.shape[1], c + buffer + 1)
                edges_copy[y_min:y_max, x_min:x_max] = 0

        # Gradually decrease threshold
        threshold = max(min_threshold, int(threshold * 0.5))
        lgap = max(2, int(lgap * 0.5))

        get_logger().debug(
            f'progressive_phl: threshold: {threshold}, gap: {lgap}')

    get_logger().debug(
        f'progressive_phl: Detected {len(all_lines)} total lines')

    return all_lines
