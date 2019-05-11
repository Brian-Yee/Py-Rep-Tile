#!/usr/bin/env python3
# pylint: disable=invalid-name
"""
Main module for creating pinwheel fractal and interfacing with CLI.
"""
import argparse

import numpy as np

from src.pinwheel import Pinwheel
from src.sphinx import Sphinx
from src.renderer import draw_rep_tiles


def main(iterations, rep_tile_name):
    """
    Tile a set of rep-tiles.

    Arguments:
        iterations: int
            Number of times to iteratively subdivide rep-tiles into.
        rep_tile: str
            Rep-tile to use for generation.
    """
    if rep_tile_name == "pinwheel":
        rep_tiles = [
            Pinwheel(origin=complex(0, 0), index=complex(2, 0), thumb=complex(0, 1))
        ]
    elif rep_tile_name == "sphinx":
        rep_tiles = [
            Sphinx(
                origin=complex(0, 0),
                index=complex(6, 0),
                thumb=complex(2, 2 * np.sqrt(3)),
            )
        ]
    else:
        raise ValueError("Invalid rep_tile passed.")

    for _ in range(iterations - 1):
        new_rep_tiles = []
        for rep_tile in rep_tiles:
            new_rep_tiles += rep_tile.subdivide()
        rep_tiles = new_rep_tiles

    draw_rep_tiles(
        rep_tiles, fpath="imgs/{rep_tile_name}.png".format(rep_tile_name=rep_tile_name)
    )


def parse_arguments(supported_rep_tiles):
    """
    Main CLI for interfacing with pinwheel tiler.

    Returns:
        argparse.Namespace
            Argparse namespace containg CLI inputs.
    """
    parser = argparse.ArgumentParser(description=("Pinwheel tiling program."))

    parser.add_argument(
        "rep_tile",
        type=str,
        help=(
            "Type of rep-tile to iteratively generate. Select from "
            + str(supported_rep_tiles)
        ),
    )
    parser.add_argument(
        "iterations",
        type=int,
        help="Number of times to iteratively subdivide rep-tiles into.",
    )

    return parser.parse_args()


def assert_argument_vals(args, supported_rep_tiles):
    """
    Various asserts to enforce CLI arguments passed are valid.

    Arguments:
        args: argparse.Namespace
            Argparse namespace containg CLI inputs.
    """
    assert args.iterations >= 1, "Invalid amount of sides passed."
    assert (
        args.rep_tile in supported_rep_tiles
    ), "Invalid reptile, use -h for supported list."


if __name__ == "__main__":
    SUPPORTED_REP_TILES = ("pinwheel", "sphinx")

    ARGS = parse_arguments(SUPPORTED_REP_TILES)

    assert_argument_vals(ARGS, SUPPORTED_REP_TILES)

    main(ARGS.iterations, ARGS.rep_tile)
