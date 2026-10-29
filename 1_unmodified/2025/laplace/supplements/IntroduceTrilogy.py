# ==============================================================================
# Scene:      IntroduceTrilogy
# Source:     videos/_2025/laplace/supplements.py (lines 4-147)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl IntroduceTrilogy.py IntroduceTrilogy -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class IntroduceTrilogy(InteractiveScene):
    def construct(self):
        # Add definition
        self.add(FullScreenRectangle().fix_in_frame())
        frame = self.frame
        name = Text("Laplace Transform", font_size=60)
        name.to_edge(UP)
        t2c = {"s": YELLOW, R"{t}": BLUE}
        laplace = Tex(R"F(s) = \int_0^\infty f({t}) e^{\minus s{t}} d{t}", font_size=36, t2c=t2c)
        laplace.next_to(name, DOWN)

        frames = Square().replicate(3)
        frames.set_stroke(WHITE, 1).set_fill(BLACK, 1)
        frames.set_width(0.3 * FRAME_WIDTH)
        frames.arrange(RIGHT, buff=MED_LARGE_BUFF)
        frames.set_y(-1.0)
        frames.fix_in_frame()
        name.fix_in_frame()

        frame.match_x(laplace["f({t})"])

        self.play(
            Write(name),
            FadeIn(frames, lag_ratio=0.25, run_time=2)
        )
        self.play(
            Write(laplace["f({t})"]),
        )
        self.play(
            Write(laplace[R"e^{\minus s"]),
            TransformFromCopy(*laplace[R"{t}"][0:2]),
            frame.animate.match_x(laplace[R"f({t}) e^{\minus s{t}}"])
        )
        self.play(
            FadeIn(laplace[R"\int_0^\infty"], shift=0.25 * RIGHT, scale=1.5),
            FadeIn(laplace[R"d{t}"], shift=0.25 * LEFT, scale=1.5),
        )
        self.play(
            FadeTransform(laplace["f("].copy(), laplace["F("], path_arc=-PI / 2),
            TransformFromCopy(laplace[")"][1], laplace[")"][0], path_arc=-PI / 2),
            TransformFromCopy(laplace["s"][1], laplace["s"][0], path_arc=-PI / 4),
            Write(laplace["="]),
            frame.animate.center(),
        )
        self.wait()

        # Contrast the pair
        brace = Brace(frames[1:], UP)
        brace_ghost = brace.copy().set_fill(GREY_D)

        ilp = Tex(R"f({t}) = \frac{1}{2\pi i} \int_{a - i \infty}^{a + i \infty} F(s) e^{s{t}} d{s}", t2c=t2c, font_size=36)
        ilp.scale(0.75)
        ilp.next_to(frames[2], UP, MED_LARGE_BUFF)

        self.play(
            GrowFromCenter(brace),
            laplace.animate.scale(0.75).next_to(frames[1], UP, MED_LARGE_BUFF),
            name.animate.scale(0.75).next_to(frames[1:], UP, buff=1.75),
        )
        self.play(TransformMatchingTex(
            laplace.copy(), ilp,
            lag_ratio=1e-2,
            path_arc=-20 * DEG,
            matched_keys=["f({t})", "F(s)", "e^{s{t}}", R"\int"],
            key_map={"d{t}": "d{s}"},
        ))
        self.wait()
        self.add(brace_ghost, brace)
        self.play(
            brace.animate.match_width(frames[0], stretch=True).next_to(frames[0], UP).set_anim_args(path_arc=15 * DEG)
        )
        self.wait()

        # Clear the board
        self.play(
            LaggedStartMap(FadeOut, VGroup(*frames[1:], brace, brace_ghost, name, laplace, ilp), shift=RIGHT, lag_ratio=0.15),
            frames[0].animate.set_shape(16, 9).set_width(0.45 * FRAME_WIDTH).move_to(FRAME_WIDTH * LEFT / 4 + 0.5 * DOWN),
            run_time=2
        )
        self.wait()

        # Add new frame
        new_frame = frames[0].copy()
        new_frame.set_x(FRAME_WIDTH / 4)
        arc = -120 * DEG
        arrow = Arrow(frames[0].get_top(), new_frame.get_top(), path_arc=arc, thickness=6)
        arrow_line = Line(frames[0].get_top(), new_frame.get_top(), path_arc=arc, buff=0.2)
        arrow_line.pointwise_become_partial(arrow_line, 0, 0.95)
        arrow.set_fill(TEAL)
        arrow_line.set_stroke(TEAL, 10)
        self.play(
            ShowCreation(arrow_line, time_span=(0, 0.8)),
            FadeIn(arrow, time_span=(0.7, 1)),
            FadeIn(new_frame)
        )

    def old_material(self):
        # Show trilogy
        background = FullScreenRectangle().set_fill(GREY_E, 1)
        screens = ScreenRectangle().replicate(3)
        screens.set_fill(BLACK, 1)
        screens.set_stroke(WHITE, 2)
        screens.set_width(0.3 * FRAME_WIDTH)
        screens.arrange(RIGHT, buff=0.25 * (FRAME_WIDTH - 3 * screens[0].get_width()))
        screens.set_width(FRAME_WIDTH - 1)
        screens.to_edge(UP)

        screens[1].save_state()
        screens[1].replace(background)
        screens[1].set_stroke(width=0)
        screens.set_stroke(behind=True)

        terms = VGroup(name, laplace)

        self.add(background, screens, terms)
        self.play(
            FadeIn(background),
            Restore(screens[1]),
            terms.animate.scale(0.4).move_to(screens[1].saved_state),
        )
        self.wait()

        # Inverse
        ilp = VGroup(
            Text("Inverse Laplace Transform"),
            Tex(R"f({t}) = \frac{1}{2\pi i} \int_{a - i \infty}^{a + i \infty} F(s) e^{s{t}} ds", t2c={"s": YELLOW})
        )
        for mob1, mob2 in zip(ilp, terms):
            mob1.replace(mob2, dim_to_match=1)

        ilp.move_to(screens[2])

        self.play(
            TransformMatchingStrings(name.copy(), ilp[0], lag_ratio=1e-2, path_arc=-20 * DEG),
            TransformMatchingTex(
                laplace.copy(),
                ilp[1],
                lag_ratio=1e-2,
                path_arc=-20 * DEG,
                matched_keys=["f({t})", "F(s)", "e^{s{t}}", R"\int"],
                key_map={"dt": "ds"},
            ),
        )
        self.wait()
