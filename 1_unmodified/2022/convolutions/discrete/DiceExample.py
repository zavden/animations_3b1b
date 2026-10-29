# ==============================================================================
# Scene:      DiceExample
# Source:     videos/_2022/convolutions/discrete.py (lines 348-782)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl DiceExample.py DiceExample -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

def get_die_faces(**kwargs):
    result = VGroup(*(DieFace(n, **kwargs) for n in range(1, 7)))
    result.arrange(RIGHT, buff=MED_LARGE_BUFF)
    return result


def get_aligned_pairs(group1, group2, n):
    return VGroup(*(
        VGroup(m1, m2)
        for m1 in group1
        for m2 in group2
        if m1.index + m2.index == n
    ))


def get_pair_rects(pairs, together=True, buff=SMALL_BUFF, corner_radius=0.1):
    if together:
        return VGroup(*(
            SurroundingRectangle(pair, buff=buff).round_corners(corner_radius)
            for pair in pairs
        ))
    else:
        return VGroup(*(
            VGroup(*(
                SurroundingRectangle(m, buff=buff).round_corners(corner_radius)
                for m in pair
            ))
            for pair in pairs
        ))


def get_row_shift(top_row, low_row, n):
    min_index = low_row[0].index
    max_index = top_row[-1].index
    max_sum = min_index + max_index
    if n <= max_sum:
        x_shift = top_row[n - 2 * min_index].get_x() - low_row[0].get_x()
    else:
        x_shift = top_row[-1].get_x() - low_row[n - max_sum].get_x()
    return low_row.animate.shift(x_shift * RIGHT)


class DiceExample(InteractiveScene):
    def construct(self):
        # Start showing grid
        blue_dice = get_die_faces(fill_color=BLUE_E, dot_color=WHITE)
        red_dice = get_die_faces(fill_color=RED_E, dot_color=WHITE)
        VGroup(blue_dice, red_dice).arrange(DOWN, buff=LARGE_BUFF)
        grid = Square().get_grid(6, 6, buff=0)
        grid.set_height(6)
        grid.to_edge(LEFT, buff=2.0)
        grid.shift(0.5 * DOWN)
        grid.set_stroke(WHITE, 1)

        blue_dice.save_state()
        red_dice.save_state()

        self.play(LaggedStart(
            FadeIn(blue_dice, lag_ratio=0.1, shift=0.25 * UP, run_time=2, rate_func=overshoot),
            FadeIn(red_dice, lag_ratio=0.1, shift=0.25 * UP, run_time=2, rate_func=overshoot),
            lag_ratio=0.2
        ))
        self.wait()
        self.play(
            Write(grid, run_time=2, stroke_color=YELLOW, stroke_width=4),
            *(
                die.animate.set_width(0.6 * square.get_width()).next_to(square, UP, SMALL_BUFF)
                for die, square in zip(blue_dice, grid[:6])
            ),
            *(
                die.animate.set_width(0.6 * square.get_width()).next_to(square, LEFT, SMALL_BUFF)
                for die, square in zip(red_dice, grid[0::6])
            ),
        )

        # Add all mini dice
        mini_dice = VGroup()
        for n, square in enumerate(grid):
            j, i = n // 6, n % 6
            blue = blue_dice[i].copy()
            red = red_dice[j].copy()
            blue.sum = i + j + 2
            red.sum = i + j + 2
            blue.generate_target()
            red.generate_target()
            group = VGroup(blue.target, red.target)
            group.set_stroke(width=1)
            group.arrange(RIGHT, buff=SMALL_BUFF)
            group.set_width(square.get_width() * 0.8)
            group.move_to(square)
            mini_dice.add(blue, red)

        combinations_label = VGroup(
            OldTex("6^2 = "), Integer(36), Text("Combinations")
        )
        combinations_label.arrange(RIGHT, aligned_edge=DOWN)
        combinations_label.to_edge(RIGHT)

        self.play(
            LaggedStartMap(MoveToTarget, mini_dice, lag_ratio=0.02, run_time=2),
            FadeIn(combinations_label[0]),
            CountInFrom(combinations_label[1], 1, run_time=2),
            VFadeIn(combinations_label[1]),
            FadeIn(combinations_label[2], 0),
        )
        self.wait()

        # Go Through diagonals
        last_prob_label = VMobject()
        for n in range(2, 13):
            to_fade = VGroup()
            to_highlight = VGroup()
            for die in mini_dice:
                if die.sum == n:
                    to_highlight.add(die)
                else:
                    to_fade.add(die)
            pairs = VGroup(*(VGroup(m1, m2) for m1, m2 in zip(to_highlight[::2], to_highlight[1::2])))
            num = len(pairs)
            prob_label = self.get_p_sum_expr(n, Rf"\frac{{{num}}}{{36}}")
            prob_label.next_to(combinations_label, UP, buff=1.5)

            self.play(
                FadeIn(prob_label, UP),
                FadeOut(last_prob_label, UP),
                to_highlight.animate.set_opacity(1),
                to_fade.animate.set_opacity(0.2),
                blue_dice.animate.set_opacity(0.5),
                red_dice.animate.set_opacity(0.5),
            )
            if n <= 4:
                self.play(
                    LaggedStart(*(
                        FlashAround(pair.copy(), remover=True, time_width=1, run_time=1.5)
                        for pair in pairs
                    ), lag_ratio=0.2),
                )
                self.wait()
            last_prob_label = prob_label
            self.wait()

        # Reset
        self.play(
            FadeOut(grid),
            FadeOut(mini_dice, lag_ratio=0.01),
            FadeOut(combinations_label, RIGHT),
            FadeOut(prob_label, RIGHT),
            blue_dice.animate.restore(),
            red_dice.animate.restore(),
        )
        self.wait()

        # Slide rows across
        self.play(
            Rotate(red_dice, PI),
        )
        self.wait()

        last_prob_label = VMobject()
        last_rects = VMobject()
        for n in range(2, 13):
            pairs = self.get_aligned_pairs(blue_dice, red_dice, n)
            prob_label = self.get_p_sum_expr(n, Rf"\frac{{{len(pairs)}}}{{36}}")
            prob_label.to_edge(UP)

            self.play(
                self.get_dice_shift(blue_dice, red_dice, n),
                FadeOut(last_rects, run_time=0.5)
            )
            rects = get_pair_rects(pairs)
            self.play(
                FadeOut(last_prob_label, UP),
                FadeIn(prob_label, UP),
                LaggedStartMap(ShowCreation, rects, lag_ratio=0.2),
            )
            self.wait()

            last_prob_label = prob_label
            last_rects = rects

        # Realign
        self.play(
            FadeOut(last_rects),
            FadeOut(last_prob_label, UP),
            red_dice.animate.next_to(blue_dice, DOWN, buff=1.5),
        )

        # Show implicit probabilities, and alternates
        all_dice = VGroup(*blue_dice, *red_dice)
        sixths = VGroup(*(
            OldTex("1 / 6", font_size=36).next_to(die, UP, SMALL_BUFF)
            for die in all_dice
        ))
        sixths.set_stroke(WHITE, 0)
        blue_probs, red_probs = [
            np.random.uniform(0, 1, 6)
            for x in range(2)
        ]
        for probs in blue_probs, red_probs:
            probs[:] = (probs / probs.sum()).round(2)
            probs[-1] = 1.0 - probs[:-1].sum()  # Ensure it's a valid distribution

        new_prob_labels = VGroup()
        all_dice.generate_target()
        for die, prob in zip(all_dice.target, (*blue_probs, *red_probs)):
            label = DecimalNumber(prob, font_size=36)
            label.next_to(die, UP, SMALL_BUFF)
            die.set_opacity(prob / (2 / 6))
            new_prob_labels.add(label)

        question = Text("Non-uniform probabilities?")
        question.to_edge(UP)

        self.play(LaggedStartMap(Write, sixths, lag_ratio=0.1))
        self.wait()
        self.play(
            Write(question, run_time=1),
            FadeOut(sixths, 0.25 * UP, lag_ratio=0.03, run_time=4),
            FadeIn(new_prob_labels, 0.25 * UP, lag_ratio=0.03, run_time=4),
            MoveToTarget(all_dice, run_time=3)
        )
        self.wait()

        for die, prob_label in zip(all_dice, new_prob_labels):
            die.prob_label = prob_label
            die.prob = prob_label.get_value()
            die.add(prob_label)

        # March!
        last_rects = VMobject()
        last_prob_label = question
        n = 2
        while n < 13:
            pairs = self.get_aligned_pairs(blue_dice, red_dice, n)
            prob_label = self.get_p_sum_expr(n, rhs=" ")
            rhs = self.get_conv_rhs(pairs, prob_label)
            VGroup(prob_label, rhs).center().to_edge(UP)

            self.play(
                self.get_dice_shift(blue_dice, red_dice, n),
                FadeOut(last_rects, run_time=0.5),
                FadeOut(last_prob_label, 0.5 * UP),
                FadeIn(prob_label, 0.5 * UP),
            )
            rects = self.get_pair_rects(pairs)
            self.play(FadeIn(rects, lag_ratio=0.2))
            self.play(TransformMatchingShapes(
                VGroup(*(
                    VGroup(blue.prob_label, red.prob_label)
                    for blue, red in pairs
                )).copy(),
                rhs
            ))
            self.wait()

            if n == 4 and isinstance(blue_dice[0].prob_label, DecimalNumber):
                # Make more general
                blue_labels = VGroup(*(OldTex(f"a_{{{i}}}", font_size=42) for i in range(1, 7)))
                red_labels = VGroup(*(OldTex(f"b_{{{i}}}", font_size=42) for i in range(1, 7)))
                blue_labels.set_color(BLUE)
                red_labels.set_color(RED)
                old_prob_labels = VGroup()
                for die, label in zip(all_dice, (*blue_labels, *red_labels)):
                    label.next_to(die[0], UP, SMALL_BUFF)
                    die.remove(die.prob_label)
                    old_prob_labels.add(die.prob_label)
                    die.prob_label = label
                    die.add(label)
                self.play(
                    FadeIn(VGroup(*blue_labels, *red_labels), shift=0.25 * UP, lag_ratio=0.04),
                    FadeOut(old_prob_labels, shift=0.25 * UP, lag_ratio=0.04),
                    FadeOut(rhs, time_span=(0, 1)),
                    run_time=4
                )
            else:
                n += 1

            last_prob_label = VGroup(prob_label, rhs)
            last_rects = rects

        # Show all formulas
        n_range = list(range(2, 13))
        lhss = VGroup(*(self.get_p_sum_expr(n) for n in n_range))
        pairss = VGroup(*(self.get_aligned_pairs(blue_dice, red_dice, n) for n in n_range))
        rhss = VGroup(*(self.get_conv_rhs(pairs, lhs) for pairs, lhs in zip(pairss, lhss)))
        prob_labels = VGroup()
        for lhs, rhs in zip(lhss, rhss):
            prob_labels.add(VGroup(lhs, rhs))
        prob_labels.arrange(DOWN, aligned_edge=LEFT)
        prob_labels.set_height(FRAME_HEIGHT - 1)
        prob_labels.to_edge(LEFT)

        dice = VGroup(blue_dice, red_dice)
        dice.generate_target()
        dice.target[1].rotate(PI)
        for m in dice.target[1]:
            m.prob_label.rotate(PI)
            m.prob_label.next_to(m, UP, SMALL_BUFF)
        dice.target.arrange(DOWN, buff=MED_LARGE_BUFF)
        dice.target.set_width(5)
        dice.target.to_edge(RIGHT)
        dice.target.to_corner(DR)
        self.play(
            LaggedStartMap(FadeIn, prob_labels[:-1], lag_ratio=0.2, run_time=2),
            FadeTransform(last_prob_label, prob_labels[-1], time_span=(0.5, 2.0)),
            MoveToTarget(dice, path_arc=PI / 2),
            FadeOut(last_rects),
        )
        self.wait()

        # Name convolution
        a_rect = SurroundingRectangle(VGroup(*(die.prob_label for die in blue_dice)))
        b_rect = SurroundingRectangle(VGroup(*(die.prob_label for die in red_dice)))
        rhs_rects = VGroup(*(SurroundingRectangle(rhs) for rhs in rhss))
        VGroup(a_rect, b_rect, *rhs_rects).set_stroke(YELLOW, 2)

        conv_name = OldTexText(
            R"Convolution of ", "$(a_i)$", " and ", "$(b_i)$",
            tex_to_color_map={"$(a_i)$": BLUE, "$(b_i)$": RED}
        )
        conv_eq = Tex(
            R"(a * b)_n = \sum_{\substack{i, j \\ i + j = n}} a_i \cdot b_j",
            isolate=["a_i", "*", "b_j", "(a * b)_n"]
        )
        conv_label = VGroup(conv_name, conv_eq)
        conv_label.arrange(DOWN, buff=LARGE_BUFF)
        conv_label.scale(0.9)
        conv_label.to_corner(UR)

        self.play(
            LaggedStartMap(
                ShowCreationThenFadeOut,
                VGroup(a_rect, b_rect),
                lag_ratio=0.5,
                run_time=3,
            ),
            LaggedStartMap(
                FadeIn,
                conv_name[1:5:2],
                shift=UP,
                lag_ratio=0.5,
                run_time=2,
            )
        )
        self.wait()
        self.play(FadeIn(conv_name[0:4:2], lag_ratio=0.1))
        self.play(LaggedStartMap(
            ShowCreationThenFadeOut,
            rhs_rects,
            lag_ratio=0.1,
            run_time=5
        ))
        self.wait()

        # Show grid again
        diagonals = VGroup()
        plusses = VGroup()
        rhss.save_state()
        for n, rhs in zip(it.count(2), rhss):
            diag = VGroup()
            for i in range(0, len(rhs), 4):
                diag.add(rhs[i:i + 3])
                if i > 0:
                    plusses.add(rhs[i - 1])
            diagonals.add(diag)

        diagonals.generate_target()
        for k, square in enumerate(grid):
            i = k // 6
            j = k % 6
            i2 = j if (i + j <= 5) else 5 - i
            diagonals.target[i + j][i2].move_to(square)

        blue_dice.save_state()
        blue_dice.generate_target()
        red_dice.save_state()
        red_dice.generate_target()
        for dice, squares, vect in (blue_dice, grid[:6], UP), (red_dice, grid[::6], LEFT):
            dice.save_state()
            dice.generate_target()
            for die, square in zip(dice.target, squares):
                die.scale(0.75)
                die.next_to(square, vect, SMALL_BUFF)

        self.play(
            plusses.animate.set_opacity(0),
            FadeOut(lhss, LEFT, run_time=0.5, lag_ratio=0.01),
            MoveToTarget(diagonals),
            MoveToTarget(blue_dice),
            MoveToTarget(red_dice),
            run_time=2
        )
        self.play(FadeIn(grid, lag_ratio=0.01))
        self.add(diagonals)
        self.wait()
        for n in range(len(diagonals)):
            diagonals.generate_target()
            diagonals.target.set_opacity(0.2)
            diagonals.target[n].set_opacity(1)
            self.play(MoveToTarget(diagonals))
        self.wait()
        self.play(
            Restore(blue_dice),
            Restore(red_dice),
            diagonals.animate.set_opacity(1)
        )
        self.remove(diagonals)
        self.play(
            FadeOut(grid),
            Restore(rhss),
            FadeIn(lhss, time_span=(1, 2), lag_ratio=0.01),
            run_time=2
        )
        self.wait()

        # Write equation
        self.wait(2)
        self.play(FadeIn(conv_eq, DOWN))
        self.wait()

        # Highlight example
        n = 4
        pairs = self.get_aligned_pairs(blue_dice, red_dice, n + 2)
        pair_rects = get_pair_rects(pairs, together=False)

        self.play(
            prob_labels[:n].animate.set_opacity(0.35),
            prob_labels[n + 1:].animate.set_opacity(0.35),
        )
        self.wait()
        self.play(ShowSubmobjectsOneByOne(pair_rects, remover=True, rate_func=linear, run_time=3))
        self.wait()

        # Alternate formula notation
        alt_rhs = OldTex(R"\sum_{i = 1}^6 a_i \cdot b_{n - i}")
        alt_rhs.scale(0.9)
        alt_rhs.move_to(conv_eq[7], LEFT)

        self.play(
            FadeIn(alt_rhs, 0.5 * DOWN),
            conv_eq[7:].animate.shift(1.5 * DOWN).set_opacity(0.5),
            dice.animate.to_edge(DOWN)
        )
        self.wait()

    def get_p_sum_expr(self, n, rhs=" "):
        raw_expr = Tex(
            fR"P\big(O + O = {n}\big) = \, {rhs}",
            isolate=("O", str(n), "=", rhs)
        )
        for index, color in zip([2, 4], [BLUE_E, RED_E]):
            square = DieFace(1, fill_color=color, stroke_width=1)[0]
            square.replace(raw_expr[index])
            square.match_y(raw_expr[3])
            raw_expr.replace_submobject(index, square)
        return raw_expr

    def get_dice_shift(self, top_dice, low_dice, n):
        return get_row_shift(top_dice, low_dice, n)

    def get_aligned_pairs(self, top_dice, low_dice, n):
        return get_aligned_pairs(top_dice, low_dice, n)

    def get_pair_rects(self, pairs, together=True):
        return get_pair_rects(pairs, together)

    def get_conv_rhs(self, pairs, prob_label):
        rhs = VGroup()
        for (blue, red) in pairs:
            rhs.add(blue.prob_label.copy().set_color(BLUE))
            rhs.add(OldTex(R"\cdot"))
            rhs.add(red.prob_label.copy().set_color(RED))
            rhs.add(OldTex("+"))
        rhs.remove(rhs[-1])
        rhs.arrange(RIGHT, buff=SMALL_BUFF)
        rhs.next_to(prob_label, RIGHT, buff=0.2)
        return rhs
