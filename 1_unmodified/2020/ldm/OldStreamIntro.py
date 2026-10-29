# ==============================================================================
# Scene:      OldStreamIntro
# Source:     videos/_2020/ldm.py (lines 39-69)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl OldStreamIntro.py OldStreamIntro -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class OldStreamIntro(Scene):
    def construct(self):
        morty = Mortimer()
        morty.flip()
        morty.set_height(2)
        morty.to_corner(DL)
        self.play(PiCreatureSays(
            morty, "The lesson will\\\\begin soon.",
            bubble_config={
                "height": 2,
                "width": 3,
            },
            target_mode="hooray",
        ))
        bound = AnimatedBoundary(morty.bubble.content, max_stroke_width=1)
        self.add(bound, morty.bubble, morty.bubble.content)
        self.remove(morty.bubble.content)
        morty.bubble.set_fill(opacity=0)

        self.camera.frame.scale(0.6, about_edge=DL)

        self.play(Blink(morty))
        self.wait(5)
        self.play(Blink(morty))
        self.wait(3)
        return

        text = OldTexText("The lesson will\\\\begin soon.")
        text.set_height(1.5)
        text.to_corner(DL, buff=LARGE_BUFF)
        self.add(text)
