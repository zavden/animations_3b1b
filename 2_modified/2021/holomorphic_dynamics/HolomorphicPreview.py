# ==============================================================================
# Scene:      HolomorphicPreview
# Source:     videos/_2021/holomorphic_dynamics.py (lines 318-398)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl HolomorphicPreview.py HolomorphicPreview -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - background_line_style without "stroke_color" -> BLUE_D is added, the previous default (manimgl bug: NumberPlane.init_background_lines reads background_line_style["stroke_color"] with no fallback, coordinate_systems.py:669)
# ==============================================================================

from manim_imports_ext import *

class HolomorphicPreview(Scene):
    def construct(self):
        in_plane = ComplexPlane(
            (-2, 2),
            (-2, 2),
            height=5,
            width=5,
        )
        in_plane.add_coordinate_labels(font_size=18)
        in_plane.to_corner(DL)
        out_plane = in_plane.deepcopy()
        out_plane.to_corner(DR)

        input_word = Text("Input")
        output_word = Text("Output")

        input_word.next_to(in_plane, UP)
        output_word.next_to(out_plane, UP)

        self.add(in_plane, out_plane, input_word, output_word)

        # Show tiny neighborhood
        tiny_plane = ComplexPlane(
            (-2, 2),
            (-2, 2),
            height=0.5,
            width=0.5,
            axis_config={
                "stroke_width": 1.0,
            },
            # CHANGE: NumberPlane/ComplexPlane: background_line_style without stroke_color gives KeyError (manimgl no longer merges it with the default value, BLUE_D)
            background_line_style={
                "stroke_color": BLUE_D,
                "stroke_width": 1.0,
            },
            faded_line_ratio=1,
        )
        tiny_plane.move_to(in_plane.c2p(1, 1))

        for plane in in_plane, out_plane:
            plane.generate_target()
            for mob in plane.target.family_members_with_points():
                mob.set_opacity(mob.get_opacity() * 0.25)

        self.play(
            ShowCreation(tiny_plane),
            MoveToTarget(in_plane),
        )
        self.wait()

        def f(z):
            w = z - complex(1, 1)
            return complex(-1, 0.5) + complex(-1, 1) * w + 0.2 * w**2

        tiny_plane.prepare_for_nonlinear_transform()
        tiny_plane_image = tiny_plane.copy()
        tiny_plane_image.apply_function(
            lambda p: out_plane.n2p(f(in_plane.p2n(p)))
        )

        arrow = Arrow(
            tiny_plane, tiny_plane_image,
            path_arc=-PI / 4,
            stroke_width=5,
        )
        f_label = OldTex("f(z)")
        f_label.next_to(arrow, UP, SMALL_BUFF)

        words = Text("Looks roughly like\nscaling + rotating")
        words.set_width(2.5)
        words.move_to(VGroup(in_plane, out_plane))

        self.play(
            ShowCreation(arrow),
            FadeIn(f_label, 0.1 * UP),
        )
        self.play(
            TransformFromCopy(tiny_plane, tiny_plane_image),
            MoveToTarget(out_plane),
            FadeIn(words),
            run_time=2,
        )
        self.wait(2)
