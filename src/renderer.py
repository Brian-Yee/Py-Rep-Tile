#!/usr/bin/env python3
"""
Functions for drawing images.
"""
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.backends.backend_agg import FigureCanvasAgg
import numpy as np

plt.rcParams["figure.figsize"] = (20, 20)


def draw_triangles(triangles, fpath="triangles.png"):
    """
    Renders a set of triangles.

    Arguments:
        triangles: list(Triangle)
            List of triangles to render.
    """
    resolution = 1024
    viridis = cm.get_cmap("viridis", resolution)
    viridis(np.linspace(0, 1, resolution))
    for triangle in triangles:
        theta = np.arctan2(triangle.short_leg.real, triangle.short_leg.imag)
        triangle = triangle.rect()
        color = viridis(int(resolution * theta / (2 * np.pi)))
        plt.fill(*list(zip(*triangle + triangle[:1])), color=color)

    plt.gca().set_aspect("equal")
    plt.gca().axis("off")
    canvas = FigureCanvasAgg(plt.gcf())
    canvas.draw()

    stream, (width, height) = canvas.print_to_buffer()
    img = np.fromstring(stream, np.uint8).reshape((height, width, 4))

    plt.imsave(fpath, _trim_border(img))


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
