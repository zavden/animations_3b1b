# ==============================================================================
# Scene:      RobotEncodingsV2
# Source:     videos/_2026/cross_entropy/robot.py (lines 1421-2497)
# Category:   2 · Renders with modifications
# Includes code copied from: _2026/cross_entropy/distribution.py
#
# Run from this folder:
#     manimgl RobotEncodingsV2.py RobotEncodingsV2 -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Uses the placeholder images/pi_creature_mission_control.png (the original is private to Grant).
#   - Uses the placeholder clockwise.svg (the original is private to Grant).
#
# Placeholder assets (not Grant's originals):
#   - images/pi_creature_mission_control.png (placeholder image: pi creature at a mission control console)
#   - clockwise.svg (placeholder clockwise-turn icon)
#
# Notes:
#   images/arrow.svg is the faithful conversion of images/arrow.ai (PDF) to SVG with pdftocairo; it is not an invented asset.
#   images/lunar_rover_assets/stationary.png is the faithful conversion of Stationary.tif (the code looks it up in lowercase).
# ==============================================================================

from __future__ import annotations
import math
from manim_imports_ext import *
import random


# ----- From _2026/cross_entropy/distribution.py -----

class StackedProbDistribution(VGroup):
    def __init__(
        self,
        distribution,
        width=12,
        height=0.5,
        fill_colors=(BLUE_E, TEAL_E),
        fill_opacity=1,
        stroke_width=1,
        stroke_color=WHITE,
        labels=None,
        label_height_ratio=0.5,
        label_width_ratio=0.8,
        fit_labels_to_height=True,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.distribution = distribution
        self.cdf = np.cumsum(distribution)
        self.bar_color_bounds = fill_colors
        self.label_height_ratio = label_height_ratio
        self.label_width_ratio = label_width_ratio

        # Set bars with dummy values
        self.bars = Rectangle().get_grid(1, len(distribution), buff=0)
        self.bars.set_shape(width, height)
        self.bars.set_fill(fill_colors, 1, gradient_direction=RIGHT)
        self.bars.set_stroke(stroke_color, stroke_width)

        # Initialize labels as empty
        self.labels = VGroup()

        self.add(self.bars, self.labels)

        self.set_distribution(distribution)
        self.fit_labels_to_height = fit_labels_to_height
        if labels is not None:
            self.set_labels(labels)

    def set_labels(self, labels: VMobject):
        self.labels.set_submobjects(labels)
        self.original_labels = labels.copy()
        self.reposition_labels()
        return self

    def reposition_labels(self):
        self.labels.become(self.original_labels)
        if self.fit_labels_to_height:
            self.labels.set_height(self.bars.get_height() * self.label_height_ratio)
        self.labels.move_to(self.bars)
        for label, bar in zip(self.labels, self.bars):
            label.match_x(bar)
            fill_opacity = float(label.get_width() < bar.get_width() * self.label_width_ratio)
            label.set_fill(opacity=fill_opacity)
        return self

    def set_distribution(self, distribution):
        center = self.bars.get_center().copy()
        width, height = self.bars.get_shape()[:2]
        n_bars = len(distribution)
        bar_style = self.bars[0].get_style()

        if len(self.bars) != n_bars:
            self.bars.set_submobjects(Rectangle().replicate(n_bars))

        for bar, prob in zip(self.bars, distribution):
            bar.set_shape(width * prob, height)
            bar.set_style(**bar_style)
        self.bars.arrange(RIGHT, buff=0)
        self.bars.move_to(center)
        self.bars.set_fill(self.bar_color_bounds, gradient_direction=RIGHT)

        if len(self.labels) > 0:
            self.reposition_labels()

        return self

    def highlight(self, index, color=None, other_bar_opacity=0.35, fade_labels=True):
        self.bars.set_fill(self.bar_color_bounds, opacity=other_bar_opacity, gradient_direction=RIGHT)
        self.bars[index].set_fill(color, opacity=1)
        if fade_labels:
            for idx, label in enumerate(self.labels):
                if label.get_fill_opacity() == 0:
                    op = 0
                elif idx == index:
                    op = 1
                else:
                    op = other_bar_opacity
                label.set_fill(opacity=op)
        return self

    def renormalize_around(self, index: int):
        width, height = self.get_shape()[:2]
        center = self.get_center().copy()
        bar_width = self.bars[index].get_width()
        self.bars.stretch(width / bar_width, 0)
        self.bars.shift(center - self.bars[index].get_center())
        self.reposition_labels()
        return self

    def stretch(self, factor, dim, **kwargs):
        super().stretch(factor, dim, **kwargs)
        if dim == 0:
            self.reposition_labels()
        return self

    def float_to_index(self, value: float):
        """
        Given a value in [0, 1], returns the index of the
        corresponding event from the distribution
        """
        for idx, upper_value in enumerate(self.cdf):
            if value < upper_value:
                return idx
        # Otherwise, last element
        return len(self.distribution) - 1



# ----- From _2026/cross_entropy/robot.py -----

PURE_MAGENTA = "#FF00FF"


class InstructionArrow(SVGMobject):
    def __init__(self, direction=RIGHT, *args, **kwargs):
        super().__init__("images/arrow.svg", *args, **kwargs)
        if (direction == UP).all():
            self.rotate(PI / 2)
        elif (direction == LEFT).all():
            self.rotate(PI)
        elif (direction == DOWN).all():
            self.rotate(3 * PI / 2)
        self.direction = direction


def generate_random_instructions(n, distribution, seed=0):
    np.random.seed(seed)
    instructions = []
    for _ in range(n):
        x = np.random.random()
        for i in range(len(distribution)):
            if x < sum(distribution[:i + 1]):
                instructions.append(i)
                break
    return instructions


class RobotEncodingsV2(InteractiveScene):
    def construct(self):
        # Add mission_control and the robot
        mission_control = ImageMobject(
            "images/pi_creature_mission_control.png"
        ).set_width(2).to_edge(RIGHT, buff=0.4).to_edge(DOWN, buff=0.6)
        robot = ImageMobject(
            "images/lunar_rover_assets/stationary.png"
        ).match_height(mission_control).to_edge(LEFT, buff=0.4).align_to(mission_control, DOWN)
        self.add(mission_control, robot)
        self.wait(2)

        # Create a stream of bits flowing towards the bot, and decode them into instructions by chunks of 2
        distribution = [1 / 2, 1 / 4, 1 / 8, 1 / 8]
        instructions = [1, 0, 2]  # Start with DOWN, UP, LEFT = 100110 with perfect encoding
        instructions += generate_random_instructions(13, distribution, seed=7)  # 16 total instructions
        instructions[-3] = 3
        bit_string = ""
        for instruction in instructions:
            bit_string += f"{instruction:02b}"
        bit_buff = 0.1
        bits = VGroup(*[
            Tex(bit_string[i], font_size=32)
            for i in range(len(bit_string))
        ]).arrange(buff=bit_buff).set_color(YELLOW).match_y(robot).align_to(mission_control, LEFT)
        bits_opacity_tracker = ValueTracker(0)

        def update_bits(m):
            for bit in m:
                bit.set_opacity(bits_opacity_tracker.get_value() * min(1, max(0, 0.8 * (mission_control.get_left()[0] - bit.get_x()))))
                if bit.get_x() < robot.get_x():
                    bit.set_opacity(0)
            self.bring_to_front(robot)
        bits.add_updater(update_bits)

        rects = VGroup(*[
            SurroundingRectangle(bits[i:i + 2], stroke_width=2, stroke_color=WHITE, buff=bit_buff * 0.5)
            for i in range(0, len(bit_string), 2)
        ])
        for rect in rects:
            rect.stretch_to_fit_height(rects[0].get_height())
        rect_opacity_trackers = [ValueTracker(0) for _ in range(4)]

        def update_rects(m):
            for i, rect in enumerate(m):
                target_bits = bits[2 * i:2 * (i + 1)]
                rect.match_x(target_bits)
                rect.set_stroke(
                    opacity=rect_opacity_trackers[
                        instructions[i]
                    ].get_value() * min(1, max(0, 0.8 * (mission_control.get_left()[0] - (rect.get_x() + 0.2))))
                )
                if rect.get_x() < robot.get_x():
                    rect.set_stroke(opacity=0)
        rects.add_updater(update_rects)

        arrows = VGroup(*[
            InstructionArrow([UP, DOWN, LEFT, RIGHT][instructions[i]]).scale(0.07).move_to(rects[i]).shift(UP * 0.62)
            for i in range(len(instructions))
        ])
        arrows_opacity_tracker = ValueTracker(1)

        def update_arrows(m):
            for i, arrow in enumerate(m):
                target_bits = bits[2 * i:2 * (i + 1)]
                arrow.match_x(target_bits)
                opacity = min(1, max(0, 0.8 * (mission_control.get_left()[0] - (arrow.get_x() + 0.2))))
                if arrow.get_x() < robot.get_right()[0]:
                    opacity = min(1, max(0, 1 - 1.2 * (robot.get_right()[0] - arrow.get_x())))
                arrow.set_opacity(arrows_opacity_tracker.get_value() * opacity)
        arrows.add_updater(update_arrows)

        self.add(bits, rects, arrows)
        self.play(
            AnimationGroup(
                bits.animate(run_time=40, rate_func=smooth).align_to(robot.get_right() + RIGHT * 0.2, LEFT),
                bits_opacity_tracker.animate.set_value(1), lag_ratio=0.65, rate_func=linear)
        )

        # Show the naive encoding
        table = VGroup(*[
            VGroup(
                Tex(f"{i:02b}").set_color(YELLOW),
                Tex(":"),
                InstructionArrow(direction=[UP, DOWN, LEFT, RIGHT][i]).scale(0.15)
            ).arrange()
            for i in range(4)
        ])
        table.arrange(DOWN)
        for row in table:
            row.shift(RIGHT * (table[0][1].get_x() - row[1].get_x()))
        for i, row in enumerate(table):
            row[2].match_x(table[2][2])
            row.set_y(table[0].get_y() + i * (table[1].get_y() - table[0].get_y()))
        table.set_width(2).to_edge(RIGHT, buff=2).to_edge(UP, buff=0.7)
        table_box = SurroundingRectangle(table, buff=0.15).set_color(WHITE).set_stroke(opacity=0)

        arrows.save_state()
        for i, row in enumerate(table):
            anims = []
            anims.append(FadeIn(row))
            anims.append(rect_opacity_trackers[i].animate.set_value(1))
            if i == 0:
                anims.append(table_box.animate.set_stroke(opacity=1))
            else:
                anims.append(rect_opacity_trackers[i - 1].animate(run_time=1).set_value(0))
                anims.append(
                    AnimationGroup(*[
                        arrow.animate(run_time=1).set_color(WHITE if instructions[j] == i else YELLOW)
                        for j, arrow in enumerate(arrows)
                    ])
                )
            self.play(AnimationGroup(*anims, run_time=2))
        self.wait(1)
        self.play(arrows.animate.restore(), run_time=2)
        self.wait(2)

        self.play(AnimationGroup(*[t.animate.set_value(1) for t in rect_opacity_trackers]), run_time=2)

        # Transform the table into a stacked bar diagram
        naive_chart = EntropyChart(
            distribution,
            event_labels=VGroup(*[InstructionArrow([UP, DOWN, LEFT, RIGHT][i]) for i in range(4)]),
            probability_labels=[
                Tex(R"\frac{1}{" + ["2", "4", "8", "8"][i] + "}", font_size=80)
                for i in range(4)
            ],
            bar_labels=[
                Tex(["00", "01", "10", "11"][i], font_size=90)
                for i in range(4)
            ],
            bar_heights=[2, 2, 2, 2],
            width=9,
            include_vertical_axis=False,
            segments_height=1,
            fill_colors=[YELLOW_B, YELLOW_D]
        ).match_height(table).scale(0.5).match_y(table).align_to(table, RIGHT).shift(RIGHT)
        naive_chart.bar_labels.set_color(WHITE)
        naive_chart.update()
        self.wait(0.01)
        naive_chart.suspend_updating()
        self.play(
            AnimationGroup(
                FadeOut(VGroup(table_box, *[row[1] for row in table])),
                AnimationGroup(
                    FadeIn(naive_chart.segments.bars),
                    AnimationGroup(*[
                        ReplacementTransform(table[i][2], naive_chart.event_labels[i])
                        for i in range(len(table))
                    ]),
                    FadeIn(naive_chart.probability_labels),
                    AnimationGroup(*[
                        ReplacementTransform(table[i][0], naive_chart.bar_labels[i])
                        for i in range(len(table))
                    ])
                ), lag_ratio=0.4)
        )
        self.play(
            AnimationGroup(
                naive_chart.create_bars(),
                naive_chart.bar_labels.animate.set_color(BLACK), lag_ratio=0.5)
        )
        self.wait(1.8)

        # Contrast the naive example vs the better one
        encoding = ["0", "10", "110", "111"]
        huffman_chart = EntropyChart(
            distribution,
            event_labels=VGroup(*[InstructionArrow([UP, DOWN, LEFT, RIGHT][i]) for i in range(4)]).set_color(PINK),
            probability_labels=[
                Tex(R"\frac{1}{" + ["2", "4", "8", "8"][i] + "}", font_size=80)
                for i in range(4)
            ],
            bar_labels=[
                Tex(encoding[i], font_size=60)
                for i in range(4)
            ],
            bar_heights=[1, 2, 3, 3],
            width=9,
            height=6,
            include_vertical_axis=False,
            segments_height=1,
            fill_colors=[PURE_MAGENTA, LIGHT_PINK]
        ).match_width(naive_chart)
        huffman_chart.bar_labels.set_color(WHITE)
        huffman_chart.update()
        self.wait(0.01)
        naive_chart.clear_updaters()
        huffman_chart.clear_updaters()

        naive_chart.generate_target()
        VGroup(naive_chart.target, huffman_chart).arrange(buff=3)
        huffman_chart.align_to(naive_chart.target, DOWN)
        rects.clear_updaters()
        arrows.clear_updaters()
        bits.clear_updaters()
        naive_encoding_text = TexText("Naive").next_to(naive_chart.target, UP, buff=1.4)
        new_encoding_text = TexText("Optimized").match_x(huffman_chart).match_y(naive_encoding_text)
        VGroup(naive_chart.target, huffman_chart, naive_encoding_text, new_encoding_text).set_y(0)
        arrow = Arrow(
            naive_chart.target.bars.get_right() + RIGHT * 0.2,
            [huffman_chart.bars.get_left()[0] - 0.2, naive_chart.target.bars.get_y(), 0]
        )
        huffman_chart.bars.set_opacity(0.2)
        self.play(
            AnimationGroup(
                FadeOut(Group(robot, rects, arrows, bits, mission_control)),
                AnimationGroup(MoveToTarget(naive_chart, path_arc=PI * 0.2), FadeIn(naive_encoding_text), lag_ratio=0.8),
                GrowArrow(arrow),
                AnimationGroup(
                    AnimationGroup(*[
                        FadeIn(VGroup(segment, arrow, prob, bar))
                        for segment, arrow, prob, bar in zip(
                            huffman_chart.segments.bars,
                            huffman_chart.event_labels,
                            huffman_chart.probability_labels,
                            huffman_chart.bars
                        )
                    ], lag_ratio=0.2),
                    FadeIn(new_encoding_text), lag_ratio=0.3), lag_ratio=0.4), run_time=6.5)
        self.wait(2)
        circ = Circle(
            radius=0.47, fill_opacity=0, stroke_width=3, stroke_color=GREEN
        ).move_to(huffman_chart.probability_labels[0])
        self.play(ShowCreation(circ))
        self.play(FadeOut(circ))
        self.wait(2)

        for i in range(4):
            self.play(huffman_chart.bars[i].animate.set_opacity(1), FadeIn(huffman_chart.bar_labels[i]), run_time=2)
            self.wait(2)
        self.wait(2)

        # Compare the longer strings from the new code with the naive code
        naive_chart.save_state()
        huffman_chart.save_state()
        arrow.save_state()
        self.play(
            VGroup(
                arrow,
                huffman_chart.bars[:2],
                huffman_chart.bar_labels[:2],
                huffman_chart.segments.bars[:2],
                huffman_chart.event_labels[:2],
                huffman_chart.probability_labels[:2]
            ).animate.fade(0.8),
            naive_chart.animate.fade(0.8)
        )
        self.wait(2)
        naive_chart.generate_target()
        naive_chart.target.restore()
        VGroup(
            naive_chart.target.bars[:2],
            naive_chart.target.bar_labels[:2],
            naive_chart.target.segments.bars[:2],
            naive_chart.target.event_labels[:2],
            naive_chart.target.probability_labels[:2]
        ).fade(0.8)
        self.play(MoveToTarget(naive_chart))
        self.wait(2)
        naive_chart.generate_target()
        naive_chart.target.restore()
        VGroup(
            naive_chart.target.bars[1:],
            naive_chart.target.bar_labels[1:],
            naive_chart.target.segments.bars[1:],
            naive_chart.target.event_labels[1:],
            naive_chart.target.probability_labels[1:]
        ).fade(0.8)
        huffman_chart.generate_target()
        huffman_chart.target.restore()
        VGroup(
            huffman_chart.target.bars[1:],
            huffman_chart.target.bar_labels[1:],
            huffman_chart.target.segments.bars[1:],
            huffman_chart.target.event_labels[1:],
            huffman_chart.target.probability_labels[1:]
        ).fade(0.8)
        self.play(MoveToTarget(naive_chart), MoveToTarget(huffman_chart))
        self.wait(2)
        self.play(arrow.animate.restore(), naive_chart.animate.restore(), huffman_chart.animate.restore(), run_time=2)

        # Show the sample sequence of instructions again
        self.play(
            FadeOut(arrow, run_time=1),
            VGroup(naive_encoding_text, new_encoding_text).animate(run_time=2).to_edge(UP, buff=0.5),
            VGroup(naive_chart, huffman_chart).animate(run_time=2).shift(UP * 1.7)
        )
        sample_instruction_arrows = arrows.copy().set_color(WHITE).set_width(FRAME_WIDTH * 0.75).to_edge(DOWN, buff=1.5).set_x(0)
        self.play(
            AnimationGroup(*[
                FadeIn(arrow, shift=UP * 0.2)
                for arrow in sample_instruction_arrows
            ], lag_ratio=0.1)
        )
        self.wait(2)

        # Highlight the ups, downs, lefts, and rights
        for direction in [UP, DOWN, LEFT, RIGHT]:
            self.play(
                AnimationGroup(*[
                    arrow.animate.set_opacity(1 if (arrow.direction == direction).all() else 0.1)
                    for arrow in sample_instruction_arrows
                ])
            )
            self.wait(2)
        self.play(sample_instruction_arrows.animate.set_opacity(1))

        # Show the two examples side by side
        arrows.clear_updaters()
        rects.clear_updaters()
        bits.clear_updaters()
        naive_chart.generate_target()
        naive_example_group = Group(robot, Group(arrows, rects, bits), mission_control, naive_chart.target)
        naive_example_group.scale(1.3)
        naive_example_group.arrange(buff=0.6).to_edge(UP, buff=0.7).set_width(FRAME_WIDTH * 0.96)
        naive_example_group[1].shift(
            DOWN * (naive_example_group[1][2].get_y() - naive_example_group.get_y())
        )
        naive_example_group[2].align_to(naive_example_group[0], DOWN)
        naive_example_group[3].shift(DOWN * 0.4)
        naive_example_group.to_edge(UP, buff=0.7).set_x(0)

        robot_2 = robot.copy()
        arrows_2 = arrows.copy().set_color(PINK)
        mission_control_2 = mission_control.copy()
        huffman_chart.generate_target()
        huffman_chart.target.match_width(
            naive_chart.target
        ).match_x(
            naive_chart.target
        ).shift(
            DOWN * (huffman_chart.segments.get_bottom()[1] - mission_control_2.get_bottom()[1])
        )
        Group(robot_2, arrows_2, mission_control_2, huffman_chart.target).to_edge(DOWN, buff=0.4)

        self.play(
            AnimationGroup(
                AnimationGroup(
                    AnimationGroup(
                        MoveToTarget(naive_chart, path_arc=-PI * 0.2),
                        naive_encoding_text.animate.scale(0.7).next_to(arrows, DOWN, buff=1),
                        AnimationGroup(
                            ReplacementTransform(sample_instruction_arrows.copy().set_opacity(0), naive_example_group[1][0]),
                            AnimationGroup(
                                FadeIn(naive_example_group[0]),
                                FadeIn(naive_example_group[1][1:]),
                                FadeIn(naive_example_group[2])
                            ), lag_ratio=0.5), run_time=2.5),
                    AnimationGroup(
                        MoveToTarget(huffman_chart, path_arc=-PI * 0.2),
                        new_encoding_text.animate.scale(0.7).set_opacity(0.1).next_to(arrows_2, DOWN, buff=1),
                        AnimationGroup(
                            ReplacementTransform(sample_instruction_arrows, arrows_2),
                            AnimationGroup(
                                FadeIn(robot_2),
                                FadeIn(mission_control_2)
                            ), lag_ratio=0.5), run_time=2.5)
                ), lag_ratio=0.4)
        )

        # Encode the new sequence with the Huffman code
        bit_string = ""
        for instruction in instructions:
            bit_string += encoding[instruction]
        bits_2 = VGroup(*[
            Tex(bit_string[i])
            for i in range(len(bit_string))
        ]).set_color(PINK).match_height(bits)
        bits_2.set_y(robot_2.get_y() + (bits.get_y() - robot.get_y()))

        def update_bits_2(m):
            for bit in m:
                if bit.get_x() < robot_2.get_x():
                    bit.set_opacity(0)
            self.bring_to_front(robot_2)
        bits_2.add_updater(update_bits_2)
        index = 0
        bit_groups = VGroup()
        for instruction, arrow in zip(instructions, arrows):
            code_word_length = 1 if instruction == 0 else 2 if instruction == 1 else 3
            target_bits = bits_2[index:index + code_word_length]
            target_bits.arrange(center=False, buff=0).match_x(arrow)
            bit_groups.add(target_bits)
            index += code_word_length
        self.play(
            new_encoding_text.animate(run_time=2).set_opacity(1),
            AnimationGroup(*[
                TransformMatchingShapes(huffman_chart.bar_labels[instructions[i]].copy(), grouping, path_arc=PI * 0.1)
                for i, grouping in enumerate(bit_groups)
            ], lag_ratio=0.08, run_time=6)
        )
        self.wait(1)

        def update_arrows_2(m):
            index = 0
            for arrow, instruction in zip(m, instructions):
                code_word_length = 1 if instruction == 0 else 2 if instruction == 1 else 3
                target_bits = bits_2[index:index + code_word_length]
                arrow.match_x(target_bits)
                if arrow.get_x() < robot_2.get_right()[0]:
                    arrow.set_opacity(min(1, max(0, 1 - 1.2 * (robot_2.get_right()[0] - arrow.get_x()))))
                index += code_word_length

        arrows_2.add_updater(update_arrows_2)

        rects_2 = VGroup(*[Rectangle() for _ in instructions])
        rects_2_opacity_tracker = ValueTracker(0)

        def update_rects_2(m):
            index = 0
            for i, rect in enumerate(m):
                instruction = instructions[i]
                code_word_length = 1 if instruction == 0 else 2 if instruction == 1 else 3
                target_bits = bits_2[index:index + code_word_length]
                rect.become(
                    SurroundingRectangle(
                        target_bits,
                        stroke_width=2,
                        stroke_color=WHITE,
                        stroke_opacity=rects_2_opacity_tracker.get_value(),
                        buff=0.5 * (bits_2[1].get_left()[0] - bits_2[0].get_right()[0])
                    )
                )
                if i > 0:
                    rect.stretch_to_fit_height(rects_2[0].get_height())
                if rect.get_x() < robot_2.get_x():
                    rect.set_stroke(opacity=0)
                index += code_word_length
        rects_2.add_updater(update_rects_2)
        self.add(rects_2)

        self.play(
            AnimationGroup(
                AnimationGroup(*[
                    bit_2.animate.match_x(bit)
                    for bit_2, bit in zip(bits_2, bits)
                ]),
                rects_2_opacity_tracker.animate.set_value(1), lag_ratio=0.5)
        )
        self.wait(0.5)
        bits_2.suspend_updating()
        rects_2.suspend_updating()
        arrows_2.suspend_updating()

        # Focus on the perfect example
        self.add(huffman_chart)
        perfect_example_group = Group(robot_2, Group(arrows_2, rects_2, bits_2), mission_control_2, huffman_chart)
        self.play(
            AnimationGroup(
                FadeOut(Group(naive_example_group[:-1], naive_chart), shift=UP, run_time=2),
                FadeOut(VGroup(naive_encoding_text, new_encoding_text), shift=DOWN * 0.2, run_time=1),
                perfect_example_group[-1].animate(path_arc=PI * 0.2, run_time=2).scale(1.2).to_edge(UP, buff=1).to_edge(RIGHT, buff=1),
                perfect_example_group[:-1].animate(run_time=2).set_width(FRAME_WIDTH * 0.9).set_x(0).to_edge(DOWN, buff=0.4), lag_ratio=0.1)
        )

        # Introduce "code word" term
        code_words_text = Tex(R"\text{code words}").next_to(huffman_chart, UP).set_color(WHITE).fix_in_frame()
        huffman_chart.clear_updaters()
        huffman_chart.fix_in_frame()
        huffman_chart.bar_labels.add_updater(lambda m: self.bring_to_front(m))
        huffman_chart.save_state()
        self.play(
            Write(code_words_text, run_time=1.5),
            VGroup(huffman_chart.bars, huffman_chart.segments, huffman_chart.probability_labels).animate.fade(0.8)
        )

        self.camera.frame.save_state()
        self.play(
            self.camera.frame.animate.scale(0.7, about_point=robot_2.get_corner(DL) + DOWN * 0.3).shift(UR * 0.2),
            FadeOut(VGroup(arrows_2, rects_2)), run_time=2)

        self.wait(1.2)
        huffman_chart.clear_updaters()
        self.play(huffman_chart.animate.restore(), run_time=2)

        # Break down the first code word
        self.play(
            bits_2[0].animate.set_color(PURE_GREEN),
            bits_2[1:].animate.set_opacity(0.2)
        )
        self.wait(1)
        huffman_chart.bar_labels.save_state()
        self.play(
            huffman_chart.bar_labels[0].animate.set_opacity(0.2),
            huffman_chart.bars[0].animate.set_opacity(0.2),
            huffman_chart.segments.bars[0].animate.set_opacity(0.2),
            huffman_chart.event_labels[0].animate.set_opacity(0.2),
            huffman_chart.probability_labels[0].animate.set_opacity(0.2),
            AnimationGroup(*[huffman_chart.bar_labels[i][0].animate.set_color(PURE_GREEN) for i in range(1, 4)]), run_time=0.3)
        self.wait(1)
        self.play(bits_2[1].animate.set_opacity(1).set_color(PURE_GREEN))
        self.wait(1)
        self.play(
            huffman_chart.bar_labels[2:].animate.set_opacity(0.2),
            huffman_chart.bars[2:].animate.set_opacity(0.2),
            huffman_chart.segments.bars[2:].animate.set_opacity(0.2),
            huffman_chart.event_labels[2:].animate.set_opacity(0.2),
            huffman_chart.probability_labels[2:].animate.set_opacity(0.2),
            huffman_chart.bar_labels[1][1].animate.set_color(PURE_GREEN), run_time=0.3)
        self.play(FadeIn(VGroup(rects_2[0], arrows_2[0])))
        self.wait(0.5)

        # Do the second chunk
        self.play(
            AnimationGroup(*[
                bit.animate.set_color(PURE_GREEN if i == 2 else PINK).set_opacity(0.2 if i > 2 else 1)
                for i, bit in enumerate(bits_2)
            ]),
            huffman_chart.animate.restore()
        )
        self.wait(1)
        self.play(
            huffman_chart.bar_labels[1:].animate.set_opacity(0.2),
            huffman_chart.bars[1:].animate.set_opacity(0.2),
            huffman_chart.segments.bars[1:].animate.set_opacity(0.2),
            huffman_chart.event_labels[1:].animate.set_opacity(0.2),
            huffman_chart.probability_labels[1:].animate.set_opacity(0.2),
            huffman_chart.bar_labels[0][0].animate.set_color(PURE_GREEN), run_time=0.3)
        self.play(FadeIn(VGroup(rects_2[1], arrows_2[1])))

        # Do the third chunk
        self.play(
            AnimationGroup(*[
                bit.animate.set_color(PURE_GREEN if i == 3 else PINK).set_opacity(0.2 if i > 3 else 1)
                for i, bit in enumerate(bits_2)
            ]),
            huffman_chart.animate.restore()
        )
        self.wait(1)
        self.play(
            huffman_chart.bar_labels[0].animate.set_opacity(0.2),
            huffman_chart.bars[0].animate.set_opacity(0.2),
            huffman_chart.segments.bars[0].animate.set_opacity(0.2),
            huffman_chart.event_labels[0].animate.set_opacity(0.2),
            huffman_chart.probability_labels[0].animate.set_opacity(0.2),
            AnimationGroup(*[huffman_chart.bar_labels[i][0].animate.set_color(PURE_GREEN) for i in range(1, 4)]), run_time=0.3)
        self.wait(0.5)
        self.play(bits_2[4].animate.set_color(PURE_GREEN).set_opacity(1))
        self.play(
            huffman_chart.bar_labels[1].animate.set_opacity(0.2),
            huffman_chart.bars[1].animate.set_opacity(0.2),
            huffman_chart.segments.bars[1].animate.set_opacity(0.2),
            huffman_chart.event_labels[1].animate.set_opacity(0.2),
            huffman_chart.probability_labels[1].animate.set_opacity(0.2),
            AnimationGroup(*[huffman_chart.bar_labels[i][1].animate.set_color(PURE_GREEN) for i in range(2, 4)]), run_time=0.3)
        self.wait(0.5)
        self.play(bits_2[5].animate.set_color(PURE_GREEN).set_opacity(1))
        self.play(
            huffman_chart.bar_labels[3].animate.set_opacity(0.2),
            huffman_chart.bars[3].animate.set_opacity(0.2),
            huffman_chart.segments.bars[3].animate.set_opacity(0.2),
            huffman_chart.event_labels[3].animate.set_opacity(0.2),
            huffman_chart.probability_labels[3].animate.set_opacity(0.2),
            huffman_chart.bar_labels[2][2].animate.set_color(PURE_GREEN), run_time=0.3)
        self.play(FadeIn(VGroup(rects_2[2], arrows_2[2])))

        # Show all the chunks being decoded
        self.play(
            huffman_chart.animate.restore(),
            bits_2.animate.set_color(PINK).set_opacity(1),
            FadeIn(rects_2[3:]),
            FadeIn(arrows_2[3:].set_opacity(1))
        )
        bits_2.resume_updating()
        arrows_2.resume_updating()
        rects_2.resume_updating()
        self.add(bits_2, arrows_2, rects_2)
        self.play(
            self.camera.frame.animate(run_time=3).restore(),
            rects_2_opacity_tracker.animate.set_value(1),
            bits_2.animate(run_time=7.5).align_to(robot.get_center(), RIGHT)
        )

        # Show prefix rule
        huffman_chart.save_state()
        code_word_1 = Tex("10", font_size=80)
        code_word_2 = Tex("100", font_size=80).next_to(code_word_1, DOWN, buff=0.8).align_to(code_word_1, LEFT)
        VGroup(code_word_1, code_word_2).center()
        background = Group(robot_2, code_words_text, mission_control_2)
        background.save_state()
        self.play(Group(huffman_chart, background).animate.fade(0.9))
        self.play(FadeIn(code_word_1))
        self.play(FadeIn(code_word_2))
        self.play(code_word_1[:2].animate.set_color(RED), code_word_2[:2].animate.set_color(RED))

        # Contemplate adding a 5th instruction
        fifth_instruction_chart = EntropyChart(
            [40 / 90, 20 / 90, 10 / 90, 10 / 90, 10 / 90],
            event_labels=VGroup(
                *[InstructionArrow([UP, DOWN, LEFT, RIGHT][i]) for i in range(4)],
                SVGMobject("clockwise.svg").scale(2).set_stroke(width=2, behind=True)
            ).set_color(PINK),
            probability_labels=None,
            bar_labels=[
                Tex(encoding[i], font_size=60)
                for i in range(4)
            ] + [Tex("100", font_size=60)],
            bar_heights=[1, 2, 3, 3, 3],
            width=9,
            height=13.5,
            include_vertical_axis=False,
            segments_height=1,
            fill_colors=[PURE_MAGENTA, LIGHT_PINK]
        )
        fifth_instruction_chart.clear_updaters()
        fifth_instruction_chart.fix_in_frame().match_width(huffman_chart).match_x(huffman_chart).align_to(huffman_chart, UP)
        self.play(
            AnimationGroup(
                AnimationGroup(
                    background.animate.restore(),
                    code_word_1.animate.match_width(fifth_instruction_chart.bar_labels[1]).move_to(fifth_instruction_chart.bar_labels[1]).set_color(BLACK),
                    code_word_2.animate.match_width(fifth_instruction_chart.bar_labels[-1]).move_to(fifth_instruction_chart.bar_labels[-1]).set_color(BLACK)
                ),
                AnimationGroup(
                    ReplacementTransform(huffman_chart.bars[:4], fifth_instruction_chart.bars[:4]),
                    ReplacementTransform(huffman_chart.bar_labels[:4], fifth_instruction_chart.bar_labels[:4]),
                    ReplacementTransform(huffman_chart.segments.bars[:4], fifth_instruction_chart.segments.bars[:4]),
                    ReplacementTransform(huffman_chart.event_labels[:4], fifth_instruction_chart.event_labels[:4]),
                    FadeOut(huffman_chart.probability_labels),
                    FadeIn(
                        VGroup(
                            fifth_instruction_chart.bars[-1],
                            fifth_instruction_chart.bar_labels[-1],
                            fifth_instruction_chart.segments.bars[-1],
                            fifth_instruction_chart.event_labels[-1]
                        ),
                        shift=LEFT * 0.5
                    )
                ), lag_ratio=0.3, run_time=2)
        )

        # Show how it fails
        bit_string = "10•••••••••••••••"
        bits_3 = VGroup(*[
            Text(b, font_size=40) for b in bit_string]
        ).set_color(PINK).arrange(buff=bit_buff).align_to(mission_control_2, LEFT)
        for bit in bits_3[2:]:
            bit.scale(0.6)
        bits_3.match_y(bits_2)
        bits_opacity_tracker = ValueTracker(0)

        def update_bits_3(m):
            for bit in m:
                bit.set_opacity(bits_opacity_tracker.get_value() * min(1, max(0, 0.8 * (mission_control_2.get_left()[0] - bit.get_x()))))
                if bit.get_x() < robot_2.get_x():
                    bit.set_opacity(0)
            self.bring_to_front(robot_2)
        bits_3.add_updater(update_bits_3)
        self.add(bits_3)

        self.play(
            bits_3.animate(run_time=6).align_to(robot_2.get_right(), LEFT).shift(RIGHT * 0.3),
            bits_opacity_tracker.animate(run_time=2).set_value(1)
        )
        bits_3.suspend_updating()
        self.wait(2)

        fifth_instruction_chart.save_state()
        self.play(
            bits_3[:2].animate.set_color(PURE_GREEN),
            fifth_instruction_chart.animate.fade(0.8),
            VGroup(
                fifth_instruction_chart.bars[1],
                fifth_instruction_chart.bar_labels[1],
                fifth_instruction_chart.segments.bars[1],
                fifth_instruction_chart.event_labels[1]
            ).animate.shift(0)
        )
        self.wait(2)
        self.play(
            bits_3[2].animate.become(Integer(0).match_height(bits_3[1]).match_y(bits_3[1]).match_x(bits_3[2]).set_color(YELLOW)),
            fifth_instruction_chart.animate.restore().fade(0.8),
            VGroup(
                fifth_instruction_chart.bars[-1],
                fifth_instruction_chart.bar_labels[-1],
                fifth_instruction_chart.segments.bars[-1],
                fifth_instruction_chart.event_labels[-1]
            ).animate.set_opacity(1)
        )
        self.wait(2)

        # Robot gets confused
        question_mark = Tex(
            "?", font_size=80
        ).set_color(
            LIGHT_BROWN
        ).next_to(robot_2, UP, buff=0)
        self.play(FadeIn(question_mark, shift=DOWN * 0.05))
        self.wait(1)

        # Bring back the original chart
        huffman_chart.restore()
        self.play(
            FadeOut(VGroup(bits_3, question_mark)),
            ReplacementTransform(fifth_instruction_chart.bars[:4], huffman_chart.bars[:4]),
            ReplacementTransform(fifth_instruction_chart.bar_labels[:4], huffman_chart.bar_labels[:4]),
            ReplacementTransform(fifth_instruction_chart.segments.bars[:4], huffman_chart.segments.bars[:4]),
            ReplacementTransform(fifth_instruction_chart.event_labels[:4], huffman_chart.event_labels[:4]),
            FadeIn(huffman_chart.probability_labels),
            FadeOut(
                VGroup(
                    fifth_instruction_chart.bars[-1],
                    fifth_instruction_chart.segments.bars[-1],
                    fifth_instruction_chart.event_labels[-1],
                    fifth_instruction_chart.bar_labels[-1]
                ),
                shift=RIGHT * 0.5
            ), run_time=2)

        # Fade out everything but the chart
        self.remove(bits_2, rects_2, arrows_2)
        self.play(
            FadeOut(code_words_text),
            FadeOut(Group(robot_2, mission_control_2), shift=DOWN),
            huffman_chart.animate(path_arc=PI * 0.1).scale(1.2).align_to(huffman_chart, RIGHT).center(), run_time=2)
        self.wait(3)

        # Calculate the efficiency of the Huffman code
        self.wait(2)
        weighted_sum_lines = VGroup(
            Tex(R"\frac{1}{2} \cdot 1", font_size=30).next_to(huffman_chart.bars[0], UP),
            Tex(R"\frac{1}{4} \cdot 2", font_size=30).next_to(huffman_chart.bars[1], UP),
            Tex(R"\frac{1}{8} \cdot 3", font_size=30).next_to(huffman_chart.bars[2], UP),
            Tex(R"\frac{1}{8} \cdot 3", font_size=30).next_to(huffman_chart.bars[3], UP)
        )
        self.play(
            AnimationGroup(
                TransformFromCopy(huffman_chart.probability_labels[0], weighted_sum_lines[0][:-2]),
                FadeIn(weighted_sum_lines[0][-2:], shift=UP * 0.1), run_time=1.5)
        )
        self.wait(1.5)
        self.play(
            AnimationGroup(
                TransformFromCopy(huffman_chart.probability_labels[1], weighted_sum_lines[1][:-2]),
                FadeIn(weighted_sum_lines[1][-2:], shift=UP * 0.1), run_time=1.5)
        )
        self.wait(2.5)
        self.play(
            AnimationGroup(*[
                AnimationGroup(
                    TransformFromCopy(label, line[:-2]),
                    FadeIn(line[-2:], shift=UP * 0.1), run_time=1.5)
                for label, line in zip(huffman_chart.probability_labels[2:], weighted_sum_lines[2:])
            ], lag_ratio=0.3)
        )
        self.wait(0.35)

        # Show the weighted sum result
        sum_result = Tex(
            R"\frac{1}{2} \cdot 1 + \frac{1}{4} \cdot 2 + \frac{1}{8} \cdot 3 + \frac{1}{8} \cdot 3 \\ = 1.75 \text{ bits}",
            font_size=49
        )
        sum_result[-9:].align_to(sum_result[:-9], RIGHT)
        sum_result.to_edge(RIGHT, buff=1.2)

        self.play(
            huffman_chart.animate.scale(0.8).to_edge(LEFT, buff=1),
            TransformMatchingShapes(weighted_sum_lines, sum_result[:-9], path_arc=PI * 0.2, run_time=1.5)
        )
        self.wait(0.5)
        self.play(FadeIn(sum_result[R"= 1.75 \text{ bits}"]))

        # Compare to the naive encoding
        huffman_group = VGroup(huffman_chart, sum_result)
        naive_sum_result = Tex(
            R"\frac{1}{2} \cdot 2 + \frac{1}{4} \cdot 2 + \frac{1}{8} \cdot 2 + \frac{1}{8} \cdot 2 \\ = 2 \text{ bits}",
            font_size=49
        )
        naive_sum_result[-6:].align_to(naive_sum_result[:-6], RIGHT)
        naive_sum_result.to_edge(RIGHT, buff=1.2)
        naive_chart.match_width(huffman_chart).move_to(huffman_chart)
        for label in naive_chart.bar_labels:
            label.match_height(huffman_chart.bar_labels[0])
        naive_group = VGroup(naive_chart, naive_sum_result).to_edge(UP, buff=1)

        huffman_group.generate_target()
        huffman_group.target[0].scale(0.7)
        huffman_group.target.arrange(buff=1).to_edge(DOWN, buff=0.7)
        naive_group[0].scale(0.7)
        naive_group.arrange(buff=1).to_edge(UP, buff=0.7)
        naive_group.to_edge(UP, buff=0.7)

        huffman_group.save_state()
        self.play(
            MoveToTarget(huffman_group),
            FadeIn(naive_group, shift=DOWN), run_time=1.5)
        self.wait(3)

        # Bring the huffman code back to focus
        self.play(
            huffman_group.animate.restore(),
            FadeOut(naive_group, shift=UP), run_time=1.5)
        self.wait(3)

        # Put away the calculation and focus on the chart
        self.play(FadeOut(sum_result, shift=RIGHT * 3), huffman_chart.animate.set_x(0).to_edge(DOWN, buff=0.7), run_time=1.5)
        self.wait(3)

        # Show a message that looks like random noise
        mission_control_and_robot_group = Group(
            robot.scale(0.8).to_edge(LEFT, buff=0.7),
            mission_control.scale(0.8).to_edge(RIGHT, buff=0.7)
        ).set_x(0).to_edge(UP, buff=0.5)
        robot = mission_control_and_robot_group[0]
        mission_control = mission_control_and_robot_group[1]
        message = VGroup(*[
            Integer(0).set_color(YELLOW)
            for _ in range(42)
        ]).arrange(
            buff=0.08
        ).set_width(
            mission_control_and_robot_group.get_width() * 0.76
        ).match_y(
            mission_control
        ).match_x(
            mission_control_and_robot_group
        ).shift(
            RIGHT * 0.1
        )
        bit_opacity_trackers = [ValueTracker(0) for _ in message]
        for i, bit in enumerate(message):
            def update_bit(m, i=i):
                m.set_value(random.choice([0, 1])).set_opacity(bit_opacity_trackers[i].get_value())
            bit.add_updater(update_bit)
        self.add(message)
        self.play(
            AnimationGroup(*[t.animate.set_value(1) for t in bit_opacity_trackers]),
            FadeIn(mission_control_and_robot_group)
        )
        self.wait(1)

        # Show the probability of the first bit being 0 vs 1
        arrow = Arrow(ORIGIN, UP).set_color(WHITE).next_to(message[0], DOWN)
        huffman_chart.save_state()
        self.play(
            GrowArrow(arrow),
            AnimationGroup(*[t.animate.set_value(0.2) for t in bit_opacity_trackers[1:]]),
            huffman_chart.bars[1:].animate.set_opacity(0.2),
            huffman_chart.bar_labels[1:].animate.set_opacity(0.2),
            huffman_chart.segments.bars[1:].animate.set_opacity(0.2),
            huffman_chart.event_labels[1:].animate.set_opacity(0.2),
            huffman_chart.probability_labels[1:].animate.set_opacity(0.2)
        )
        message[0].suspend_updating()
        message[0].set_value(0)
        self.play(message[0].animate.set_color(PURE_GREEN))
        self.wait(1.5)
        self.play(
            message[0].animate.set_value(1),
            huffman_chart.animate.restore(),
            huffman_chart.bars[0].animate.set_opacity(0.2),
            huffman_chart.bar_labels[0].animate.set_opacity(0.2),
            huffman_chart.segments.bars[0].animate.set_opacity(0.2),
            huffman_chart.event_labels[0].animate.set_opacity(0.2),
            huffman_chart.probability_labels[0].animate.set_opacity(0.2)
        )
        self.wait(3)

        # Show the probability of the second bit being 0 vs 1
        arrow2 = Arrow(ORIGIN, UP).set_color(WHITE).next_to(message[1], DOWN)
        self.play(
            FadeOut(arrow),
            GrowArrow(arrow2),
            bit_opacity_trackers[1].animate.set_value(1),
            huffman_chart.bars[2:].animate.set_opacity(0.2),
            huffman_chart.bar_labels[2:].animate.set_opacity(0.2),
            huffman_chart.segments.bars[2:].animate.set_opacity(0.2),
            huffman_chart.event_labels[2:].animate.set_opacity(0.2),
            huffman_chart.probability_labels[2:].animate.set_opacity(0.2)
        )
        message[1].suspend_updating()
        message[1].set_value(0)
        self.play(message[1].animate.set_color(PURE_GREEN))
        self.wait(1.2)
        self.play(
            message[1].animate.set_value(1),
            huffman_chart.animate.restore(),
            huffman_chart.bars[:2].animate.set_opacity(0.2),
            huffman_chart.bar_labels[:2].animate.set_opacity(0.2),
            huffman_chart.segments.bars[:2].animate.set_opacity(0.2),
            huffman_chart.event_labels[:2].animate.set_opacity(0.2),
            huffman_chart.probability_labels[:2].animate.set_opacity(0.2)
        )
        self.wait(3)

        # Show the probability of the third bit being 0 vs 1
        arrow3 = Arrow(ORIGIN, UP).set_color(WHITE).next_to(message[2], DOWN)
        self.play(
            FadeOut(arrow2),
            GrowArrow(arrow3),
            bit_opacity_trackers[2].animate.set_value(1),
            huffman_chart.bars[3].animate.set_opacity(0.2),
            huffman_chart.bar_labels[3].animate.set_opacity(0.2),
            huffman_chart.segments.bars[3].animate.set_opacity(0.2),
            huffman_chart.event_labels[3].animate.set_opacity(0.2),
            huffman_chart.probability_labels[3].animate.set_opacity(0.2)
        )
        message[2].suspend_updating()
        message[2].set_value(0)
        self.play(message[2].animate.set_color(PURE_GREEN))
        self.wait(1.2)
        self.play(
            message[2].animate.set_value(1),
            huffman_chart.animate.restore(),
            huffman_chart.bars[:3].animate.set_opacity(0.2),
            huffman_chart.bar_labels[:3].animate.set_opacity(0.2),
            huffman_chart.segments.bars[:3].animate.set_opacity(0.2),
            huffman_chart.event_labels[:3].animate.set_opacity(0.2),
            huffman_chart.probability_labels[:3].animate.set_opacity(0.2)
        )
        self.wait(1.2)
        self.play(message[:3].animate.set_color(YELLOW)),
        message[0].resume_updating()
        message[1].resume_updating()
        message[2].resume_updating()
        self.play(
            FadeOut(arrow3),
            huffman_chart.animate.restore(),
            AnimationGroup(*[t.animate.set_value(1) for t in bit_opacity_trackers])
        )
        self.wait(3)

        # Define information
        huffman_chart.generate_target()
        huffman_chart.target.scale(0.8).to_corner(DL, buff=1)
        arrow = Arrow(huffman_chart.get_top(), huffman_chart.get_top() + UP * 2.7).set_color(WHITE)
        self.play(GrowArrow(arrow), run_time=2)
        self.wait(5)
        message_probability = Tex(
            R"\mathbf{P}(\text{any $n$-bit message}) = \frac{1}{2^n}"
        ).next_to(huffman_chart.target, RIGHT, buff=1).align_to(huffman_chart, UP).to_edge(RIGHT, buff=2).shift(DOWN * 0.3)
        new_arrow = Arrow(huffman_chart.target.get_corner(UR) + UR * 0.4, arrow.get_end(), buff=0)
        self.play(
            AnimationGroup(
                AnimationGroup(
                    MoveToTarget(huffman_chart, run_time=2),
                    arrow.animate(run_time=2.3).become(new_arrow)
                ),
                Write(message_probability), run_time=4.5, lag_ratio=0.4)
        )
        self.wait(5)
        message_probability_line_2 = Tex("p = 2^{-n}").next_to(message_probability, DOWN, buff=0.3)
        message_probability_line_2.shift(RIGHT * (message_probability[18].get_x() - message_probability_line_2["="].get_x()))
        self.play(
            TransformFromCopy(message_probability[:18], message_probability_line_2["p"], run_time=1.5),
            TransformMatchingShapes(message_probability[18:].copy(), message_probability_line_2["= 2^{-n}"], run_time=1.5)
        )
        self.wait(1.2)
        log_of_both_sides = Tex(R"\log_2(p) = \log_2(2^{-n})").match_y(message_probability_line_2)
        log_of_both_sides.shift(RIGHT * (message_probability_line_2["="].get_x() - log_of_both_sides["="].get_x()))
        self.play(TransformMatchingShapes(message_probability_line_2, log_of_both_sides), run_time=1)
        log_of_both_sides_simplified = Tex(R"\log_2(p) = -n").match_y(log_of_both_sides)
        log_of_both_sides_simplified.shift(RIGHT * (log_of_both_sides["="].get_x() - log_of_both_sides_simplified["="].get_x()))
        self.play(
            TransformMatchingShapes(log_of_both_sides[R"\log_2(p) ="], log_of_both_sides_simplified[R"\log_2(p) ="]),
            FadeOut(VGroup(log_of_both_sides[R"\log_2(2"], log_of_both_sides[")"][1])),
            ReplacementTransform(log_of_both_sides["-n"], log_of_both_sides_simplified["-n"]), run_time=1)
        negated = Tex(R"\text{Information} =  -\log_2(p) = {n}").match_y(log_of_both_sides_simplified)
        negated["Information"].set_color(TEAL)
        negated.shift(RIGHT * (log_of_both_sides_simplified["="].get_x() - negated["="][1].get_x()))
        self.play(
            TransformMatchingShapes(log_of_both_sides_simplified[R"\log_2(p) ="], negated[R"\log_2(p) ="]),
            TransformMatchingShapes(log_of_both_sides_simplified[R"n"], negated[R"{n}"]),
            TransformMatchingShapes(log_of_both_sides_simplified[R"-"], negated[R"-"], path_arc=PI * 0.4)
        )
        self.wait(6)
        rect = SurroundingRectangle(negated[R"-\log_2(p)"], stroke_width=3, stroke_color=TEAL)
        self.play(ShowCreation(rect), run_time=2)
        self.wait(4)
        # self.wait(16)
        # self.play(Write(negated[R"\text{Information} ="], run_time = 1.2))
        # self.wait(7.5)

        # Draw a graph of -log_2 p
        x_range = [0, 1]
        y_range = [0, 10]
        axes = Axes(
            x_range=x_range,
            y_range=y_range,
            width=6,
            height=5
        ).to_edge(RIGHT, buff=3)
        p_label = Tex("p").next_to(axes, DOWN, buff=0.5).set_opacity(0)
        labels = axes.add_coordinate_labels(
            x_values=[0.001, 1],
            y_values=[0, 2, 4, 6, 8, 10]
        )

        def func(x):
            return -math.log2(x)
        curve = ParametricCurve(
            lambda t: (axes.c2p(t, func(t))), (0.001, x_range[1], 0.001)
        ).set_stroke(width=4, color=TEAL, opacity=0.9)
        negated[R"\text{Information} ="].set_opacity(0)
        information_definition = negated[R"\text{Information} = -\log_2(p)"]
        self.play(
            AnimationGroup(
                AnimationGroup(
                    FadeOut(mission_control_and_robot_group),
                    AnimationGroup(*[t.animate.set_value(0) for t in bit_opacity_trackers]),
                    FadeOut(arrow),
                    FadeOut(huffman_chart),
                    FadeOut(message_probability),
                    FadeOut(rect),
                    FadeOut(negated["= {n}"])
                ),
                information_definition.animate.scale(1.1).next_to(axes, LEFT, buff=0.6),
                AnimationGroup(
                    FadeIn(VGroup(axes, p_label)),
                    ShowCreation(curve, run_time=1), lag_ratio=0.5), lag_ratio=0.6), run_time=3)
        self.remove(message)

        # Track values of p vs -log_2(p)
        p_tracker = ValueTracker(0.314)
        p_dot = Group(GlowDot(), TrueDot()).set_color(YELLOW)
        p_dot.add_updater(lambda m: m.move_to(axes.c2p(p_tracker.get_value(), func(p_tracker.get_value()))))
        dashed_line = always_redraw(lambda: DashedLine(p_dot.get_center(), [curve.get_left()[0], p_dot.get_y(), 0]).set_color(YELLOW))
        p_value_triangle = Triangle(fill_opacity=0.7, fill_color=YELLOW, stroke_width=0).set_width(0.25).stretch_to_fit_height(0.3)
        p_value_triangle.add_updater(lambda m: m.move_to(axes.c2p(p_tracker.get_value(), 0)).align_to([0, axes.get_x_axis()[0].get_y(), 0], UP))
        p_display = Tex("p = 0.00", font_size=30).set_stroke(color=BLACK, width=2, behind=True)
        p_display.add_updater(lambda m: m.next_to(p_value_triangle, DOWN))
        p_value = p_display.make_number_changeable("0.00")
        p_value.add_updater(lambda m: m.set_value(p_tracker.get_value()))
        self.play(
            FadeIn(p_dot, suspend_mobject_updating=True),
            ShowCreation(dashed_line, suspend_mobject_updating=True),
            FadeIn(VGroup(p_value_triangle, p_display)), run_time=0.9)
        bits_text = TexText("(bits)").next_to(information_definition, DOWN, buff=0.3)
        bits_display = TexText("Information $=$ 0.00 bits", font_size=38)
        bits_display["Information"].set_color(TEAL)
        display_group = VGroup(bits_display)
        display_group.arrange(DOWN)
        bits_display.shift(LEFT * (bits_display["="].get_x() - p_display["="].get_x()))
        display_group.align_to(axes, UR)
        bits_value = bits_display.make_number_changeable("0.00")
        bits_value.add_updater(lambda m: m.set_value(func(p_tracker.get_value())))
        display_opacity_tracker = ValueTracker(0)
        display_group.add_updater(lambda m: m.set_opacity(display_opacity_tracker.get_value()))
        self.add(display_group)
        values = [random.random() for _ in range(3)] + [0.019, 0.789] + [random.random() for _ in range(17)]
        for i, value in enumerate(values):
            anims = [p_tracker.animate.set_value(value)]
            if i == 1:
                anims.append(
                    AnimationGroup(
                        self.camera.frame.animate(run_time=2).match_x(VGroup(information_definition, axes)),
                        information_definition.animate(run_time=2).set_opacity(1), lag_ratio=0.4)
                )
            if i == 12:
                anims.append(AnimationGroup(FadeIn(bits_text), display_opacity_tracker.animate(run_time=2).set_value(1)))
            if i == 17:
                # Show the distinction between the different meanings of "bits"
                length = 13
                discrete_bits = VGroup(*[
                    Integer(random.choice([0, 1]), font_size=60) for _ in range(length)
                ]).arrange(buff=0.1).set_color(YELLOW).next_to(information_definition, LEFT, buff=0)
                num_bits_label = Tex(str(length) + R"\text{ bits}").next_to(discrete_bits, DOWN)
                anims.append(
                    AnimationGroup(
                        FadeOut(VGroup(negated[R"\text{Information} ="], bits_text), run_time=1),
                        self.camera.frame.animate(run_time=2.5).scale(1.5).move_to(VGroup(discrete_bits, axes)).shift(LEFT * 0.5),
                        FadeIn(VGroup(discrete_bits, num_bits_label), shift=RIGHT, run_time=2)
                    )
                )
            if i > 17:
                # Update the discrete bit count
                length = random.randint(2, 15)
                discrete_bits.become(
                    VGroup(*[
                        Integer(random.choice([0, 1]), font_size=60) for _ in range(length)
                    ]).arrange(buff=0.1).set_color(YELLOW).move_to(discrete_bits)
                )
                num_bits_label.become(Tex(str(length) + R"\text{ bits}").next_to(discrete_bits, DOWN))
            self.play(*anims, run_time=2.5)
            self.wait(0.8)
        self.wait(1)


class EntropyChart(VGroup):
    def __init__(
        self,
        initial_distribution,
        event_labels=None,
        probability_labels="default",
        bar_labels=None,
        bar_heights=None,
        width=6,
        height=6,
        segments_height=0.5,
        stroke_width=3,
        fit_event_labels_to_height=True,
        include_vertical_axis=True,
        vertical_axis_label_text=R"\text{Information } \\ (-\log_2 p_i \text{ bits})",
        vertical_axis_font_size=42,
        fill_colors=(BLUE_E, TEAL_E),
        bar_fill_colors=None,
        *args,
        **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.stroke_width = stroke_width
        self.distribution_trackers = [ValueTracker(p) for p in initial_distribution]
        self.segments = StackedProbDistribution(
            initial_distribution,
            labels=event_labels,
            width=width,
            height=segments_height,
            fit_labels_to_height=fit_event_labels_to_height,
            fill_colors=(BLUE_E, TEAL_E),
            stroke_width=self.stroke_width
        )

        def update_segments(m):
            m.set_distribution([t.get_value() for t in self.distribution_trackers])
        self.segments.add_updater(update_segments)
        self.add(self.segments)
        if event_labels is not None:
            self.event_labels = self.segments.labels
        else:
            self.event_labels = None

        self.width = width
        self.height = height

        i = 0
        include_labels_every = 1
        self.include_vertical_axis = include_vertical_axis
        if self.include_vertical_axis:
            self.reference_lines = VGroup()
            while i * self.height / self.width <= self.height:
                group = VGroup()
                line = Line(
                    ORIGIN, RIGHT * self.segments.get_width(),
                    stroke_width=1.3,
                ).align_to(
                    self.segments, UL
                ).shift(
                    UP * i * self.height / self.width
                ).set_opacity(0.4)
                group.add(line)
                label = Tex(str(i), font_size=20).next_to(line)
                if i % include_labels_every == 0:
                    group.add(label)
                self.reference_lines.add(group)

                i += 1
            self.add(self.reference_lines)

        self.bar_heights = [ValueTracker(h) for h in bar_heights] if bar_heights is not None else None

        def get_bars():
            colors = fill_colors if bar_fill_colors is None else bar_fill_colors
            bars = VGroup()
            for (i, segment), t in zip(enumerate(self.segments.bars), self.distribution_trackers):
                bar_height = -math.log2(t.get_value()) if self.bar_heights is None else self.bar_heights[i].get_value()
                bar = Rectangle(
                    width=segment.get_width(),
                    height=bar_height * self.height / self.width,
                    fill_opacity=0.8,
                    fill_color=interpolate_color(colors[0], colors[1], i / (len(self.distribution_trackers) - 1))
                ).set_stroke(
                    width=self.stroke_width, color=WHITE
                ).next_to(
                    segment, UP, buff=0
                )
                bar.height = bar_height
                bars.add(bar)
            return bars
        self.bars = always_redraw(get_bars)
        self.add(self.bars)

        if bar_labels is not None:
            self.bar_labels = VGroup(*bar_labels)
            self.add(self.bar_labels)
            for i, label in enumerate(self.bar_labels):
                label.set_color(BLACK)

            def update_labels(m):
                for label, bar in zip(m, self.bars):
                    label.move_to(bar)
            self.bar_labels.add_updater(update_labels)
        else:
            self.bar_labels = None

        if probability_labels == "default":
            self.probability_labels = VGroup(*[Tex(F"p_{i}") for i in range(len(self.distribution_trackers))])
        elif probability_labels is not None:
            self.probability_labels = VGroup(*probability_labels)
        else:
            self.probability_labels = None
        if self.probability_labels is not None:
            for i, label in enumerate(self.probability_labels):
                label.set_color(interpolate_color(fill_colors[0], fill_colors[1], i / (len(self.distribution_trackers) - 1)))

            def update_labels(m):
                for label, segment in zip(m, self.segments.bars):
                    label.next_to(segment, DOWN).match_y(m[0])
            self.probability_labels.add_updater(update_labels)
            self.add(self.probability_labels)

        if self.include_vertical_axis:
            self.vertical_axis = Line(ORIGIN, UP * self.height, stroke_width=self.stroke_width).align_to(self.segments.get_corner(UL), DL)
            self.vertical_axis_label = Tex(
                vertical_axis_label_text, font_size=vertical_axis_font_size
            ).next_to(self.vertical_axis, LEFT)
            self.vertical_axis_label["Information"].match_x(self.vertical_axis_label[len("Information"):])
            self.add(self.vertical_axis, self.vertical_axis_label)

    def set_distribution(self, distribution):
        return AnimationGroup(*[
            t.animate.set_value(p)
            for p, t in zip(distribution, self.distribution_trackers)
        ])
        self.segments.set_distribution(distribution)

    def create_bars(self):
        return AnimationGroup(*[
            UpdateFromAlphaFunc(
                bar,
                lambda m, a, t=t, i=i: m.stretch_to_fit_height(
                    max(0.0001, a) * (-math.log2(t.get_value()) if self.bar_heights is None else self.bar_heights[i].get_value()) * self.height / self.width,
                    about_point=m.get_bottom()
                ).set_stroke(
                    width=self.stroke_width * a
                ),
                suspend_mobject_updating=True
            )
            for i, (bar, t) in enumerate(zip(self.bars, self.distribution_trackers))
        ], lag_ratio=0.2)

    def create_reference_lines(self):
        anims = []
        for line in self.reference_lines:
            anim = [ShowCreation(line[0])]
            if len(line) > 1:
                anim.append(Write(line[1]))
            anims.append(AnimationGroup(*anim, lag_ratio=0.8))
        return AnimationGroup(*anims, lag_ratio=0.04)

    def create(self):
        anims_1 = []
        anims_2 = []
        for i in range(len(self.segments.bars)):
            fadeins = []
            fadeins.append(FadeIn(self.segments.bars[i]))
            if self.event_labels is not None:
                fadeins.append(FadeIn(self.event_labels[i]))
            if self.probability_labels is not None:
                fadeins.append(FadeIn(self.probability_labels[i]))
            anims_1.append(AnimationGroup(*fadeins))
        anims_2.append(self.create_bars())
        if self.bar_labels is not None:
            anims_2.append(
                AnimationGroup(*[
                    FadeIn(bar_label)
                    for bar_label in self.bar_labels
                ])
            )
        if self.include_vertical_axis:
            anims_2.append(
                AnimationGroup(
                    Write(self.vertical_axis_label),
                    ShowCreation(self.vertical_axis),
                    self.create_reference_lines()
                )
            )
        return AnimationGroup(AnimationGroup(*anims_1), AnimationGroup(*anims_2, lag_ratio=0.5))
