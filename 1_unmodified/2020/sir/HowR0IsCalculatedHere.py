# ==============================================================================
# Scene:      HowR0IsCalculatedHere
# Source:     videos/_2020/sir.py (lines 2645-2690)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl HowR0IsCalculatedHere.py HowR0IsCalculatedHere -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class HowR0IsCalculatedHere(Scene):
    def construct(self):
        words = VGroup(
            OldTexText("Count ", "\\# transfers"),
            OldTexText("for every infectious case")
        )
        words.arrange(DOWN)
        words[1].set_color(RED)
        words.to_edge(UP)

        estimate = OldTexText("Estimate")
        estimate.move_to(words[0][0], RIGHT)

        lp, rp = parens = OldTex("(", ")")
        parens.match_height(words)
        lp.next_to(words, LEFT, SMALL_BUFF)
        rp.next_to(words, RIGHT, SMALL_BUFF)
        average = OldTexText("Average")
        average.scale(1.5)
        average.next_to(parens, LEFT, SMALL_BUFF)

        words.save_state()
        words[1].move_to(words[0])
        words[0].set_opacity(0)

        self.add(FullScreenFadeRectangle(fill_color=GREY_E, fill_opacity=1).scale(2))
        self.wait()
        self.play(Write(words[1], run_time=1))
        self.wait()
        self.add(words)
        self.play(Restore(words))
        self.wait()
        self.play(
            FadeOut(words[0][0], UP),
            FadeIn(estimate, DOWN),
        )
        self.wait()

        self.play(
            Write(parens),
            FadeIn(average, 0.5 * RIGHT),
            self.camera.frame.shift, LEFT,
        )
        self.wait()

        self.embed()
