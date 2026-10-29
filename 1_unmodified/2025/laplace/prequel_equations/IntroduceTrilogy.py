# ==============================================================================
# Scene:      IntroduceTrilogy
# Source:     videos/_2025/laplace/prequel_equations.py (lines 4-81)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl IntroduceTrilogy.py IntroduceTrilogy -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class IntroduceTrilogy(InteractiveScene):
    def construct(self):
        # Add definition
        frame = self.frame
        laplace = Tex(R"F(s) = \int_0^\infty f({t}) e^{-s{t}} dt", font_size=72, t2c={"s": YELLOW, R"{t}": WHITE})
        name = Text("Laplace Transform", font_size=72)
        name.next_to(laplace, UP, LARGE_BUFF)

        frame.move_to(laplace["f({t})"])
        self.play(
            Write(laplace["f({t})"]),
        )
        self.play(
            Write(laplace["e^{-s"]),
            TransformFromCopy(*laplace[R"{t}"][0:2]),
            frame.animate.move_to(laplace[R"f({t}) e^{-s{t}}"])
        )
        self.play(
            FadeIn(laplace[R"\int_0^\infty"], shift=0.25 * RIGHT, scale=1.5),
            FadeIn(laplace[R"dt"], shift=0.25 * LEFT, scale=1.5),
        )
        self.play(
            FadeTransform(laplace["f("].copy(), laplace["F("], path_arc=-PI / 2),
            TransformFromCopy(laplace[")"][1], laplace[")"][0], path_arc=-PI / 2),
            TransformFromCopy(laplace["s"][1], laplace["s"][0], path_arc=-PI / 4),
            Write(laplace["="]),
            frame.animate.center(),
        )
        self.play(Write(name))
        self.wait()

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
