# ==============================================================================
# Scene:      SumAlongDiagonal
# Source:     videos/_2023/convolutions2/dice.py (lines 93-710)
# Category:   1 · Renders unmodified
# Includes code copied from: _2022/convolutions/discrete.py, _2023/clt/main.py
#
# Run from this folder:
#     manimgl SumAlongDiagonal.py SumAlongDiagonal -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *
import scipy.signal
import scipy.stats


# ----- From _2022/convolutions/discrete.py -----

def get_die_faces(**kwargs):
    result = VGroup(*(DieFace(n, **kwargs) for n in range(1, 7)))
    result.arrange(RIGHT, buff=MED_LARGE_BUFF)
    return result


def dist_to_bars(dist, bar_width=0.5, height=2.0, bar_colors=(BLUE_D, GREEN_D)):
    bars = Rectangle(width=bar_width).get_grid(1, len(dist), buff=0)
    bars.set_color_by_gradient(*bar_colors)
    bars.set_fill(opacity=1)
    bars.set_stroke(WHITE, 1)
    for bar, value, index in zip(bars, dist, it.count()):
        bar.set_height(value, stretch=True, about_edge=DOWN)
        bar.index = index
    bars.set_height(height, stretch=True)
    bars.center()
    return bars



# ----- From _2023/clt/main.py -----

EXP_DISTRIBUTION = [0.41, 0.25, 0.15, 0.10, 0.06, 0.03]



# ----- From _2023/convolutions2/dice.py -----

SKEW_DISTRIBUTION = [0.12, 0.23, 0.31, 0.18, 0.12, 0.04]


def get_bar_group(
    dist,
    bar_colors=(BLUE_D, TEAL_D),
    value_labels=None,
    width_ratio=0.7,
    height=2.0,
    number_config=dict(),
    label_buff=SMALL_BUFF,
):
    bars = dist_to_bars(dist, bar_colors=bar_colors, height=height)
    p_labels = VGroup(*(DecimalNumber(x, **number_config) for x in dist))
    p_labels.set_max_width(width_ratio * bars[0].get_width())
    for p_label, bar in zip(p_labels, bars):
        p_label.next_to(bar, UP, SMALL_BUFF)

    if value_labels is None:
        value_labels = VectorizedPoint().replicate(len(dist))

    for value_label, bar in zip(value_labels, bars):
        value_label.set_width(width_ratio * bars[0].get_width())
        value_label.next_to(bar, DOWN, buff=label_buff)

    labeled_bars = VGroup(*(
        VGroup(bar, value_label, p_label)
        for bar, value_label, p_label in zip(bars, value_labels, p_labels)
    ))
    for group in labeled_bars:
        group.bar, group.die, group.value_label = group

    return labeled_bars


def die_sum_labels(color1=BLUE_E, color2=RED_E, height=1.0):
    die1, die2 = dice = [
        DieFace(1, fill_color=color)
        for color in [color1, color2]
    ]
    for die in dice:
        die.remove(die[1])
        die.set_height(height / 3)

    result = VGroup()
    for n in range(2, 13):
        sum_sym = VGroup(
            die1.copy(),
            Tex("+", font_size=24),
            die2.copy(),
            Tex("=", font_size=24).rotate(90 * DEGREES),
            Tex(str(n), font_size=30),
        )
        sum_sym.arrange(DOWN, buff=SMALL_BUFF)
        sum_sym[:2].shift(0.05 * DOWN)
        sum_sym[:1].shift(0.05 * DOWN)
        sum_sym.set_height(height)
        result.add(sum_sym)
    result.arrange(RIGHT)
    return result


def p_mob(mob, scale_factor=1.0):
    used_mob = mob.copy()
    aspect_ratio = mob.get_width() / mob.get_height()
    Os = "O" * int(np.round(aspect_ratio))
    tex = Tex(f"P({Os})")
    used_mob.replace(tex[Os], dim_to_match=0)
    used_mob.scale(scale_factor)
    result = VGroup(*tex[:2], used_mob, tex[-1])
    result.arg = used_mob
    return result


class SumAlongDiagonal(InteractiveScene):
    samples = 4

    dist1 = EXP_DISTRIBUTION
    dist2 = SKEW_DISTRIBUTION

    dist1_colors = (BLUE_D, TEAL_D)
    dist2_colors = (RED_D, GOLD_E)
    sum_colors = (GREEN_E, YELLOW_E)

    def construct(self):
        # Setup distributions
        dist1 = self.dist1
        dist2 = self.dist2
        blue_dice = get_die_faces(fill_color=BLUE_E, dot_color=WHITE)
        red_dice = get_die_faces(fill_color=RED_E, dot_color=WHITE)
        bar_groups = VGroup(
            get_bar_group(dist1, self.dist1_colors, blue_dice),
            get_bar_group(dist2, self.dist2_colors, red_dice),
        )

        bar_groups.arrange(DOWN, buff=LARGE_BUFF)
        bar_groups.to_edge(LEFT)

        self.add(bar_groups)

        # Setup the sum distribution
        conv_dist = np.convolve(dist1, dist2)
        sum_labels = die_sum_labels()
        sum_bar_group = get_bar_group(
            conv_dist, self.sum_colors, sum_labels,
            number_config=dict(num_decimal_places=3, font_size=30),
            label_buff=MED_SMALL_BUFF,
        )
        sum_bar_group.to_edge(RIGHT, buff=LARGE_BUFF)
        sum_bar_group.set_y(0)

        buckets = VGroup()
        for bar in sum_bar_group:
            base = Line(LEFT, RIGHT)
            base.match_width(bar)
            base.move_to(bar[0], DOWN)
            v_lines = Line(DOWN, UP).replicate(2)
            v_lines.set_height(6)
            v_lines[0].move_to(base.get_left(), DOWN)
            v_lines[1].move_to(base.get_right(), DOWN)
            bucket = VGroup(base, *v_lines)
            bucket.set_stroke(GREY_C, 2)
            buckets.add(bucket)

        self.add(sum_labels)
        self.add(buckets)

        # Repeatedly sample from these two (for a while)
        self.show_repeated_samples(
            dist1, dist2, *bar_groups, buckets, sum_labels,
            n_animated_runs=1, n_total_runs=2,
        )

        # Ask about sum values
        rects = VGroup(*(
            SurroundingRectangle(sum_label)
            for sum_label in sum_labels
        ))
        words1 = Text("What's the probability\nof this?", font_size=36)
        words2 = Text("Or this?", font_size=36)

        words1.next_to(rects[0], DOWN, MED_SMALL_BUFF)
        words2.next_to(rects[1], DOWN, MED_SMALL_BUFF)

        self.play(ShowCreation(rects[0]), FadeIn(words1))
        self.wait()
        self.play(
            TransformMatchingStrings(words1, words2, run_time=1),
            FadeOut(rects[0]),
            FadeIn(rects[1]),
        )
        self.wait()
        for i in range(1, len(rects) - 1):
            self.play(
                FadeOut(rects[i]), FadeIn(rects[i + 1]),
                words2.animate.match_x(rects[i + 1]),
                run_time=0.5
            )
        self.wait()
        self.play(FadeOut(words2), FadeOut(rects[-1]))
        self.play(FadeOut(sum_labels), FadeOut(buckets))

        # Draw grid of dice values
        grid = Square().get_grid(6, 6, buff=0, fill_rows_first=False, )
        grid.flip(RIGHT)
        grid.set_stroke(WHITE, 1)
        grid.set_height(5.5)
        grid.to_edge(RIGHT, buff=LARGE_BUFF)
        grid.to_edge(UP)

        blue_row = blue_dice.copy()
        red_col = red_dice.copy()
        for square, die in zip(grid[::6], blue_row):
            die.set_width(0.5 * square.get_width())
            die.next_to(square, DOWN)
        for square, die in zip(grid, red_col):
            die.set_width(0.5 * square.get_width())
            die.next_to(square, LEFT)

        self.play(
            ShowCreation(grid, lag_ratio=0.5),
            TransformFromCopy(blue_dice, blue_row),
            TransformFromCopy(red_dice, red_col),
        )

        dice_pairs = VGroup()
        anims = []
        for n, square in enumerate(grid):
            templates = VGroup(
                blue_row[n // 6],
                red_col[n % 6],
            )
            pair = templates.copy()
            pair.arrange(RIGHT, buff=SMALL_BUFF)
            pair.set_width(square.get_width() * 0.7)
            pair.move_to(square)
            dice_pairs.add(pair)
            anims.extend([
                TransformFromCopy(templates, pair),
            ])

        self.play(LaggedStart(*anims, lag_ratio=0.1))
        self.add(dice_pairs)
        self.wait()

        full_table = VGroup(blue_row, red_col, grid, dice_pairs)

        # Highlight (4, 2) pair
        pairs = [
            (1, 1),
            (1, 2),
            (1, 3),
            (1, 4),
            (1, 5),
            (2, 5),
            (2, 4),
            (2, 3),
            (3, 3),
            (3, 2),
            (4, 2),
        ]

        for pair in pairs:
            self.isolate_pairs(bar_groups, full_table, pair)
            self.wait(0.5)
        self.wait()

        # Show the probability of (4, 2)
        def get_p_label(dice):
            p_label = VGroup(
                p_mob(dice), Tex("="),
                p_mob(dice[0]),
                p_mob(dice[1]),
            )
            p_label.arrange(RIGHT, buff=SMALL_BUFF)
            return p_label

        i0, j0 = pairs[-1]
        p_label = get_p_label(dice_pairs[(i0 - 1) * 6 + (j0 - 1)])
        p_label.to_edge(UP)
        p_label.shift(2.5 * LEFT)

        movers = VGroup(
            dice_pairs[(i0 - 1) * 6 + j0 - 1],
            blue_row[(i0 - 1)],
            red_col[(j0 - 1)],
        ).copy()
        self.play(
            bar_groups.animate.set_width(2.5, about_edge=DL),
            full_table.animate.set_width(5.5, about_edge=DR),
            LaggedStart(
                movers[0].animate.replace(p_label[0][2]),
                movers[1].animate.replace(p_label[2][2]),
                movers[2].animate.replace(p_label[3][2]),
                lag_ratio=0.25,
            ),
        )
        self.play(FadeIn(p_label))
        self.remove(movers)
        self.wait()

        # Show numerical product
        prod_rhs = Tex("= (0.00)(0.00)")
        num_rhs = Tex("= 0.000")

        value1, value2 = prod_rhs.make_number_changeable("0.00", replace_all=True)
        value1.set_value(dist1[i0 - 1]).set_color(BLUE)
        value2.set_value(dist2[j0 - 1]).set_color(RED)
        prod_rhs.next_to(p_label[1], DOWN, MED_LARGE_BUFF, aligned_edge=LEFT)

        pair_prob = num_rhs.make_number_changeable("0.000")
        pair_prob.set_value(dist1[i0 - 1] * dist2[j0 - 1])
        num_rhs.next_to(prod_rhs, DOWN, MED_LARGE_BUFF, aligned_edge=LEFT)

        self.play(LaggedStart(
            Transform(bar_groups[0][i0 - 1][2].copy(), value1.copy(), remover=True),
            Transform(bar_groups[1][j0 - 1][2].copy(), value2.copy(), remover=True),
            Write(prod_rhs, lag_ratio=0.1),
            lag_ratio=0.5
        ))
        self.wait()
        self.play(FadeIn(num_rhs, DOWN))
        self.wait()

        example = VGroup(p_label, prod_rhs, num_rhs)

        # Assumption
        morty = Mortimer(height=2.0).flip()
        morty.next_to(example, DOWN, buff=2.0)
        morty.shift(0.5 * LEFT)

        self.play(
            morty.says(
                "Assuming rolls\nare independent!",
                mode="surprised",
            ),
            VFadeIn(morty),
        )
        self.play(Blink(morty))
        self.wait()
        self.play(LaggedStartMap(FadeOut, VGroup(morty, morty.bubble, morty.bubble.content)))

        # Set up the multiplication table
        full_table.generate_target()
        full_table.target.set_width(6.5)
        full_table.target.set_opacity(1)
        full_table.target[2].set_fill(opacity=0)
        full_table.target.to_edge(RIGHT, buff=1.5)
        full_table.target.set_y(0)

        self.play(
            MoveToTarget(full_table),
            example.animate.scale(0.75, about_edge=UL).shift(0.5 * LEFT)
        )

        marginal_labels = VGroup(*(
            VGroup(*(bar[2] for bar in group)).copy()
            for group in bar_groups
        ))
        margin_dice = VGroup(*full_table[:2], full_table[3])
        for margins, dice in zip(marginal_labels, margin_dice):
            margins.generate_target()
            dice.generate_target()
            for die, prob in zip(dice.target, margins.target):
                center = die.get_center()
                die.scale(0.7)
                die.set_opacity(0.85)
                prob.next_to(die, DOWN, buff=0.125)
                prob.scale(1.5)
                VGroup(prob, die).move_to(center)

        marginal_labels[0].target.set_fill(BLUE, 1)
        marginal_labels[1].target.set_fill(RED, 1)

        margin_dice[2].generate_target()
        for dice in margin_dice[2].target:
            dice.scale(0.75, about_edge=UP)
            dice.set_opacity(0.85)
            dice.set_stroke(width=1)
            dice.shift(0.1 * UP)

        for groups in zip(marginal_labels, margin_dice):
            self.play(*map(MoveToTarget, groups), lag_ratio=0.001)
        self.play(MoveToTarget(margin_dice[2], lag_ratio=0.001))
        self.wait()

        full_table.add(marginal_labels)

        # Fill in multiplication table
        grid_probs = VGroup()
        self.add(grid_probs)
        for n, square in enumerate(grid):
            i, j = n // 6, n % 6
            dice = margin_dice[2][n]
            margin1 = marginal_labels[0][i]
            margin2 = marginal_labels[1][j]
            prob = DecimalNumber(
                margin1.get_value() * margin2.get_value(),
                num_decimal_places=3
            )
            prob.set_height(margin1.get_height())
            prob.next_to(dice, DOWN, SMALL_BUFF)

            rects = VGroup(*(
                SurroundingRectangle(mob, buff=SMALL_BUFF)
                for mob in [margin1, margin2, prob]
            ))
            rects.set_stroke(YELLOW, 1)

            grid_probs.add(prob)

            value1.set_value(dist1[i])
            value2.set_value(dist2[j])
            pair_prob.set_value(dist1[i] * dist2[j])
            new_p_label = get_p_label(dice.copy().set_opacity(1))
            new_p_label.replace(p_label, dim_to_match=1)
            p_label.become(new_p_label)

            bar_groups.set_opacity(0.35)
            bar_groups[0][i].set_opacity(1)
            bar_groups[1][j].set_opacity(1)

            self.add(rects)
            self.wait(0.25)
            self.remove(rects)
        self.wait()

        full_table.add(grid_probs)

        # Fade out example
        self.play(
            FadeOut(example),
            bar_groups.animate.set_opacity(1),
        )
        self.wait()

        # Show it as a 3d plot
        bar_groups.fix_in_frame()
        sum_bar_group.fix_in_frame()

        bars_3d = VGroup()
        scale_factor = 30
        for square, prob in zip(grid, grid_probs):
            prism = VCube()
            prism.set_fill(GREY_D, 0.85)
            prism.set_stroke(WHITE, 1, 0.5)
            prism.match_width(square)
            prism.set_depth(scale_factor * prob.get_value(), stretch=True)
            prism.move_to(square, IN)
            prism.save_state()
            prism.stretch(0.001, 2, about_edge=IN)
            prism.set_opacity(0)
            bars_3d.add(prism)

        self.play(
            LaggedStartMap(Restore, bars_3d),
            self.frame.animate.reorient(12, 65, 0).move_to([-0.48, 0.37, 0.77]).set_height(9.43),
            run_time=3,
        )
        self.add(full_table, *bars_3d)
        self.play(
            self.frame.animate.reorient(43, 66, 0).move_to([-0.06, 0.21, -0.29]).set_height(10.59),
            run_time=7,
        )
        self.wait()

        # Show sum distribution
        self.play(
            LaggedStartMap(FadeOut, bar_groups, shift=2 * LEFT),
            FadeIn(sum_bar_group),
            full_table.animate.to_edge(LEFT),
            self.frame.animate.reorient(4, 65, 0).move_to([0.64, 0.8, 0.69]).set_height(10.59),
            *(
                MaintainPositionRelativeTo(bar, full_table)
                for bar in bars_3d
            ),
            run_time=2,
        )
        self.wait()

        # Reposition
        self.play(
            self.frame.animate.to_default_state(),
            FadeOut(bars_3d),
            run_time=2,
        )
        self.wait()

        # Add up along all diagonals
        low_group = VGroup(blue_row, marginal_labels[0])
        left_group = VGroup(red_col, marginal_labels[1])
        diagonals = VGroup(*(
            VGroup(*(
                VGroup(dice_pairs[n], grid_probs[n])
                for n in range(36)
                if (n // 6) + (n % 6) == s
            ))
            for s in range(11)
        ))

        diagonals.save_state()
        rects = VGroup()
        diagonals.rotate(45 * DEGREES)
        for diagonal in diagonals:
            rect = SurroundingRectangle(diagonal)
            rect.stretch(0.9, 1)
            rect.round_corners()
            rects.add(rect)
        VGroup(rects, diagonals).rotate(-45 * DEGREES, about_point=diagonals.get_center())

        rects.set_fill(YELLOW, 0.25)
        rects.set_stroke(YELLOW, 2)

        last_rect = VGroup(low_group, left_group)
        for n, rect in zip(it.count(), rects):
            self.add(rect, diagonals)
            diagonals.generate_target()
            diagonals.target.set_opacity(0.5)
            diagonals.target[n].set_opacity(1)

            sum_bar_group.generate_target()
            sum_bar_group.target.set_opacity(0.4)
            sum_bar_group.target[n].set_opacity(1)

            self.play(
                FadeOut(last_rect),
                FadeIn(rect),
                MoveToTarget(diagonals),
                MoveToTarget(sum_bar_group),
            )
            last_rect = rect
        self.wait()
        self.play(
            diagonals.animate.set_opacity(1),
            sum_bar_group.animate.set_opacity(1),
            FadeOut(last_rect),
            FadeIn(low_group),
            FadeIn(left_group),
        )

        # Show 3d grid again
        self.play(
            self.frame.animate.reorient(27, 66, 0).move_to([-0.16, 1.41, 0.77]).set_height(9.36),
            FadeIn(bars_3d),
            sum_bar_group.animate.to_edge(RIGHT),
            run_time=2,
        )
        self.wait()

        # Go through diagonals of the plot
        sorted_bars = VGroup(*bars_3d)
        camera_pos = self.frame.get_implied_camera_location()
        sorted_bars.sort(lambda p: -get_norm(p - camera_pos))
        self.add(*sorted_bars)

        diagonal_bar_groups = VGroup().replicate(11)

        for s in range(11):
            sum_bar_group.generate_target()
            sum_bar_group.target.set_opacity(0.2)
            sum_bar_group.target[s].set_opacity(1)

            for n, bar in enumerate(bars_3d):
                bar.generate_target()
                bar.target.set_opacity(0.1)
                bar.target.set_stroke(width=0)
                if (n // 6) + (n % 6) == s:
                    bar.target.set_opacity(1)
                    diagonal_bar_groups[s].add(bar)

            self.play(
                MoveToTarget(sum_bar_group),
                *map(MoveToTarget, bars_3d),
            )
            self.wait()
        self.play(
            bars_3d.animate.set_opacity(0.8).set_stroke(width=0.5),
            sum_bar_group.animate.set_opacity(1),
        )
        self.wait()

        # Highlight bars
        bars_3d.save_state()
        bar_highlights = bars_3d.copy()
        bar_highlights.set_fill(opacity=0)
        bar_highlights.set_stroke(TEAL, 3)
        self.play(ShowCreationThenFadeOut(bar_highlights, lag_ratio=0.001, run_time=2))

        # Collapase diagonals
        bars_3d.generate_target()
        for bar in bars_3d.target:
            bar.stretch(0.5, 0)
            bar.stretch(0.5, 1)
        bars_3d.target.set_fill(opacity=1)
        bars_3d.target.set_submobject_colors_by_gradient(GREEN_D, YELLOW_D)
        bars_3d.target.set_stroke(WHITE, 1)
        self.play(
            self.frame.animate.reorient(36, 46, 0).move_to([-0.56, 0.55, 1.22]).set_height(7.71),
            MoveToTarget(bars_3d),
            # FadeOut(full_table, IN),
            sum_bar_group.animate.set_width(4.0).to_edge(RIGHT),
            run_time=2,
        )
        self.wait()

        diagonal_bar_groups.apply_depth_test()
        new_diagonals = diagonal_bar_groups.copy()
        for group in new_diagonals:
            group.arrange(IN, buff=0)
        new_diagonals.arrange(UR, buff=MED_SMALL_BUFF, aligned_edge=IN)
        new_diagonals.move_to(bars_3d.get_corner(DR))
        new_diagonals.shift(DR)
        
        self.play(
            self.frame.animate.reorient(40, 61, 0).move_to([1.69, 0.33, -0.73]).set_height(12.96),
            ReplacementTransform(
                diagonal_bar_groups, new_diagonals,
                lag_ratio=0.001,
            ),
            run_time=5,
        )
        self.add(full_table, new_diagonals)
        self.play(
            self.frame.animate.reorient(40, 85, 0).move_to([3.05, 1.93, 0.77]).set_height(14.93),
            sum_bar_group.animate.set_width(5.5, about_edge=RIGHT),
            FadeOut(full_table),
            run_time=3
        )
        self.wait()

    def show_repeated_samples(
        self,
        dist1,
        dist2,
        bar_group1,
        bar_group2,
        buckets,
        sum_labels,
        n_animated_runs=20,
        n_total_runs=150,
        marker_height=0.1,
        marker_color=YELLOW_D,
    ):
        marker_template = Rectangle(
            height=marker_height,
            width=buckets[0].get_width() * 0.8,
            fill_color=marker_color,
            fill_opacity=1,
            stroke_color=WHITE,
            stroke_width=1,
        )
        markers = VGroup(*(
            VGroup(VectorizedPoint(bucket.get_bottom()))
            for bucket in buckets
        ))

        var1 = scipy.stats.rv_discrete(values=(range(6), dist1))
        var2 = scipy.stats.rv_discrete(values=(range(6), dist2))

        for n in range(n_total_runs):
            x = var1.rvs()
            y = var2.rvs()

            animate = n < n_animated_runs

            # Show dice
            dice = VGroup()
            for group, value in [(bar_group1, x), (bar_group2, y)]:
                die = group[value][1].copy()
                die.set_opacity(1)
                die.scale(2)
                die.next_to(group, RIGHT, LARGE_BUFF)
                dice.add(die)
                group.set_opacity(0.5)
                group[value].set_opacity(1)
                self.add(die)
                self.wait(0.25 if animate else 0.0)

            # Highlight sum
            sum_labels.set_opacity(0.25)
            sum_labels[x + y].set_opacity(1)

            # Drop marker in the appropriate sum bucket
            marker = marker_template.copy()
            marker.move_to(markers[x + y].get_top(), DOWN)
            if animate:
                self.play(FadeIn(marker, DOWN, rate_func=rush_into, run_time=0.5))
                self.wait(0.5)

            markers[x + y].add(marker)
            self.add(markers)

            if animate:
                self.play(LaggedStart(
                    FadeOut(dice[0]),
                    bar_group1.animate.set_opacity(0.5),
                    FadeOut(dice[1]),
                    bar_group2.animate.set_opacity(0.5),
                    sum_labels.animate.set_opacity(0.25),
                    run_time=0.5
                ))
            else:
                self.wait(0.1)
                self.remove(dice)
                VGroup(bar_group1, bar_group2).set_opacity(0.5)
                sum_labels.set_opacity(0.25)

        self.wait()
        self.play(
            FadeOut(markers, lag_ratio=0.01),
            bar_group1.animate.set_opacity(1),
            bar_group2.animate.set_opacity(1),
            sum_labels.animate.set_opacity(1),
        )

    def isolate_pairs(self, bar_groups, full_table, *ij_tuples):
        full_table.set_opacity(0.25)
        full_table[2].set_fill(opacity=0)
        bar_groups.set_opacity(0.35)

        for i, j in ij_tuples:
            im1 = i - 1
            jm1 = j - 1
            n = im1 * 6 + jm1

            bar_groups[0][im1].set_opacity(1)
            bar_groups[1][jm1].set_opacity(1)

            full_table[0][im1].set_opacity(1)
            full_table[1][jm1].set_opacity(1)
            full_table[2][n].set_stroke(opacity=1)
            full_table[3][n].set_opacity(1)
