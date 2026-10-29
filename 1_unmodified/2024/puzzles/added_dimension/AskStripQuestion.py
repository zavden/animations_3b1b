# ==============================================================================
# Scene:      AskStripQuestion
# Source:     videos/_2024/puzzles/added_dimension.py (lines 1241-1495)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl AskStripQuestion.py AskStripQuestion -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class AskStripQuestion(InteractiveScene):
    def construct(self):
        # Add circle
        radius = 2.5
        circle = Circle(radius=radius)
        circle.set_stroke(YELLOW, 2)
        radial_line = Line(circle.get_center(), circle.get_right())
        radial_line.set_stroke(WHITE, 2)
        radius_label = Integer(1)
        radius_label.next_to(radial_line, UP, SMALL_BUFF)

        self.play(
            ShowCreation(radial_line),
            FadeIn(radius_label, RIGHT)
        )
        self.play(
            Rotate(radial_line, 2 * PI, about_point=circle.get_center()),
            ShowCreation(circle),
            run_time=2
        )
        self.wait()

        # Show first strip
        r0_tracker = ValueTracker(0.2)
        r1_tracker = ValueTracker(0.8)
        strip1 = always_redraw(lambda: self.get_strip(
            circle,
            r0_tracker.get_value(), r1_tracker.get_value(),
            theta=TAU / 3,
            color=TEAL,
            include_arrow=True,
            label=""
        ))
        radius = radial_line.get_length()
        width_label = DecimalNumber(0)
        width_label.add_updater(lambda m: m.set_value(r1_tracker.get_value() - r0_tracker.get_value()))
        width_label.add_updater(lambda m: m.set_height(min(0.33, 0.5 * strip1.submobjects[0].get_height())))
        width_label.always.next_to(strip1.submobjects[0].get_center(), UR, SMALL_BUFF)

        d_label = Tex(R"d_1")
        d_label.move_to(width_label, DL)

        strip1.suspend_updating()
        self.animate_strip_in(strip1)
        self.wait()

        self.play(Write(width_label, suspend_mobject_updating=True))
        strip1.resume_updating()
        self.play(
            r0_tracker.animate.set_value(0.49),
            r1_tracker.animate.set_value(0.51),
            run_time=4,
            rate_func=there_and_back,
        )
        strip1.clear_updaters()
        width_label.clear_updaters()
        self.wait()
        self.play(ReplacementTransform(width_label, d_label))
        strip1.add(d_label)

        # Add first couple strips
        new_strips = VGroup(
            self.get_strip(
                circle, r0, r1, angle,
                color=color,
                include_arrow=True,
                label=f"d_{n}",
            )
            for n, r0, r1, angle, color in [
                (2, 0.5, 0.75, 2 * TAU / 3, GREEN),
                (3, 0.1, 0.3, 0.8 * TAU, BLUE_D),
                (4, 0.4, 0.7, 0.1 * TAU, BLUE_B),
            ]
        )

        for strip in new_strips:
            self.animate_strip_in(strip)

        # Cover in lots of strips
        np.random.seed(0)
        strips = VGroup(
            self.get_strip(
                circle,
                *sorted(np.random.uniform(-1, 1, 2)),
                TAU * np.random.uniform(0, TAU),
                opacity=0.25
            ).set_stroke(width=1)
            for n in range(10)
        )
        self.add(strips, strip1, new_strips, circle, radius_label)
        self.play(FadeIn(strips, lag_ratio=0.5, run_time=3))
        self.wait()

        # Add together all the widths
        frame = self.frame
        arrows = VGroup(strip.submobjects[0] for strip in (strip1, *new_strips))
        d_labels = VGroup(strip.submobjects[1] for strip in (strip1, *new_strips))

        top_expr = Tex(R"d_1 + d_2 + d_3 + d_4 + \cdots + d_n")
        top_expr.to_edge(UP, buff=0)
        d_labels.target = VGroup(
            top_expr[f"d_{n}"][0]
            for n in range(1, 5)
        )

        self.play(
            LaggedStart(
                MoveToTarget(d_labels, lag_ratio=0.01),
                Write(top_expr["+"]),
                Write(top_expr[R"\cdots"]),
                Write(top_expr[R"d_n"]),
                lag_ratio=0.5
            ),
            FadeOut(arrows),
            frame.animate.move_to(UP).set_anim_args(run_time=2)
        )
        self.remove(d_labels)
        self.add(top_expr)
        self.wait()

        # Compress sum
        short_expr = Tex(R"\min\left( \sum_i d_i \right)")
        short_expr.move_to(top_expr)

        self.play(
            LaggedStart(
                ReplacementTransform(top_expr[re.compile("d_.")], short_expr["d_i"]),
                ReplacementTransform(top_expr["+"], short_expr[R"\sum"]),
                ReplacementTransform(top_expr[R"\cdots"], short_expr["i"][1]),
                lag_ratio=0.25
            )
        )
        self.wait()
        self.play(LaggedStart(
            Write(short_expr[R"\min\left("]),
            Write(short_expr[R"\right)"]),
            lag_ratio=0.5
        ))
        self.wait()

        # Show various alternate coverings
        d_labels.set_opacity(0)
        arrows.set_opacity(0)
        curr_strips = VGroup(strip1, *new_strips, *strips)
        og_strips = curr_strips

        for _ in range(4):
            self.play(FadeOut(curr_strips))
            base_hue = random.random()
            curr_strips = VGroup(
                self.get_strip(
                    circle,
                    *sorted(np.random.uniform(-1, 1, 2)),
                    TAU * np.random.uniform(0, TAU),
                    color=random_bright_color(hue_range=(base_hue, base_hue + 0.2)),
                    opacity=0.25
                ).set_stroke(width=1)
                for n in range(15)
            )
            self.play(ShowIncreasingSubsets(curr_strips))

        self.play(FadeOut(curr_strips))
        self.play(ShowIncreasingSubsets(og_strips))

        # Show trivial covering
        fat_strip = self.get_strip(circle, -1, 1, 0, RED_B)
        fat_strip.rect.set_height(6, stretch=True)
        fat_strip.pre_rect.move_to(fat_strip.rect, DOWN)

        top_brace = Brace(fat_strip.rect, UP)
        top_label = top_brace.get_text("2")

        self.play(
            FadeOut(og_strips),
            short_expr.animate.next_to(circle, RIGHT, buff=LARGE_BUFF),
            frame.animate.move_to(0.5 * UP)
        )
        self.play(Transform(fat_strip.pre_rect, fat_strip.rect))
        self.play(GrowFromCenter(top_brace), Write(top_label))
        self.wait()

        # Subdivide trivial covering
        subdivision = sorted([-1, 1, *np.random.uniform(-1, 1, 10)])
        strips = VGroup(
            self.get_strip(circle, r0, r1, theta=0, color=random_bright_color(hue_range=(0.3, 0.5)))
            for r0, r1 in zip(subdivision, subdivision[1:])
        )

        self.play(
            FadeOut(fat_strip.pre_rect),
            FadeIn(strips, lag_ratio=0.5, run_time=2)
        )
        self.wait()

        # Show suggestive fan covering
        fan_covering = VGroup(
            self.get_strip(circle, -0.4, 0.4, theta=theta)
            for theta in np.arange(0, TAU, TAU / 3)
        )
        fan_covering.add(*(
            self.get_strip(circle, 0.6, 0.9, theta=theta)
            for theta in np.arange(TAU / 12, TAU, TAU / 3)
        ))

        self.play(FadeOut(strips))
        for strip in fan_covering:
            self.animate_strip_in(strip)
        self.wait()

    def get_strip(self, circle, r0, r1, theta, color=None, opacity=0.5, include_arrow=False, label="", rect_length=10.0):
        diam = circle.get_width()
        width = (r1 - r0) * diam / 2
        if color is None:
            color = random_bright_color(luminance_range=(0.5, 0.7))

        rect = Rectangle(width, rect_length)
        rect.move_to(
            interpolate(circle.get_center(), circle.get_right(), r0),
            LEFT,
        )
        rect.set_fill(color, opacity)
        rect.set_stroke(color, 1)
        pre_rect = rect.copy().stretch(0, 1, about_edge=DOWN)
        pre_rect.set_stroke(width=0)
        VGroup(rect, pre_rect).rotate(theta, about_point=circle.get_center())

        strip = Intersection(rect, circle)
        strip.match_style(rect)
        strip.rect = rect
        strip.pre_rect = pre_rect

        if include_arrow:
            arrow = Tex(R"\longleftrightarrow")
            arrow.set_width(width, stretch=True)
            arrow.rotate(theta)
            arrow.move_to(rect)
            strip.add(arrow)
        if len(label) > 0:
            label = Tex(label, font_size=36)
            label.move_to(rect.get_center())
            vect = 0.25 * rotate_vector(UP, theta)
            vect *= np.sign(vect[1])
            label.shift(vect)
            strip.add(label)

        return strip

    def animate_strip_in(self, strip):
        self.play(Transform(strip.pre_rect, strip.rect))
        self.play(LaggedStart(
            FadeIn(strip),
            FadeOut(strip.pre_rect),
            lag_ratio=0.5,
            run_time=1,
        ))
