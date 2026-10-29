# ==============================================================================
# Scene:      SudokuBruteForce
# Source:     videos/_2025/grover/clarification.py (lines 1337-1377)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl SudokuBruteForce.py SudokuBruteForce -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class SudokuBruteForce(InteractiveScene):
    def construct(self):
        # Test
        words = Text("Comically inefficient\nbrute force approach:")
        steps = TexText("$9^{60}$ Steps", isolate=["60"])
        steps.scale(1.5)
        group = VGroup(words, steps)
        group.arrange(RIGHT, buff=MED_LARGE_BUFF)
        group.to_edge(UP)

        brace = Brace(steps[:3], DOWN)
        number = Tex("{:,d}".format(9**60).replace(",", "{,}"))
        number.scale(0.75)
        number.set_color(RED)
        number.next_to(brace, DOWN).shift_onto_screen()

        self.add(group)
        self.play(
            GrowFromCenter(brace),
            FadeIn(number, lag_ratio=0.1)
        )
        self.wait()

        # Show Grover
        grover_words = TexText("Using Grover's Algorithm:")
        grover_words.move_to(words, RIGHT)
        grover_steps = TexText(R"$\displaystyle \left\lceil\frac{\pi}{4} 9^{30}\right\rceil$ Steps", isolate=["30"])
        grover_steps.move_to(steps, LEFT)
        new_brace = Brace(grover_steps[:8], DOWN)
        new_number = Tex("{:,d}".format(int(np.ceil(9**30 * PI / 4))).replace(",", "{,}"))
        new_number.scale(0.75)
        new_number.set_color(RED)
        new_number.next_to(new_brace, DOWN)

        self.play(
            FadeTransformPieces(words, grover_words),
            FadeTransform(steps, grover_steps),
            Transform(brace, new_brace),
            FadeTransformPieces(number, new_number),
        )
        self.wait()
