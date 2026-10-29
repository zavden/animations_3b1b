# ==============================================================================
# Scene:      IveSeenThis
# Source:     videos/_2021/holomorphic_dynamics.py (lines 694-732)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl IveSeenThis.py IveSeenThis -w -m --fps 15
#
# Placeholder assets (not Grant's originals):
#   - _lib/assets/raster_images/Mandelbrot_boundary.png (outline of the Mandelbrot set computed with numpy; generator _lib/assets/generated/2021/newton_fractal/make_newton_fractal_assets.py)
# ==============================================================================

from manim_imports_ext import *

class IveSeenThis(TeacherStudentsScene):
    def construct(self):
        equation = OldTex("f(z) = z^2 + c")
        equation.to_edge(UP)
        self.add(equation)

        mandelbrot_outline = ImageMobject("Mandelbrot_boundary")
        mandelbrot_outline.set_height(3)
        mandelbrot_outline.move_to(self.students[2].get_corner(UR))
        mandelbrot_outline.shift(1.2 * UP)

        self.student_says(
            "I've seen this one",
            target_mode="surprised",
            look_at=equation,
            added_anims=[
                self.students[0].change("tease", equation),
                self.students[1].change("happy", equation),
                self.teacher.change("happy", equation),
            ]
        )
        self.play(self.teacher.change("tease"))
        self.wait(2)
        self.add(mandelbrot_outline, *self.mobjects)
        self.play(
            FadeOut(self.background),
            RemovePiCreatureBubble(
                self.students[2],
                target_mode="raise_right_hand",
                look_at=mandelbrot_outline,
            ),
            FadeIn(mandelbrot_outline, 0.5 * UP, scale=2),
            self.students[0].change("pondering", mandelbrot_outline),
            self.students[1].change("thinking", mandelbrot_outline),
            self.teacher.change("happy", self.students[2].eyes),
        )
        self.wait(4)

        self.embed()
