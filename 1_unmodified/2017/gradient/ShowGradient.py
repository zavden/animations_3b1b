# ==============================================================================
# Scene:      ShowGradient
# Source:     videos/_2017/gradient.py (lines 118-161)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ShowGradient.py ShowGradient -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ShowGradient(Scene):
    def construct(self):
        lhs = OldTex(
            "\\nabla f(x, y)=",
            tex_to_color_map={"x": BLUE, "y": RED}
        )
        vector = Matrix([
            ["\\partial f / \\partial x"],
            ["\\partial f / \\partial y"],
        ], v_buff=1)
        gradient = VGroup(lhs, vector)
        gradient.arrange(RIGHT, buff=SMALL_BUFF)
        gradient.scale(1.5)

        del_x, del_y = partials = vector.get_entries()
        background_rects = VGroup()
        for partial, color in zip(partials, [BLUE, RED]):
            partial[-1].set_color(color)
            partial.rect = SurroundingRectangle(
                partial, buff=MED_SMALL_BUFF
            )
            partial.rect.set_stroke(width=0)
            partial.rect.set_fill(color=color, opacity=0.5)
            background_rects.add(partial.rect.copy())
        background_rects.set_fill(opacity=0.1)

        partials.set_fill(opacity=0)

        self.play(
            LaggedStartMap(FadeIn, gradient),
            LaggedStartMap(
                FadeIn, background_rects,
                rate_func=squish_rate_func(smooth, 0.5, 1)
            )
        )
        self.wait()
        for partial in partials:
            self.play(DrawBorderThenFill(partial.rect))
            self.wait()
            self.play(FadeOut(partial.rect))
        self.wait()
        for partial in partials:
            self.play(Write(partial))
            self.wait()
