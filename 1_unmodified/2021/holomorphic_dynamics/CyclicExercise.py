# ==============================================================================
# Scene:      CyclicExercise
# Source:     videos/_2021/holomorphic_dynamics.py (lines 2257-2284)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl CyclicExercise.py CyclicExercise -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class CyclicExercise(Scene):
    def construct(self):
        words = OldTexText(
            "Exercise 2: If $f(z) = z - {z^3 - 2z + 2 \\over 3z^2 - 2}$,\\\\",
            "and $g(z) = f(f(z))$, confirm that $|g'(0)| < 1$."
        )
        words[1].shift(SMALL_BUFF * DOWN)
        box = SurroundingRectangle(words, buff=0.45)
        box.set_stroke(WHITE, 2)
        box.set_fill(BLACK, 1)
        group = VGroup(box, words)
        group.to_edge(UP, buff=0)

        hint = OldTexText(
            "Hint: Don't expand out $g(z)$. Use\\\\",
            "the chain rule: $g'(0) = f'(f(0))f'(0)$"
        )
        hint.scale(0.8)
        hint.set_color(GREY_A)
        hint_box = SurroundingRectangle(hint, buff=0.25)
        hint_box.match_style(box)
        hint_group = VGroup(hint_box, hint)
        hint_group.next_to(group, DOWN, buff=0)

        self.add(group)
        self.wait(2)
        self.play(FadeIn(hint_group))
        self.wait()
