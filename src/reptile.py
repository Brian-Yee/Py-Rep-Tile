#!/usr/bin/env python3
"""
Abstract base class for creating rep-tiles.
"""
import cmath

import numpy as np


class RepTile:
    """
    Rep-Tile.
    """

    def __init__(self, origin, index, thumb):
        """
        Initialize parameters required to define the parameters of rep-tile.

        Arguments:
            origin: complex
                Intersecting point of triangle legs.
            index: complex
                Long edge touching the origin vertex.
            thumb: complex
                Short edge touching the origin vertex.
        """
        self._origin = origin
        self._index = index
        self._thumb = thumb

        vecs = (self._thumb - origin, self._index - origin)
        self.sign = np.sign(np.cross(*[np.array([x.real, x.imag]) for x in vecs]))
        self._perimeter = ()

    @property
    def max_real(self):
        """
        Largest real component of triangle.

        Returns:
            float
                Largest real component of triangle.
        """
        if not self._perimeter:
            raise ValueError("._perimeter not implemented.")

        return max(x.real for x in self._perimeter)

    @property
    def max_imag(self):
        """
        Largest imaginary component of triangle.

        Returns:
            float
                Largest imaginary component of triangle.
        """
        if not self._perimeter:
            raise ValueError("._perimeter not implemented.")

        return max(x.imag for x in self._perimeter)

    @property
    def phase(self):
        """
        Phase of triangle, defined by the shortest leg.

        Returns:
            float
                Phase of shortest leg vector.
        """
        return cmath.phase(self._thumb - self._origin)

    @property
    def perimeter(self):
        """
        Returns the perimeter of triangle {A, B, C} defined as (A, B, C, A)

        Returns:
            tuple(float, float)
                Perimeter of triangle
        """
        if not self._perimeter:
            raise ValueError("._perimeter not implemented.")

        points = tuple([(x.real, x.imag) for x in self._perimeter])

        return points + points[:1]
