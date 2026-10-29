# ==============================================================================
# Scene:      ExponentsAsHomomorphism
# Source:     videos/_2017/efvgt.py (lines 2519-2736)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ExponentsAsHomomorphism.py ExponentsAsHomomorphism -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

MULTIPLIER_COLOR = YELLOW


class ExponentsAsHomomorphism(Scene):
    CONFIG = {
        "top_line_center" : 2.5*UP,
        "top_line_config" : {
            "x_min" : -16,
            "x_max" : 16,
        },
        "bottom_line_center" : 2.5*DOWN,
        "bottom_line_config" : {
            "x_min" : -FRAME_WIDTH,
            "x_max" : FRAME_WIDTH,
        }
    }
    def construct(self):
        self.comment_on_equation()
        self.show_adders()
        self.show_multipliers()
        self.confused_at_mapping()
        self.talk_through_composition()
        self.add_quote()

    def comment_on_equation(self):
        equation = OldTex(
            "2", "^{x", "+", "y}", "=", "2^x", "2^y"
        )
        lhs = VGroup(*equation[:4])
        rhs = VGroup(*equation[5:])
        lhs_brace = Brace(lhs, UP)
        lhs_text = lhs_brace.get_text("Add inputs")
        lhs_text.set_color(GREEN_B)
        rhs_brace = Brace(rhs, DOWN)
        rhs_text = rhs_brace.get_text("Multiply outputs")
        rhs_text.set_color(MULTIPLIER_COLOR)

        self.add(equation)
        for brace, text in (lhs_brace, lhs_text), (rhs_brace, rhs_text):
            self.play(
                GrowFromCenter(brace),
                Write(text)
            )
            self.wait()
        self.wait()

        self.equation = equation
        self.lhs_brace_group = VGroup(lhs_brace, lhs_text)
        self.rhs_brace_group = VGroup(rhs_brace, rhs_text)

    def show_adders(self):
        equation = self.equation
        adders = VGroup(equation[1], equation[3]).copy()
        top_line = NumberLine(**self.top_line_config)
        top_line.add_numbers()
        top_line.shift(self.top_line_center)

        self.play(
            adders.scale, 1.5,
            adders.center,
            adders.space_out_submobjects, 2,
            adders.to_edge, UP,
            adders.set_color, GREEN_B,
            FadeOut(self.lhs_brace_group),
            Write(top_line)
        )
        self.wait()
        for x in 3, 5, -8:
            self.play(top_line.shift, x*RIGHT, run_time = 2)
            self.wait()

        self.top_line = top_line
        self.adders = adders

    def show_multipliers(self):
        equation = self.equation
        multipliers = VGroup(*self.equation[-2:]).copy()

        bottom_line = NumberLine(**self.bottom_line_config)
        bottom_line.add_numbers()
        bottom_line.shift(self.bottom_line_center)

        self.play(
            multipliers.space_out_submobjects, 4,
            multipliers.next_to, self.bottom_line_center, 
                UP, MED_LARGE_BUFF,
            multipliers.set_color, YELLOW,
            FadeOut(self.rhs_brace_group),
            Write(bottom_line),
        )
        stretch_kwargs = {
        }
        for x in 3, 1./5, 5./3:
            self.play(
                self.get_stretch_anim(bottom_line, x),
                run_time = 3
            )
        self.wait()

        self.bottom_line = bottom_line
        self.multipliers = multipliers

    def confused_at_mapping(self):
        arrow = Arrow(
            self.top_line.get_bottom()[1]*UP,
            self.bottom_line.get_top()[1]*UP,
            color = WHITE
        )
        randy = Randolph(mode = "confused")
        randy.scale(0.75)
        randy.flip()
        randy.next_to(arrow, RIGHT, LARGE_BUFF)
        randy.look_at(arrow.get_top())

        self.play(self.equation.to_edge, LEFT)
        self.play(
            ShowCreation(arrow),
            FadeIn(randy)
        )
        self.play(randy.look_at, arrow.get_bottom())
        self.play(Blink(randy))
        self.wait()
        for x in 1, -2, 3, 1, -3:
            self.play(
                self.get_stretch_anim(self.bottom_line, 2**x),
                self.top_line.shift, x*RIGHT,
                randy.look_at, self.top_line,
                run_time = 2
            )
            if random.random() < 0.3:
                self.play(Blink(randy))
            else:
                self.wait()

        self.randy = randy

    def talk_through_composition(self):
        randy = self.randy
        terms = list(self.adders) + list(self.multipliers)
        inputs = [-1, 2]
        target_texs = list(map(str, inputs))
        target_texs += ["2^{%d}"%x for x in inputs]
        for mob, target_tex in zip(terms, target_texs):
            target = OldTex(target_tex)
            target.set_color(mob[0].get_color())
            target.move_to(mob, DOWN)
            if mob in self.adders:
                target.to_edge(UP)
            mob.target = target

        self.play(
            self.equation.next_to, ORIGIN, LEFT, MED_LARGE_BUFF,
            randy.change_mode, "pondering",
            randy.look_at, self.equation
        )
        self.wait()
        self.play(randy.look_at, self.top_line)
        self.show_composition(
            *inputs,
            parallel_anims = list(map(MoveToTarget, self.adders))
        )
        self.play(
            FocusOn(self.bottom_line_center),
            randy.look_at, self.bottom_line_center,
        )
        self.show_composition(
            *inputs,
            parallel_anims = list(map(MoveToTarget, self.multipliers))
        )
        self.wait()

    def add_quote(self):
        brace = Brace(self.equation, UP)
        quote = OldTexText("``Preserves the group structure''")
        quote.add_background_rectangle()
        quote.next_to(brace, UP)

        self.play(
            GrowFromCenter(brace),
            Write(quote),
            self.randy.look_at, quote,
        )
        self.play(self.randy.change_mode, "thinking")
        self.play(Blink(self.randy))
        self.wait()
        self.show_composition(-1, 2)
        self.wait()

    ####

    def show_composition(self, *inputs, **kwargs):
        parallel_anims = kwargs.get("parallel_anims", [])
        for x in range(len(inputs) - len(parallel_anims)):
            parallel_anims.append(Animation(Mobject()))

        for line in self.top_line, self.bottom_line:
            line.save_state()

        for x, parallel_anim in zip(inputs, parallel_anims):
            anims = [
                ApplyMethod(self.top_line.shift, x*RIGHT),
                self.get_stretch_anim(self.bottom_line, 2**x),
            ]
            for anim in anims:
                anim.set_run_time(2)
            self.play(parallel_anim)
            self.play(*anims)
            self.wait()
        self.play(*[
            line.restore 
            for line in (self.top_line, self.bottom_line)
        ])

    def get_stretch_anim(self, bottom_line, x):
        target = bottom_line.copy()
        target.stretch_about_point(
            x, 0, self.bottom_line_center,
        )
        for number in target.numbers:
            number.stretch_in_place(1./x, dim = 0)
        return Transform(bottom_line, target)
