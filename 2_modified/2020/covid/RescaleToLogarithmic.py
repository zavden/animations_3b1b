# ==============================================================================
# Scene:      RescaleToLogarithmic
# Source:     videos/_2020/covid.py (lines 818-1201)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl RescaleToLogarithmic.py RescaleToLogarithmic -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - append_points with 3 points is no longer valid (quadratics in pairs): set_points_as_corners is used
#   - append_points with 3 points is no longer valid (quadratics in pairs): set_points_as_corners is used
# ==============================================================================

from manim_imports_ext import *
import scipy.stats

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


class RescaleToLogarithmic(IntroducePlot):
    def construct(self):
        # Setup axes
        axes = self.get_axes(width=10)
        title = self.get_title(axes)

        dots = VGroup()
        for day, nc in zip(it.count(1), CASE_DATA):
            dot = Dot()
            dot.set_height(0.075)
            dot.move_to(axes.c2p(day, nc))
            dots.add(dot)
        dots.set_color(YELLOW)

        self.add(axes, axes.h_lines, dots, title)

        # Create logarithmic y axis
        log_y_axis = NumberLine(
            x_min=0,
            x_max=9,
        )
        log_y_axis.rotate(90 * DEGREES)
        log_y_axis.move_to(axes.c2p(0, 0), DOWN)

        labels_text = [
            "10", "100",
            "1k", "10k", "100k",
            "1M", "10M", "100M",
            "1B",
        ]
        log_y_labels = VGroup()
        for text, tick in zip(labels_text, log_y_axis.tick_marks[1:]):
            label = OldTexText(text)
            label.set_height(0.25)
            always(label.next_to, tick, LEFT, SMALL_BUFF)
            log_y_labels.add(label)

        # Animate the rescaling to a logarithmic plot
        logarithm_title = OldTexText("(Logarithmic scale)")
        logarithm_title.set_color(TEAL)
        logarithm_title.next_to(title, DOWN)
        logarithm_title.add_background_rectangle()

        def scale_logarithmically(p):
            result = np.array(p)
            y = axes.y_axis.p2n(p)
            result[1] = log_y_axis.n2p(np.log10(y))[1]
            return result

        log_h_lines = VGroup()
        for exponent in range(0, 9):
            for mult in range(2, 12, 2):
                y = mult * 10**exponent
                line = Line(
                    axes.c2p(0, y),
                    axes.c2p(axes.x_max, y),
                )
                log_h_lines.add(line)
        log_h_lines.set_stroke(WHITE, 0.5, opacity=0.5)
        log_h_lines[4::5].set_stroke(WHITE, 1, opacity=1)

        movers = [dots, axes.y_axis.tick_marks, axes.h_lines, log_h_lines]
        for group in movers:
            group.generate_target()
            for mob in group.target:
                mob.move_to(scale_logarithmically(mob.get_center()))

        log_y_labels.suspend_updating()
        log_y_labels.save_state()
        for exponent, label in zip(it.count(1), log_y_labels):
            label.set_y(axes.y_axis.n2p(10**exponent)[1])
            label.set_opacity(0)

        self.add(log_y_axis)
        log_y_axis.save_state()
        log_y_axis.tick_marks.set_opacity(0)
        log_h_lines.set_opacity(0)
        self.wait()
        self.add(log_h_lines, title, logarithm_title)
        self.play(
            MoveToTarget(dots),
            MoveToTarget(axes.y_axis.tick_marks),
            MoveToTarget(axes.h_lines),
            MoveToTarget(log_h_lines),
            VFadeOut(axes.y_labels),
            VFadeOut(axes.y_axis.tick_marks),
            VFadeOut(axes.h_lines),
            Restore(log_y_labels),
            FadeIn(logarithm_title),
            run_time=2,
        )
        self.play(Restore(log_y_axis))
        self.wait()

        # Walk up y axis
        brace = Brace(
            log_y_axis.tick_marks[1:3],
            RIGHT,
            buff=SMALL_BUFF,
        )
        brace_label = brace.get_tex(
            "\\times 10",
            buff=SMALL_BUFF
        )
        VGroup(brace, brace_label).set_color(TEAL)
        brace_label.set_stroke(BLACK, 8, background=True)

        self.play(
            GrowFromCenter(brace),
            FadeIn(brace_label)
        )
        brace.add(brace_label)
        for i in range(2, 5):
            self.play(
                brace.next_to,
                log_y_axis.tick_marks[i:i + 2],
                {"buff": SMALL_BUFF}
            )
            self.wait(0.5)
        self.play(FadeOut(brace))
        self.wait()

        # Show order of magnitude jumps
        remove_anims = []
        for i, j in [(7, 27), (27, 40)]:
            line = Line(dots[i].get_center(), dots[j].get_center())
            rect = Rectangle()
            rect.set_fill(TEAL, 0.5)
            rect.set_stroke(width=0)
            rect.replace(line, stretch=True)
            label = OldTexText(f"{j - i} days")
            label.next_to(rect, UP, SMALL_BUFF)
            label.set_color(TEAL)

            rect.save_state()
            rect.stretch(0, 0, about_edge=LEFT)
            self.play(
                Restore(rect),
                FadeIn(label, LEFT)
            )
            self.wait()

            remove_anims += [
                ApplyMethod(
                    rect.stretch, 0, 0, {"about_edge": RIGHT},
                    remover=True,
                ),
                FadeOut(label, RIGHT),
            ]
        self.wait()

        # Linear regression
        def c2p(x, y):
            xp = axes.x_axis.n2p(x)
            yp = log_y_axis.n2p(np.log10(y))
            return np.array([xp[0], yp[1], 0])

        reg = scipy.stats.linregress(
            range(7, len(CASE_DATA)),
            np.log10(CASE_DATA[7:])
        )
        x_max = axes.x_max
        axes.y_axis = log_y_axis
        reg_line = Line(
            c2p(0, 10**reg.intercept),
            c2p(x_max, 10**(reg.intercept + reg.slope * x_max)),
        )
        reg_line.set_stroke(TEAL, 3)

        self.add(reg_line, dots)
        dots.set_stroke(BLACK, 3, background=True)
        self.play(
            LaggedStart(*remove_anims),
            ShowCreation(reg_line)
        )

        # Describe linear regression
        reg_label = OldTexText("Linear regression")
        reg_label.move_to(c2p(25, 10), DOWN)
        reg_arrows = VGroup()
        for prop in [0.4, 0.6, 0.5]:
            reg_arrows.add(
                Arrow(
                    reg_label.get_top(),
                    reg_line.point_from_proportion(prop),
                    buff=SMALL_BUFF,
                )
            )

        reg_arrow = reg_arrows[0].copy()
        self.play(
            Write(reg_label, run_time=1),
            Transform(reg_arrow, reg_arrows[1], run_time=2),
            VFadeIn(reg_arrow),
        )
        self.play(Transform(reg_arrow, reg_arrows[2]))
        self.wait()

        # Label slope
        slope_label = OldTexText("$\\times 10$ every $16$ days (on average)")
        slope_label.set_color(BLUE)
        slope_label.set_stroke(BLACK, 8, background=True)
        slope_label.rotate(reg_line.get_angle())
        slope_label.move_to(reg_line.get_center())
        slope_label.shift(MED_LARGE_BUFF * UP)

        self.play(FadeIn(slope_label, lag_ratio=0.1))
        self.wait()

        # R^2 label
        R2_label = VGroup(
            OldTex("R^2 = "),
            DecimalNumber(0, num_decimal_places=3)
        )
        R2_label.arrange(RIGHT, aligned_edge=DOWN)
        R2_label.next_to(reg_label[0][-1], RIGHT, LARGE_BUFF, aligned_edge=DOWN)

        self.play(
            ChangeDecimalToValue(R2_label[1], reg.rvalue**2, run_time=2),
            UpdateFromAlphaFunc(
                R2_label,
                lambda m, a: m.set_opacity(a),
            )
        )
        self.wait()

        rect = SurroundingRectangle(R2_label, buff=0.15)
        rect.set_stroke(YELLOW, 3)
        rect.set_fill(BLACK, 0)
        self.add(rect, R2_label)
        self.play(ShowCreation(rect))
        self.play(
            rect.set_stroke, WHITE, 2,
            rect.set_fill, GREY_E, 1,
        )
        self.wait()
        self.play(
            FadeOut(rect),
            FadeOut(R2_label),
            FadeOut(reg_label),
            FadeOut(reg_arrow),
        )

        # Zoom out
        extended_x_axis = NumberLine(
            x_min=axes.x_axis.x_max,
            x_max=axes.x_axis.x_max + 90,
            unit_size=get_norm(
                axes.x_axis.n2p(1) -
                axes.x_axis.n2p(0)
            ),
            big_tick_numbers=[],
        )
        extended_x_axis.move_to(axes.x_axis.get_right(), LEFT)
        self.play(
            self.camera.frame.scale, 2, {"about_edge": DL},
            self.camera.frame.shift, 2.5 * DOWN + RIGHT,
            log_h_lines.stretch, 3, 0, {"about_edge": LEFT},
            ShowCreation(extended_x_axis, rate_func=squish_rate_func(smooth, 0.5, 1)),
            run_time=3,
        )
        self.play(
            reg_line.scale, 3, {"about_point": reg_line.get_start()}
        )
        self.wait()

        # Show future projections
        target_ys = [1e6, 1e7, 1e8, 1e9]
        last_point = dots[-1].get_center()
        last_label = None
        last_rect = None

        date_labels_text = [
            "Apr 5",
            "Apr 22",
            "May 9",
            "May 26",
        ]

        for target_y, date_label_text in zip(target_ys, date_labels_text):
            log_y = np.log10(target_y)
            x = (log_y - reg.intercept) / reg.slope
            line = Line(last_point, c2p(x, target_y))
            rect = Rectangle().replace(line, stretch=True)
            rect.set_stroke(width=0)
            rect.set_fill(TEAL, 0.5)
            label = OldTexText(f"{int(x) - axes.x_max} days")
            label.scale(1.5)
            label.next_to(rect, UP, SMALL_BUFF)

            date_label = OldTexText(date_label_text)
            date_label.set_height(0.25)
            date_label.rotate(45 * DEGREES)
            axis_point = axes.c2p(int(x), 0)
            date_label.move_to(axis_point, UR)
            date_label.shift(MED_SMALL_BUFF * DOWN)
            date_label.shift(SMALL_BUFF * RIGHT)

            v_line = DashedLine(
                axes.c2p(x, 0),
                c2p(x, target_y),
            )
            v_line.set_stroke(WHITE, 2)

            if target_y is target_ys[-1]:
                self.play(self.camera.frame.scale, 1.1, {"about_edge": LEFT})

            if last_label:
                self.play(
                    ReplacementTransform(last_label, label),
                    ReplacementTransform(last_rect, rect),
                )
            else:
                rect.save_state()
                rect.stretch(0, 0, about_edge=LEFT)
                self.play(Restore(rect), FadeIn(label, LEFT))
            self.wait()

            self.play(
                ShowCreation(v_line),
                FadeIn(date_label),
            )

            last_label = label
            last_rect = rect

        self.wait()
        self.play(
            FadeOut(last_label, RIGHT),
            ApplyMethod(
                last_rect.stretch, 0, 0, {"about_edge": RIGHT},
                remover=True
            ),
        )

        # Show alternate petering out possibilities
        def get_dots_along_curve(curve):
            x_min = int(axes.x_axis.p2n(curve.get_start()))
            x_max = int(axes.x_axis.p2n(curve.get_end()))
            result = VGroup()
            for x in range(x_min, x_max):
                prop = binary_search(
                    lambda p: axes.x_axis.p2n(
                        curve.point_from_proportion(p),
                    ),
                    x, 0, 1,
                )
                prop = prop or 0
                point = curve.point_from_proportion(prop)
                dot = Dot(point)
                dot.shift(0.02 * (random.random() - 0.5))
                dot.set_height(0.075)
                dot.set_color(RED)
                result.add(dot)
            dots.remove(dots[0])
            return result

        def get_point_from_y(y):
            log_y = np.log10(y)
            x = (log_y - reg.intercept) / reg.slope
            return c2p(x, 10**log_y)

        p100k = get_point_from_y(1e5)
        p100M = get_point_from_y(1e8)
        curve1 = VMobject()
        # CHANGE: append_points with 3 points is no longer valid (quadratics in pairs): set_points_as_corners is used
        curve1.set_points_as_corners([
            dots[-1].get_center(),
            p100k,
            p100k + 5 * RIGHT,
        ])
        curve2 = VMobject()
        # CHANGE: append_points with 3 points is no longer valid (quadratics in pairs): set_points_as_corners is used
        curve2.set_points_as_corners([
            dots[-1].get_center(),
            p100M,
            p100M + 5 * RIGHT + 0.25 * UP,
        ])

        proj_dots1 = get_dots_along_curve(curve1)
        proj_dots2 = get_dots_along_curve(curve2)

        for proj_dots in [proj_dots1, proj_dots2]:
            self.play(FadeIn(proj_dots, lag_ratio=0.1))
            self.wait()
            self.play(FadeOut(proj_dots, lag_ratio=0.1))
