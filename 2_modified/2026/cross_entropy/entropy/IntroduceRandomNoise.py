# ==============================================================================
# Scene:      IntroduceRandomNoise
# Source:     videos/_2026/cross_entropy/entropy.py (lines 470-674)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl IntroduceRandomNoise.py IntroduceRandomNoise -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - The robot is looked up in 'Lunar Rover Assets/' next to the file (before: Grant's output folder, with Path(...) which gave 'PosixPath + str'); the path is passed to ImageMobject as a str.
#
# Placeholder assets (not Grant's originals):
#   - Lunar Rover Assets/Stationary_fade_right.png (approximation derived from Stationary.tif with the right edge faded out)
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *
import math
import numpy as np

def bit_string_mobject(
    bit_string: str,
    font: str = "Consolas",
    font_size: int = 48,
    colors: List[Colors] = [GREY_C, GREY_B]
):
    result = Text(bit_string, font=font, font_size=font_size)
    result["0"].set_color(colors[0])
    result["1"].set_color(colors[1])
    return result


def int_to_bit_string(n_bits, value=None, **kwargs):
    if value is None:
        value = np.random.randint(0, 2**n_bits)
    return bit_string_mobject(f"{value:0{n_bits}b}", **kwargs)


class IntroduceRandomNoise(InteractiveScene):
    def construct(self):
        # Add robot
        # CHANGE: the robot lived in a "Lunar Rover Assets" folder next to Grant's video output; now it is next to this file (Stationary_fade_right.png is an
        # approximation derived from Stationary.tif). Also ImageMobject requires str (not Path) in this version of manimgl.
        robot_path = str(Path(__file__).parent / 'Lunar Rover Assets' / 'Stationary_fade_right.png')
        robot = ImageMobject(robot_path)
        robot.set_height(2).to_edge(LEFT, buff=0)
        robot.set_z_index(1)
        self.add(robot)

        # Show bit streams
        symbols = VGroup(
            Vector(0.5 * v, thickness=4, fill_color=PINK).center()
            for v in [UP, DOWN, LEFT, RIGHT]
        )
        n_terms = 100
        indices = np.random.choice(
            np.arange(4),
            n_terms,
            p=[0.5, 0.25, 0.125, 0.125]
        )
        codewords = ["0", "10", "110", "111"]
        segregated_encoding = [codewords[i] for i in indices]
        bit_stream = bit_string_mobject("".join(segregated_encoding))
        bit_stream.next_to(robot, RIGHT).shift(0.15 * DOWN)

        symbol_stream = VGroup(symbols[i].copy() for i in indices)
        symbol_stream.next_to(bit_stream, UP, SMALL_BUFF)
        curr_i = 0
        for sym, codeword in zip(symbol_stream, segregated_encoding):
            new_i = curr_i + len(codeword)
            sym.match_x(bit_stream[curr_i:new_i])
            curr_i = new_i

        streams = VGroup(bit_stream, symbol_stream)
        velocity = 1.0
        streams.add_updater(lambda m, dt: m.shift(velocity * dt * LEFT))

        self.add(streams)
        self.wait(6)

        # Noise word
        noise_word = Text("Random Noise", font_size=72)
        noise_word.next_to(bit_stream, DOWN, MED_LARGE_BUFF)
        noise_word.set_x(0)

        self.play(Write(noise_word))
        self.wait(1.5)

        # Noise box
        frame = self.frame
        box = Square(side_length=5.5)
        box.next_to(noise_word, DOWN, buff=3.0)
        noise_word.save_state()

        full_sentence = Text(
            "Random Noise is incompressible",
            t2s={"incompressible": ITALIC},
            t2c={"incompressible": RED}
        )
        full_sentence.next_to(box, UP)

        def get_box_contents(row_size=32):
            rows = VGroup(int_to_bit_string(row_size) for n in range(row_size // 2))
            rows.arrange(DOWN, buff=0.225)
            result = VGroup(*it.chain(*rows))
            result.set_max_width(0.9 * box.get_width())
            result.move_to(box)
            return result

        def update_contents(bits):
            centers = [bit.get_center().copy() for bit in bits]
            random.shuffle(centers)
            for bit, center in zip(bits, centers):
                bit.move_to(center)

        contents = get_box_contents()

        self.play(
            frame.animate.move_to(box).shift(MED_SMALL_BUFF * UP),
            TransformFromCopy(bit_stream, contents),
            Transform(noise_word, full_sentence["Random Noise"][0]),
            Write(full_sentence["is incompressible"], time_span=(0.5, 1.5)),
            FadeIn(box),
            run_time=1.5
        )
        contents.add_updater(update_contents)
        streams.suspend_updating()
        self.wait(0.5)

        # Try to squish
        box.insert_n_curves(120)
        squish_box = box.copy().center().apply_function(
            lambda p: p * (1 - 0.1 * abs(math.cos(2 * math.atan2(*p[:2]))))
        )
        squish_box.move_to(box)
        squish_box.set_stroke(RED, 3)

        squish_arrows = VGroup(
            Vector(vect, thickness=8, fill_color=RED).next_to(box, -vect, buff=-0.1)
            for vect in [LEFT, RIGHT]
        )

        self.play(
            Transform(box, squish_box),
            FadeIn(squish_arrows, scale=0.8),
            rate_func=bezier([0, 1.5, 1.5, 0.5, 0.5, 0.5, 1.1, 1.1, 1.1, -0.1, -0.1, 0, 0]),
            run_time=3,
        )
        self.wait(5)

        # Back to the stream
        streams.resume_updating()
        streams.next_to(robot, RIGHT, buff=0)

        self.play(
            frame.animate.to_default_state(),
            VFadeOut(contents),
            FadeOut(box),
            Restore(noise_word),
            FadeOut(full_sentence["is incompressible"]),
            run_time=2,
        )
        self.wait(15)
        streams.clear_updaters()

        # Boxes
        boxes = VGroup(
            SurroundingRectangle(bit, buff=0.025)
            for bit in bit_stream
        )
        boxes.stretch(1.2, 1)
        boxes.set_stroke(WHITE, 1)

        min_index = 18

        self.play(
            FadeOut(symbol_stream, lag_ratio=0.1,),
            FadeOut(bit_stream[min_index:], lag_ratio=0.1),
            FadeIn(boxes, lag_ratio=0.1),
            run_time=2
        )

        # 50/50 Question
        box = boxes[min_index]
        question = Text("0 or 1", font="consolas")
        question.next_to(box, UP, buff=0.75)
        choices = [question[c] for c in "01"]
        percentages = VGroup(
            Text(R"50%", font_size=30).set_fill(GREY_B).next_to(choice, UP, buff=0.15)
            for choice in choices
        )
        question.add(percentages)
        choice_rects = VGroup(SurroundingRectangle(choice) for choice in choices)
        choice_rects.set_stroke(YELLOW, 2)
        question.add(choice_rects)

        arrows = VGroup(
            Arrow(choice.get_bottom(), box.get_top(), buff=SMALL_BUFF, fill_color=TEAL)
            for choice in choices
        )
        question.add(arrows)

        self.add(question)

        # Make choices
        bit_tracker = ValueTracker(0)
        bit_tracker.add_updater(lambda m, dt: m.increment_value(PI * dt))
        self.add(bit_tracker)

        def get_bit():
            return int(bit_tracker.get_value() * 2**10) % 2

        def toggle_stroke(pair):
            bit = get_bit()
            pair[bit].set_stroke(opacity=1)
            pair[1 - bit].set_stroke(opacity=0)

        def toggle_fill(pair):
            bit = get_bit()
            pair[bit].set_fill(opacity=1)
            pair[1 - bit].set_fill(opacity=0)

        n_boxes_covered = 20

        for box in boxes[min_index:min_index + n_boxes_covered]:
            inner_bit = bit_string_mobject("01")
            for part in inner_bit:
                part.match_x(bit_stream[0])
                part.move_to(box)

            choice_rects.set_stroke(opacity=0)
            self.play(
                question.animate.match_x(box),
                run_time=0.2
            )
            self.play(
                UpdateFromFunc(choice_rects, toggle_stroke),
                UpdateFromFunc(inner_bit, toggle_fill),
                run_time=0.5
            )
            self.add(inner_bit)
