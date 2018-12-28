# point.py
#
# ICS 32 Spring 2017
# Code Example
#
# This module contains a Point class.  Objects of this class
# represent points in a two-dimensional space that can report
# their coordinates in both fractional and pixel coordinate
# systems.  They are created using either a fractional or a
# pixel coordinate system, then can be asked to translate
# themselves to either system.
#
# The idea is that a point in the fractional system corresponds
# naturally to a point in the pixel system, and vice versa.
# So rather than spread the code that performs these conversions
# throughout our program, we're better off creating a tool to
# make this kind of conversion simpler.  We could manipulate
# text without string objects, but string objects make the job
# easier by providing a variety of useful methods like strip(),
# split(), and upper().  Similarly, our Point objects provide
# the raw materials to handle coordinate system conversions
# for points in two-dimensional space.
#
# When we wrote this module in lecture, we first decided what we
# wanted to build, by considering how it should work when we
# were finished with it.  This is how we decided it should work:
#
# >>> import point
# >>> p1 = point.from_frac(0.5, 0.6)
# >>> p1
# <point.Point object ...>
# >>> p1.frac()
# (0.5, 0.6)
# >>> p1.pixel(1000, 800)
# (500, 480)
# >>> p2 = point.from_pixel(400, 600, 800, 800)
# >>> p2.frac()
# (0.5, 0.75)
# >>> p2.pixel(2000, 2000)
# (1000, 1500)

import math



class Point:
    def __init__(self, frac_x: float, frac_y: float):
        '''
        Initializes a Point object, given its fractional coordinates.
        '''
        self._frac_x = frac_x
        self._frac_y = frac_y


    def frac(self) -> (float, float):
        '''
        Returns an (x, y) tuple that contains fractional coordinates
        for this Point object.
        '''
        return (self._frac_x, self._frac_y)


    def pixel(self, width: float, height: float) -> (float, float):
        '''
        Returns an (x, y) tuple that contains pixel coordinates for
        this Point object.  The total_size parameter specifies the
        total size, in pixels, of the area in which the point needs
        to be specified -- this is used to make the appropriate
        conversion, since the pixel position of a fractional point
        changes as the size changes.
        '''
        return (int(self._frac_x * width), int(self._frac_y * height))


    def frac_distance_from(self, p: 'Point') -> float:
        '''
        Given another Point object, returns the distance, in
        terms of fractional coordinates, between this Point and the
        other Point.
        '''

        # Per the Pythagorean theorem from mathematics, the distance
        # between two points is the square root of the sum of the
        # squares of the differences in the x- and y-coordinates.
        return math.sqrt(
            (self._frac_x - p._frac_x) * (self._frac_x - p._frac_x)
            + (self._frac_y - p._frac_y) * (self._frac_y - p._frac_y))

        # Note, too, that there's a function in the Python standard
        # library, math.hypot, that does exactly this calculation.



# These two functions are used to create Points that are either
# being created from fractional or pixel coordinates.  Given these
# two functions, we'll never create Point objects by calling the
# Point constructor; instead, we'll just call the appropriate
# of these two functions, depending on whether we have fractional or
# pixel coordinates already.
#
# You might be wondering why we would solve the problem this way,
# instead of just using the Point constructor.  The problem is that
# the Point constructor doesn't make clear, when looking at it, whether
# its parameters are fractional or pixel coordinates.  If, instead, we
# say "point.from_frac" or "point.from_pixel", what we've written reads
# like English (e.g., "Make me a point from a fractional coordinate.").


def from_frac(frac_x: float, frac_y: float) -> Point:
    '''Builds a Point given fractional x and y coordinates.'''
    return Point(frac_x, frac_y)



def from_pixel(pixel_x: float, pixel_y: float, width: float, height: float) -> Point:
    '''
    Builds a Point given pixel x and y coordinates, along with
    the width and height of the area (necessary for conversion
    to fractional).
    '''
    return Point(pixel_x / width, pixel_y / height)
