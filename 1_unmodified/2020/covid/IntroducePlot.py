# ==============================================================================
# Scene:      IntroducePlot
# Source:     videos/_2020/covid.py (lines 61-329)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl IntroducePlot.py IntroducePlot -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

CASE_DATA = [
    9,
    15,
    30,
    40,
    56,
    66,
    84,
    102,
    131,
    159,
    173,
    186,
    190,
    221,
    248,
    278,
    330,
    354,
    382,
    461,
    481,
    526,
    587,
    608,
    697,
    781,
    896,
    999,
    1124,
    1212,
    1385,
    1715,
    2055,
    2429,
    2764,
    3323,
    4288,
    5364,
    6780,
    8555,
    10288,
    12742,
    14901,
    17865,
    21395,
    # 25404,
    # 29256,
    # 33627,
    # 38170,
    # 45421,
    # 53873,
]


class IntroducePlot(Scene):
    def construct(self):
        axes = self.get_axes()
        self.add(axes)

        # Dots
        dots = VGroup()
        for day, nc in zip(it.count(1), CASE_DATA):
            dot = Dot()
            dot.set_height(0.075)
            dot.x = day
            dot.y = nc
            dot.axes = axes
            dot.add_updater(lambda d: d.move_to(d.axes.c2p(d.x, d.y)))
            dots.add(dot)
        dots.set_color(YELLOW)

        # Rescale y axis
        origin = axes.c2p(0, 0)
        axes.y_axis.tick_marks.save_state()
        for tick in axes.y_axis.tick_marks:
            tick.match_width(axes.y_axis.tick_marks[0])
        axes.y_axis.add(
            axes.h_lines,
            axes.small_h_lines,
            axes.tiny_h_lines,
            axes.tiny_ticks,
        )
        axes.y_axis.stretch(25, 1, about_point=origin)
        dots.update()

        self.add(axes.small_y_labels)
        self.add(axes.tiny_y_labels)

        # Add title
        title = self.get_title(axes)
        self.add(title)

        # Introduce the data
        day = 10
        self.add(*dots[:day + 1])

        dot = Dot()
        dot.match_style(dots[day])
        dot.replace(dots[day])
        count = Integer(CASE_DATA[day])
        count.add_updater(lambda m: m.next_to(dot, UP))
        count.add_updater(lambda m: m.set_stroke(BLACK, 5, background=True))

        v_line = Line(DOWN, UP)
        v_line.set_stroke(YELLOW, 1)
        v_line.add_updater(
            lambda m: m.put_start_and_end_on(
                axes.c2p(
                    axes.x_axis.p2n(dot.get_center()),
                    0,
                ),
                dot.get_bottom(),
            )
        )

        self.add(dot)
        self.add(count)
        self.add(v_line)

        for new_day in range(day + 1, len(dots)):
            new_dot = dots[new_day]
            new_dot.update()
            line = Line(dot.get_center(), new_dot.get_center())
            line.set_stroke(PINK, 3)

            self.add(line, dot)
            self.play(
                dot.move_to, new_dot.get_center(),
                dot.set_color, RED,
                ChangeDecimalToValue(count, CASE_DATA[new_day]),
                ShowCreation(line),
            )
            line.rotate(PI)
            self.play(
                dot.set_color, YELLOW,
                Uncreate(line),
                run_time=0.5
            )
            self.add(dots[new_day])

            day = new_day

            if day == 27:
                self.add(
                    axes.y_axis, axes.tiny_y_labels, axes.tiny_h_lines, axes.tiny_ticks,
                    title
                )
                self.play(
                    axes.y_axis.stretch, 0.2, 1, {"about_point": origin},
                    VFadeOut(axes.tiny_y_labels),
                    VFadeOut(axes.tiny_h_lines),
                    VFadeOut(axes.tiny_ticks),
                    MaintainPositionRelativeTo(dot, dots[new_day]),
                    run_time=2,
                )
                self.add(axes, title, *dots[:new_day])
            if day == 36:
                self.add(axes.y_axis, axes.small_y_labels, axes.small_h_lines, title)
                self.play(
                    axes.y_axis.stretch, 0.2, 1, {"about_point": origin},
                    VFadeOut(axes.small_y_labels),
                    VFadeOut(axes.small_h_lines),
                    MaintainPositionRelativeTo(dot, dots[new_day]),
                    run_time=2,
                )
                self.add(axes, title, *dots[:new_day])

        count.add_background_rectangle()
        count.background_rectangle.stretch(1.1, 0)
        self.add(count)

        # Show multiplications
        last_label = VectorizedPoint(dots[25].get_center())
        last_line = VMobject()
        for d1, d2 in zip(dots[25:], dots[26:]):
            line = Line(
                d1.get_top(),
                d2.get_corner(UL),
                path_arc=-90 * DEGREES,
            )
            line.set_stroke(PINK, 2)

            label = VGroup(
                OldTex("\\times"),
                DecimalNumber(
                    axes.y_axis.p2n(d2.get_center()) /
                    axes.y_axis.p2n(d1.get_center()),
                )
            )
            label.arrange(RIGHT, buff=SMALL_BUFF)
            label.set_height(0.25)
            label.next_to(line.point_from_proportion(0.5), UL, SMALL_BUFF)
            label.match_color(line)
            label.add_background_rectangle()
            label.save_state()
            label.move_to(last_label)
            label.set_opacity(0)

            self.play(
                ShowCreation(line),
                Restore(label),
                last_label.move_to, label.saved_state,
                VFadeOut(last_label),
                FadeOut(last_line),
            )
            last_line = line
            last_label = label
        self.wait()
        self.play(
            FadeOut(last_label),
            FadeOut(last_line),
        )

    #
    def get_title(self, axes):
        title = OldTexText(
            "Recorded COVID-19 cases\\\\outside mainland China",
            tex_to_color_map={"COVID-19": RED}
        )
        title.next_to(axes.c2p(0, 1e3), RIGHT, LARGE_BUFF)
        title.to_edge(UP)
        title.add_background_rectangle()
        return title

    def get_axes(self, width=12, height=6):
        n_cases = len(CASE_DATA)
        axes = Axes(
            x_range=(0, n_cases),
            y_range=(0, 25000, 1000),
            width=width,
            height=height,
        )
        axes.center()
        axes.to_edge(DOWN, buff=LARGE_BUFF)

        # Add dates
        text_pos_pairs = [
            ("Mar 6", 0),
            ("Feb 23", -12),
            ("Feb 12", -23),
            ("Feb 1", -34),
            ("Jan 22", -44),
        ]
        labels = VGroup()
        extra_ticks = VGroup()
        for text, pos in text_pos_pairs:
            label = OldTexText(text)
            label.set_height(0.2)
            label.rotate(45 * DEGREES)
            axis_point = axes.c2p(n_cases + pos, 0)
            label.move_to(axis_point, UR)
            label.shift(MED_SMALL_BUFF * DOWN)
            label.shift(SMALL_BUFF * RIGHT)
            labels.add(label)

            tick = Line(UP, DOWN)
            tick.set_stroke(GREEN, 3)
            tick.set_height(0.25)
            tick.move_to(axis_point)
            extra_ticks.add(tick)

        axes.x_labels = labels
        axes.extra_x_ticks = extra_ticks
        axes.add(labels, extra_ticks)

        # Adjust y ticks
        axes.y_axis.ticks.stretch(0.5, 0)
        axes.y_axis.ticks[0::5].stretch(2, 0)

        # Add y_axis_labels
        def get_y_labels(axes, y_values):
            labels = VGroup()
            for y in y_values:
                try:
                    label = OldTexText(f"{y}k")
                    label.set_height(0.25)
                    tick = axes.y_axis.ticks[y]
                    always(label.next_to, tick, LEFT, SMALL_BUFF)
                    labels.add(label)
                except IndexError:
                    pass
            return labels

        main_labels = get_y_labels(axes, range(5, 30, 5))
        axes.y_labels = main_labels
        axes.add(main_labels)
        axes.small_y_labels = get_y_labels(axes, range(1, 6))

        tiny_labels = VGroup()
        tiny_ticks = VGroup()
        for y in range(200, 1000, 200):
            tick = axes.y_axis.ticks[0].copy()
            point = axes.c2p(0, y)
            tick.move_to(point)
            label = Integer(y)
            label.set_height(0.25)
            always(label.next_to, tick, LEFT, SMALL_BUFF)
            tiny_labels.add(label)
            tiny_ticks.add(tick)

        axes.tiny_y_labels = tiny_labels
        axes.tiny_ticks = tiny_ticks

        # Horizontal lines
        axes.h_lines = VGroup()
        axes.small_h_lines = VGroup()
        axes.tiny_h_lines = VGroup()
        group_range_pairs = [
            (axes.h_lines, 5e3 * np.arange(1, 6)),
            (axes.small_h_lines, 1e3 * np.arange(1, 5)),
            (axes.tiny_h_lines, 200 * np.arange(1, 5)),
        ]
        for group, _range in group_range_pairs:
            for y in _range:
                group.add(
                    Line(
                        axes.c2p(0, y),
                        axes.c2p(n_cases, y),
                    )
                )
            group.set_stroke(WHITE, 1, opacity=0.5)

        return axes
