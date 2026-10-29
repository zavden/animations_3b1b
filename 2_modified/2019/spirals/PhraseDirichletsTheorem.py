# ==============================================================================
# Scene:      PhraseDirichletsTheorem
# Source:     videos/_2019/spirals.py (lines 4045-4212)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl PhraseDirichletsTheorem.py PhraseDirichletsTheorem -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Use CairoImageMobject to keep Cairo's default height and pixel reading, without changing other years.
# ==============================================================================

from manim_imports_ext import *

# CHANGE: keep Cairo's height (2) and the pixel_array reading through a local adapter.
from cairo_compat import CairoImageMobject as ImageMobject

class DirichletIn1837(Scene):
    def construct(self):
        # Add timeline
        dates = list(range(1780, 2030, 10))
        timeline = NumberLine(
            x_min=1700,
            x_max=2020,
            tick_frequency=1,
            big_tick_numbers=dates,
            unit_size=0.2,
            stroke_color=GREY,
            stroke_width=2,
        )
        timeline.add_numbers(
            *dates,
            group_with_commas=False,
        )
        timeline.numbers.shift(SMALL_BUFF * DOWN)
        timeline.to_edge(RIGHT)

        # Special dates
        d_arrow, rh_arrow, pnt_arrow = arrows = VGroup(*[
            Vector(DOWN).next_to(timeline.n2p(date), UP)
            for date in [1837, 1859, 1896]
        ])
        d_label, rh_label, pnt_label = labels = VGroup(*[
            OldTexText(text).next_to(arrow, UP)
            for arrow, text in zip(arrows, [
                "Dirichlet's\\\\theorem\\\\1837",
                "Riemann\\\\hypothesis\\\\1859",
                "Prime number\\\\theorem\\\\1896",
            ])
        ])

        # Back in time
        frame = self.camera_frame
        self.add(timeline, arrows, labels)
        self.play(
            frame.move_to, timeline.n2p(1837),
            run_time=4,
        )
        self.wait()

        # Show picture
        image = ImageMobject("Dirichlet")
        image.set_height(3)
        image.next_to(d_label, LEFT)
        self.play(FadeIn(image, RIGHT))
        self.wait()

        # Flash
        self.play(
            Flash(
                d_label.get_center(),
                num_lines=12,
                line_length=0.25,
                flash_radius=1.5,
                line_stroke_width=3,
                lag_ratio=0.05,
            )
        )
        self.wait()

        # Transition title
        title, underline = self.get_title_and_underline()
        n = len(title[0])
        self.play(
            ReplacementTransform(d_label[0][:n], title[0][:n]),
            FadeOut(d_label[0][n:]),
            LaggedStartMap(
                FadeOutAndShiftDown, Group(
                    image, d_arrow,
                    rh_label, rh_arrow,
                    pnt_label, pnt_arrow,
                    *timeline,
                )
            ),
        )
        self.play(ShowCreation(underline))
        self.wait()

    def get_title_and_underline(self):
        frame = self.camera_frame
        title = OldTexText("Dirichlet's theorem")
        title.scale(1.5)
        title.next_to(frame.get_top(), DOWN, buff=MED_LARGE_BUFF)
        underline = Line()
        underline.match_width(title)
        underline.next_to(title, DOWN, SMALL_BUFF)
        return title, underline


class PhraseDirichletsTheorem(DirichletIn1837):
    def construct(self):
        self.add(*self.get_title_and_underline())

        # Copy-pasted, which isn't great
        expression = OldTex(
            "\\lim_{x \\to \\infty}",
            "\\left(",
            "{\\text{\\# of primes $p$ where $p \\le x$} \\text{ and $p \\equiv 1$ mod 10}",
            "\\over",
            "\\text{\\# of primes $p$ where $p \\le x$}}",
            "\\right)",
            "=",
            "\\frac{1}{4}",
        )
        lim, lp, num, over, denom, rp, eq, fourth = expression
        expression.shift(1.5 * UP)
        expression.to_edge(LEFT, MED_SMALL_BUFF)
        num[len(denom):].set_color(YELLOW)
        #

        # Terms and labels
        ten = num[-2:]
        one = num[-6]
        four = fourth[-1]

        N = OldTex("N")
        r = OldTex("r")
        one_over_phi_N = OldTex("1", "\\over", "\\phi(", "N", ")")

        N.set_color(MAROON_B)
        r.set_color(BLUE)
        one_over_phi_N.set_color_by_tex("N", N.get_color())

        N.move_to(ten, DL)
        r.move_to(one, DOWN)
        one_over_phi_N.move_to(fourth, LEFT)

        N_label = OldTexText("$N$", " is any number")
        N_label.set_color_by_tex("N", N.get_color())
        N_label.next_to(expression, DOWN, LARGE_BUFF)

        r_label = OldTexText("$r$", " is coprime to ", "$N$")
        r_label[0].set_color(r.get_color())
        r_label[2].set_color(N.get_color())
        r_label.next_to(N_label, DOWN, MED_LARGE_BUFF)

        phi_N_label = OldTex(
            "\\phi({10}) = ",
            "\\#\\{1, 3, 7, 9\\} = 4",
            tex_to_color_map={
                "{10}": N.get_color(),
            }
        )
        phi_N_label[-1][2:9:2].set_color(r.get_color())
        phi_N_label.next_to(r_label, DOWN, MED_LARGE_BUFF)
        #

        self.play(
            LaggedStart(*[
                FadeIn(denom),
                ShowCreation(over),
                FadeIn(num),
                Write(VGroup(lp, rp)),
                FadeIn(lim),
                Write(VGroup(eq, fourth)),
            ]),
            run_time=3,
            lag_ratio=0.7,
        )
        self.wait()
        for mob in denom, num:
            self.play(ShowCreationThenFadeAround(mob))
            self.wait()
        self.play(
            FadeIn(r, DOWN),
            FadeOut(one, UP),
        )
        self.play(
            FadeIn(N, DOWN),
            FadeOut(ten, UP),
        )
        self.wait()
        self.play(
            TransformFromCopy(N, N_label[0]),
            FadeIn(N_label[1:], DOWN)
        )
        self.wait()
        self.play(
            FadeIn(r_label[1:-1], DOWN),
            TransformFromCopy(r, r_label[0]),
        )
        self.play(
            TransformFromCopy(N_label[0], r_label[-1]),
        )
        self.wait()

        self.play(
            ShowCreationThenFadeAround(fourth),
        )
        self.play(
            FadeIn(one_over_phi_N[2:], LEFT),
            FadeOut(four, RIGHT),
            ReplacementTransform(fourth[0], one_over_phi_N[0][0]),
            ReplacementTransform(fourth[1], one_over_phi_N[1][0]),
        )
        self.play(
            FadeIn(phi_N_label, DOWN)
        )
        self.wait()

        # Fancier version
        new_expression = OldTex(
            "\\lim_{x \\to \\infty}",
            "\\left(",
            "{\\pi(x; {N}, {r})",
            "\\over",
            "\\pi(x)}",
            "\\right)",
            "=",
            "\\frac{1}{\\phi({N})}",
            tex_to_color_map={
                "{N}": N.get_color(),
                "{r}": r.get_color(),
                "\\pi": WHITE,
            }
        )
        pis = new_expression.get_parts_by_tex("\\pi")

        randy = Randolph(height=2)
        randy.next_to(new_expression, LEFT, buff=LARGE_BUFF)
        randy.shift(0.75 * DOWN)

        new_expression.next_to(expression, DOWN, LARGE_BUFF)
        ne_rect = SurroundingRectangle(new_expression, color=BLUE)

        label_group = VGroup(N_label, r_label)
        label_group.generate_target()
        label_group.target.arrange(RIGHT, buff=LARGE_BUFF)
        label_group.target.next_to(new_expression, DOWN, buff=LARGE_BUFF)

        self.play(
            FadeIn(randy),
        )
        self.play(
            randy.change, "hooray", expression
        )
        self.play(Blink(randy))
        self.wait()
        self.play(
            FadeIn(new_expression),
            MoveToTarget(label_group),
            phi_N_label.to_edge, DOWN, MED_LARGE_BUFF,
            randy.change, "horrified", new_expression,
        )
        self.play(ShowCreation(ne_rect))
        self.play(randy.change, "confused")
        self.play(Blink(randy))
        self.wait()
        self.play(
            LaggedStartMap(
                ShowCreationThenFadeAround, pis,
            ),
            randy.change, "angry", new_expression
        )
        self.wait()
        self.play(Blink(randy))
        self.wait()
