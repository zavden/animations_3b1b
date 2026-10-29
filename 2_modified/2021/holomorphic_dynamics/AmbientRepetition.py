# ==============================================================================
# Scene:      AmbientRepetition
# Source:     videos/_2021/holomorphic_dynamics.py (lines 401-467)
# Category:   2 · Renders with modifications
# Includes code copied from: _2021/newton_fractal.py
#
# Run from this folder:
#     manimgl AmbientRepetition.py AmbientRepetition -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - The loop stops when the orbit leaves the screen (|point|>100): it escapes to infinity and gave NaN/overflow
# ==============================================================================

from manim_imports_ext import *


# ----- From _2021/newton_fractal.py -----

class AmbientRepetition(Scene):
    n_steps = 30

    def construct(self):
        plane = ComplexPlane((-2, 2), (-2, 2))
        plane.set_height(FRAME_HEIGHT)
        plane.add_coordinate_labels(font_size=24)
        self.add(plane)

        font_size = 36

        z0 = complex(0, 0)
        dot = Dot(color=BLUE)
        dot.move_to(plane.n2p(z0))
        z_label = OldTex("z", font_size=font_size)
        z_label.set_stroke(BLACK, 5, background=True)
        z_label.next_to(dot, UP, SMALL_BUFF)
        self.add(dot, z_label)

        def func(z):
            return z**2 + complex(-0.6436875, -0.441)

        def get_new_point():
            z = plane.p2n(dot.get_center())
            return plane.n2p(func(z))

        for n in range(self.n_steps):
            new_point = get_new_point()
            # CHANGE: the orbit escapes to infinity; it stops when it leaves the screen (huge points give NaN/overflow)
            if np.linalg.norm(new_point) > 100:
                break
            arrow = Arrow(dot.get_center(), new_point, buff=dot.get_height() / 2)

            dot_copy = dot.copy()
            dot_copy.move_to(new_point)
            dot_copy.set_color(YELLOW)
            fz_label = OldTex("f(z)", font_size=font_size)
            fz_label.set_stroke(BLACK, 8, background=True)
            fz_label.next_to(dot_copy, UP, SMALL_BUFF)

            self.add(dot, dot_copy, arrow, z_label)
            self.play(
                ShowCreation(arrow),
                TransformFromCopy(dot, dot_copy),
                FadeInFromPoint(fz_label, z_label.get_center()),
            )
            self.wait(0.5)
            to_fade = VGroup(
                dot.copy(), z_label.copy(),
                dot_copy, arrow, fz_label,
            )
            dot.move_to(dot_copy)
            z_label.next_to(dot, UP, SMALL_BUFF)
            self.remove(z_label)
            self.play(
                *map(FadeOut, to_fade),
                FadeIn(z_label),
            )

        self.embed()



# ----- From _2021/holomorphic_dynamics.py -----

class AmbientRepetition(Scene):
    n_steps = 30
    # c = -0.6436875 + -0.441j
    c = -0.5436875 + -0.641j
    show_labels = True

    def construct(self):
        plane = ComplexPlane((-2, 2), (-2, 2))
        plane.set_height(6)
        plane.add_coordinate_labels(font_size=18)
        plane.to_corner(DR, buff=SMALL_BUFF)
        self.add(plane)

        font_size = 30

        z0 = complex(0, 0)
        dot = Dot(color=BLUE)
        dot.move_to(plane.n2p(z0))
        z_label = OldTex("z", font_size=font_size)
        z_label.set_stroke(BLACK, 5, background=True)
        z_label.next_to(dot, UP, SMALL_BUFF)
        if not self.show_labels:
            z_label.set_opacity(0)
        self.add(dot, z_label)

        self.add(TracedPath(dot.get_center, stroke_width=1))

        func = self.func

        def get_new_point():
            z = plane.p2n(dot.get_center())
            return plane.n2p(func(z))

        for n in range(self.n_steps):
            new_point = get_new_point()
            # CHANGE: the orbit escapes to infinity; it stops when it leaves the screen (huge points give NaN/overflow)
            if np.linalg.norm(new_point) > 100:
                break
            arrow = Arrow(dot.get_center(), new_point, buff=dot.get_height() / 2)

            dot_copy = dot.copy()
            dot_copy.move_to(new_point)
            dot_copy.set_color(YELLOW)
            fz_label = OldTex("f(z)", font_size=font_size)
            fz_label.set_stroke(BLACK, 8, background=True)
            fz_label.next_to(dot_copy, normalize(new_point - dot.get_center()), buff=0)
            if not self.show_labels:
                fz_label.set_opacity(0)

            self.add(dot, dot_copy, arrow, z_label)
            self.play(
                ShowCreation(arrow),
                TransformFromCopy(dot, dot_copy),
                FadeInFromPoint(fz_label, z_label.get_center()),
            )
            self.wait(0.5)
            to_fade = VGroup(
                dot.copy(), z_label.copy(),
                dot_copy, arrow, fz_label,
            )
            dot.move_to(dot_copy)
            z_label.next_to(dot, UP, SMALL_BUFF)
            self.remove(z_label)
            self.play(
                *map(FadeOut, to_fade),
                FadeIn(z_label),
            )

    def func(self, z):
        return 2 * ((z / 2)**2 + self.c)
