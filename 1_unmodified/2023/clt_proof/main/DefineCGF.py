# ==============================================================================
# Scene:      DefineCGF
# Source:     videos/_2023/clt_proof/main.py (lines 650-721)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl DefineCGF.py DefineCGF -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class DefineCGF(InteractiveScene):
    def construct(self):
        # Take logs
        kw = dict(t2c={"t": PINK, R"\log": RED_B})
        mgf_eq = Tex(R"M_{X+Y}(t) = M_X(t)M_Y(t)", **kw)
        mgf_eq.to_edge(UP)
        log_eq = Tex(R"""
            \log\left( M_{X + Y}(t) \right) =
            \log\left( M_{X}(t) \right) +
            \log\left( M_{Y}(t) \right)
        """, font_size=36, **kw)
        log_eq.next_to(mgf_eq, DOWN, LARGE_BUFF)

        self.add(mgf_eq)
        self.wait()
        self.play(
            TransformMatchingTex(mgf_eq.copy(), log_eq)
        )
        self.wait()

        # Name CGF
        parts = log_eq[re.compile(r"\\log\\left(.* \\right)")]
        braces = VGroup()
        for part in parts:
            braces.add(Brace(part, DOWN, buff=SMALL_BUFF))

        cgf_funcs = VGroup(
            Tex("K_{X + Y}(t)", font_size=36, **kw),
            Tex("K_{X}(t)", font_size=36, **kw),
            Tex("K_{Y}(t)", font_size=36, **kw),
        )
        for name, brace in zip(cgf_funcs, braces):
            name.next_to(brace, DOWN, SMALL_BUFF)

        cgf_name = TexText("``Cumulant Generating Function''")
        cgf_name.next_to(cgf_funcs, DOWN, buff=1.5)
        arrows = VGroup(*(Arrow(cgf_name, func) for func in cgf_funcs))

        self.play(
            LaggedStartMap(GrowFromCenter, braces, lag_ratio=0.2),
            LaggedStartMap(FadeIn, cgf_funcs, shift=0.5 * DOWN, lag_ratio=0.2),
        )
        self.wait()
        self.play(
            Write(cgf_name),
            LaggedStartMap(GrowArrow, arrows),
        )
        self.wait()

        # Highlight generating function
        gen_func = cgf_name["Generating Function"]
        rect = SurroundingRectangle(gen_func, buff=0.1)
        rect.set_stroke(YELLOW, 1)

        series = Tex(
            R"K_X(t) = k_0 + k_1 t + k_2 \frac{t^2}{2} + k_3 \frac{t^3}{6} + \cdots",
            font_size=42,
            t2c={
                R"t": PINK,
                R"\frac{t^2}{2}": PINK,
                R"\frac{t^3}{6}": PINK,
            },
        )
        series.next_to(cgf_name, DOWN, LARGE_BUFF)

        self.play(
            ShowCreation(rect),
            gen_func.animate.set_color(YELLOW)
        )
        self.wait()
        self.play(FadeIn(series, lag_ratio=0.1, run_time=2))
        self.wait()
