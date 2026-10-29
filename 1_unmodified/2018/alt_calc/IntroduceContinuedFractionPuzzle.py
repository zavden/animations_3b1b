# ==============================================================================
# Scene:      IntroduceContinuedFractionPuzzle
# Source:     videos/_2018/alt_calc.py (lines 2027-2165)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl IntroduceContinuedFractionPuzzle.py IntroduceContinuedFractionPuzzle -w -m --fps 15
# ==============================================================================

 # -*- coding: utf-8 -*-
from manim_imports_ext import *

def get_nested_one_plus_one_over_x(n_terms, bottom_term="x"):
    tex = "1+ {1 \\over" * n_terms + bottom_term + "}" * n_terms
    return OldTex(tex, isolate=["1", "\\over", bottom_term])


def get_phi_continued_fraction(n_terms):
    return get_nested_one_plus_one_over_x(n_terms, bottom_term="1+\\cdots")


class IntroduceContinuedFractionPuzzle(PiCreatureScene):
    CONFIG = {
        "remove_initial_rhs": True,
    }

    def construct(self):
        self.ask_question()
        self.set_equal_to_x()

    def create_pi_creatures(self):
        morty = Mortimer(height=2)
        morty.to_corner(DR)

        friend = PiCreature(color=GREEN, height=2)
        friend.to_edge(DOWN)
        friend.shift(LEFT)

        group = VGroup(morty, friend)
        group.shift(2 * LEFT)

        return morty, friend

    def ask_question(self):
        morty, friend = self.pi_creatures
        frac = get_phi_continued_fraction(9)
        frac.scale(0.8)
        rhs = DecimalNumber(
            (1 - np.sqrt(5)) / 2.0,
            num_decimal_places=5,
            show_ellipsis=True,
        )
        rhs.set_color(YELLOW)
        equals = OldTex("=")
        equals.next_to(frac.get_part_by_tex("\\over"), RIGHT)
        rhs.next_to(equals, RIGHT)
        group = VGroup(frac, equals, rhs)
        group.scale(1.5)
        group.to_corner(UR)

        self.play(
            LaggedStartMap(
                Write, frac,
                run_time=15,
                lag_ratio=0.15,
            ),
            FadeInFromDown(equals),
            FadeInFromDown(rhs),
            PiCreatureSays(
                friend, "Would this be valid? \\\\ If not, why not?",
                target_mode="confused",
                look_at=frac,
                bubble_config={
                    "direction": RIGHT,
                    "width": 4,
                    "height": 3,
                }
            ),
            morty.change, "pondering",
        )
        self.wait()

        anims = [
            RemovePiCreatureBubble(
                friend, target_mode="pondering",
                look_at=frac
            ),
        ]
        if self.remove_initial_rhs:
            anims += [
                Animation(frac),
                FadeOut(equals),
                rhs.scale, 0.5,
                rhs.to_corner, DL,
            ]
        self.play(*anims)

        self.neg_one_over_phi = rhs
        self.equals = equals
        self.frac = frac

    def set_equal_to_x(self):
        frac = self.frac
        morty, friend = self.get_pi_creatures()

        inner_frac = frac[4:]
        inner_frac_rect = SurroundingRectangle(
            inner_frac, stroke_width=2, buff=0.5 * SMALL_BUFF
        )
        inner_frac_group = VGroup(inner_frac, inner_frac_rect)

        equals = OldTex("=")
        equals.next_to(frac[3], RIGHT)
        x, new_x = [Tex("x") for i in range(2)]
        xs = VGroup(x, new_x)
        xs.set_color(YELLOW)
        xs.scale(1.3)
        x.next_to(equals, RIGHT)
        new_x.next_to(frac[3], DOWN, 2 * SMALL_BUFF)

        fixed_point_words = VGroup(
            OldTexText("Fixed point of"),
            OldTex(
                "f(x) = 1 + \\frac{1}{x}",
                tex_to_color_map={"x": YELLOW}
            )
        )
        fixed_point_words.arrange(DOWN)

        self.play(Write(x), Write(equals))
        self.wait()
        self.play(ShowCreation(inner_frac_rect))
        self.wait()
        self.play(
            inner_frac_group.scale, 0.75,
            inner_frac_group.center,
            inner_frac_group.to_edge, LEFT,
            ReplacementTransform(
                x.copy(), new_x,
                path_arc=-90 * DEGREES
            )
        )
        self.wait()
        self.play(
            frac[3].stretch, 0.1, 0, {"about_edge": RIGHT},
            MaintainPositionRelativeTo(
                VGroup(frac[2], new_x), frac[3]
            ),
            UpdateFromFunc(
                frac[:2], lambda m: m.next_to(frac[3], LEFT)
            )
        )
        self.wait()
        fixed_point_words.next_to(VGroup(frac[0], xs), DOWN, LARGE_BUFF)
        self.play(
            Write(fixed_point_words),
            morty.change, "hooray",
            friend.change, "happy"
        )
        self.wait(3)
