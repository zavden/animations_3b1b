# ==============================================================================
# Scene:      CompareTwoConstantToEightConstant
# Source:     videos/_2017/eoc/chapter5.py (lines 1005-1068)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl CompareTwoConstantToEightConstant.py CompareTwoConstantToEightConstant -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class CompareTwoConstantToEightConstant(PiCreatureScene):
    def construct(self):
        two_deriv, eight_deriv = derivs = VGroup(*[
            self.get_derivative_expression(base)
            for base in (2, 8)
        ])

        derivs.arrange(
            DOWN, buff = 1.5, aligned_edge = LEFT
        )
        derivs.to_edge(LEFT, LARGE_BUFF).shift(UP)
        arrow = Arrow(*[deriv[-2] for deriv in derivs])
        times_three = OldTex("\\times 3")
        times_three.next_to(arrow, RIGHT)

        why = OldTexText("Why?")
        why.next_to(self.pi_creature, UP, MED_LARGE_BUFF)

        self.add(eight_deriv)
        self.wait()
        self.play(ReplacementTransform(
            eight_deriv.copy(),
            two_deriv
        ))
        self.wait()
        self.play(ShowCreation(arrow))
        self.play(
            Write(times_three),
            self.pi_creature.change_mode, "thinking"
        )
        self.wait(3)

        self.play(
            Animation(derivs),
            Write(why),
            self.pi_creature.change, "confused", derivs
        )
        self.wait()
        for deriv in derivs:
            for index in -5, -2:
                self.play(Indicate(deriv[index]))
            self.wait()
        self.wait(2)

    def get_derivative_expression(self, base):
        base_str = str(base)
        const_str = "%.4f\\dots"%np.log(base)
        result = OldTex(
            "{d(", base_str, "^t", ")", "\\over", "dt}", 
            "=", base_str, "^t", "(", const_str, ")"
        )
        tex_color_paris = [
            ("t", YELLOW), 
            ("dt", GREEN), 
            (const_str, BLUE)
        ]
        for tex, color in tex_color_paris:
            result.set_color_by_tex(tex, color)
        return result

    def create_pi_creature(self):
        self.pi_creature = Randolph().flip()
        self.pi_creature.to_edge(DOWN).shift(3*RIGHT)
        return self.pi_creature
