# ==============================================================================
# Scene:      SomeTurbulenceEquations
# Source:     videos/_2018/turbulence.py (lines 428-476)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl SomeTurbulenceEquations.py SomeTurbulenceEquations -w -m --fps 15
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


class SomeTurbulenceEquations(PiCreatureScene):
    def construct(self):
        randy, morty = self.pi_creatures
        navier_stokes = NavierStokesEquations()
        line = Line(randy.get_right(), morty.get_left())
        navier_stokes.replace(line, dim_to_match=0)
        navier_stokes.scale(1.2)

        distribution = OldTex(
            "E(k) \\propto k^{-5/3}",
            tex_to_color_map={
                "k": GREEN,
                "-5/3": YELLOW,
            }
        )
        distribution.next_to(morty, UL)
        brace = Brace(distribution, DOWN, buff=SMALL_BUFF)
        brace_words = brace.get_text("Explained soon...")
        brace_group = VGroup(brace, brace_words)

        self.play(
            Write(navier_stokes),
            randy.change, "confused", navier_stokes,
            morty.change, "confused", navier_stokes,
        )
        self.wait(3)
        self.play(
            morty.change, "raise_right_hand", distribution,
            randy.look_at, distribution,
            FadeInFromDown(distribution),
            navier_stokes.fade, 0.5,
        )
        self.play(GrowFromCenter(brace_group))
        self.play(randy.change, "pondering", distribution)
        self.wait(3)
        dist_group = VGroup(distribution, brace_group)
        self.play(
            LaggedStartMap(FadeOut, VGroup(randy, morty, navier_stokes)),
            dist_group.scale, 1.5,
            dist_group.center,
            dist_group.to_edge, UP,
        )
        self.wait()

    def create_pi_creatures(self):
        randy, morty = Randolph(), Mortimer()
        randy.to_corner(DL)
        morty.to_corner(DR)
        return (randy, morty)
