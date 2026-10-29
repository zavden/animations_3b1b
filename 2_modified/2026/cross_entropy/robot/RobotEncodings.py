# ==============================================================================
# Scene:      RobotEncodings
# Source:     videos/_2026/cross_entropy/robot.py (lines 531-1418)
# Category:   2 · Renders with modifications
# Includes code copied from: _2026/cross_entropy/distribution.py
#
# Run from this folder:
#     manimgl RobotEncodings.py RobotEncodings -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Uses the placeholder images/pi_creature_mission_control.png (the original is private to Grant).
#
# Placeholder assets (not Grant's originals):
#   - images/pi_creature_mission_control.png (placeholder image: pi creature at a mission control console)
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


class RobotEncodings(InteractiveScene):
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

        # Save the Naive example
        arrows.clear_updaters()
        rects.clear_updaters()
        bits.clear_updaters()
        naive_example_group = Group(robot, Group(arrows, rects, bits), mission_control, naive_chart)
        naive_example_group.generate_target()
        naive_example_group.target[-1].scale(1.3)
        naive_example_group.target.arrange(buff=0.6).to_edge(UP, buff=0.7).set_width(FRAME_WIDTH * 0.96)
        naive_example_group.target[1].shift(
            DOWN * (naive_example_group.target[1][2].get_y() - naive_example_group.target.get_y())
        )
        naive_example_group.target[2].align_to(naive_example_group.target[0], DOWN)
        naive_example_group.target[3].shift(DOWN * 0.4)
        naive_example_group.target.to_edge(UP, buff=0.7).set_x(0)
        self.play(MoveToTarget(naive_example_group, path_arc=-PI * 0.2))

        # Change the encoding to a Huffman code
        robot_2 = robot.copy()
        arrows_2 = arrows.copy().set_color(PINK)
        mission_control_2 = mission_control.copy()
        huffman_chart_init = EntropyChart(
            distribution,
            event_labels=VGroup(*[InstructionArrow([UP, DOWN, LEFT, RIGHT][i]) for i in range(4)]).set_color(PINK),
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
            height=6,
            include_vertical_axis=False,
            segments_height=1,
            fill_colors=[PURE_MAGENTA, LIGHT_PINK]
        ).match_width(naive_chart).match_x(naive_chart)
        huffman_chart_init.shift(DOWN * (huffman_chart_init.segments.get_bottom()[1] - mission_control_2.get_bottom()[1]))
        huffman_chart_init.bar_labels.set_color(WHITE)
        huffman_chart_init.update()
        self.wait(0.01)
        huffman_chart_init.suspend_updating()
        Group(robot_2, arrows_2, mission_control_2, huffman_chart_init).to_edge(DOWN, buff=0.4)
        self.play(TransformFromCopy(Group(robot, arrows, mission_control, naive_chart), Group(robot_2, arrows_2, mission_control_2, huffman_chart_init)))
        self.wait(2)

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
            fill_colors=[RED, LIGHT_PINK]
        ).match_width(huffman_chart_init).match_x(huffman_chart_init)
        huffman_chart.bar_labels.set_color(WHITE)
        huffman_chart.update()
        self.wait(0.01)
        huffman_chart.align_to(huffman_chart_init, DOWN)

        for i in range(4):
            self.play(
                ReplacementTransform(huffman_chart_init.bars[i], huffman_chart.bars[i], suspend_mobject_updating=True),
                ReplacementTransform(huffman_chart_init.bar_labels[i], huffman_chart.bar_labels[i], suspend_mobject_updating=True)
            )
            self.wait(2)

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
        self.remove(huffman_chart_init)
        self.add(huffman_chart)
        perfect_example_group = Group(robot_2, Group(arrows_2, rects_2, bits_2), mission_control_2, huffman_chart)
        self.play(
            AnimationGroup(
                FadeOut(naive_example_group, shift=UP),
                perfect_example_group[-1].animate(path_arc=PI * 0.2).scale(1.2).to_edge(UP, buff=0.7).to_edge(RIGHT, buff=0.5),
                perfect_example_group[:-1].animate.set_width(FRAME_WIDTH * 0.9).set_x(0).to_edge(DOWN, buff=0.4), lag_ratio=0.1, run_time=2)
        )

        # Introduce "code word" term
        code_words_text = Tex(R"\text{code words}").next_to(huffman_chart, UP).set_color(WHITE).fix_in_frame()
        huffman_chart.clear_updaters()
        huffman_chart.fix_in_frame()
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
            bits_2.animate(run_time=10).align_to(robot.get_center(), RIGHT)
        )

        # Fade out everything but the chart
        self.remove(bits_2, rects_2, arrows_2)
        self.play(
            FadeOut(code_words_text),
            FadeOut(Group(robot_2, mission_control_2), shift=DOWN),
            huffman_chart.animate.scale(1.2).align_to(huffman_chart, RIGHT).set_y(0)
        )
        self.wait(3)

        # Write two questions
        questions = BulletedList(
            "How much more efficient?",
            "Prove optimality",
            numbered=True,
            font_size=40
        ).to_edge(LEFT, buff=1)
        for question in questions:
            self.play(Write(question), run_time=2)
            self.wait(3)

        # Center the chart
        self.play(
            FadeOut(questions, shift=LEFT * 2),
            huffman_chart.animate.scale(1.2).set_x(0).to_edge(DOWN, buff=1), run_time=2)

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

        bit_string = "•" * len(message)
        dummy_message = VGroup(*[
            Text(b, font_size=30) for b in bit_string]
        ).set_color(PINK).arrange(buff=0.08).match_width(message).match_y(message).align_to(mission_control, LEFT)
        dummy_message_opacity_tracker = ValueTracker(0)

        def update_dummy_message(m):
            for bit in m:
                bit.set_opacity(dummy_message_opacity_tracker.get_value() * min(1, max(0, 0.8 * (mission_control.get_left()[0] - bit.get_x()))))
                if bit.get_x() < robot.get_x():
                    bit.set_opacity(0)
            self.bring_to_front(robot)
        dummy_message.add_updater(update_dummy_message)
        self.add(dummy_message)

        self.play(
            FadeIn(mission_control_and_robot_group),
            dummy_message.animate(run_time=6).move_to(message),
            dummy_message_opacity_tracker.animate(run_time=2).set_value(1)
        )
        dummy_message.clear_updaters()

        self.play(
            FadeOut(dummy_message),
            AnimationGroup(*[t.animate.set_value(1) for t in bit_opacity_trackers])
        )
        self.wait(1)

        # Show the probability of the first bit being 0 vs 1
        arrow = Arrow(ORIGIN, UP).set_color(WHITE).next_to(message[0], DOWN)
        huffman_chart.save_state()
        self.play(
            huffman_chart.bars[1:].animate.set_opacity(0.2),
            huffman_chart.bar_labels[1:].animate.set_opacity(0.2),
            huffman_chart.segments.bars[1:].animate.set_opacity(0.2),
            huffman_chart.event_labels[1:].animate.set_opacity(0.2),
            huffman_chart.probability_labels[1:].animate.set_opacity(0.2)
        )
        self.wait(2)
        self.play(
            GrowArrow(arrow),
            AnimationGroup(*[t.animate.set_value(0.2) for t in bit_opacity_trackers[1:]]),
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
            huffman_chart.bars[2:].animate.set_opacity(0.2),
            huffman_chart.bar_labels[2:].animate.set_opacity(0.2),
            huffman_chart.segments.bars[2:].animate.set_opacity(0.2),
            huffman_chart.event_labels[2:].animate.set_opacity(0.2),
            huffman_chart.probability_labels[2:].animate.set_opacity(0.2)
        )
        self.wait(2)
        self.play(
            GrowArrow(arrow2),
            bit_opacity_trackers[1].animate.set_value(1),
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
        self.wait(10)

        # Zoom in on the receiver
        self.camera.frame.save_state()
        huffman_chart.unfix_from_frame()
        self.play(self.camera.frame.animate.scale(0.75, about_point=robot.get_corner(UL)), run_time=3)
        self.wait(5)

        # Zoom out to think about entire messages
        n = 6
        robot.generate_target()
        robot.target.scale(2)
        sample_n_bits = message[:n]
        for bit, val in zip(sample_n_bits, "110101"):
            bit.set_value(int(val))
        sample_n_bits.clear_updaters()
        sample_n_bits.generate_target()
        sample_n_bits.target.scale(1.2).next_to(robot.target, RIGHT, buff=0.4)
        Group(robot.target, sample_n_bits.target).center()
        right_shift_tracker = ValueTracker(0)
        for bit in message[n:]:
            original_x = bit.get_x()

            def update_bit(m, original_x=original_x):
                m.set_x(original_x)
                m.shift(RIGHT * right_shift_tracker.get_value())
            bit.add_updater(update_bit)
        self.play(
            AnimationGroup(
                AnimationGroup(
                    self.camera.frame.animate(run_time=3).restore(),
                    FadeOut(Group(mission_control, huffman_chart), shift=DR * 1.4, run_time=1.3),
                    right_shift_tracker.animate(run_time=1.3).set_value(4),
                    AnimationGroup(*[t.animate.set_value(0) for t in bit_opacity_trackers[n:]], run_time=1.3)
                ),
                AnimationGroup(
                    MoveToTarget(robot, run_time=3),
                    MoveToTarget(sample_n_bits, run_time=3)
                )
            )
        )
        self.remove(message[n:])
        self.wait(2)

        # Brace the n bits
        brace = Brace(sample_n_bits, direction=DOWN)
        label = brace.get_tex(R"n \text{ bits}")
        self.play(GrowFromEdge(brace, UP), Write(label))

        # Show all of the 2^n messages
        messages = VGroup(*[
            Tex(F"{i:0{n}b}", font_size=40).set_color(YELLOW)
            for i in range(2**n)
        ]).arrange_in_grid(n_cols=4, h_buff=0.3, v_buff=0.1).align_to(sample_n_bits, LEFT)
        message_index = sum([2**i * sample_n_bits[n - 1 - i].get_value() for i in range(n)])
        messages[message_index].set_color(BLUE)
        new_brace = Brace(messages, direction=DOWN)
        new_label = new_brace.get_tex(R"n \text{ bits}")
        VGroup(messages, new_brace, new_label).set_y(0)
        two_to_then_n_brace = Brace(messages, direction=RIGHT)
        two_to_the_n_label = two_to_then_n_brace.get_tex(R"2^n\ n\text{-bit messages} \\ \text{(all equally likely)}")
        two_to_the_n_label.shift(DOWN * (two_to_the_n_label[0].get_y() - two_to_then_n_brace.get_y()))
        self.play(
            self.camera.frame.animate(run_time=3).match_x(Group(robot, two_to_the_n_label)),
            FadeOut(VGroup(brace, label).fix_in_frame(), shift=DOWN),
            AnimationGroup(
                AnimationGroup(*[
                    TransformMatchingShapes(sample_n_bits[i], messages[message_index][i], run_time=2)
                    for i in range(n)
                ]),
                AnimationGroup(*[FadeIn(message, shift=DOWN * 0.3) for message in messages[:message_index]], lag_ratio=0.02),
                AnimationGroup(*[FadeIn(message, shift=UP * 0.3) for message in messages[message_index + 1:]], lag_ratio=0.02),
                AnimationGroup(
                    GrowFromEdge(two_to_then_n_brace, LEFT),
                    Write(two_to_the_n_label[R"2^n\ n\text{-bit messages}"])
                ), lag_ratio=0.2)
        )
        self.add(messages)
        self.wait(2)
        self.play(FadeIn(two_to_the_n_label["(all equally likely)"]))
        self.wait(2)

        # View the chart again
        self.play(
            FadeOut(VGroup(messages, two_to_then_n_brace, two_to_the_n_label)),
            FadeIn(
                huffman_chart.scale(0.8).next_to(
                    self.camera.frame.get_right(), LEFT, buff=robot.get_left()[0] - self.camera.frame.get_left()[0]
                ),
                shift=LEFT
            )
        )
        self.camera.frame.center()
        Group(robot, huffman_chart).move_to(self.camera.frame)

        # Show some sample messages
        message_instructions = [
            [0, 0, 0],
            [3],
            [1, 0]
        ]
        messages = VGroup(*[
            VGroup(*[InstructionArrow([UP, DOWN, LEFT, RIGHT][i]).set_color(PINK) for i in row]).arrange(buff=3)
            for row in message_instructions
        ]).arrange_in_grid(n_cols=1, aligned_edge=RIGHT, buff=5).set_width(2).next_to(robot, RIGHT, buff=1.85)
        for message in messages:
            self.play(FadeIn(message))
            self.wait(1.5)
        self.wait(1)

        # Show their encodings
        encodings = VGroup(*[
            Tex(R":\ " + "".join([encoding[i] for i in row]), font_size=50).set_color(PINK)
            for row in message_instructions
        ])
        for message, enc, in zip(messages, encodings):
            enc[":"].match_y(enc[-1])
            enc.next_to(message, RIGHT, buff=0.3)
        for message in messages:
            message.generate_target()
        VGroup(*[message.target for message in messages], encodings).match_x(messages)
        self.play(
            AnimationGroup(*[
                AnimationGroup(
                    MoveToTarget(message, run_time=1.5),
                    FadeIn(enc[":"], shift=LEFT, run_time=1.5),
                    AnimationGroup(*[
                        TransformFromCopy(huffman_chart.bar_labels[row[j]], enc[1:][
                            sum([len(encoding[row[k]]) for k in range(j)]):sum([len(encoding[row[k]]) for k in range(j + 1)])
                        ], path_arc=PI * 0.2)
                        for j in range(len(row))
                    ], lag_ratio=0.1, run_time=3)
                )
                for message, row, enc in zip(messages, message_instructions, encodings)
            ], lag_ratio=0.05)
        )

        # Show the probability of each
        probability_calculations = VGroup(
            Tex(R"\frac{1}{2}\ \ \cdot\ \  \frac{1}{2}\ \  \cdot\ \  \frac{1}{2}", font_size=30),
            Tex(R"\frac{1}{8}", font_size=30),
            Tex(R"\frac{1}{4}\ \  \cdot\ \  \frac{1}{2}", font_size=30)
        )
        for calculation, message in zip(probability_calculations, messages):
            calculation.next_to(message, UP)

        self.play(
            AnimationGroup(*[
                AnimationGroup(*[
                    TransformFromCopy(huffman_chart.probability_labels[row[j]], calculation[j * 4: j * 4 + 3], path_arc=PI * 0.2)
                    for j in range(len(row))
                ], lag_ratio=0.1)
                for calculation, row in zip(probability_calculations, message_instructions)
            ], lag_ratio=0.1, run_time=2.5)
        )
        self.play(AnimationGroup(*[FadeIn(calculation[R"\cdot"]) for calculation in probability_calculations]))
        self.wait(1.5)

        # Highlight the different sizes of the messages
        for _ in range(2):
            self.play(
                AnimationGroup(*[
                    AnimationGroup(*[
                        Indicate(arrow)
                        for arrow in message
                    ], lag_ratio=0.3, run_time=2)
                    for message in messages
                ])
            )

        # Highlight the same size of the encoded messages and relate it to the probability
        rect = SurroundingRectangle(VGroup(*[enc[1:] for enc in encodings]), stroke_width=4, buff=0.2, stroke_color=YELLOW)
        self.play(FadeIn(rect), run_time=2)
        rects = VGroup(*[
            SurroundingRectangle(calculation, stroke_width=3, buff=0.1, stroke_color=YELLOW)
            for calculation in probability_calculations
        ])
        self.play(FadeIn(rects), run_time=2)
        self.wait(2)


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
