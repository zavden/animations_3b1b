# ==============================================================================
# Scene:      ShowNavierStokesEquations
# Source:     videos/_2018/turbulence.py (lines 979-1170)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ShowNavierStokesEquations.py ShowNavierStokesEquations -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class NavierStokesEquations(Tex):
    CONFIG = {
        "tex_to_color_map": {
            "\\rho": YELLOW,
            "\\mu": GREEN,
            "\\textbf{v}": BLUE,
            "p{}": RED,
        },
        "width": 10,
    }

    def __init__(self, **kwargs):
        v_tex = "\\textbf{v}"
        Tex.__init__(
            self,
            "\\rho",
            "\\left("
            "{\\partial", v_tex, "\\over",
            "\\partial", "t}",
            "+",
            v_tex, "\\cdot", "\\nabla", v_tex,
            "\\right)",
            "=",
            "-", "\\nabla", "p{}", "+",
            "\\mu", "\\nabla^2", v_tex, "+",
            # "\\frac{1}{3}", "\\mu", "\\nabla",
            # "(", "\\nabla", "\\cdot", v_tex, ")", "+",
            "\\textbf{F}",
            "\\qquad\\qquad",
            "\\nabla", "\\cdot", v_tex, "=", "0",
            **kwargs
        )
        self.set_width(self.width)

    def get_labels(self):
        parts = self.get_parts()
        words = [
            "Analogous to \\\\ mass $\\times$ acceleration",
            "Pressure\\\\forces",
            "Viscous\\\\forces",
            "External\\\\forces",
        ]

        result = VGroup()
        braces = VGroup()
        word_mobs = VGroup()
        for i, part, word in zip(it.count(), parts, words):
            brace = Brace(part, DOWN, buff=SMALL_BUFF)
            word_mob = brace.get_text(word)
            word_mob.scale(0.7, about_edge=UP)
            word_mobs.add(word_mob)
            braces.add(brace)
            result.add(VGroup(brace, word_mob))
        word_mobs[1:].arrange(RIGHT, buff=MED_SMALL_BUFF)
        word_mobs[1:].next_to(braces[2], DOWN, SMALL_BUFF)
        word_mobs[1].set_color(RED)
        word_mobs[2].set_color(GREEN)
        return result

    def get_parts(self):
        return VGroup(
            self[:12],
            self[13:16],
            self[17:20],
            self[21:22],
        )


class ShowNavierStokesEquations(Scene):
    def construct(self):
        self.introduce_equations()
        self.ask_about_evolution()
        self.ask_about_reasonable()
        self.ask_about_blowup()
        self.show_money()

    def introduce_equations(self):
        name = OldTexText("Navier-Stokes equations (incompressible)")
        equations = NavierStokesEquations()
        name.to_edge(UP)
        equations.next_to(name, DOWN, MED_LARGE_BUFF)
        labels = equations.get_labels()
        parts = equations.get_parts()
        newtons_second = OldTexText(
            "Newton's 2nd law \\\\ $ma = F$"
        )
        newtons_second.next_to(parts, DOWN)
        variables = OldTex(
            "&\\textbf{v}", "\\text{ is velocity}\\\\",
            "&\\rho", "\\text{ is density}\\\\",
            "&p{}", "\\text{ is pressure}\\\\",
            "&\\mu", "\\text{ is viscosity}\\\\",
            tex_to_color_map=NavierStokesEquations.CONFIG["tex_to_color_map"]
        )
        variables.to_corner(DL)

        self.play(FadeInFromDown(equations))
        self.play(Write(name))
        self.play(LaggedStartMap(
            FadeInFrom, variables,
            lambda m: (m, RIGHT),
        ))
        self.wait()
        self.play(Write(newtons_second))
        self.wait()
        self.play(
            FadeInFromDown(labels[0]),
            newtons_second.next_to, variables, RIGHT, LARGE_BUFF
        )
        self.play(ShowCreationThenFadeAround(parts[0]))
        self.wait()
        self.play(LaggedStartMap(FadeInFrom, labels[1:]))
        self.wait(3)
        self.play(LaggedStartMap(
            FadeOut, VGroup(*it.chain(labels, variables, newtons_second))
        ))

        self.equations = equations

    def ask_about_evolution(self):
        words = OldTexText(
            "Given a start state...",
            "...how does it evolve?"
        )
        words.arrange(RIGHT, buff=2)

        words.next_to(self.equations, DOWN, LARGE_BUFF)

        self.play(Write(words[0]))
        self.wait()
        self.play(Write(words[1]))
        self.wait(2)
        self.play(FadeOut(words))

    def ask_about_reasonable(self):
        question = OldTexText(
            "Do ``reasonable'' \\\\"
            "solutions always\\\\"
            "exist?"
        )
        self.play(FadeInFromDown(question))
        self.wait()

        self.reasonable_question = question

    def ask_about_blowup(self):
        axes, graph = self.get_axes_and_graph()
        question = OldTexText("Is this possible?")
        question.set_color(YELLOW)
        question.move_to(axes.get_corner(UR), LEFT)
        question.align_to(axes, UP)
        q_arrow = Arrow(
            question.get_bottom(),
            graph.point_from_proportion(0.8),
            buff=SMALL_BUFF,
            path_arc=-60 * DEGREES
        )
        q_arrow.set_stroke(WHITE, 3)
        morty = Mortimer()
        morty.to_corner(DR)
        morty.change('confused', graph)

        self.play(
            Write(axes, run_time=1),
            self.reasonable_question.to_edge, LEFT,
            self.reasonable_question.shift, DOWN,
        )
        self.play(
            Write(question),
            ShowCreation(graph),
            FadeIn(morty),
        )
        self.add(q_arrow, morty)
        self.play(ShowCreation(q_arrow), Blink(morty))
        self.wait()
        self.play(morty.look_at, question)
        self.wait()
        self.play(morty.change, "maybe", graph)
        self.wait(2)
        to_fade = VGroup(question, q_arrow, axes, graph)
        self.play(
            LaggedStartMap(FadeOut, to_fade),
            morty.change, "pondering"
        )
        self.wait(2)
        self.play(Blink(morty))
        self.wait(2)

        self.morty = morty

    def show_money(self):
        # Million dollar problem
        problem = OldTexText(
            "Navier-Stokes existence \\\\ and smoothness problems"
        )
        money = OldTexText("\\$1{,}000{,}000")
        money.set_color(GREEN)
        money.next_to(problem, DOWN)
        pi1 = Randolph()
        pi2 = self.morty
        pi1.to_corner(DL)
        pis = VGroup(pi1, pi2)
        for pi in pis:
            pi.change("pondering")
            pi.money_eyes = VGroup()
            for eye in pi.eyes:
                cash = OldTex("\\$")
                cash.set_color(GREEN)
                cash.replace(eye, dim_to_match=1)
                pi.money_eyes.add(cash)

        self.play(
            ReplacementTransform(
                self.reasonable_question,
                problem,
            ),
            pi2.look_at, problem,
            pi1.look_at, problem,
            VFadeIn(pi1),
        )
        self.wait()
        self.play(FadeInFromLarge(money))
        self.play(
            pi1.change, "hooray",
            pi2.change, "hooray",
        )
        self.play(
            ReplacementTransform(pi1.pupils, pi1.money_eyes),
            ReplacementTransform(pi2.pupils, pi2.money_eyes),
        )
        self.wait()

    # Helpers
    def get_axes_and_graph(self):
        axes = Axes(
            x_min=-1,
            x_max=5,
            y_min=-1,
            y_max=5,
        )
        time = OldTexText("Time")
        time.next_to(axes.x_axis, RIGHT)
        ke = OldTexText("Kinetic energy")
        ke.next_to(axes.y_axis, UP)
        axes.add(time, ke)
        axes.set_height(4)
        axes.center()
        axes.to_edge(DOWN)
        v_line = DashedLine(
            axes.coords_to_point(4, 0),
            axes.coords_to_point(4, 5),
        )
        axes.add(v_line)
        graph = axes.get_graph(
            lambda x: -1.0 / (x - 4),
            x_min=0.01,
            x_max=3.8,
        )
        graph.set_color(BLUE)
        return axes, graph
