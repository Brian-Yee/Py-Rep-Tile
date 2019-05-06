#!/usr/bin/env python3
"""
Main module for creating pinwheel fractal and interfacing with CLI.
"""
import argparse
import numpy as np
import matplotlib.pyplot as plt
import itertools


def generate_base_coords():
    """
    Consider the following sketch of the pinwheel fractal the following
    quantities are as defined:
        AB 1
        AD 2
        BD sqrt(5)

    If we can define AC we can easily derive all other nested triangles. Note that the
    triangle {AB, AC, BC} has the same ratios by definition of {AB, AD, BD}. Thus the
    length of AC is 2/sqrt(5), and the angle <EAF is arctan2(sqrt(5)/1). From here the
    rest is trivial:

        B
        .  .
        .     .
        .        C
        .       .  .
        .      .   .  .
        .     .          .
        .    .      .       .
        .   E                  G
        .  .  .      .      .     .
        . .      .        .          .
        ..          . . .               .
        A . . . . . . F . . . . . . . . .  D

    Note that if we rotate by the <FDG to set the y-component of BD to zero and perform
    a reflection we obtain a scaled version of AEF. It is trivial to see that simple
    translation yield FGD, while a rotation and shift yields ABC. Less clear are how
    to obtain CEF and CGF.

    Note that CEF and CGF form the rectangle CEFG and another rectangle can be made by
    rotating the triangle by pi around A and then translating by {AB, BD}. Given the
    triangle has retained the same area it is to the same scale as triangles
    {ABC, AEF, FGD} rescaled by the prior "rotate and flip method". Thus the rectanngle
    need only be rotated by angle <AFE and shifted so that the original point D aligns
    with the rescaled point F.

    In this way we have inflated the triangle.

    Returns:
        coords: list(float, float)

    """
    # -2
    theta_FAE = np.pi / 2 - np.arctan2(1, 2)
    radius_AC = 2 / np.sqrt(5)
    coord_C = (radius_AC * np.cos(theta_FAE), radius_AC * np.sin(theta_FAE))

    coords = np.array(
        [
            (0, 0),
            (0, 1),
            (1, 0),
            (2, 0),
            coord_C,
            (coord_C[0] / 2, coord_C[1] / 2),
            (1 + coord_C[0] / 2, coord_C[1] / 2),
        ]
    ).T

    all_coords = coords
    # fmt: off
    triangle_idxs = [
        [0, 1, 4],
        [0, 2, 5],
        [3, 2, 6],
        [2, 4, 6],
        [2, 4, 5], # easy way first
    ]
    triangles = [coords[:, x].T for x in triangle_idxs]
    # fmt: on

    # NOTE need to remove redundancies
    for x in range(1):
        new_triangles = []
        for e, triangle in enumerate(triangles):
            edges = sorted(
                itertools.combinations(triangle, 2),
                key=lambda x: np.linalg.norm(x[1] - x[0]),
            )

            for point1, point2 in itertools.product(*edges[:2]):
                if np.all(np.isclose(point1, point2)):
                    shared_point = point1
                    break

            for sign in [1, -1]:
                coords[1, :] *= sign

                edge_length = np.linalg.norm(edges[0][1] - edges[0][0])
                scaled_coords = edge_length * coords

                v1 = edges[1][1] - edges[1][0]
                theta = np.arctan2(v1[1], v1[0])
                rotated_coords = rotate(
                    scaled_coords[:, 0], scaled_coords, np.pi + theta
                )

                trans_vec = (
                    shared_point.reshape(-1, 2) - rotated_coords[:, 0]
                ).reshape(2, -1)
                translated_coords = trans_vec + rotated_coords

                coords[1, :] *= sign

                triangle_patch = np.vstack([triangle, triangle[0, :]])
                xs, ys = np.vsplit(triangle_patch, 2)

                for x in triangle_idxs:
                    new_triangles.append(translated_coords[:, x].T)
                all_coords = np.hstack([all_coords, translated_coords])
            triangles = new_triangles
        print(len(triangles))
        print(len(triangles[0]))

    for triangle in triangles:
        # print(triangle)
        plt.fill(*np.hsplit(triangle, 2))
    # plt.scatter(*all_coords)

    plt.gca().set_aspect("equal")
    plt.show()
    # plt.show(block=False)
    # plt.pause(5)
    # plt.close()


def rotate(origin, coords, theta):
    """
    Rotate a point counterclockwise by a given angle around a given origin.

    The angle should be given in radians.
    """
    cos, sin = np.cos(theta), np.sin(theta)
    rotation_matrix = np.array(((cos, -sin), (sin, cos)))
    rotated_coords = origin.reshape(2, -1) + np.dot(
        rotation_matrix, (coords - origin.reshape(2, -1))
    )
    return rotated_coords


def main(depth):
    """
    Draws polygon spiral artwork.

    Arguments:
        depth: int
            Depth of copies to form fractal.
    """

    generate_base_coords()


def parse_arguments():
    """
    Main CLI for interfacing with Polygon Spiral art generator.

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
