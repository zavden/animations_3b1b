# ==============================================================================
# Scene:      DiceSimulationAlt4
# Source:     videos/_2023/clt/dice_sims.py (lines 237-238)
# Category:   1 · Renders unmodified
# Includes code copied from: _2023/clt/main.py
#
# Run from this folder:
#     manimgl DiceSimulationAlt4.py DiceSimulationAlt4 -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *
from typing import TYPE_CHECKING


# ----- From _2023/clt/main.py -----

if TYPE_CHECKING:
    from typing import Sequence
    from manimlib.typing import ManimColor


class ChartBars(VGroup):
    def __init__(
        self,
        axes,
        values: Sequence[float | int],
        xs: Sequence[float] | None = None,
        width_ratio: float = 1.0,
        offset: float = 0.5,
        fill_color: ManimColor = BLUE,
        fill_opacity: float = 0.5,
        stroke_color: ManimColor = WHITE,
        stroke_width: float = 1.0
    ):
        xs = xs if xs is not None else np.arange(*axes.x_range)

        self.x_to_index = dict(zip(xs, it.count()))
        x_step = xs[1] - xs[0]
        x_unit = axes.x_axis.get_unit_size()
        y_unit = axes.y_axis.get_unit_size()

        width = width_ratio * x_unit * x_step

        # Create a list of rectangles arranged side by side,
        # one for each x value
        rects = []
        epsilon = 1e-8
        for x, y in zip(xs, values):
            rect = Rectangle(
                width=width,
                height=max(y * y_unit, epsilon),
                fill_color=fill_color,
                fill_opacity=fill_opacity,
                stroke_color=stroke_color,
                stroke_width=stroke_width,
            )
            rect.move_to(axes.c2p(x + offset * x_step, 0), DOWN)
            rects.append(rect)
        super().__init__(*rects)
        self.axes = axes
        self.xs = xs
        self.set_values(values)

    def set_values(self, values: Iterable[float | int]):
        y_unit = self.axes.y_axis.get_unit_size()
        for rect, value in zip(self, values):
            rect.set_height(
                y_unit * value,
                stretch=True,
                about_edge=DOWN,
            )


def get_die_distribution_chart(
    dist: list[float],
    die_config=dict(),
    axes_config=dict(
        width=4,
        height=3,
    ),
    font_size=25,
    y_range=(0, 1, 0.2),
    max_value: int = 6,
    bar_colors=(BLUE, TEAL)
):
    axes = Axes((0, max_value), y_range, **axes_config)
    ndp = len(str(y_range[2])) - 2
    axes.y_axis.add_numbers(font_size=font_size, num_decimal_places=ndp)
    bars = ChartBars(axes, dist)
    bars.set_submobject_colors_by_gradient(*bar_colors)

    dice = VGroup()
    for n in range(1, max_value + 1):
        die = DieFace(n, **die_config)
        die.set_width(0.5 * axes.x_axis.get_unit_size())
        die.next_to(axes.c2p(n - 0.5, 0), DOWN, SMALL_BUFF)
        dice.add(die)

    result = VGroup(axes, bars, dice)
    result.axes = axes
    result.bars = bars
    result.dice = dice
    return result


def get_sample_markers(bars, samples):
    width = 0.25 * bars[0].get_width()
    tips = ArrowTip(angle=-90 * DEGREES).replicate(len(samples))
    tips.set_width(width)
    tips.set_height(0.5 * width, stretch=True)
    tips.set_fill(YELLOW, 1)
    tip_map = [VGroup() for b in bars]
    for sample, tip in zip(samples, tips):
        tip_map[sample - 1].add(tip)

    for value, group in enumerate(tip_map):
        group.arrange(UP, buff=0.5 * width)
        group.next_to(bars[value], UP, SMALL_BUFF)

    return tips



# ----- From _2023/clt/dice_sims.py -----

class DiceSimulation(InteractiveScene):
    n_dice = 10
    n_samples = 3000
    distribution = [1 / 6] * 6
    die_distribution_config = dict(
        axes_config=dict(width=3.5, height=1.5),
        y_range=(0, 0.5, 0.25),
    )
    brick_height = 0.2
    initial_brick_color = YELLOW
    full_dist_color = GREEN_D
    spread = 22
    dice_width = 5

    def setup(self):
        super().setup()
        self.add_die_distribution()
        self.add_sum_axes()
        self.add_sample_label()
        self.buckets = dict()
        self.all_bricks = VGroup()

    def construct(self):
        # Slow samples
        for _ in range(3):
            self.run_one_sum()

        # Speedier samples
        for _ in range(10):
            self.run_one_sum(run_time=0.5, transition_time=0.5)

        # First few instant samples
        for _ in range(200):
            self.run_one_sum(transition_time=1 / 30, still_frame=True)

        # Thousands of samples
        self.scale_brick_height(0.1)
        for _ in range(self.n_samples - int(self.sample_label.count.get_value())):
            self.run_one_sum(transition_time=1 / 30, still_frame=True)

        self.play(self.all_bricks.animate.set_fill(color=self.full_dist_color))

    def add_die_distribution(self, animate=False):
        die_dist = get_die_distribution_chart(
            self.distribution,
            **self.die_distribution_config,
        )
        die_dist.to_corner(UL)
        die_dist.shift(0.25 * DOWN)

        axes, bars, dice = die_dist

        if animate:
            self.play(
                Write(axes),
                LaggedStartMap(GrowFromEdge, bars, edge=DOWN),
                Write(dice),
            )

        self.add(die_dist)

        self.die_dist = die_dist

    def add_sum_axes(self):
        # (Value, probability) pairs
        vps = list(zip(it.count(1), self.distribution))
        mu = sum(v * p for v, p in vps)
        var = sum(p * (v - mu)**2 for v, p in vps)

        n = self.n_dice
        x_mid = int(n * mu)
        spread = self.spread or int(2.5 * math.sqrt(var * n))

        x_range = (x_mid - spread, x_mid + spread, 1)
        axes = Axes(
            x_range,
            (0, int(math.sqrt(self.n_samples))),
            width=FRAME_WIDTH - 1,
            height=4,
        )

        # dots = Tex(R"\dots", font_size=24)
        # dots.next_to(axes.x_axis, LEFT, SMALL_BUFF)
        # axes.y_axis.set_x(dots.get_left()[0] - SMALL_BUFF)
        # axes.add(dots)

        x_axis = axes.x_axis
        x_axis.add_numbers(font_size=16)
        x_axis.numbers.remove(x_axis.numbers[-1])
        x_axis.numbers.shift(
            0.5 * x_axis.get_unit_size() * RIGHT + \
            0.1 * UP
        )

        # axes.center()
        # axes.to_edge(DOWN)

        x_axis.center()
        x_axis.to_edge(DOWN)

        self.add(x_axis)

        self.sum_axes = axes
        self.sum_axis = x_axis

    def add_sample_label(self):
        label = TexText(R"\# Sums = 0", font_size=36)
        label.set_fill(GREY_B)
        label.to_edge(LEFT)
        label.count = label.make_number_changeable("0")
        label.count.edge_to_fix = LEFT

        self.add(label)

        self.sample_label = label

    def run_one_sum(self, run_time=3.0, transition_time=1.0, still_frame=False):
        # Setup sample
        values = list(range(1, 7))
        bars = self.die_dist.bars
        samples = np.random.choice(values, size=self.n_dice, p=self.distribution)
        dice = VGroup(*(DieFace(sample) for sample in samples))
        dice.arrange_in_grid(n_cols=5)
        dice.set_width(self.dice_width)
        dice.to_corner(UR)

        bar_highlights = VGroup(*(
            bars[sample - 1].copy()
            for sample in samples
        ))
        bar_highlights.set_fill(YELLOW, 1)

        face_counts = [0] * len(self.distribution)
        for sample in samples:
            face_counts[sample - 1] += 1

        # Tips
        tips = get_sample_markers(bars, samples)

        def get_sum():
            return sum(d.value for d in dice)

        # Sum label
        sum_label = TexText(f"Sum = 0")
        sum_label.count = sum_label.make_number_changeable(0)
        sum_label.next_to(dice, DOWN, buff=MED_LARGE_BUFF)
        sum_label.count.set_value(get_sum())

        # Mark the sample
        brick = self.get_brick()
        s = get_sum()
        if s not in self.buckets:
            self.buckets[s] = VGroup(VectorizedPoint(
                self.sum_axis.n2p(s + 0.5)
            ))
        bucket = self.buckets[s]

        brick.next_to(bucket, UP, buff=0)

        count_copy = sum_label.count.copy()
        count_copy.target = bucket[0]
        for number in self.sum_axis.numbers:
            if number.get_value() == sum_label.count.get_value():
                sum_label.count.target = number
                break

        # Animate!
        if still_frame:
            self.all_bricks.set_fill(color=self.full_dist_color)
            self.sample_label.count.increment_value()
            self.add(dice, brick, sum_label, tips)
            self.wait(transition_time)
            self.remove(dice, sum_label, tips)
        else:
            self.play(
                ShowIncreasingSubsets(dice, int_func=np.ceil),
                ShowIncreasingSubsets(tips, int_func=np.ceil),
                ShowSubmobjectsOneByOne(bar_highlights, remover=True),
                UpdateFromFunc(sum_label, lambda m: m.count.set_value(get_sum())),
                self.all_bricks.animate.set_fill(color=self.full_dist_color),
                run_time=run_time,
            )
            self.wait(transition_time)
            self.play(
                FadeInFromPoint(brick, count_copy.get_center()),
                MoveToTarget(count_copy),
                FadeOut(sum_label, lag_ratio=0.1),
                FadeOut(dice, lag_ratio=0.1),
                FadeOut(tips, lag_ratio=0.1),
                run_time=transition_time
            )
            self.sample_label.count.increment_value()
            self.wait(transition_time)

        self.buckets[s].add(brick)
        self.all_bricks.add(brick)
        self.add(self.all_bricks)

    def scale_brick_height(self, scale_factor):
        self.brick_height *= scale_factor
        bricks = self.all_bricks
        bricks.target = bricks.generate_target()
        bricks.target.stretch(scale_factor, 1, about_edge=DOWN)
        bricks.target.set_stroke(width=scale_factor * bricks[0].get_stroke_width())
        self.play(MoveToTarget(bricks), run_time=3)
        self.wait()

    def get_brick(self):
        return Rectangle(
            stroke_width=self.brick_height * 5,
            stroke_color=BLACK,
            fill_color=self.initial_brick_color,
            fill_opacity=1,
            height=self.brick_height,
            width=0.8 * self.sum_axis.get_unit_size()
        )


class DiceSimulationAlt4(DiceSimulation):
    random_seed = 4
