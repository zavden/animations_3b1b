# ==============================================================================
# Scene:      DerivativesOfLinearFunction
# Source:     videos/_2019/diffyq/part3/wordy_scenes.py (lines 618-693)
# Category:   1 · Renders unmodified
# Includes code copied from: _2019/diffyq/part2/wordy_scenes.py
#
# Run from this folder:
#     manimgl DerivativesOfLinearFunction.py DerivativesOfLinearFunction -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *


# ----- From _2019/diffyq/part2/wordy_scenes.py -----

class WriteHeatEquationTemplate(Scene):
    CONFIG = {
        "tex_mobject_config": {
            "tex_to_color_map": {
                "{T}": WHITE,
                "{t}": YELLOW,
                "{x}": GREEN,
                "{y}": RED,
                "{z}": BLUE,
                "\\partial": WHITE,
                "2": WHITE,
            },
        },
    }

    def get_d1_equation(self):
        return OldTex(
            "{\\partial {T} \\over \\partial {t}}({x}, {t})", "=",
            "\\alpha \\cdot",
            "{\\partial^2 {T} \\over \\partial {x}^2} ({x}, {t})",
            **self.tex_mobject_config
        )

    def get_d1_equation_without_inputs(self):
        return OldTex(
            "{\\partial {T} \\over \\partial {t}}", "=",
            "\\alpha \\cdot",
            "{\\partial^2 {T} \\over \\partial {x}^2}",
            **self.tex_mobject_config
        )

    def get_d3_equation(self):
        return OldTex(
            "{\\partial {T} \\over \\partial {t}}", "=",
            "\\alpha \\left(",
            "{\\partial^2 {T} \\over \\partial {x}^2} + ",
            "{\\partial^2 {T} \\over \\partial {y}^2} + ",
            "{\\partial^2 {T} \\over \\partial {z}^2}",
            "\\right)",
            **self.tex_mobject_config
        )

    def get_general_equation(self):
        return OldTex(
            "{\\partial {T} \\over \\partial {t}}", "=",
            "\\alpha", "\\nabla^2 {T}",
            **self.tex_mobject_config,
        )

    def get_d3_equation_with_inputs(self):
        return OldTex(
            "{\\partial {T} \\over \\partial {t}}",
            "({x}, {y}, {z}, {t})", "=",
            "\\alpha \\left(",
            "{\\partial^2 {T} \\over \\partial {x}^2}",
            "({x}, {y}, {z}, {t}) + ",
            "{\\partial^2 {T} \\over \\partial {y}^2}",
            "({x}, {y}, {z}, {t}) + ",
            "{\\partial^2 {T} \\over \\partial {z}^2}",
            "({x}, {y}, {z}, {t})",
            "\\right)",
            **self.tex_mobject_config
        )

    def get_d1_words(self):
        return OldTexText("Heat equation\\\\", "(1 dimension)")

    def get_d3_words(self):
        return OldTexText("Heat equation\\\\", "(3 dimensions)")

    def get_d1_group(self):
        group = VGroup(
            self.get_d1_words(),
            self.get_d1_equation(),
        )
        group.arrange(DOWN, buff=MED_LARGE_BUFF)
        return group

    def get_d3_group(self):
        group = VGroup(
            self.get_d3_words(),
            self.get_d3_equation(),
        )
        group.arrange(DOWN, buff=MED_LARGE_BUFF)
        return group



# ----- From _2019/diffyq/part3/wordy_scenes.py -----

class DerivativesOfLinearFunction(WriteHeatEquationTemplate):
    CONFIG = {
        "tex_mobject_config": {
            "tex_to_color_map": {
                "{c}": WHITE,
            }
        }
    }

    def construct(self):
        func = OldTex(
            "T({x}, {t}) = {c} \\cdot {x}",
            **self.tex_mobject_config
        )
        dx_T = OldTex("{c}", **self.tex_mobject_config)
        ddx_T = OldTex("0")
        dt_T = OldTex("0")

        for mob in func, dx_T, ddx_T, dt_T:
            mob.scale(1.5)

        func.generate_target()

        arrows = VGroup(*[
            Vector(1.5 * RIGHT, color=WHITE)
            for x in range(3)
        ])
        dx_arrows = arrows[:2]
        dt_arrow = arrows[2]
        dt_arrow.rotate(-TAU / 4)
        dx_group = VGroup(
            func.target,
            dx_arrows[0],
            dx_T,
            dx_arrows[1],
            ddx_T,
        )
        dx_group.arrange(RIGHT)
        for arrow, char, vect in zip(arrows, "xxt", [UP, UP, RIGHT]):
            label = OldTex(
                "\\partial \\over \\partial {%s}" % char,
                **self.tex_mobject_config
            )
            label.scale(0.7)
            label.next_to(arrow.get_center(), vect)
            arrow.add(label)

        dt_arrow.shift(
            func.target[-3:].get_bottom() + MED_SMALL_BUFF * DOWN -
            dt_arrow.get_start(),
        )
        dt_T.next_to(dt_arrow.get_end(), DOWN)

        self.play(FadeInFromDown(func))
        self.wait()
        self.play(
            MoveToTarget(func),
            LaggedStartMap(Write, dx_arrows),
            run_time=1,
        )
        self.play(
            TransformFromCopy(func[-3:], dx_T),
            path_arc=-TAU / 4,
        )
        self.play(
            TransformFromCopy(dx_T, ddx_T),
            path_arc=-TAU / 4,
        )
        self.wait()

        # dt
        self.play(Write(dt_arrow))
        self.play(
            TransformFromCopy(func[-3:], dt_T)
        )
        self.wait()
