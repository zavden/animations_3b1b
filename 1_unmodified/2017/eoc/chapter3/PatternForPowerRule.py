# ==============================================================================
# Scene:      PatternForPowerRule
# Source:     videos/_2017/eoc/chapter3.py (lines 1279-1409)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl PatternForPowerRule.py PatternForPowerRule -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class PatternForPowerRule(PiCreatureScene):
    CONFIG = {
        "num_exponents" : 5,
    }
    def construct(self):
        self.introduce_pattern()
        self.generalize_pattern()
        self.show_hopping()

    def introduce_pattern(self):
        exp_range = list(range(1, 1+self.num_exponents))
        colors = color_gradient([BLUE_D, YELLOW], self.num_exponents)
        derivatives = VGroup()
        for exponent, color in zip(exp_range, colors):
            derivative = OldTex(
                "\\frac{d(x^%d)}{dx} = "%exponent,
                "%d x^{%d}"%(exponent, exponent-1)
            )
            VGroup(*derivative[0][2:4]).set_color(color)
            derivatives.add(derivative)
        derivatives.arrange(
            DOWN, aligned_edge = LEFT,
            buff = MED_LARGE_BUFF
        )
        derivatives.set_height(FRAME_HEIGHT-1)
        derivatives.to_edge(LEFT)

        self.play(FadeIn(derivatives[0]))
        for d1, d2 in zip(derivatives, derivatives[1:]):
            self.play(Transform(
                d1.copy(), d2,
                replace_mobject_with_target_in_scene = True  
            ))
        self.change_mode("thinking")
        self.wait()
        for derivative in derivatives[-2:]:
            derivative.save_state()
            self.play(
                derivative.scale, 2,
                derivative.next_to, derivative,
                RIGHT, SMALL_BUFF, DOWN,
            )
            self.wait(2)
            self.play(derivative.restore)
            self.remove(derivative)
            derivative.restore()
            self.add(derivative)

        self.derivatives = derivatives
        self.colors = colors

    def generalize_pattern(self):
        derivatives = self.derivatives


        power_rule = OldTex(
            "\\frac{d (x^n)}{dx} = ",
            "nx^{n-1}"
        )
        title = OldTexText("``Power rule''")        
        title.next_to(power_rule, UP, MED_LARGE_BUFF)
        lines = VGroup(*[
            Line(
                deriv.get_right(), power_rule.get_left(),
                buff = MED_SMALL_BUFF,
                color = deriv[0][2].get_color()
            )
            for deriv in derivatives
        ])

        self.play(
            Transform(
                VGroup(*[d[0].copy() for d in derivatives]),
                VGroup(power_rule[0]),
                replace_mobject_with_target_in_scene = True
            ),
            ShowCreation(lines),
            lag_ratio = 0.5,
            run_time = 2,
        )
        self.wait()
        self.play(Write(power_rule[1]))
        self.wait()
        self.play(
            Write(title),
            self.pi_creature.change_mode, "speaking"
        )
        self.wait()

    def show_hopping(self):
        exp_range = list(range(2, 2+self.num_exponents-1))
        self.change_mode("tired")
        for exp, color in zip(exp_range, self.colors[1:]):
            form = OldTex(
                "x^",
                str(exp),
                "\\rightarrow",
                str(exp),
                "x^",
                str(exp-1)
            )
            form.set_color(color)
            form.to_corner(UP+RIGHT, buff = LARGE_BUFF)
            lhs = VGroup(*form[:2])
            lhs_copy = lhs.copy()
            rhs = VGroup(*form[-2:])
            arrow = form[2]

            self.play(Write(lhs))
            self.play(
                lhs_copy.move_to, rhs, DOWN+LEFT,
                Write(arrow)
            )
            self.wait()
            self.play(
                ApplyMethod(
                    lhs_copy[1].replace, form[3],
                    path_arc = np.pi,
                    rate_func = running_start,
                ),
                FadeIn(
                    form[5],
                    rate_func = squish_rate_func(smooth, 0.5, 1)
                )   
            )
            self.wait()
            self.play(
                self.pi_creature.change_mode, "hesitant",
                self.pi_creature.look_at, lhs_copy
            )
            self.play(*list(map(FadeOut, [form, lhs_copy])))
