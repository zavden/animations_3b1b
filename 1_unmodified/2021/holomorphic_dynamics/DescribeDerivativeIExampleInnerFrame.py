# ==============================================================================
# Scene:      DescribeDerivativeIExampleInnerFrame
# Source:     videos/_2021/holomorphic_dynamics.py (lines 1735-1736)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl DescribeDerivativeIExampleInnerFrame.py DescribeDerivativeIExampleInnerFrame -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class DescribeDerivative(Scene):
    zoom_in_frame = False
    z = 1
    z_str = "{1}"
    fz_str = "1"
    fpz_str = "2"

    def construct(self):
        # Add plane
        plane = ComplexPlane((-4, 4), (-2, 2))
        plane.set_height(FRAME_HEIGHT)
        plane.add_coordinate_labels(font_size=18)
        self.add(plane)

        # Add function labels
        z_str = self.z_str
        fz_str = self.fz_str
        fpz_str = self.fpz_str
        kw = {
            "tex_to_color_map": {
                "z": GREY_A,
                z_str: YELLOW,
            },
            "isolate": ["f", "(", ")", "=", z_str, fz_str, fpz_str],
        }
        f_label = OldTex("f(z) = z^2", **kw)
        df_label = OldTex("f'(z) = 2z", **kw)
        labels = VGroup(f_label, df_label)
        labels.arrange(DOWN)
        labels.to_corner(UL)
        labels.set_stroke(BLACK, 5, background=True)
        corner_rect = SurroundingRectangle(labels, buff=0.25)
        corner_rect.set_stroke(WHITE, 2)
        corner_rect.set_fill(BLACK, 0.9)
        corner_group = VGroup(corner_rect, *labels)
        corner_group.to_corner(UL, buff=0)

        df_question = Text("Derivative?")
        df_question.set_stroke(BLACK, 5, background=True)
        df_arrow = Vector(LEFT)
        df_arrow.next_to(f_label, RIGHT, SMALL_BUFF)
        df_question.next_to(df_arrow, RIGHT, SMALL_BUFF)

        self.add(corner_rect, f_label)
        self.play(
            FadeIn(df_question, 0.2 * RIGHT),
            ShowCreation(df_arrow)
        )
        self.wait()
        self.play(
            FadeIn(df_label, shift=0.5 * DOWN),
            FadeOut(df_question),
            Uncreate(df_arrow),
        )

        # Add dots
        density = 10
        dot_radius = 0.025
        dots = DotCloud([
            plane.c2p(x, y)
            for x in np.arange(-3.7, 3.7, 1.0 / density)
            for y in np.arange(-2.0, 2.1, 1.0 / density)
        ])
        dots.set_radius(dot_radius)
        dots.set_color(GREY_B)
        dots.set_gloss(0.2)
        dots.set_opacity(0.5)
        dots.add_updater(lambda m: m)

        epsilon = 5e-3
        tiny_dots = DotCloud([
            plane.n2p(self.z + epsilon * complex(x, y))
            for x in np.arange(-20, 20)
            for y in np.arange(-10, 10)
        ])
        tiny_dots.set_radius(dot_radius * 15 * epsilon)
        tiny_dots.set_opacity(0.75)
        tiny_dots.set_color_by_gradient(YELLOW, BLUE)
        tiny_dots.set_gloss(0.2)

        self.add(dots, corner_group)
        self.play(ShowCreation(dots), run_time=2)
        self.wait()

        # Show function evaluation
        ex_labels = VGroup(
            OldTex(f"f({z_str}) = {fz_str}", **kw),
            OldTex(f"f'({z_str}) = {fpz_str}", **kw),
        )
        for ex_label, gen_label in zip(ex_labels, labels):
            ex_label.next_to(gen_label, RIGHT, MED_LARGE_BUFF)

        ex_labels[0].align_to(ex_labels[1], LEFT)

        corner_rect.generate_target()
        corner_rect.target.set_width(
            VGroup(ex_labels, labels).get_width() + 0.5,
            about_edge=LEFT,
            stretch=True,
        )

        self.add(*corner_group)
        self.play(
            MoveToTarget(corner_rect),
            FadeIn(ex_labels),
        )
        self.wait()

        # Apply function
        fade_anims = []
        if self.zoom_in_frame:
            rect = self.camera.frame
            plane.generate_target()
            fade_anims = [
                ApplyMethod(dots.set_opacity, 0, rate_func=squish_rate_func(smooth, 0.5, 1.0)),
                plane.animate.set_stroke(width=0.25),
            ]
        else:
            rect = ScreenRectangle()
            rect.set_height(FRAME_HEIGHT)
            rect.set_stroke(WHITE, 2)

        self.play(
            rect.animate.replace(tiny_dots, 1).move_to(plane.n2p(self.z)),
            *fade_anims,
            FadeIn(tiny_dots),
            run_time=3,
        )
        self.wait()

        # def func(p):
        #     z = plane.p2n(p)
        #     return plane.n2p(z**2)

        def homotopy(x, y, z, t):
            z = plane.p2n([x, y, z])
            return plane.n2p(z**(1 + t))

        rc = rect.get_center()
        path = ParametricCurve(lambda t: homotopy(*rc, t))

        self.play(
            Homotopy(homotopy, dots),
            Homotopy(homotopy, tiny_dots),
            MoveAlongPath(rect, path),
            # dots.animate.apply_function(func),
            # tiny_dots.animate.apply_function(func),
            # rect.animate.move_to(func(rect.get_center())),
            run_time=5,
        )
        self.wait()


class DescribeDerivativeIExample(DescribeDerivative):
    z = 1j
    z_str = "{i}"
    fz_str = "-1"
    fpz_str = "2i"


class DescribeDerivativeIExampleInnerFrame(DescribeDerivativeIExample):
    zoom_in_frame = True
