# ==============================================================================
# Scene:      QuantifyConvexity
# Source:     videos/_2021/shadows.py (lines 6441-6520)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl QuantifyConvexity.py QuantifyConvexity -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

def get_overline(mob):
    overline = Underline(mob).next_to(mob, UP, buff=0.05)
    overline.set_stroke(WHITE, 2)
    return overline


def get_key_result(solid_name, color=BLUE):
    eq = OldTex(
        "\\text{Area}\\big(\\text{Shadow}(\\text{" + solid_name + "})\\big)",
        "=",
        "\\frac{1}{2}", "{c}", "\\cdot",
        "(\\text{Surface area})",
        tex_to_color_map={
            "\\text{Shadow}": GREY_B,
            f"\\text{{{solid_name}}}": color,
            "\\text{Solid}": BLUE,
            "{c}": RED,
        }
    )
    eq.add_to_back(get_overline(eq[:5]))
    return eq


class QuantifyConvexity(Scene):
    def construct(self):
        # Ask question
        nonconvex = Text("Non-convex")
        nonconvex.to_edge(UP)
        nonconvex.set_color(RED)
        question = Text("Can we quantify this?")
        question.next_to(nonconvex, DOWN, buff=1.5)
        question.to_edge(LEFT)
        arrow = Arrow(question, nonconvex.get_corner(DL))

        self.play(Write(nonconvex))
        self.wait()
        self.play(
            FadeIn(question, 0.5 * DOWN),
            ShowCreation(arrow),
        )
        self.wait()

        # Binary choice
        double_arrow = OldTex("\\leftrightarrow")
        double_arrow.move_to(nonconvex)
        convex = Text("Convex")
        convex.set_color(GREEN)
        convex.next_to(double_arrow, RIGHT)

        self.play(
            nonconvex.animate.next_to(double_arrow, LEFT),
            Write(double_arrow),
            FadeIn(convex, shift=0.25 * RIGHT),
            Uncreate(arrow),
            FadeOut(question, 0.5 * DOWN),
        )
        self.wait()

        # Spectrum
        interval = UnitInterval(width=7)
        interval.add_numbers()
        interval.to_corner(UL, buff=LARGE_BUFF)

        self.play(
            FadeTransform(double_arrow, interval),
            convex.animate.scale(0.5).next_to(interval.n2p(1), UP),
            nonconvex.animate.scale(0.5).next_to(interval.n2p(0), UP),
        )
        self.wait()

        # Fraction
        shadow = get_key_result("Solid").slice_by_tex(None, "=")
        shadow.add(shadow[0].copy())
        shadow.remove(shadow[0])
        four_shadow = VGroup(OldTex("4 \\cdot"), shadow)
        four_shadow.arrange(RIGHT, buff=SMALL_BUFF)
        sa = Text("Surface area")
        frac = VGroup(
            four_shadow,
            Line().match_width(four_shadow).set_stroke(width=2),
            sa
        )
        frac.arrange(DOWN)
        frac.set_width(3)
        frac.to_corner(UR)
        frac.match_y(interval)

        self.play(Write(shadow))
        self.play(FadeIn(four_shadow[0]))
        self.wait()
        self.play(ShowCreation(frac[1]))
        self.play(FadeIn(sa))
        self.wait()

        # Dot
        dot = GlowDot()
        dot.scale(2)
        dot.move_to(interval.n2p(1))

        self.play(FadeIn(dot, RIGHT))
        self.wait()
        self.play(dot.animate.move_to(interval.n2p(0.6)), run_time=2)
        self.wait()
