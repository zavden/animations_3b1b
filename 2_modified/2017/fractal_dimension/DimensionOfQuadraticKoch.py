# ==============================================================================
# Scene:      DimensionOfQuadraticKoch
# Source:     videos/_2017/fractal_dimension.py (lines 1395-1482)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl DimensionOfQuadraticKoch.py DimensionOfQuadraticKoch -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Python 2 integer division in slice
# ==============================================================================

from manim_imports_ext import *

def break_up(mobject, factor = 1.3):
    mobject.scale(factor)
    for submob in mobject:
        submob.scale(1./factor)
    return mobject


class DimensionOfKoch(Scene):
    CONFIG = {
        "scaling_factor_color" : YELLOW,
        "mass_scaling_color" : BLUE,
        "dimension_color" : GREEN_A,
        "curve_class" : KochCurve,
        "scaling_factor" : 3,
        "mass_scaling_factor" : 4,
        "num_subparts" : 4,
        "koch_curve_order" : 5,
        "koch_curve_width" : 5,
        "break_up_factor" : 1.5,
        "down_shift" : 3*DOWN,
        "dimension_rhs" : "\\approx 1.262",
    }
    def construct(self):
        self.add_labels()
        self.add_curve()
        self.break_up_curve()
        self.compare_sizes()
        self.show_dimension()

    def add_labels(self):
        scaling_factor = OldTexText(
            "Scaling factor:",
            "$\\frac{1}{%d}$"%self.scaling_factor,
        )
        scaling_factor.next_to(ORIGIN, UP)
        scaling_factor.to_edge(LEFT)
        scaling_factor[1].set_color(self.scaling_factor_color)
        self.add(scaling_factor[0])

        mass_scaling = OldTexText(
            "Mass scaling factor:",
            "$\\frac{1}{%d}$"%self.mass_scaling_factor
        )
        mass_scaling.next_to(ORIGIN, DOWN)
        mass_scaling.to_edge(LEFT)
        mass_scaling[1].set_color(self.mass_scaling_color)
        self.add(mass_scaling[0])

        self.scaling_factor_mob = scaling_factor[1]
        self.mass_scaling_factor_mob = mass_scaling[1]

    def add_curve(self):
        curve = self.curve_class(order = self.koch_curve_order)
        curve.set_width(self.koch_curve_width)
        curve.to_corner(UP+RIGHT, LARGE_BUFF)

        self.play(ShowCreation(curve, run_time = 2))
        self.wait()
        self.curve = curve

    def break_up_curve(self):
        curve_copy = self.curve.copy()
        length = len(curve_copy)
        n_parts = self.num_subparts
        broken_curve = VGroup(*[
            # CHANGE: Python 2 integer division in slice
            VGroup(*curve_copy[i*length//n_parts:(i+1)*length//n_parts])
            for i in range(n_parts)
        ])
        self.play(broken_curve.shift, self.down_shift)

        broken_curve.generate_target()
        break_up(broken_curve.target, self.break_up_factor)
        broken_curve.target.shift_onto_screen
        self.play(MoveToTarget(broken_curve))
        self.wait()

        self.add(broken_curve)
        self.broken_curve = broken_curve

    def compare_sizes(self):
        big_brace = Brace(self.curve, DOWN)
        one = big_brace.get_text("$1$")
        little_brace = Brace(self.broken_curve[0], DOWN)
        one_third = little_brace.get_text("1/%d"%self.scaling_factor)
        one_third.set_color(self.scaling_factor_color)

        self.play(
            GrowFromCenter(big_brace),
            GrowFromCenter(little_brace),
            Write(one),
            Write(one_third),
        )
        self.wait()
        self.play(Write(self.scaling_factor_mob))
        self.wait()
        self.play(Write(self.mass_scaling_factor_mob))
        self.wait()

    def show_dimension(self):
        raw_formula = OldTex("""
            \\left( \\frac{1}{%s} \\right)^D
            =
            \\left( \\frac{1}{%s} \\right)
        """%(self.scaling_factor, self.mass_scaling_factor))
        formula = VGroup(
            VGroup(*raw_formula[:5]),
            VGroup(raw_formula[5]),
            VGroup(raw_formula[6]),
            VGroup(*raw_formula[7:]),
        )
        formula.to_corner(UP+LEFT)

        simpler_formula = OldTex(
            str(self.scaling_factor),
            "^D", "=",
            str(self.mass_scaling_factor)
        )
        simpler_formula.move_to(formula, UP)

        for mob in formula, simpler_formula:
            mob[0].set_color(self.scaling_factor_color)
            mob[1].set_color(self.dimension_color)
            mob[3].set_color(self.mass_scaling_color)

        log_expression = OldTex(
            "D = \\log_%d(%d) %s"%(
                self.scaling_factor,
                self.mass_scaling_factor,
                self.dimension_rhs
            )
        )
        log_expression[0].set_color(self.dimension_color)
        log_expression[5].set_color(self.scaling_factor_color)
        log_expression[7].set_color(self.mass_scaling_color)
        log_expression.next_to(
            simpler_formula, DOWN,
            aligned_edge = LEFT,
            buff = MED_LARGE_BUFF
        )

        third = self.scaling_factor_mob.copy()
        fourth = self.mass_scaling_factor_mob.copy()
        for mob in third, fourth:
            mob.add(VectorizedPoint(mob.get_right()))
            mob.add_to_back(VectorizedPoint(mob.get_left()))



        self.play(
            Transform(third, formula[0]),
            Transform(fourth, formula[-1]),
        )
        self.play(*list(map(FadeIn, formula[1:-1])))
        self.remove(third, fourth)
        self.add(formula)
        self.wait(2)
        self.play(Transform(formula, simpler_formula))
        self.wait(2)
        self.play(Write(log_expression))
        self.wait(2)


class DimensionOfQuadraticKoch(DimensionOfKoch):
    CONFIG = {
        "curve_class" : QuadraticKoch,
        "scaling_factor" : 4,
        "mass_scaling_factor" : 8,
        "num_subparts" : 8,
        "koch_curve_order" : 4,
        "koch_curve_width" : 4,
        "break_up_factor" : 1.7,
        "down_shift" : 4*DOWN,
        "dimension_rhs" : "= \\frac{3}{2} = 1.5",
    }
    def construct(self):
        self.add_labels()
        self.add_curve()
        self.set_color_curve_subparts()
        self.show_dimension()

    def get_curve(self, order):
        curve = self.curve_class(
            order = order,
            monochromatic = True
        )
        curve.set_width(self.koch_curve_width)
        alpha = float(order) / self.koch_curve_order
        stroke_width = interpolate(3, 1, alpha)
        curve.set_stroke(width = stroke_width)
        return curve

    def add_curve(self):
        seed_label = OldTexText("Seed")
        seed_label.shift(FRAME_X_RADIUS*RIGHT/2).to_edge(UP)
        seed = self.get_curve(order = 1)
        seed.next_to(seed_label, DOWN)

        curve = seed.copy()

        resulting_fractal = OldTexText("Resulting fractal")
        resulting_fractal.shift(FRAME_X_RADIUS*RIGHT/2)

        self.add(seed_label, seed)
        self.wait()
        self.play(
            curve.next_to, resulting_fractal, DOWN, MED_LARGE_BUFF,
            Write(resulting_fractal, run_time = 1)
        )
        for order in range(2, self.koch_curve_order+1):
            new_curve = self.get_curve(order)
            new_curve.move_to(curve)
            n_curve_parts = curve.get_num_curves()
            curve.insert_n_curves(6 * n_curve_parts)
            curve.make_jagged()
            self.play(Transform(curve, new_curve, run_time = 2))
        self.wait()

        self.curve = curve

    def set_color_curve_subparts(self):
        n_parts = self.num_subparts
        colored_curve = self.curve_class(
            order = self.koch_curve_order,
            stroke_width = 1
        )
        colored_curve.replace(self.curve)
        length = len(colored_curve)
        broken_curve = VGroup(*[
            # CHANGE: Python 2 integer division in slice
            VGroup(*colored_curve[i*length//n_parts:(i+1)*length//n_parts])
            for i in range(n_parts)
        ])
        colors = it.cycle([WHITE, RED])
        for subpart, color in zip(broken_curve, colors):
            subpart.set_color(color)
        self.play(
            FadeOut(self.curve),
            FadeIn(colored_curve)
        )
        self.play(
            ApplyFunction(
                lambda m : break_up(m, self.break_up_factor),
                broken_curve,
                rate_func = there_and_back,
                run_time = 2
            )
        )
        self.wait()
        self.play(Write(self.scaling_factor_mob))
        self.play(Write(self.mass_scaling_factor_mob))
        self.wait(2)
