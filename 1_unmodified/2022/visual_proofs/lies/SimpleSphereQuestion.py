# ==============================================================================
# Scene:      SimpleSphereQuestion
# Source:     videos/_2022/visual_proofs/lies.py (lines 134-159)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl SimpleSphereQuestion.py SimpleSphereQuestion -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class SimpleSphereQuestion(InteractiveScene):
    def construct(self):
        # Intro statement
        text = OldTexText("A ``proof'' of a formula for\\\\the surface area of a sphere")
        text.set_stroke(WHITE, 0)

        rect = Rectangle(width=TAU, height=TAU / 4)
        rect.set_stroke(width=0)
        rect.set_fill(GREY_E, 1)
        rect.set_width(FRAME_WIDTH)
        self.add(rect)

        morty = Mortimer(height=1.5)
        randy = Randolph(height=1.5)
        morty.next_to(text, RIGHT)
        randy.next_to(text, LEFT)
        VGroup(morty, randy).align_to(rect, DOWN).shift(0.1 * UP)
        self.add(morty, randy)

        self.play(
            Write(text),
            morty.change("raise_right_hand", text),
            randy.change("thinking", text)
        )
        self.play(Blink(morty))
        self.wait()
