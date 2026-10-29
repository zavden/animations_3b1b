# ==============================================================================
# Scene:      ImagineProving
# Source:     videos/_2023/clt_proof/main.py (lines 14-52)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ImagineProving.py ImagineProving -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ImagineProving(InteractiveScene):
    def construct(self):
        self.add(FullScreenRectangle())
        screen = ScreenRectangle()
        screen.set_height(0.70 * FRAME_HEIGHT)
        screen.to_edge(DOWN)
        screen.set_stroke(GREY_A, 1)
        self.add(screen)

        # Randy
        randy = Randolph(height=1.5)
        randy.next_to(screen, UP, aligned_edge=LEFT)
        words = Text("""
            Imagine yourself proving
            the central limit theorem
        """)
        yourself = words["Imagine yourself"][0]
        words["central limit theorem"].set_color(YELLOW)
        words.next_to(randy, RIGHT, buff=1.5)
        arrow = Arrow(words, randy)

        yourself.save_state()
        yourself.match_y(words)

        self.play(
            Write(yourself),
            ShowCreation(arrow),
            randy.change("pondering", screen)
        )
        self.play(Blink(randy))
        self.wait()
        self.play(
            Restore(yourself),
            Write(words[len(yourself):]),
            randy.change("thinking"),
        )
        for x in range(2):
            self.play(Blink(randy))
            self.wait(2)
