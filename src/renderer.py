#!/usr/bin/env python3
"""
Functions for drawing images.
"""
import matplotlib.cm
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
import numpy as np

plt.rcParams["figure.figsize"] = (30, 30)


def draw_triangles(
    triangles, as_rectangle, fpath="triangles.png", cmap_resolution=1024
):
    """
    Renders a set of triangles coloured by phase.

    Arguments:
        triangles: list(Triangle)
            List of triangles to render.
        cmap_resolution: int
            Resolution of color map.
        rectangle: bool
            Whether to print the final image as a rectangle or triangle.
    """
    fig, ax = plt.subplots()
    ax.set_xlim(0, max(x.max_real for x in triangles))
    ax.set_ylim(0, max(x.max_imag for x in triangles))
    ax.set_aspect("equal")
    ax.axis("off")

    patch_collection = PatchCollection(
        [Polygon(x.perimeter) for x in triangles],
        cmap=matplotlib.cm.get_cmap("twilight", cmap_resolution),
    )

    phases = np.array([x.phase for x in triangles])
    patch_collection.set_array(cmap_resolution * phases / (2 * np.pi))

    ax.add_collection(patch_collection)

    canvas = FigureCanvasAgg(fig)
    canvas.draw()

    stream, (width, height) = canvas.print_to_buffer()
    img = np.fromstring(stream, np.uint8).reshape((height, width, 4))

    img = _trim_border(img)
    if as_rectangle:
        img += img[::-1, ::-1]

    plt.imsave(fpath, img)


def _trim_border(img):
    """
    Trims white space border of a numpy image.

    Arguments:
        img: np.array
            Numpy image.

    Returns:
        img: np.array
            Numpy image with no white border space.
    """
    for i in range(img.shape[0]):
        if np.any(img[i, :, :] != 255):
            img = img[i:, :, :]
            break

    for i in range(img.shape[0] - 1, 0, -1):
        if np.any(img[i, :, :] != 255):
            img = img[: i + 1, :, :]
            break

    for i in range(img.shape[1]):
        if np.any(img[:, i, :] != 255):
            img = img[:, i:, :]
            break

    for i in range(img.shape[1] - 1, 0, -1):
        if np.any(img[:, i, :] != 255):
            img = img[:, : i + 1, :]
            break

    return img
