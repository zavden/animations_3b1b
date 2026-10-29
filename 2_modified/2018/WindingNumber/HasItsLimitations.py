# ==============================================================================
# Scene:      HasItsLimitations
# Source:     videos/_2018/WindingNumber.py (lines 1575-1661)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl HasItsLimitations.py HasItsLimitations -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Arc.set_bound_angles()/init_points() do not exist in GL: the arc is built directly from (start_angle, angle) = (pi, -pi)
#   - same as above: (start_angle, angle) = (3pi/4, -3pi/4)
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


class HasItsLimitations(Scene):
    CONFIG = {
        "camera_config" : {"use_z_coordinate_for_display_order": True},
    }

    def construct(self):
        num_line = NumberLine()
        num_line.add_numbers()
        self.add(num_line)

        self.wait()

        # We arrange to go from 2 to 4, a la the squaring in FirstSqrtScene
        base_point = num_line.number_to_point(2) + OUT

        dot_color = ORANGE

        DOT_Z = OUT
        # Note: This z-buffer value is needed for our static scenes, but is
        # not sufficient for everything, in that we still need to use 
        # the foreground_mobjects trick during animations.
        # At some point, we should figure out how to have animations
        # play well with z coordinates.
        
        input_dot = Dot(base_point + DOT_Z, color = dot_color)
        input_label = OldTexText("Input", fill_color = dot_color)
        input_label.next_to(input_dot, UP + LEFT)
        input_label.add_background_rectangle()
        self.add_foreground_mobject(input_dot)
        self.add(input_label)

        # CHANGE: Arc.set_bound_angles()/init_points() do not exist in GL: the arc is built directly from (start_angle, angle) = (pi, -pi)
        curved_arrow = Arc(np.pi, -np.pi, color = MAROON_E)
        curved_arrow.add_tip()
        curved_arrow.move_arc_center_to(base_point + RIGHT)
        # Could do something smoother, with arrowhead moving along partial arc?
        self.play(ShowCreation(curved_arrow))

        output_dot = Dot(base_point + 2 * RIGHT + DOT_Z, color = dot_color)
        output_label = OldTexText("Output", fill_color = dot_color)
        output_label.next_to(output_dot, UP + RIGHT)
        output_label.add_background_rectangle()

        self.add_foreground_mobject(output_dot)
        self.add(output_label)
        self.wait()

        num_plane = NumberPlane()
        num_plane.add_coordinates()

        new_base_point = base_point + 2 * UP
        new_input_dot = input_dot.copy().move_to(new_base_point)
        new_input_label = input_label.copy().next_to(new_input_dot, UP + LEFT)
        
        # CHANGE: same as above: (start_angle, angle) = (3pi/4, -3pi/4)
        new_curved_arrow = Arc(np.pi * 3/4, -np.pi * 3/4).match_style(curved_arrow)
        new_curved_arrow.add_tip()

        input_diff = input_dot.get_center() - curved_arrow.get_points()[0]
        output_diff = output_dot.get_center() - curved_arrow.get_points()[-1]

        new_curved_arrow.shift((new_input_dot.get_center() - new_curved_arrow.get_points()[0]) - input_diff)

        new_output_dot = output_dot.copy().move_to(new_curved_arrow.get_points()[-1] + output_diff)
        new_output_label = output_label.copy().next_to(new_output_dot, UP + RIGHT)

        dot_objects = Group(input_dot, input_label, output_dot, output_label, curved_arrow)
        new_dot_objects = Group(new_input_dot, new_input_label, new_output_dot, new_output_label, new_curved_arrow)

        self.play(
            FadeOut(num_line), FadeIn(num_plane), 
            ReplacementTransform(dot_objects, new_dot_objects),
        )

        self.wait()

        self.add_foreground_mobject(new_dot_objects)

        complex_plane = ComplexPlane()
        complex_plane.add_coordinates()
        
        # This looks a little wonky and we may wish to do a crossfade in Premiere instead
        self.play(FadeOut(num_plane), FadeIn(complex_plane))

        self.wait()
