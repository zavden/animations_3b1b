# ==============================================================================
# Scene:      HolomorphicDynamics
# Source:     videos/_2021/holomorphic_dynamics.py (lines 143-315)
# Category:   2 · Renders with modifications
# Includes code copied from: _2021/newton_fractal.py
#
# Run from this folder:
#     manimgl HolomorphicDynamics.py HolomorphicDynamics -w -m --fps 15
#
# Placeholder assets (not Grant's originals):
#   - _lib/assets/raster_images/NewtonBoundaryProperty.png (cubic Newton fractal computed with numpy; generator _lib/assets/generated/2021/newton_fractal/make_newton_fractal_assets.py)
# ==============================================================================

from manim_imports_ext import *


# ----- From _2021/newton_fractal.py -----

class HolomorphicDynamics(Scene):
    def construct(self):
        self.ask_about_property()
        self.repeated_functions()

    def ask_about_property(self):
        back_plane = FullScreenRectangle()
        self.add(back_plane)

        image = ImageMobject("NewtonBoundaryProperty")
        border = SurroundingRectangle(image, buff=0)
        border.set_stroke(WHITE, 2)
        image = Group(border, image)
        image.set_height(FRAME_HEIGHT)

        image.generate_target()
        image.target.set_height(6)
        image.target.to_corner(DL)

        question = Text("Why is this true?")
        question.to_corner(UR)
        arrow = Arrow(
            question.get_left(), image.target.get_top() + RIGHT,
            path_arc=45 * DEGREES
        )

        self.play(
            image.animate.set_height(6).to_corner(DL),
            Write(question),
            ShowCreation(arrow, rate_func=squish_rate_func(smooth, 0.5, 1), run_time=2)
        )
        self.wait()

        title = self.title = Text("Holomorphic Dynamics", font_size=60)
        title.to_edge(UP)

        self.play(
            image.animate.set_height(1).to_corner(DL),
            FadeOut(question, shift=DL, scale=0.2),
            FadeOut(arrow, shift=DL, scale=0.2),
            FadeIn(title, shift=3 * DL, scale=0.5),
            FadeOut(back_plane),
        )
        self.wait()

        self.image = image

    def repeated_functions(self):
        basic_expr = OldTex(
            "z", "\\rightarrow ", " f(z)"
        )
        fz = basic_expr.get_part_by_tex("f(z)")
        basic_expr.next_to(self.title, DOWN, LARGE_BUFF)
        basic_expr.to_edge(LEFT, buff=LARGE_BUFF)
        brace = Brace(fz, DOWN)
        newton = OldTex("z - {P(z) \\over P'(z)}")
        newton.next_to(brace, DOWN)
        newton.align_to(basic_expr[1], LEFT)
        newton_example = OldTex("z - {z^3 + z - 1 \\over 3z^2 + 1}")
        eq = OldTex("=").rotate(PI / 2)
        eq.next_to(newton, DOWN)
        newton_example.next_to(eq, DOWN)

        newton_group = VGroup(newton, eq, newton_example)
        newton_group.generate_target()
        newton_group.target[1].rotate(-PI / 2)
        newton_group.target.arrange(RIGHT, buff=0.2)
        newton_group.target[2].shift(SMALL_BUFF * UP)
        newton_group.target.scale(0.7)
        newton_group.target.to_corner(DL)

        mandelbrot = OldTex("z^2 + c")
        mandelbrot.next_to(brace, DOWN)

        exponential = OldTex("a^z")
        exponential.next_to(brace, DOWN)

        self.play(
            FadeIn(basic_expr),
            FadeOut(self.image)
        )
        self.wait()
        self.describe_holomorphic(fz, brace)
        self.wait()
        self.play(
            FadeIn(newton),
        )
        self.play(
            FadeIn(eq),
            FadeIn(newton_example),
        )
        self.wait()
        self.play(
            MoveToTarget(newton_group),
            FadeIn(mandelbrot, DOWN),
        )
        self.wait()
        self.play(
            mandelbrot.animate.scale(0.7).next_to(newton, UP, LARGE_BUFF, LEFT),
            FadeIn(exponential, DOWN)
        )
        self.wait()

        # Show fractals
        rhss = VGroup(exponential, mandelbrot, newton)
        f_eqs = VGroup()
        lhss = VGroup()
        for rhs in rhss:
            rhs.generate_target()
            if rhs is not exponential:
                rhs.target.scale(1 / 0.7)
            lhs = OldTex("f(z) = ")
            lhs.next_to(rhs.target, LEFT)
            f_eqs.add(VGroup(lhs, rhs.target))
            lhss.add(lhs)
        f_eqs.arrange(RIGHT, buff=1.5)
        f_eqs.next_to(self.title, DOWN, MED_LARGE_BUFF)

        rects = ScreenRectangle().replicate(3)
        rects.arrange(DOWN, buff=0.5)
        rects.set_height(6.5)
        rects.next_to(ORIGIN, RIGHT, MED_LARGE_BUFF)
        rects.to_edge(DOWN, MED_SMALL_BUFF)
        rects.set_stroke(WHITE, 1)
        arrows = VGroup()
        for rect, f_eq in zip(rects, f_eqs):
            arrow = Vector(0.7 * RIGHT)
            arrow.next_to(rect, LEFT)
            arrows.add(arrow)
            f_eq.next_to(arrow, LEFT)

        self.play(
            LaggedStartMap(MoveToTarget, rhss),
            LaggedStartMap(Write, lhss),
            LaggedStartMap(FadeIn, rects),
            LaggedStartMap(ShowCreation, arrows),
            FadeOut(brace),
            basic_expr.animate.to_edge(UP),
            FadeOut(newton_group[1:]),
        )
        self.wait()

    def describe_holomorphic(self, fz, brace):
        self.title.set_stroke(BLACK, 5, background=True)
        word = self.title.get_part_by_text("Holomorphic")
        underline = Underline(word, buff=-0.05)
        underline.scale(1.2)
        underline.insert_n_curves(40)
        underline.set_stroke(YELLOW, [1, *6 * [3], 1])

        self.add(underline, self.title)
        self.play(
            word.animate.set_fill(YELLOW),
            ShowCreation(underline)
        )

        in_words = Text("Complex\ninputs", font_size=36)
        in_words.to_corner(UL)
        in_arrow = Arrow(
            in_words.get_right(),
            fz[2].get_top(),
            path_arc=-80 * DEGREES,
            buff=0.2,
        )
        VGroup(in_words, in_arrow).set_color(YELLOW)

        out_words = Text("Complex\noutputs", font_size=36)
        out_words.next_to(brace, DOWN)
        out_words.set_color(YELLOW)

        f_prime = OldTexText("$f'(z)$ exists")
        f_prime.set_color(YELLOW)
        f_prime.next_to(underline, DOWN, MED_LARGE_BUFF)
        f_prime.match_y(fz)

        self.wait()
        self.play(
            Write(in_words),
            ShowCreation(in_arrow),
            run_time=1,
        )
        self.play(
            GrowFromCenter(brace),
            FadeIn(out_words, lag_ratio=0.05)
        )
        self.wait()
        self.play(FadeIn(f_prime, 0.5 * DOWN))
        self.wait()

        self.play(
            LaggedStartMap(FadeOut, VGroup(
                in_words, in_arrow, out_words, f_prime, underline,
            )),
            word.animate.set_fill(WHITE)
        )



# ----- From _2021/holomorphic_dynamics.py -----

def get_iteration_label(font_size=36):
    kw = {
        "tex_to_color_map": {
            "z_0": BLUE_C,
            "z_1": BLUE_D,
            "z_2": GREEN_D,
            "z_3": GREEN_E,
            "z_{n + 1}": GREEN_D,
            "z_n": BLUE,
            "\\longrightarrow": WHITE,
        },
        "font_size": font_size,
    }
    iterations = OldTex(
        """
        z_0 \\longrightarrow
        z_1 \\longrightarrow
        z_2 \\longrightarrow
        z_3 \\longrightarrow
        \\cdots
        """,
        **kw
    )
    for part in iterations.get_parts_by_tex("\\longrightarrow"):
        f = OldTex("f", **kw)
        f.scale(0.5)
        f.next_to(part, UP, buff=0)
        part.add(f)

    rule = OldTex("z_{n + 1} &= f(z_n)", **kw)
    result = VGroup(rule, iterations)
    result.arrange(DOWN, buff=MED_LARGE_BUFF)
    return result


class HolomorphicDynamics(Scene):
    def construct(self):
        self.show_goals()
        self.complex_functions()
        self.repeated_functions()
        self.example_fractals()

    def show_goals(self):
        background = FullScreenRectangle()
        self.add(background)

        title = self.title = Text("Holomorphic Dynamics", font_size=60)
        title.to_edge(UP)
        title.set_stroke(BLACK, 3, background=True)
        underline = Underline(title, buff=-0.05)
        underline.scale(1.2)
        underline.insert_n_curves(20)
        underline.set_stroke(YELLOW, [1, *5 * [3], 1])
        self.add(title)
        self.add(underline, title)
        self.play(ShowCreation(underline))
        self.wait()

        frames = Square().replicate(2)
        frames.set_height(5)
        frames.set_width(6, stretch=True)
        frames.set_stroke(WHITE, 2)
        frames.set_fill(BLACK, 1)
        frames.arrange(RIGHT, buff=1)
        frames.to_edge(DOWN)

        goals = VGroup(
            # OldTexText("Newton's fractal $\\leftrightarrow$ Mandelbrot"),
            # OldTexText("Tie up loose ends"),
            OldTexText("Goal 1: Other Mandelbrot occurrences"),
            OldTexText("Goal 2: Tie up loose ends"),
        )
        goals.set_width(frames[0].get_width())
        goals.set_fill(GREY_A)
        for goal, frame in zip(goals, frames):
            goal.next_to(frame, UP)
            goal.align_to(goals[0], UP)

        self.play(
            FadeIn(frames[0]),
            FadeIn(goals[0], 0.5 * UP),
        )
        self.wait()
        self.play(
            FadeIn(frames[1]),
            FadeIn(goals[1], 0.5 * UP),
        )
        self.wait()

        # Transition
        rect = SurroundingRectangle(title.get_part_by_text("Holomorphic"))
        rect.set_stroke(YELLOW, 2)
        self.play(
            ReplacementTransform(underline, rect),
            FadeOut(background),
            LaggedStartMap(FadeOut, VGroup(
                *goals, *frames,
            ))
        )

        self.title_rect = rect

    def complex_functions(self):
        kw = {
            "tex_to_color_map": {
                "\\mathds{C}": BLUE,
                "z": YELLOW,
            }
        }
        f_def = VGroup(
            OldTex("f : \\mathds{C} \\rightarrow \\mathds{C}", **kw),
            OldTex("f'(z) \\text{ exists}", **kw)
        )
        f_def.arrange(RIGHT, aligned_edge=DOWN, buff=LARGE_BUFF)
        f_def.next_to(self.title, DOWN, buff=MED_LARGE_BUFF)

        for part in f_def:
            self.play(Write(part, stroke_width=1))
            self.wait()

        # Examples
        examples = VGroup(
            OldTex("f(z) = z^2 + 1", **kw),
            OldTex("f(z) = e^z", **kw),
            OldTex("f(z) = \\sin\\left(z\\right)", **kw),
            OldTex("\\vdots")
        )
        examples.arrange(DOWN, buff=0.35, aligned_edge=LEFT)
        examples[-1].shift(0.25 * RIGHT)
        examples.set_width(2.5)
        examples.to_corner(UL)

        self.play(LaggedStartMap(
            FadeIn, examples,
            shift=0.25 * DOWN,
            run_time=3,
            lag_ratio=0.5
        ))

        # Transition
        rect = self.title_rect
        new_rect = SurroundingRectangle(self.title.get_part_by_text("Dynamics"))
        new_rect.match_style(rect)

        self.play(
            FadeOut(examples, lag_ratio=0.1),
            FadeOut(f_def, lag_ratio=0.1),
            Transform(rect, new_rect)
        )
        self.wait()

    def repeated_functions(self):
        words = OldTexText("For some function $f(z)$,")
        rule, iterations = get_iteration_label()
        group = VGroup(words, iterations, rule)
        group.arrange(DOWN, buff=MED_LARGE_BUFF)
        group.next_to(self.title, DOWN, LARGE_BUFF)
        group.to_edge(LEFT)

        self.play(
            FadeIn(words),
            FadeIn(iterations, lag_ratio=0.2, run_time=2)
        )
        self.play(FadeIn(rule, 0.5 * DOWN))
        self.wait()
        self.play(LaggedStartMap(FadeOut, VGroup(
            words, iterations, rule, self.title_rect
        )))

    def example_fractals(self):
        newton = OldTex("z - {P(z) \\over P'(z)}")
        mandelbrot = OldTex("z^2 + c")
        exponential = OldTex("a^z")

        rhss = VGroup(newton, mandelbrot, exponential)
        f_eqs = VGroup()
        lhss = VGroup()
        for rhs in rhss:
            rhs.generate_target()
            lhs = OldTex("f(z) = ")
            lhs.next_to(rhs, LEFT)
            f_eqs.add(VGroup(lhs, rhs))
            lhss.add(lhs)
        VGroup(exponential, mandelbrot).shift(0.05 * UP)
        f_eqs.arrange(RIGHT, buff=1.5)
        f_eqs.next_to(self.title, DOWN, MED_LARGE_BUFF)

        rects = Square().replicate(3)
        rects.arrange(RIGHT, buff=0.2 * rects.get_width())
        rects.set_width(FRAME_WIDTH - 1)
        rects.center().to_edge(DOWN, buff=LARGE_BUFF)
        rects.set_stroke(WHITE, 1)
        arrows = VGroup()
        for rect, f_eq in zip(rects, f_eqs):
            arrow = Vector(0.5 * DOWN)
            arrow.next_to(rect, UP)
            arrows.add(arrow)
            f_eq.next_to(arrow, UP)
        f_eqs[0].match_y(f_eqs[1])

        self.play(
            FadeOut(self.title, UP),
            LaggedStartMap(Write, rhss),
            LaggedStartMap(FadeIn, lhss),
            LaggedStartMap(FadeIn, rects),
            LaggedStartMap(ShowCreation, arrows),
        )
        self.wait()
