# ==============================================================================
# Scene:      CommentsOnNaming
# Source:     videos/_2021/newton_fractal.py (lines 4403-4539)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl CommentsOnNaming.py CommentsOnNaming -w -m --fps 15
#
# Placeholder assets (not Grant's originals):
#   - _lib/assets/raster_images/FFT_Diagram.png (placeholder; generator _lib/assets/generated/2021/newton_fractal/make_newton_fractal_assets.py)
# ==============================================================================

from manim_imports_ext import *

def get_newton_rule(font_size=36, var="z", **kwargs):
    terms = [f"{var}_n", f"{var}_{{n + 1}}"]
    t0, t1 = terms
    return OldTex(
        t1, "=", t0, "-",
        "{P(", t0, ")", "\\over ", "P'(", t0, ")}",
        font_size=36,
        **kwargs
    )


def get_figure(image_name, person_name, year_text, height=3, label_direction=DOWN):
    image = ImageMobject(image_name)
    image.set_height(height)
    rect = SurroundingRectangle(image, buff=0)
    rect.set_stroke(WHITE, 2)
    name = Text(f"{person_name}", font_size=36)
    name.set_color(GREY_A)
    year_label = Text(f"{year_text}", font_size=30)
    year_label.match_color(name)
    year_label.next_to(name, DOWN, buff=0.2)
    VGroup(name, year_label).next_to(image, label_direction)
    return Group(rect, image, name, year_label)


class CommentsOnNaming(Scene):
    def construct(self):
        self.setup_table()
        self.show_everyone()

    def setup_table(self):
        titles = VGroup(
            OldTexText("How it started", font_size=60),
            OldTexText("How it's going", font_size=60),
        )
        titles.to_edge(UP, buff=MED_SMALL_BUFF)
        titles.set_color(GREY_A)
        titles[0].set_x(-FRAME_WIDTH / 4)
        titles[1].set_x(FRAME_WIDTH / 4)
        h_line = Line(LEFT, RIGHT).set_width(FRAME_WIDTH)
        h_line.next_to(titles, DOWN).set_x(0)
        v_line = Line(UP, DOWN).set_height(FRAME_HEIGHT)
        lines = VGroup(h_line, v_line)
        lines.set_stroke(WHITE, 2)

        self.left_point = [-FRAME_WIDTH / 4, -1, 0]
        self.right_point = [FRAME_WIDTH / 4, -1, 0]

        self.add(titles, lines)

    def show_everyone(self):
        # Newton
        newton = get_figure(
            "Newton", "Isaac Newton", "1643-1727",
            height=4,
        )
        newton.move_to(self.left_point)

        newton_formula = get_newton_rule(var="x")
        newton_formula.next_to(newton, UP)

        nf_label = OldTexText("``Newton's'' fractal")
        nf_label.align_to(newton_formula, UP)
        nf_label.set_x(self.right_point[0])

        self.play(
            FadeIn(newton_formula),
            LaggedStartMap(FadeIn, newton)
        )
        self.wait()
        self.play(Write(nf_label))
        self.wait(2)

        # Hamilton
        hamilton = get_figure(
            "Hamilton", "William Rowan Hamilton", "1805 - 1865",
            height=4,
        )
        hamilton.move_to(self.left_point)
        hamiltons_equation = OldTex(
            r"\frac{\mathrm{d} \boldsymbol{q}}{\mathrm{d} t}=\frac{\partial \mathcal{H}}{\partial \boldsymbol{p}}, \quad \frac{\mathrm{d} \boldsymbol{p}}{\mathrm{d} t}=-\frac{\partial \mathcal{H}}{\partial \boldsymbol{q}}"
        )
        hamiltons_equation.match_width(hamilton[0])
        hamiltons_equation.next_to(hamilton, UP)

        hamiltonians = Text("Hamiltonians")
        hamiltonians.move_to(nf_label)

        self.play(
            LaggedStart(
                FadeOut(newton, shift=0.25 * LEFT),
                FadeOut(newton_formula, shift=0.25 * LEFT),
                FadeOut(nf_label, shift=0.25 * RIGHT),
            ),
            LaggedStart(
                FadeIn(hamilton, shift=0.25 * LEFT),
                FadeIn(hamiltons_equation, shift=0.25 * LEFT),
                FadeIn(hamiltonians, shift=0.25 * RIGHT),
            )
        )
        self.wait(2)

        # Fourier
        fourier = get_figure(
            "Joseph Fourier", "Joseph Fourier", "1768-1830",
            height=4
        )
        fourier.move_to(self.left_point)
        fourier_transform = OldTex(
            r"f(t)=\int_{0}^{\infty}(a(\lambda) \cos (2 \pi \lambda t)+b(\lambda) \sin (2 \pi \lambda t)) d \lambda"
        )
        fourier_transform.set_width(fourier.get_width() * 1.5)
        fourier_transform.next_to(fourier, UP)

        FFT = Text("FFT")
        FFT.move_to(hamiltonians)

        FFT_diagram = ImageMobject("FFT_Diagram")
        FFT_diagram.move_to(self.right_point),

        self.play(
            LaggedStart(
                FadeOut(hamilton, shift=0.25 * LEFT),
                FadeOut(hamiltons_equation, shift=0.25 * LEFT),
                FadeOut(hamiltonians, shift=0.25 * RIGHT),
            ),
            LaggedStart(
                FadeIn(fourier, shift=0.25 * LEFT),
                FadeIn(fourier_transform, shift=0.25 * LEFT),
                FadeIn(FFT, shift=0.25 * RIGHT),
            ),
            FadeIn(FFT_diagram),
        )
        self.wait(2)

        # Everyone
        people = Group(newton, hamilton, fourier)
        people.generate_target()
        people.target.arrange(DOWN, buff=LARGE_BUFF)
        people.target.set_height(6.4)
        people.target.move_to(self.left_point)
        people.target.to_edge(DOWN, buff=SMALL_BUFF)

        self.play(
            FadeOut(fourier_transform),
            FadeOut(FFT),
            MoveToTarget(people, run_time=2),
            FFT_diagram.animate.scale(1 / 3).match_y(people.target[2]),
        )

        arrow = Arrow(
            fourier, FFT_diagram,
            buff=1.0,
            stroke_width=8
        )
        arrows = VGroup(
            arrow.copy().match_y(newton),
            arrow.copy().match_y(hamilton),
            arrow,
        )
        self.play(LaggedStartMap(ShowCreation, arrows, lag_ratio=0.5, run_time=3))
        self.wait()
