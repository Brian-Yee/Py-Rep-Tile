#!/usr/bin/env python3
import cmath
import numpy as np


class Triangle:
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

    def __init__(self, origin, long_leg, short_leg):
        """
        Initialize parameters required to define the parameters of a triangle.

        Arguments:
            origin: complex
                Intersecting point of triangle legs.
            long_leg: complex
                Longest leg of triangle.
            short_leg: complex
                Shortest leg of triangle.
        """
        # to ensure consist I/O interface capabilities
        self.origin = origin
        self.long_leg = long_leg
        self.short_leg = short_leg

        # internal geometric notation
        self._Q = origin
        self._R = long_leg
        self._P = short_leg

    def subdivide(self):
        """
        Subdivide the triangle into a pinwheel triangle.

        Note the set of triangles {bac, dac} are chiral to {cPQ, baQ, daR}, thus we
        define handedness of the system via the cross product of the legs.

        Returns:
            tuple(Triangle)
                Subdividing pinwheel triangles of self triangle.
        """
        QP = self._P - self._Q
        QR = self._R - self._Q

        sign = np.sign(
            np.cross(np.array([QP.real, QP.imag]), np.array([QR.real, QR.imag]))
        )

        QP_rad, QP_phi = cmath.polar(QP)
        Qa = cmath.rect(QP_rad, QP_phi + sign * np.pi / 2)
        Qc = cmath.rect(2 / np.sqrt(5) * QP_rad, QP_phi + sign * self.alpha)
        Qb = Qc / 2

        a = self._Q + Qa
        c = self._Q + Qc
        b = self._Q + Qb

        d = a + Qb

        return (
            Triangle(origin=c, short_leg=self._P, long_leg=self._Q),
            Triangle(origin=b, long_leg=a, short_leg=self._Q),
            Triangle(origin=b, long_leg=a, short_leg=c),
            Triangle(origin=d, short_leg=a, long_leg=self._R),
            Triangle(origin=d, short_leg=a, long_leg=c),
        )

    def rect(self, tol=8):
        """
        Return triangular points as real floats.

        Arguments:
            tol: int
                Tolerance for rounding complex values.

        Returns:
            list(tuple(float, float))
                Points defining triangle in the Cartesian plane.
        """
        return tuple([(x.real, x.imag) for x in (self._Q, self._P, self._R)])
