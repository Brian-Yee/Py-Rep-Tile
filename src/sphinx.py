#!/usr/bin/env python3
# pylint: disable=invalid-name, too-many-instance-attributes, too-many-locals
"""
Concrete sphinx class implementing the sphinx rep-tile.
"""
import cmath

import numpy as np

from src.reptile import RepTile


class Sphinx(RepTile):
    """
    Methods for aiding in generating the triangles of the sphinx tile.

    Geometric notation for this class uses the sketched noted points:
        ^
        |          P
        |         . .
     I  |        .   .
        |       .     .
        |      i   f . a . . . b
        |     .   . .         . .
        |    h . g   .   d . c   .
        |   .         . . alpha ( .
        |  Q . j . . . e . . . k . R
        |
        +---------------------------------------->
                           R
    """

    alpha = np.pi / 3

    def __init__(self, origin, index, thumb):
        """
        Initialize coordinate system of sphinx tile.

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
        QR = self._R - self._Q
        QP_rad, QP_phi = cmath.polar(QP)
        QR_rad, QR_phi = cmath.polar(QR)

        Pa = cmath.rect(QP_rad / 2, QP_phi + 2 * self._sign * self.alpha)

        self._a = self._P + Pa
        self._b = self._R - Pa

        Qe = cmath.rect(QR_rad / 2, QR_phi)
        Qh = cmath.rect(QP_rad / 4, QP_phi)
        self._e = self._Q + Qe
        self._h = self._Q + Qh
        self._d = self._e + Qh

        self._f = self._e - Pa

        hg = Qe / 3
        self._g = self._h + hg
        self._c = self._d + hg

        self._i = self._Q + Qh / 2
        self._j = self._Q + hg
        self._k = self._R - hg

        self._perimeter = (self._Q, self._P, self._a, self._b, self._R)

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
            Sphinx(origin=self._e, thumb=self._f, index=self._Q),
            Sphinx(origin=self._R, thumb=self._b, index=self._e),
            Sphinx(origin=self._f, thumb=self._e, index=self._b),
            Sphinx(origin=self._P, thumb=self._a, index=self._h),
        )
