# ==============================================================================
# Scene:      JulietChidingRomeo
# Source:     videos/_2021/matrix_exp.py (lines 4896-4919)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl JulietChidingRomeo.py JulietChidingRomeo -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class JulietChidingRomeo(Scene):
    def construct(self):
        juliet = PiCreature(color=BLUE_B)
        romeo = PiCreature(color=BLUE_D)
        romeo.flip()
        pis = VGroup(juliet, romeo)
        pis.set_height(2)
        pis.arrange(RIGHT, buff=LARGE_BUFF)
        pis.to_edge(DOWN)
        romeo.make_eye_contact(juliet)

        self.add(pis)
        self.play(
            PiCreatureSays(
                juliet, OldTexText("It just seems like \\\\ your feelings aren't \\\\ real"),
                bubble_config={"height": 2.5, "width": 3.5},
                target_mode="sassy",
            ),
            romeo.change("guilty"),
        )
        for x in range(2):
            self.play(Blink(juliet))
            self.play(Blink(romeo))
            self.wait()
