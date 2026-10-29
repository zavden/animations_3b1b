# ==============================================================================
# Scene:      RepeatedApplicationWithNegativeSeed
# Source:     videos/_2018/alt_calc.py (lines 2525-2552)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl RepeatedApplicationWithNegativeSeed.py RepeatedApplicationWithNegativeSeed -w -m --fps 15
# ==============================================================================

 # -*- coding: utf-8 -*-
from manim_imports_ext import *

def get_nested_one_plus_one_over_x(n_terms, bottom_term="x"):
    tex = "1+ {1 \\over" * n_terms + bottom_term + "}" * n_terms
    return OldTex(tex, isolate=["1", "\\over", bottom_term])


def get_phi_continued_fraction(n_terms):
    return get_nested_one_plus_one_over_x(n_terms, bottom_term="1+\\cdots")


def get_nested_f(n_terms, arg="x"):
    terms = ["f("] * n_terms + [arg] + [")"] * n_terms
    return OldTex(*terms)


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


class ThinkAboutWithRepeatedApplication(IntroduceContinuedFractionPuzzle):
    CONFIG = {
        "remove_initial_rhs": False,
    }

    def construct(self):
        self.force_skipping()
        self.ask_question()
        self.revert_to_original_skipping_status()

        self.obviously_not()
        self.ask_about_fraction()
        self.plug_func_into_self()

    def obviously_not(self):
        morty, friend = self.get_pi_creatures()
        friend.change_mode("confused")
        randy = Randolph()
        randy.match_height(morty)
        randy.to_corner(DL)

        frac = self.frac
        rhs = self.neg_one_over_phi
        plusses = frac[1::4]
        plus_rects = VGroup(*[
            SurroundingRectangle(plus, buff=0) for plus in plusses
        ])
        plus_rects.set_color(PINK)

        self.play(FadeIn(randy))
        self.play(
            PiCreatureSays(
                randy, "Obviously not!",
                bubble_config={"width": 3, "height": 2},
                target_mode="angry",
                run_time=1,
            ),
            morty.change, "guilty",
            friend.change, "hesitant"
        )
        self.wait()
        self.play(
            Animation(frac),
            RemovePiCreatureBubble(randy, target_mode="sassy"),
            morty.change, "confused",
            friend.change, "confused",
        )
        self.play(LaggedStartMap(
            ShowCreationThenDestruction, plus_rects,
            run_time=2,
            lag_ratio=0.35,
        ))
        self.play(WiggleOutThenIn(rhs))
        self.wait(2)
        self.play(
            frac.scale, 0.7,
            frac.to_corner, UL,
            FadeOut(self.equals),
            rhs.scale, 0.5,
            rhs.center,
            rhs.to_edge, LEFT,
            FadeOut(randy),
            morty.change, "pondering",
            friend.change, "pondering",
        )

    def ask_about_fraction(self):
        frac = self.frac
        arrow = Vector(LEFT, color=RED)
        arrow.next_to(frac, RIGHT)
        question = OldTexText("What does this \\\\ actually mean?")
        question.set_color(RED)
        question.next_to(arrow, RIGHT)

        self.play(
            LaggedStartMap(FadeIn, question, run_time=1),
            GrowArrow(arrow),
            LaggedStartMap(
                ApplyMethod, frac,
                lambda m: (m.set_color, RED),
                rate_func=there_and_back,
                lag_ratio=0.2,
                run_time=2
            )
        )
        self.wait()
        self.play(FadeOut(question), FadeOut(arrow))

    def plug_func_into_self(self, value=1, value_str="1"):
        morty, friend = self.pi_creatures

        def func(x):
            return 1 + 1.0 / x

        lines = VGroup()
        value_labels = VGroup()
        for n_terms in range(5):
            lhs = get_nested_f(n_terms, arg="c")
            equals = OldTex("=")
            rhs = get_nested_one_plus_one_over_x(n_terms, bottom_term=value_str)
            equals.next_to(rhs[0], LEFT)
            lhs.next_to(equals, LEFT)
            lines.add(VGroup(lhs, equals, rhs))

            value_label = OldTex("= %.3f\\dots" % value)
            value = func(value)
            value_labels.add(value_label)

        lines.arrange(
            DOWN, buff=MED_LARGE_BUFF,
        )
        VGroup(lines, value_labels).scale(0.8)
        lines.to_corner(UR)
        buff = MED_LARGE_BUFF + MED_SMALL_BUFF + value_labels.get_width()
        lines.to_edge(RIGHT, buff=buff)
        for line, value_label in zip(lines, value_labels):
            value_label.move_to(line[1]).to_edge(RIGHT)

        top_line = lines[0]
        colors = [WHITE] + color_gradient([YELLOW, RED, PINK], len(lines) - 1)
        for n in range(1, len(lines)):
            color = colors[n]
            lines[n][0].set_color(color)
            lines[n][0][1:-1].match_style(lines[n - 1][0])
            lines[n][2].set_color(color)
            lines[n][2][4:].match_style(lines[n - 1][2])

        arrow = Vector(0.5 * DOWN, color=WHITE)
        arrow.next_to(value_labels[-1], DOWN)
        q_marks = OldTex("???")
        q_marks.next_to(arrow, DOWN)

        self.play(
            FadeInFromDown(top_line),
            FadeInFromDown(value_labels[0])
        )
        for n in range(1, len(lines)):
            new_line = lines[n]
            last_line = lines[n - 1]
            value_label = value_labels[n]
            mover, target = [
                VGroup(
                    line[0][0],
                    line[0][-1],
                    line[1],
                    line[2][:4],
                )
                for line in (lines[1], new_line)
            ]
            anims = [ReplacementTransform(
                mover.copy().fade(1), target, path_arc=30 * DEGREES
            )]
            if n == 4:
                morty.generate_target()
                morty.target.change("horrified")
                morty.target.shift(2.5 * DOWN)
                anims.append(MoveToTarget(morty, remover=True))
            self.play(*anims)
            self.wait()
            self.play(
                ReplacementTransform(
                    last_line[0].copy(), new_line[0][1:-1]
                ),
                ReplacementTransform(
                    last_line[2].copy(), new_line[2][4:]
                ),
            )
            self.play(FadeIn(value_label))
            self.wait()
        self.play(
            GrowArrow(arrow),
            Write(q_marks),
            friend.change, "confused"
        )
        self.wait(3)

        self.top_line = VGroup(lines[0], value_labels[0])


class RepeatedApplicationWithPhiBro(ThinkAboutWithRepeatedApplication):
    CONFIG = {
        "value": (1 - np.sqrt(5)) / 2,
        "value_str": "-1/\\varphi",
    }

    def construct(self):
        self.force_skipping()
        self.ask_question()
        self.obviously_not()
        self.revert_to_original_skipping_status()

        self.plug_func_into_self(
            value=self.value,
            value_str=self.value_str
        )


class RepeatedApplicationWithNegativeSeed(RepeatedApplicationWithPhiBro, MovingCameraScene):
    CONFIG = {
        "value": -0.65,
        "value_str": "-0.65"
    }

    def setup(self):
        MovingCameraScene.setup(self)
        RepeatedApplicationWithPhiBro.setup(self)

    def construct(self):
        RepeatedApplicationWithPhiBro.construct(self)

        rect = SurroundingRectangle(self.top_line)
        question = OldTexText("What about a negative seed?")
        question.match_color(rect)
        question.next_to(rect, UP)
        self.play(ShowCreation(rect))
        self.play(
            Write(question),
            self.camera.frame.set_height, FRAME_HEIGHT + 1.5
        )
        self.wait()
        self.play(
            FadeOut(question),
            FadeOut(rect),
            self.camera.frame.set_height, FRAME_HEIGHT
        )
