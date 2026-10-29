# ==============================================================================
# Scene:      SoME1Name
# Source:     videos/_2021/some1.py (lines 54-84)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl SoME1Name.py SoME1Name -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - The new Text does not create submobjects for spaces; without the +1 the indices only run over the letters
# ==============================================================================

from manim_imports_ext import *

def get_tripple_underline(mobject, buff=0.1):
    ul1 = Underline(mobject, buff=buff).set_stroke(BLUE_C, 3)
    ul2 = Underline(ul1).scale(0.9).set_stroke(BLUE_D, 2)
    ul3 = Underline(ul2).scale(0.9).set_stroke(BLUE_E, 1)
    return VGroup(ul1, ul2, ul3)


class SoME1Name(Scene):
    def construct(self):
        strings = ["Summer", "of", "Math", "Exposition", "#1"]
        # CHANGE: the new Text does not create submobjects for spaces; without the +1 the indices only run over the letters
        lens = list(map(lambda s: len(s), strings))
        indices = [0, *np.cumsum(lens)]
        phrase = Text(" ".join(strings))
        phrase.set_width(12)
        words = VGroup()
        for i1, i2 in zip(indices, indices[1:]):
            words.add(phrase[i1:i2])

        acronym = VGroup(*(word[0].copy() for word in words[:-1]))
        acronym.add(words[-1][-1].copy())
        acronym.generate_target()
        acronym.target.arrange(RIGHT, buff=SMALL_BUFF, aligned_edge=DOWN)
        acronym.target.move_to(DOWN)

        self.play(LaggedStartMap(FadeIn, words, lag_ratio=0.5, run_time=1))
        self.wait()
        self.play(
            # FadeOut(phrase),
            phrase.animate.move_to(UP),
            MoveToTarget(acronym)
        )
        self.wait()

        self.play(
            ShowCreation(get_tripple_underline(words[2])),
            words[2].animate.set_color(BLUE_B),
        )
        self.wait()
