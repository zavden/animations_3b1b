# ==============================================================================
# Scene:      ShowPartialDerivativeSymbols
# Source:     videos/_2019/diffyq/part2/wordy_scenes.py (lines 252-349)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ShowPartialDerivativeSymbols.py ShowPartialDerivativeSymbols -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ShowPartialDerivativeSymbols(Scene):
    def construct(self):
        t2c = {
            "{x}": GREEN,
            "{t}": YELLOW,
        }
        d_derivs, del_derivs = VGroup(*[
            VGroup(*[
                OldTex(
                    "{" + sym, "T", "\\over", sym, var + "}",
                    "(", "{x}", ",", "{t}", ")",
                ).set_color_by_tex_to_color_map(t2c)
                for var in ("{x}", "{t}")
            ])
            for sym in ("d", "\\partial")
        ])
        dTdx, dTdt = d_derivs
        delTdelx, delTdelx = del_derivs
        dels = VGroup(*it.chain(*[
            del_deriv.get_parts_by_tex("\\partial")
            for del_deriv in del_derivs
        ]))

        dTdx.to_edge(UP)
        self.play(FadeIn(dTdx, DOWN))
        self.wait()
        self.play(ShowCreationThenFadeAround(dTdx[3:5]))
        self.play(ShowCreationThenFadeAround(dTdx[:2]))
        self.wait()

        dTdt.move_to(dTdx)
        self.play(
            dTdx.next_to, dTdt, RIGHT, {"buff": 1.5},
            dTdx.set_opacity, 0.5,
            FadeInFromDown(dTdt)
        )
        self.wait()

        for m1, m2 in zip(d_derivs, del_derivs):
            m2.move_to(m1)

        pd_words = OldTexText("Partial derivatives")
        pd_words.next_to(del_derivs, DOWN, MED_LARGE_BUFF)

        self.play(
            Write(pd_words),
            dTdx.set_opacity, 1,
            run_time=1,
        )
        self.wait()
        self.play(
            ReplacementTransform(d_derivs, del_derivs)
        )
        self.play(
            LaggedStartMap(
                ShowCreationThenFadeAround,
                dels,
                surrounding_rectangle_config={
                    "color": BLUE,
                    "buff": 0.5 * SMALL_BUFF,
                    "stroke_width": 2,
                }
            )
        )
        self.wait()

        num_words = VGroup(*[
            OldTexText(
                "Change in $T$\\\\caused by {}",
                "$\\partial$", "${}$".format(var),
                arg_separator="",
            ).set_color_by_tex_to_color_map(t2c)
            for var in ("{x}", "{t}")
        ])
        num_words.scale(0.8)
        for word, deriv in zip(num_words, del_derivs):
            num = deriv[:2]
            word.move_to(num, UP)
            word.to_edge(UP, buff=MED_SMALL_BUFF)
            deriv.rect = SurroundingRectangle(
                num,
                buff=SMALL_BUFF,
                stroke_width=2,
                color=word[-1].get_color(),
            )
            deriv.rect.mob = num
            deriv.rect.add_updater(lambda r: r.move_to(r.mob))

        self.play(
            Write(num_words[1]),
            VGroup(del_derivs, pd_words).shift, DOWN,
            ShowCreation(del_derivs[1].rect),
        )
        self.play(
            Write(num_words[0]),
            ShowCreation(del_derivs[0].rect),
        )
        self.wait()
