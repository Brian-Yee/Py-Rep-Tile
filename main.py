#!/usr/bin/env python3
# pylint: disable=invalid-name
"""
Main module for creating pinwheel fractal and interfacing with CLI.
"""
import argparse
from src.triangle import Triangle
from src.renderer import draw_triangles


def main(depth):
    """
    Draws pin wheel tile.

    Arguments:
        depth: int
            Depth of copies to form fractal.
    """
    triangles = [
        Triangle(origin=complex(0, 0), long_leg=complex(2, 0), short_leg=complex(0, 1))
    ]

    for _ in range(depth - 1):
        new_triangles = []
        for triangle in triangles:
            new_triangles += triangle.subdivide()
        triangles = new_triangles

    draw_triangles(triangles, fpath="imgs/pinwheel.png")


def parse_arguments():
    """
    Main CLI for interfacing with pinwheel tiler.

    Returns:
        argparse.Namespace
            Argparse namespace containg CLI inputs.
    """
    parser = argparse.ArgumentParser(
        description=("Polygon Spiral art creater. Create spiral art!")
    )

    parser.add_argument("depth", type=int, help="Depth of copies to form fractal")

    return parser.parse_args()


def assert_argument_vals(args):
    """
    Various asserts to enforce CLI arguments passed are valid.

    Arguments:
        args: argparse.Namespace
            Argparse namespace containg CLI inputs.
    """
    assert args.depth >= 1, "Invalid amount of sides passed."


if __name__ == "__main__":
    ARGS = parse_arguments()
    assert_argument_vals(ARGS)

    main(ARGS.depth)
