# ==============================================================================
# Scene:      ThisIsAVeryGeneralIdea
# Source:     videos/_2017/efvgt.py (lines 1157-1218)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ThisIsAVeryGeneralIdea.py ThisIsAVeryGeneralIdea -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

ADDER_COLOR = GREEN


MULTIPLIER_COLOR = YELLOW


class ThisIsAVeryGeneralIdea(Scene):
    def construct(self):
        groups = OldTexText("Groups")
        groups.to_edge(UP)
        groups.set_color(BLUE)

        examples = VGroup(*list(map(TexText, [
            "Square matrices \\\\ \\small (Where $\\det(M) \\ne 0$)",
            "Molecular \\\\ symmetry",
            "Cryptography",
            "Numbers",
        ])))
        numbers = examples[-1]
        examples.arrange(buff = LARGE_BUFF)
        examples.set_width(FRAME_WIDTH-1)
        examples.move_to(UP)

        lines = VGroup(*[
            Line(groups.get_bottom(), ex.get_top(), buff = MED_SMALL_BUFF)
            for ex in examples
        ])
        lines.set_color(groups.get_color())

        self.add(groups)

        for example, line in zip(examples, lines):
            self.play(
                ShowCreation(line),
                Write(example, run_time = 2)
            )
        self.wait()
        self.play(
            VGroup(*examples[:-1]).fade, 0.7,
            VGroup(*lines[:-1]).fade, 0.7,
        )

        self.play(
            numbers.scale, 1.2, numbers.get_corner(UP+RIGHT),
        )
        self.wait(2)

        sub_categories = VGroup(*list(map(TexText, [
            "Numbers \\\\ (Additive)",
            "Numbers \\\\ (Multiplicative)",
        ])))
        sub_categories.arrange(RIGHT, buff = MED_LARGE_BUFF)
        sub_categories.next_to(numbers, DOWN, 1.5*LARGE_BUFF)
        sub_categories.to_edge(RIGHT)
        sub_categories[0].set_color(ADDER_COLOR)
        sub_categories[1].set_color(MULTIPLIER_COLOR)

        sub_lines = VGroup(*[
            Line(numbers.get_bottom(), sc.get_top(), buff = MED_SMALL_BUFF)
            for sc in sub_categories
        ])
        sub_lines.set_color(numbers.get_color())

        self.play(*it.chain(
            list(map(ShowCreation, sub_lines)),
            list(map(Write, sub_categories))
        ))
        self.wait()
