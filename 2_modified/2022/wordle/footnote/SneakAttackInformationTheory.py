# ==============================================================================
# Scene:      SneakAttackInformationTheory
# Source:     videos/_2022/wordle/footnote.py (lines 430-480)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl SneakAttackInformationTheory.py SneakAttackInformationTheory -w -m --fps 15
#
# Placeholder assets (not Grant's originals):
#   - _lib/assets/raster_images/wordle-phone.png and svg_images/wordle-phone.svg (placeholder phone; generator 2022/wordle/make_wordle_assets.py)
# ==============================================================================

from manim_imports_ext import *

class SneakAttackInformationTheory(Scene):
    def construct(self):
        randy = Randolph()
        randy.to_edge(DOWN)
        phone = ImageMobject("wordle-phone")
        phone.set_height(4)
        phone.next_to(randy, RIGHT)
        phone.shift(UP)
        phone_outline = SVGMobject("wordle-phone")
        phone_outline.set_fill(opacity=0)
        phone_outline.set_stroke(width=0)
        phone_outline.replace(phone).scale(0.8)

        self.play(
            randy.change("thinking", phone),
            FadeIn(phone),
            Write(phone_outline, stroke_width=1, run_time=2),
        )
        self.play(Blink(randy))
        self.wait()

        # surprise
        words = VGroup(
            Text("Surprise!"),
            Text("Information theory!"),
        )
        words.scale(1.25)
        words.arrange(DOWN)
        words.to_corner(UL)
        ent_formula = OldTex("H = \\sum_{x} -p(x)\\log_2\\big(p(x)\\right)")
        ent_formula.set_color(TEAL)
        ent_formula.next_to(words, DOWN, LARGE_BUFF)

        self.play(
            FadeIn(words[0], scale=2),
            randy.change("horrified", words),
            run_time=0.5
        )
        self.play(
            FadeIn(words[1], scale=2),
            run_time=0.5,
        )
        self.play(Blink(randy))
        self.play(
            Write(ent_formula),
            randy.change("erm", ent_formula),
        )
        self.play(Blink(randy))
        self.wait(2)
        self.play(Blink(randy))
        self.wait(2)
