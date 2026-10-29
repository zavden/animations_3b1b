# ==============================================================================
# Scene:      ShowSimpleMultivariableFunction
# Source:     videos/_2017/gradient.py (lines 21-93)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ShowSimpleMultivariableFunction.py ShowSimpleMultivariableFunction -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ShowSimpleMultivariableFunction(Scene):
    def construct(self):
        scale_val = 1.5

        func_tex = OldTex(
            "C(", "x_1,", "x_2,", "\\dots,", "x_n", ")", "=",
        )
        func_tex.scale(scale_val)
        func_tex.shift(2 * LEFT)
        alt_func_tex = OldTex(
            "C(", "x,", "y", ")", "="
        )
        alt_func_tex.scale(scale_val)
        for tex in func_tex, alt_func_tex:
            tex.set_color_by_tex_to_color_map({
                "C(": RED,
                ")": RED,
            })
        alt_func_tex.move_to(func_tex, RIGHT)
        inputs = func_tex[1:-2]
        self.add(func_tex)

        many_inputs = OldTex(*[
            "x_{%d}, " % d for d in range(1, 25)
        ])
        many_inputs.set_width(FRAME_WIDTH)
        many_inputs.to_edge(UL)

        inputs_brace = Brace(inputs, UP)
        inputs_brace_text = inputs_brace.get_text("Multiple inputs")

        decimal = DecimalNumber(0)
        decimal.scale(scale_val)
        decimal.next_to(tex, RIGHT)
        value_tracker = ValueTracker(0)
        always_shift(value_tracker, rate=0.5)
        self.add(value_tracker)
        decimal_change = ContinualChangingDecimal(
            decimal,
            lambda a: 1 + np.sin(value_tracker.get_value())
        )
        self.add(decimal_change)

        output_brace = Brace(decimal, DOWN)
        output_brace_text = output_brace.get_text("Single output")

        self.wait(2)
        self.play(GrowFromCenter(inputs_brace))
        self.play(Write(inputs_brace_text))
        self.play(GrowFromCenter(output_brace))
        self.play(Write(output_brace_text))
        self.wait(3)
        self.play(
            ReplacementTransform(
                inputs,
                many_inputs[:len(inputs)]
            ),
            LaggedStartMap(
                FadeIn,
                many_inputs[len(inputs):]
            ),
            FadeOut(inputs_brace),
            FadeOut(inputs_brace_text),
        )
        self.wait()
        self.play(
            ReplacementTransform(
                func_tex[0], alt_func_tex[0]
            ),
            Write(alt_func_tex[1:3]),
            LaggedStartMap(FadeOutAndShiftDown, many_inputs)
        )
        self.wait(3)
