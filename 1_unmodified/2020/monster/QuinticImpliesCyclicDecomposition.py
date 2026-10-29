# ==============================================================================
# Scene:      QuinticImpliesCyclicDecomposition
# Source:     videos/_2020/monster.py (lines 3410-3515)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl QuinticImpliesCyclicDecomposition.py QuinticImpliesCyclicDecomposition -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class QuinticImpliesCyclicDecomposition(Scene):
    def construct(self):
        # Title
        title = OldTexText("Quintic formula")
        title.scale(1.5)
        title.to_edge(UP)
        details = OldTexText(
            "Solve ",
            "$a_5 x^5 + a_4 x^4 + a_3 x^3 + a_2 x^2 + a_1 x + a_0$\\\\",
            " using only ",
            "+, -, $\\times$, $/$, and $\\sqrt[n]{\\quad}$"
        )
        details[1].set_color(BLUE)
        details[3].set_color(TEAL)
        details.match_width(title)
        details.scale(1.2)
        details.next_to(title, DOWN)

        self.clear()
        self.add(title)
        self.wait()
        self.play(FadeIn(details, 0.5 * UP))
        self.wait()

        full_title = VGroup(title, details)

        # Show Implication
        implies = OldTex("\\Downarrow").scale(2)
        implies.next_to(details, DOWN, LARGE_BUFF)

        s5 = OldTex("S_5")
        prime_children = VGroup(
            OldTex("C_{p_1}"),
            OldTex("C_{p_2}"),
            OldTex("\\vdots"),
            OldTex("C_{p_n}"),
        )
        prime_children.set_color(RED_B)

        real_children = VGroup(
            OldTex("A_5"),
            OldTex("C_2"),
        )
        real_children.set_color(GREEN)

        for children, buff in (prime_children, MED_LARGE_BUFF), (real_children, LARGE_BUFF):
            children.arrange(DOWN, buff=buff, aligned_edge=LEFT)
            children.next_to(s5, RIGHT, buff=0.5 + 0.25 * len(children))
            children.lines = VGroup()
            for child in children:
                children.lines.add(
                    Line(s5.get_right(), child.get_left(), buff=0.1)
                )
        prime_children[2].shift(SMALL_BUFF * RIGHT)

        VGroup(
            s5, prime_children.lines, prime_children,
            real_children.lines, real_children,
        ).next_to(implies, DOWN)

        # Show decomps
        implies.save_state()
        implies.stretch(0, 1, about_edge=UP)
        self.play(
            Restore(implies),
            GrowFromPoint(s5, implies.get_top()),
        )
        self.play(
            LaggedStartMap(ShowCreation, prime_children.lines, lag_ratio=0.3),
            LaggedStartMap(
                FadeIn, prime_children,
                lambda m: (m, s5.get_right() - m.get_center()),
                lag_ratio=0.3,
            )
        )
        self.wait()
        self.play(
            FadeOut(prime_children, RIGHT),
            *[
                ApplyMethod(line.scale, 0, {"about_point": line.get_end()}, remover=True)
                for line in prime_children.lines
            ],
            LaggedStartMap(ShowCreation, real_children.lines, lag_ratio=0.3),
            LaggedStartMap(
                FadeIn, real_children,
                lambda m: (m, s5.get_right() - m.get_center()),
                lag_ratio=0.3,
            )
        )
        self.play(ShowCreationThenFadeAround(real_children[0]))

        # Reverse implication
        title_rect = SurroundingRectangle(full_title)
        title_rect.set_stroke(RED, 2)
        not_exists = OldTexText("No\\\\such\\\\thing")
        not_exists.match_height(title_rect)
        not_exists.set_color(RED)
        not_exists.next_to(title_rect, LEFT)
        full_title.add(title_rect, not_exists)

        self.play(
            Rotate(implies, PI),
            VFadeIn(title_rect),
            VFadeIn(not_exists),
            full_title.shift, 0.5 * RIGHT,
        )
