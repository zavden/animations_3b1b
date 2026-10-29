# ==============================================================================
# Scene:      VectorField
# Source:     videos/_2018/WindingNumber.py (lines 1537-1573)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl VectorField.py VectorField -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *
import warnings
import mpmath

warnings.warn("""
    Warning: This file makes use of
    ContinualAnimation, which has since
    been deprecated
""")


mpmath.mp.dps = 7


def complex_to_pair(c):
    return np.array((c.real, c.imag))


def plane_func_from_complex_func(f):
    return lambda x_y4 : complex_to_pair(f(complex(x_y4[0],x_y4[1])))


# Returns a function from 2-ples to 2-ples
# This function is specified by a list of (x, y, z) tuples, 
# and has winding number z (or total of all specified z) around each (x, y)
#
# Can also pass in (x, y) tuples, interpreted as (x, y, 1)
def plane_func_by_wind_spec(*specs):
    def embiggen(p):
        if len(p) == 3:
            return p
        elif len(p) == 2:
            return (p[0], p[1], 1)
        else:
            print("Error in plane_func_by_wind_spec embiggen!")
    specs = list(map(embiggen, specs))

    pos_specs = [x_y_z for x_y_z in specs if x_y_z[2] > 0]
    neg_specs = [x_y_z1 for x_y_z1 in specs if x_y_z1[2] < 0]

    neg_specs_made_pos = [(x_y_z2[0], x_y_z2[1], -x_y_z2[2]) for x_y_z2 in neg_specs]

    def poly(c, root_specs):
        return np.prod([(c - complex(x, y))**z for (x, y, z) in root_specs])

    def complex_func(c):
        return poly(c, pos_specs) * np.conjugate(poly(c, neg_specs_made_pos))
    
    return plane_func_from_complex_func(complex_func)


# Used in Initial2dFunc scenes, VectorField scene, and ExamplePlaneFunc
example_plane_func_spec = [(-3, -1.3, 2), (0.1, 0.2, 1), (2.8, -2, -1)]


example_plane_func = plane_func_by_wind_spec(*example_plane_func_spec)


class VectorField(Scene):
    CONFIG = {
        "func" : example_plane_func,
        "granularity" : 10,
        "arrow_scale_factor" : 0.1,
        "normalized_arrow_scale_factor" : 5
    }

    def construct(self):
        num_plane = NumberPlane()
        self.add(num_plane)

        x_min, y_min = num_plane.point_to_coords(FRAME_X_RADIUS * LEFT + FRAME_Y_RADIUS * UP)
        x_max, y_max = num_plane.point_to_coords(FRAME_X_RADIUS * RIGHT + FRAME_Y_RADIUS * DOWN)

        x_points = np.linspace(x_min, x_max, self.granularity)
        y_points = np.linspace(y_min, y_max, self.granularity)
        points = it.product(x_points, y_points)

        sized_arrows = Group()
        unsized_arrows = Group()
        for (x, y) in points:
            output = self.func((x, y))
            output_size = np.sqrt(sum(output**2))
            normalized_output = output * fdiv(self.normalized_arrow_scale_factor, output_size) # Assume output has nonzero size here
            arrow = Vector(output * self.arrow_scale_factor)
            normalized_arrow = Vector(normalized_output * self.arrow_scale_factor)
            arrow.move_to(num_plane.coords_to_point(x, y))
            normalized_arrow.move_to(arrow)
            sized_arrows.add(arrow)
            unsized_arrows.add(normalized_arrow)

        self.add(sized_arrows)
        self.wait()

        self.play(ReplacementTransform(sized_arrows, unsized_arrows))
        self.wait()
