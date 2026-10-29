# ==============================================================================
# Scene:      Initial2dFuncSceneMorphing
# Source:     videos/_2018/WindingNumber.py (lines 1775-1821)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl Initial2dFuncSceneMorphing.py Initial2dFuncSceneMorphing -w -m --fps 15
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


# Used for clockwise circling in some scenes
cw_circle = Circle(color = WHITE).stretch(-1, 0)


def complex_to_pair(c):
    return np.array((c.real, c.imag))


def plane_func_from_complex_func(f):
    return lambda x_y4 : complex_to_pair(f(complex(x_y4[0],x_y4[1])))


def point3d_func_from_plane_func(f):
    def g(xxx_todo_changeme):
        (x, y, z) = xxx_todo_changeme
        f_val = f((x, y))
        return np.array((f_val[0], f_val[1], 0))
    return g


def point3d_func_from_complex_func(f):
    return point3d_func_from_plane_func(plane_func_from_complex_func(f))


class Initial2dFuncSceneBase(Scene):
    CONFIG = {
        "func" : point3d_func_from_complex_func(lambda c : c**2 - c**3/5 + 1)
        # We don't use example_plane_func because, unfortunately, the sort of examples
        # which are good for demonstrating our color mapping haven't turned out to be
        # good for visualizing in this manner; the gridlines run over themselves multiple 
        # times in too confusing a fashion
    }

    def show_planes(self):
        print("Error! Unimplemented (pure virtual) show_planes")

    def shared_construct(self):
        points = [LEFT + DOWN, RIGHT + DOWN, LEFT + UP, RIGHT + UP]
        for i in range(len(points) - 1):
            line = Line(points[i], points[i + 1], color = RED)
            self.obj_draw(line)

        def wiggle_around(point):
             radius = 0.2
             small_circle = cw_circle.copy()
             small_circle.scale(radius)
             small_circle.move_to(point + radius * RIGHT)
             small_circle.set_color(RED)
             self.obj_draw(small_circle)

        wiggle_around(points[-1])

    def obj_draw(self, input_object):
        self.play(ShowCreation(input_object))

    def construct(self):
        self.show_planes()
        self.shared_construct()


# Alternative to the above, manually implementing split screen with a morphing animation
class Initial2dFuncSceneMorphing(Initial2dFuncSceneBase):
    CONFIG = {
        "num_needed_anchor_curves" : 10,
    }

    def setup(self):
        split_line = DashedLine(FRAME_Y_RADIUS * UP, FRAME_Y_RADIUS * DOWN)
        self.num_plane = NumberPlane(x_radius = FRAME_X_RADIUS/2)
        self.num_plane.to_edge(LEFT, buff = 0)
        self.num_plane.prepare_for_nonlinear_transform()
        self.add(self.num_plane, split_line)

    def squash_onto_left(self, object):
        object.shift(FRAME_X_RADIUS/2 * LEFT)

    def squash_onto_right(self, object):
        object.shift(FRAME_X_RADIUS/2 * RIGHT)

    def obj_draw(self, input_object):
        output_object = input_object.copy()
        if input_object.get_num_curves() < self.num_needed_anchor_curves:
            input_object.insert_n_curves(self.num_needed_anchor_curves)
        output_object.apply_function(self.func)
        self.squash_onto_left(input_object)
        self.squash_onto_right(output_object)
        self.play(
            ShowCreation(input_object), 
            ShowCreation(output_object)
            )

    def show_planes(self):
        right_plane = self.num_plane.copy()
        right_plane.center()
        right_plane.prepare_for_nonlinear_transform()
        right_plane.apply_function(self.func)
        right_plane.shift(FRAME_X_RADIUS/2 * RIGHT)
        self.right_plane = right_plane
        crappy_cropper = FullScreenFadeRectangle(fill_opacity = 1)
        crappy_cropper.stretch_to_fit_width(FRAME_X_RADIUS)
        crappy_cropper.to_edge(LEFT, buff = 0)
        self.play(
            ReplacementTransform(self.num_plane.copy(), right_plane),
            FadeIn(crappy_cropper), 
            Animation(self.num_plane),
            run_time = 3
        )
