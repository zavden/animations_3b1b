# ==============================================================================
# Scene:      SamplingTwoRandomNumbers
# Source:     videos/_2019/hyperdarts.py (lines 1310-1317)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl SamplingTwoRandomNumbers.py SamplingTwoRandomNumbers -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class SamplingFourRandomNumbers(Scene):
    CONFIG = {
        "n_terms": 4,
        "title_tex": "P\\left(x_0{}^2 + y_0{}^2 + x_1{}^2 + y_1{}^2 < 1\\right) = \\, ???",
        "nl_to_nl_buff": 0.75,
        "to_floor_buff": 0.5,
        "tip_scale_factor": 0.75,
        "include_half_labels": True,
        "include_title": True,
    }

    def construct(self):
        texs = ["x_0", "y_0", "x_1", "y_1", "x_2", "y_2"][:self.n_terms]
        colors = [BLUE, YELLOW, BLUE_B, YELLOW_B, BLUE_A, YELLOW_A][:self.n_terms]
        t2c = dict([(t, c) for t, c in zip(texs, colors)])

        # Title
        if self.include_title:
            title = OldTex(
                self.title_tex,
                tex_to_color_map=t2c
            )
            title.scale(1.5)
            title.to_edge(UP)

            h_line = DashedLine(title.get_left(), title.get_right())
            h_line.next_to(title, DOWN, MED_SMALL_BUFF)

            self.add(title, h_line)

        # Number lines
        number_lines = VGroup(*[
            NumberLine(
                x_min=-1,
                x_max=1,
                tick_frequency=0.25,
                unit_size=3,
            )
            for x in range(self.n_terms)
        ])
        for line in number_lines:
            line.add_numbers(-1, 0, 1)
            if self.include_half_labels:
                line.add_numbers(
                    -0.5, 0.5,
                    num_decimal_places=1,
                )
        number_lines.arrange(DOWN, buff=self.nl_to_nl_buff)
        number_lines.to_edge(LEFT, buff=0.5)
        number_lines.to_edge(DOWN, buff=self.to_floor_buff)

        self.add(number_lines)

        # Trackers
        trackers = Group(*[ValueTracker(0) for x in range(self.n_terms)])
        tips = VGroup(*[
            ArrowTip(
                start_angle=-PI / 2,
                color=color
            ).scale(self.tip_scale_factor)
            for color in colors
        ])
        labels = VGroup(*[
            OldTex(tex)
            for tex in texs
        ])

        for tip, tracker, line, label in zip(tips, trackers, number_lines, labels):
            tip.line = line
            tip.tracker = tracker
            tip.add_updater(lambda t: t.move_to(
                t.line.n2p(t.tracker.get_value()), DOWN
            ))

            label.tip = tip
            label.match_color(tip)
            label.arrange(RIGHT, buff=MED_SMALL_BUFF)
            label.add_updater(lambda l: l.next_to(l.tip, UP, SMALL_BUFF))
            # label.add_updater(lambda l: l[1].set_value(l.tip.tracker.get_value()))

        self.add(tips, labels)

        # Write bit sum
        summands = VGroup(*[
            OldTex("\\big(", "+0.00", "\\big)^2").set_color(color)
            for color in colors
        ])
        summands.arrange(DOWN)
        summands.to_edge(RIGHT, buff=3)
        for summand, tracker in zip(summands, trackers):
            dec = DecimalNumber(include_sign=True)
            dec.match_color(summand)
            dec.tracker = tracker
            dec.add_updater(lambda d: d.set_value(d.tracker.get_value()))
            dec.move_to(summand[1])
            summand.submobjects[1] = dec

        h_line = Line(LEFT, RIGHT)
        h_line.set_width(3)
        h_line.next_to(summands, DOWN, aligned_edge=RIGHT)
        plus = OldTex("+")
        plus.next_to(h_line.get_left(), UR)
        h_line.add(plus)

        total = DecimalNumber()
        total.scale(1.5)
        total.next_to(h_line, DOWN)
        total.match_x(summands)
        total.add_updater(lambda d: d.set_value(np.sum([
            t.get_value()**2 for t in trackers
        ])))

        VGroup(summands, h_line, total).shift_onto_screen()
        self.add(summands, h_line, total)

        # < or > 1
        lt, gt = signs = VGroup(
            OldTex("< 1 \\quad \\checkmark"),
            OldTex("\\ge 1 \\quad"),
        )
        for sign in signs:
            sign.scale(1.5)
            sign.next_to(total, RIGHT, MED_LARGE_BUFF)
        lt.set_color(GREEN)
        gt.set_color(RED)

        def update_signs(signs):
            i = int(total.get_value() > 1)
            signs[1 - i].set_opacity(0)
            signs[i].set_opacity(1)

        signs.add_updater(update_signs)

        self.add(signs)

        # Run simulation
        for x in range(9):
            trackers.generate_target()
            for t in trackers.target:
                t.set_value(np.random.uniform(-1, 1))

            if x == 8:
                for t in trackers.target:
                    t.set_value(np.random.uniform(-0.5, 0.5))

            self.remove(signs)
            self.play(MoveToTarget(trackers))
            self.add(signs)
            self.wait()

        # Less than 0.5
        nl = number_lines[0]
        line = Line(nl.n2p(-0.5), nl.n2p(0.5))
        rect = Rectangle(height=0.25)
        rect.set_stroke(width=0)
        rect.set_fill(GREEN, 0.5)
        rect.match_width(line, stretch=True)
        rects = VGroup(*[
            rect.copy().move_to(line.n2p(0))
            for line in number_lines
        ])

        self.play(LaggedStartMap(GrowFromCenter, rects))
        self.wait()
        self.play(LaggedStartMap(FadeOut, rects))

        # Set one to 0.5
        self.play(trackers[0].set_value, 0.9)
        self.play(ShowCreationThenFadeAround(summands[0]))
        self.wait()
        self.play(LaggedStart(*[
            ShowCreationThenFadeAround(summand)
            for summand in summands[1:]
        ]))
        self.play(*[
            ApplyMethod(tracker.set_value, 0.1)
            for tracker in trackers[1:]
        ])
        self.wait(10)


class SamplingTwoRandomNumbers(SamplingFourRandomNumbers):
    CONFIG = {
        "n_terms": 2,
        "title_tex": "P\\left(x_0{}^2 + y_0{}^2 < 1\\right) = \\, ???",
        "nl_to_nl_buff": 1,
        "to_floor_buff": 2,
        "random_seed": 1,
    }
