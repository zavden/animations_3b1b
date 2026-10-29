# ==============================================================================
# Scene:      StruggleWithStrips
# Source:     videos/_2024/puzzles/added_dimension.py (lines 1498-1735)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl StruggleWithStrips.py StruggleWithStrips -w -m --fps 15
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


class StruggleWithStrips(AskStripQuestion):
    def construct(self):
        # Add circle
        radius = 2.5
        circle = Circle(radius=radius)
        circle.set_stroke(YELLOW, 2)
        radial_line = Line(circle.get_center(), circle.get_right())
        radial_line.set_stroke(WHITE, 2)
        radius_label = Integer(1)
        radius_label.next_to(radial_line, UP, SMALL_BUFF)

        self.add(circle, radial_line, radius_label)

        # Show fan strategy
        angles = [*np.arange(0, TAU, TAU / 3), *np.arange(TAU / 12, TAU, TAU / 3)]
        widths = [*3 * [0.8], *3 * [0.25]]
        strips = VGroup(
            self.get_strip(circle, -0.4, 0.4, theta=theta, include_arrow=True)
            for theta in angles[:3]
        )
        strips.add(*(
            self.get_strip(circle, 0.7, 0.95, theta=theta, include_arrow=True)
            for theta in angles[3:]
        ))
        arrows = VGroup()
        for strip in strips:
            arrow = strip[0]
            strip.remove(arrow)
            arrows.add(arrow)

        self.play(LaggedStart(
            (TransformFromCopy(strip.pre_rect, strip.rect)
            for strip in strips),
            lag_ratio=0.1,
        ))
        rects = VGroup(strip.rect for strip in strips)
        self.play(
            LaggedStartMap(FadeOut, rects),
            LaggedStartMap(FadeIn, strips),
        )

        # Show the sum
        sum_expr = Tex("0.00 + 0.00 + 0.00 + 0.00 + 0.00 + 0.00 = 0.00")
        sum_expr.to_edge(UP)
        decimals = sum_expr.make_number_changeable("0.00", replace_all=True)
        width_terms = decimals[:6]
        sum_term = decimals[6]
        plusses = sum_expr["+"]
        equals = sum_expr["="][0]
        plusses.add_to_back(VectorizedPoint(sum_expr.get_left()))

        sum_term.set_fill(RED)

        last_arrow = VGroup()
        for i in range(len(strips)):
            width_term = width_terms[i]
            width_term.set_value(widths[i])
            width_term.save_state()

            arrow = arrows[i]
            width_term.next_to(
                arrow.get_center(),
                rotate_vector(UP, angles[i])
            )

            strips.target = strips.generate_target()
            strips.target.set_opacity(0.2)
            strips.target[i].set_fill(opacity=0.5)
            strips.target[i].set_stroke(opacity=1)

            self.play(
                MoveToTarget(strips),
                FadeIn(width_term),
                FadeIn(arrow),
                FadeOut(last_arrow),
            )
            self.play(
                Restore(width_term),
                FadeIn(plusses[i])
            )

            last_arrow = arrow

        sum_term.set_value(sum(wt.get_value() for wt in width_terms))
        self.play(
            FadeOut(last_arrow),
            strips.animate.set_fill(opacity=0.5).set_stroke(opacity=1),
            Write(equals),
            FadeIn(sum_term),
        )
        self.wait()

        # Turn into parallel strips
        np.random.seed(3)
        subdivision = sorted([-1, 1, *np.random.uniform(-1, 1, 5)])
        r_pairs = list(zip(subdivision, subdivision[1:]))
        new_widths = [r1 - r0 for r0, r1 in r_pairs]

        new_strips = VGroup(
            self.get_strip(circle, r0, r1, theta=0)
            for r0, r1 in r_pairs
        )
        new_strips.match_style(strips)
        new_rects = VGroup(s.rect for s in new_strips)

        self.play(
            FadeOut(strips),
            FadeIn(rects),
        )
        self.play(
            # Transform(strips, new_strips),
            ReplacementTransform(rects, new_rects),
            *(
                ChangeDecimalToValue(width_term, new_width)
                for width_term, new_width in zip(width_terms, new_widths)
            ),
            ChangeDecimalToValue(sum_term, 2.0),
            run_time=2
        )
        self.play(FadeOut(new_rects), FadeIn(new_strips))
        self.wait()

        # Show sum of the area
        width_sum = Tex(R"\sum_{\text{strip}} \textbf{Width}(\text{strip})")
        area_sum = Tex(R"\sum_{\text{strip}} \textbf{Area}(\text{strip})")
        area_sum_rhs = Tex(R"\ge \pi r^2 = \pi")
        width_sum.to_corner(UR)
        area_sum.to_corner(UL)
        area_sum_rhs.next_to(area_sum[-1], RIGHT, MED_SMALL_BUFF)

        width_brace = Brace(width_sum, DOWN)
        width_annotation = width_brace.get_text("We want to\ncontrol this")
        width_annotation.set_color(YELLOW)

        self.play(FadeTransformPieces(sum_expr, width_sum))
        self.play(GrowFromCenter(width_brace), Write(width_annotation))
        self.wait()
        self.play(Write(area_sum))
        self.wait()
        self.play(Write(area_sum_rhs))
        self.wait()

        # Add area and width label for strip
        strip = new_strips[1]
        area_label = TexText(R"Area = $0.00$")
        area_dec = area_label.make_number_changeable("0.00")
        area_dec.add_updater(lambda m: m.set_value(
            get_norm(strip.get_area_vector()) / radius**2
        ))
        area_label.add_updater(lambda m: m.next_to(strip, LEFT))
        area_label.match_color(strip)

        arrow = Tex(R"\leftrightarrow").stretch(2, 0)
        arrow.match_width(strip)
        arrow.always.move_to(strip)

        width_label = VGroup(
            Text("Width"),
            Tex("=").rotate(90 * DEGREES),
            DecimalNumber(1),
        )
        width_label.arrange(DOWN)
        width_label.set_width(strip.get_width() * 0.8)
        width_label[2].add_updater(lambda m: m.set_value(strip.get_width() / radius))
        width_label.always.next_to(arrow, UP)

        self.play(
            FadeOut(new_strips[:1]),
            FadeOut(new_strips[2:]),
            FadeOut(radial_line),
            FadeOut(radius_label),
        )
        self.play(Write(area_label))
        self.wait()
        self.play(
            GrowFromCenter(arrow),
            FadeIn(width_label),
        )
        self.wait()

        # Show varying strip
        r0 = subdivision[1]
        delta_r = subdivision[2] - subdivision[1]
        delta_r_tracker = ValueTracker(delta_r)
        r0_tracker = ValueTracker(r0)

        strip.add_updater(lambda m: m.match_points(self.get_strip(
            circle,
            r0_tracker.get_value(),
            r0_tracker.get_value() + delta_r_tracker.get_value(),
            theta=0
        )))
        for value in [-1, 0.6, r0]:
            self.play(r0_tracker.animate.set_value(value), run_time=4)

        self.play(
            delta_r_tracker.animate.set_value(0.3),
            arrow.animate.scale(0.3 / 0.44),
            run_time=3
        )

        strip.clear_updaters()
        self.play(
            FadeOut(area_label),
            FadeOut(width_label),
            FadeOut(arrow),
            FadeIn(new_strips[:1]),
            FadeIn(new_strips[2:]),
        )

        # Show the dream of proportionality
        width_label_group = VGroup(width_sum, width_brace, width_annotation)
        circle_group = VGroup(circle, new_strips)

        dream_sum = Tex(R"\sum_{\text{strip}} {k} \cdot \textbf{Width}(\text{strip})")
        dream_sum[R"{k}"].set_color(YELLOW)
        dream_sum.next_to(area_sum, DOWN, buff=2.0)
        dream_sum.shift_onto_screen()

        down_arrow = Arrow(area_sum, dream_sum, thickness=5)
        arrow_words = Text("If only...")
        arrow_words.next_to(down_arrow, RIGHT, SMALL_BUFF)

        self.play(
            circle_group.animate.shift(3 * RIGHT),
            width_label_group.animate.scale(0.5, about_edge=UR),
        )
        self.wait()
        self.play(
            GrowArrow(down_arrow),
            FadeIn(arrow_words, lag_ratio=0.1)
        )
        self.play(TransformMatchingStrings(area_sum.copy(), dream_sum))
        self.wait()

    def get_strip(self, *args, **kwargs):
        kwargs["rect_length"] = kwargs.get("rect_length", 6.0)
        return super().get_strip(*args, **kwargs)
