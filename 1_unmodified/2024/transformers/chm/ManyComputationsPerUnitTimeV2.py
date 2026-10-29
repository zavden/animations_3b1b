# ==============================================================================
# Scene:      ManyComputationsPerUnitTimeV2
# Source:     videos/_2024/transformers/chm.py (lines 1577-1807)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ManyComputationsPerUnitTimeV2.py ManyComputationsPerUnitTimeV2 -w -m --fps 15
#
# Notes:
#   The published video is the one from the 360p, 10 fps test: at 720p it takes too long (more than 500 s at 360p).
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class ManyComputationsPerUnitTimeV2(InteractiveScene):
    def construct(self):
        # Add computations
        box = Rectangle(5, 5)
        label = Text("1 Billion computations per Second")
        label.next_to(box, UP)
        self.add(box)
        self.add(label)

        comps = self.get_computations(box)
        self.add(comps)
        self.wait(3)

        # Place box into minute interval
        width = FRAME_WIDTH - 1
        number_lines = VGroup(
            minute_line := NumberLine((0, 60, 1), width=width, big_tick_spacing=10),
            hour_line := NumberLine((0, 60, 1), width=width, big_tick_spacing=10),
            day_line := NumberLine((0, 24, 1), width=width, big_tick_spacing=6),
            month_line := NumberLine((0, 31, 1), width=width),
            year_line := NumberLine((0, 12, 1), width=width),
            y100_line := NumberLine((0, 100, 1), width=width),
            y10k_line := NumberLine((0, 100, 1), width=width),
            y1M_line := NumberLine((0, 100, 1), width=width),
            y100M_line := NumberLine((0, 100, 1), width=width),
        )
        number_lines.move_to(DOWN)

        first_ticks = minute_line.ticks[:2]
        sec_brace = Brace(first_ticks, DOWN, buff=0, tex_string=R"\underbrace{\qquad\qquad}")
        sec_label = Text("Second", font_size=30).next_to(sec_brace, DOWN, SMALL_BUFF)

        self.play(
            ShowCreation(minute_line, lag_ratio=0.01),
            box.animate.match_width(first_ticks).move_to(first_ticks.get_center(), DOWN).set_stroke(width=1),
            TransformFromCopy(label["Second"][0], sec_label),
            GrowFromCenter(sec_brace),
            run_time=2
        )

        # Add other boxes
        minute_label = self.get_timeline_full_label(number_lines[1], "Minute")
        new_boxes = VGroup(
            box.copy().move_to(tick.get_center(), DL)
            for tick in minute_line.ticks[1:-1]
        )
        for new_box in new_boxes:
            new_box.save_state()
            new_box.move_to(box)
        computations = VGroup(
            self.get_computations(new_box, n_iterations=1)
            for new_box in new_boxes
        )
        # computations = VGroup()  # If needed

        self.add(computations)
        self.play(
            FadeIn(minute_label, DOWN),
            LaggedStartMap(Restore, new_boxes, lag_ratio=0.1),
            run_time=2
        )
        self.wait(2)

        # Add labels
        minute_line.add(minute_label)
        names = ["Hour", "Day", "Month", "Year", "100 Years", "10,000 Years", "1,000,000 Years", "100,000,000 Years"]
        for line, name in zip(number_lines[1:], names):
            line.label = self.get_timeline_full_label(line, name)
            line.add(line.label)

        # Arrange all lines
        number_lines[1:].arrange(DOWN, buff=2.0)
        number_lines[1:].next_to(minute_line, DOWN, buff=2.0)

        scale_lines = VGroup()
        for nl1, nl2 in zip(number_lines, number_lines[1:]):
            n = len(nl2.ticks) // 2
            mini_line = Line(nl2.ticks[n - 1].get_center(), nl2.ticks[n].get_center())
            pair = VGroup(
                DashedLine(nl1.get_start(), mini_line.get_start()),
                DashedLine(nl1.get_end(), mini_line.get_end()),
            )
            pair.set_stroke(WHITE, 2)
            nl1.target = nl1.copy()
            nl1.target.replace(mini_line, dim_to_match=0)
            nl1.target.shift(mini_line.pfp(0.5) - nl1.target.pfp(0.5))
            scale_lines.add(pair)

        # Start panning down
        lag_ratio = 1.5
        self.play(
            LaggedStart(
                *(AnimationGroup(*(ShowCreation(sl) for sl in pair)) for pair in scale_lines),
                lag_ratio=lag_ratio,
            ),
            LaggedStart(
                *(FadeIn(nl) for nl in number_lines[1:]),
                lag_ratio=lag_ratio,
            ),
            LaggedStart(
                *(TransformFromCopy(nl, nl.target) for nl in number_lines[:-1]),
                lag_ratio=lag_ratio,
            ),
            self.frame.animate.set_y(number_lines[-1].get_y() + 2).set_width(18).set_anim_args(
                rate_func=lambda t: interpolate(smooth(t), linear(t), there_and_back_with_pause(t, pause_ratio=0.8))
            ),
            run_time=30
        )
        self.play(self.frame.animate.reorient(0, 0, 0, (-0.03, -11.55, 0.0), 31.76), run_time=4)
        self.wait(4)

    def fade_in_bigger_interval(self, new_interval, prev_interval, fader, scale_factor, added_anims=[]):
        pivot = prev_interval.n2p(0)
        new_interval.save_state()
        new_interval.scale(scale_factor, about_point=pivot)
        new_interval[:-1].set_opacity(0)
        new_interval[-1].set_fill(BLACK)

        self.play(
            Restore(new_interval),
            prev_interval.animate.scale(1.0 / scale_factor, about_point=pivot).set_fill(border_width=0),
            fader.animate.scale(1.0 / scale_factor, about_point=pivot).set_opacity(0),
            *added_anims,
            run_time=4,
            rate_func=rush_from
        )
        self.remove(fader)

    def get_timeline_full_label(self, timeline, name):
        brace = Brace(Line().set_width(7), UP, buff=MED_SMALL_BUFF)
        brace.set_fill(border_width=5)
        brace.match_width(timeline)
        brace.next_to(timeline, UP, buff=MED_SMALL_BUFF)
        label = Text(name, font_size=72)
        label.next_to(brace, UP, MED_SMALL_BUFF)

        label.next_to(timeline, DOWN)
        return label

        return VGroup(brace, label)

    def get_computations(self, box, n_lines=10, n_iterations=3, n_digits=4, cycle_time=0.5):
        # Try adding lines
        lines = VGroup()
        for iteration in range(n_iterations):
            cluster = VGroup()
            for n in range(n_lines):
                x = random.uniform(0, 10**(n_digits))
                y = random.uniform(0, 10**(n_digits))
                if random.choice([True, False]):
                    comb = x * y
                    sym = Tex(R"\times")
                else:
                    comb = x + y
                    sym = Tex(R"+")
                line = VGroup(
                    DecimalNumber(x, num_decimal_places=3), sym,
                    DecimalNumber(y, num_decimal_places=3), Tex("="),
                    DecimalNumber(comb, num_decimal_places=3)
                )
                line.arrange(RIGHT, buff=SMALL_BUFF)
                lines.add(line)
                cluster.add(line)
            cluster.arrange(DOWN, buff=MED_LARGE_BUFF, aligned_edge=LEFT)
            cluster.set_max_height(0.9 * box.get_height())
            cluster.set_max_width(0.9 * box.get_width())
            cluster.move_to(box)

        # Add updater
        def update_lines(lines):
            sigma = 0.12
            alpha = (self.time / (cycle_time * n_iterations)) % 1
            step = 1.0 / len(lines)
            for n, line in enumerate(lines):
                x = min((
                    abs(a - n * step)
                    for a in (alpha - 1, alpha, alpha + 1)
                ))
                y = np.exp(-x**2 / sigma**2)
                line.set_fill(opacity=y)

            lines.set_height(0.9 * box.get_height())
            lines.move_to(box)

        lines.clear_updaters()
        lines.add_updater(update_lines)

        return lines

    def old(self):
        # Repeatedly scale down
        to_fade = VGroup(sec_brace, sec_label, box, comps, new_boxes, computations)
        scale_factors = [60, 24, 365, 1000]
        for new_int, prev_int, scale_factor in zip(number_lines[1:], number_lines[0:], scale_factors):
            self.fade_in_bigger_interval(
                new_int, prev_int, to_fade, scale_factor,
                added_anims=[label.animate.set_opacity(0)],
            )
            self.wait(2)
            to_fade = prev_int

        # Multiply last line by 100
        self.fade_in_bigger_interval(
            y1M_line, millenium_line, year_line, 1000,
            added_anims=[self.frame.animate.reorient(0, 0, 0, (-3.51, -5.18, 0.0), 12.93)],
        )

        lines = Line(LEFT, RIGHT).replicate(100)
        lines.match_width(y1M_line)
        lines.arrange_to_fit_height(10)
        lines.sort(lambda p: -p[1])
        lines.set_stroke(WHITE, 1)
        lines.move_to(y1M_line[0].get_center(), UP)

        side_brace, label100M = self.get_timeline_full_label(y1M_line, "100,000,000 Years")
        side_brace.rotate(PI / 2)
        side_brace.match_height(lines)
        side_brace.next_to(lines, LEFT)
        label100M.next_to(side_brace, LEFT)

        self.play(
            LaggedStart(
                (TransformFromCopy(lines[0].copy().set_opacity(0), line)
                for line in lines),
                lag_ratio=0.03,
                run_time=2
            ),
            FadeIn(side_brace, scale=10, shift=2 * DOWN, time_span=(1, 2)),
            FadeIn(label100M, time_span=(1, 2)),
        )
        self.wait()
