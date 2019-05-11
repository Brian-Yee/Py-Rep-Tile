#!/usr/bin/env python3
# pylint: disable=invalid-name, too-many-instance-attributes, too-many-locals
"""
Concrete pinwheel class implementing the pinwheel rep-tile.
"""
import cmath

import numpy as np

from src.reptile import RepTile


class Pinwheel(RepTile):
    """
    Methods for aiding in generating the triangles of the pinwheel tiling.

    Geometric notation for this class uses the sketched noted points:
        ^   P
        |   .  .
        |   .     .
        |   .        c
        |   .       .  .
        |   .      .   .  .
     I  |   .     .          .
        |   .    .      .       .
        |   .   b                  d
        |   .  .  .      .      .     .
        |   . .      .        .          .
        |   ..          . . .     alpha (   .
        |   Q . . . . . . a . . . . . . . . .  R
        |
        +---------------------------------------->
                           R
    """

    alpha = np.arctan2(1, 2)

    def __init__(self, origin, index, thumb):  # pylint: disable=duplicate-code
        """
        Initialize coordinate system of pinwheel tile.

        Arguments:
            origin: complex
                Origin point used as a reference for a tile.
            index: complex
                Long edge touching the origin vertex.
            thumb: complex
                Short edge touching the origin vertex.
        """
        super().__init__(origin, index, thumb)

        self._Q = origin
        self._R = index
        self._P = thumb

        QP = self._P - self._Q

        QP_rad, QP_phi = cmath.polar(QP)
        Qa = cmath.rect(QP_rad, QP_phi + self.sign * np.pi / 2)
        Qc = cmath.rect(2 / np.sqrt(5) * QP_rad, QP_phi + self.sign * self.alpha)
        Qb = Qc / 2

        self.a = self._Q + Qa
        self.c = self._Q + Qc
        self.b = self._Q + Qb

        self.d = self.a + Qb

        self._perimeter = (self._Q, self._P, self._R)

    def subdivide(self):
        """
        Subdivide the triangle into a pinwheel triangle.

        Note the set of triangles {bac, dac} are chiral to {cPQ, baQ, daR}, thus we
        define handedness of the system via the cross product of the legs.

        Returns:
            tuple(Triangle)
                Subdividing pinwheel triangles of self triangle.
        """

        return (
            Pinwheel(origin=self.c, index=self._Q, thumb=self._P),
            Pinwheel(origin=self.b, index=self.a, thumb=self._Q),
            Pinwheel(origin=self.b, index=self.a, thumb=self.c),
            Pinwheel(origin=self.d, index=self._R, thumb=self.a),
            Pinwheel(origin=self.d, index=self.c, thumb=self.a),
        )
