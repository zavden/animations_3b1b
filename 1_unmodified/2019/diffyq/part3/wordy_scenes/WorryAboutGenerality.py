# ==============================================================================
# Scene:      WorryAboutGenerality
# Source:     videos/_2019/diffyq/part3/wordy_scenes.py (lines 862-919)
# Category:   1 · Renders unmodified
# Includes code copied from: _2019/diffyq/part2/wordy_scenes.py
#
# Run from this folder:
#     manimgl WorryAboutGenerality.py WorryAboutGenerality -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *


# ----- From _2019/diffyq/part2/wordy_scenes.py -----

class WriteHeatEquationTemplate(Scene):
    CONFIG = {
        "tex_mobject_config": {
            "tex_to_color_map": {
                "{T}": WHITE,
                "{t}": YELLOW,
                "{x}": GREEN,
                "{y}": RED,
                "{z}": BLUE,
                "\\partial": WHITE,
                "2": WHITE,
            },
        },
    }

    def get_d1_equation(self):
        return OldTex(
            "{\\partial {T} \\over \\partial {t}}({x}, {t})", "=",
            "\\alpha \\cdot",
            "{\\partial^2 {T} \\over \\partial {x}^2} ({x}, {t})",
            **self.tex_mobject_config
        )

    def get_d1_equation_without_inputs(self):
        return OldTex(
            "{\\partial {T} \\over \\partial {t}}", "=",
            "\\alpha \\cdot",
            "{\\partial^2 {T} \\over \\partial {x}^2}",
            **self.tex_mobject_config
        )

    def get_d3_equation(self):
        return OldTex(
            "{\\partial {T} \\over \\partial {t}}", "=",
            "\\alpha \\left(",
            "{\\partial^2 {T} \\over \\partial {x}^2} + ",
            "{\\partial^2 {T} \\over \\partial {y}^2} + ",
            "{\\partial^2 {T} \\over \\partial {z}^2}",
            "\\right)",
            **self.tex_mobject_config
        )

    def get_general_equation(self):
        return OldTex(
            "{\\partial {T} \\over \\partial {t}}", "=",
            "\\alpha", "\\nabla^2 {T}",
            **self.tex_mobject_config,
        )

    def get_d3_equation_with_inputs(self):
        return OldTex(
            "{\\partial {T} \\over \\partial {t}}",
            "({x}, {y}, {z}, {t})", "=",
            "\\alpha \\left(",
            "{\\partial^2 {T} \\over \\partial {x}^2}",
            "({x}, {y}, {z}, {t}) + ",
            "{\\partial^2 {T} \\over \\partial {y}^2}",
            "({x}, {y}, {z}, {t}) + ",
            "{\\partial^2 {T} \\over \\partial {z}^2}",
            "({x}, {y}, {z}, {t})",
            "\\right)",
            **self.tex_mobject_config
        )

    def get_d1_words(self):
        return OldTexText("Heat equation\\\\", "(1 dimension)")

    def get_d3_words(self):
        return OldTexText("Heat equation\\\\", "(3 dimensions)")

    def get_d1_group(self):
        group = VGroup(
            self.get_d1_words(),
            self.get_d1_equation(),
        )
        group.arrange(DOWN, buff=MED_LARGE_BUFF)
        return group

    def get_d3_group(self):
        group = VGroup(
            self.get_d3_words(),
            self.get_d3_equation(),
        )
        group.arrange(DOWN, buff=MED_LARGE_BUFF)
        return group



# ----- From _2019/diffyq/part3/wordy_scenes.py -----

class WorryAboutGenerality(TeacherStudentsScene, WriteHeatEquationTemplate):
    def construct(self):
        eq = self.get_d1_equation()
        diffyq = self.get_diffyq_set()
        is_in = OldTex("\\in")
        is_in.scale(2)

        group = VGroup(eq, is_in, diffyq)
        group.arrange(RIGHT, buff=MED_LARGE_BUFF)
        group.to_edge(UP)

        arrow = Vector(DOWN)
        arrow.set_stroke(WHITE, 5)
        arrow.next_to(eq, DOWN)
        themes = OldTexText("Frequent themes")
        themes.scale(1.5)
        themes.next_to(arrow, DOWN)

        self.play(
            self.change_students(
                "sad", "tired", "pleading"
            ),
            self.teacher.change, "raise_right_hand",
            FadeInFromDown(eq)
        )
        self.play(Write(group[1:]))
        self.wait(2)
        self.play(
            ShowCreation(arrow),
            self.change_students(*3 * ["pondering"]),
        )
        self.play(
            FadeIn(themes, UP),
            self.change_students(*3 * ["thinking"]),
            self.teacher.change, "happy"
        )
        self.wait(4)


    # def get_d1_equation(self):
    #     result = super().get_d1_equation()
    #     lp, rp = parens = OldTex("(", ")")
    #     parens.match_height(result)
    #     lp.next_to(result, LEFT, SMALL_BUFF)
    #     rp.next_to(result, RIGHT, SMALL_BUFF)
    #     result.add_to_back(lp)
    #     result.add(rp)
    #     return result

    def get_diffyq_set(self):
        words = OldTexText(
            "Differential\\\\equations"
        )
        words.scale(1.5)
        words.set_color(BLUE)
        lb = Brace(words, LEFT)
        rb = Brace(words, RIGHT)
        return VGroup(lb, words, rb)
