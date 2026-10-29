# ==============================================================================
# Scene:      ConservationLawSummary
# Source:     videos/_2019/clacks/solution1.py (lines 2888-2949)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ConservationLawSummary.py ConservationLawSummary -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ConservationLawSummary(Scene):
    def construct(self):
        energy_eq = OldTex(
            "\\frac{1}{2}", "m_1", "(", "v_1", ")", "^2", "+",
            "\\frac{1}{2}", "m_2", "(", "v_2", ")", "^2", "=",
            "\\text{const.}",
        )
        energy_word = OldTexText("Energy")
        energy_word.scale(2)
        circle = Circle(color=YELLOW, radius=2)
        energy_group = VGroup(energy_word, energy_eq, circle)
        momentum_eq = OldTex(
            "m_1", "v_1", "+", "m_2", "v_2", "=",
            "\\text{const.}",
        )
        momentum_word = OldTexText("Momentum")
        momentum_word.scale(2)
        line = Line(ORIGIN, RIGHT + np.sqrt(10) * DOWN)
        line.set_color(GREEN)
        momentum_group = VGroup(momentum_word, momentum_eq, line)

        equations = VGroup(energy_eq, momentum_eq)
        words = VGroup(energy_word, momentum_word)

        for equation in equations:
            equation.set_color_by_tex("m_", BLUE)
            equation.set_color_by_tex("v_", RED)

        words.arrange(
            DOWN, buff=3,
        )
        words.to_edge(LEFT, buff=1.5)

        for group in energy_group, momentum_group:
            arrow = Arrow(
                LEFT, 2 * RIGHT,
                rectangular_stem_width=0.1,
                tip_length=0.5,
                color=WHITE
            )
            arrow.next_to(group[0], RIGHT)
            group[1].next_to(group[0], DOWN)
            group[2].next_to(arrow, RIGHT)
            group[2].set_stroke(width=6)
            group.add(arrow)
        # line.scale(4, about_edge=DR)
        red_energy_word = energy_word.copy()
        red_energy_word.set_fill(opacity=0)
        red_energy_word.set_stroke(RED, 2)

        self.add(energy_group, momentum_group)
        self.wait()
        self.play(
            LaggedStartMap(
                ShowCreationThenDestruction,
                red_energy_word
            ),
        )
        for color in [RED, BLUE, PINK, YELLOW]:
            self.play(ShowCreation(
                circle.copy().set_color(color),
            ))
