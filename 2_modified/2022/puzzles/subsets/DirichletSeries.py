# ==============================================================================
# Scene:      DirichletSeries
# Source:     videos/_2022/puzzles/subsets.py (lines 3884-4077)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl DirichletSeries.py DirichletSeries -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - time_range= -> time_span= (current name of Animation's argument)
# ==============================================================================

import mpmath
import sympy
from manim_imports_ext import *

def von_mangoldt_str(n):
    factors = sympy.factorint(n)
    if len(factors) == 1:
        return f"\\ln({list(factors.keys())[0]})"
    else:
        return "0"


class DirichletSeries(InteractiveScene):
    def construct(self):
        # Framing
        h_line = Line().set_width(FRAME_WIDTH)
        h_line.set_stroke(WHITE, 1)
        titles = VGroup(
            Text("Our puzzle", font_size=36),
            Text(f"Studying primes", font_size=36),
        )
        titles[0].to_corner(UL, buff=MED_SMALL_BUFF)
        titles[1].next_to(h_line, DOWN).align_to(titles[0], LEFT)

        self.add(titles, h_line)

        # Show series
        n_range = list(range(1, 14))
        coef_texs = [von_mangoldt_str(n) for n in n_range]
        denom_texs = [f"{{{n}}}^s" for n in n_range]
        series_terms = [f"{{ {coef} \\over  {denom} }}" for coef, denom in zip(coef_texs, denom_texs)]
        series = Tex(
            " + ".join(series_terms) + "+ \\cdots",
            isolate=["+", *coef_texs, *denom_texs]
        )

        series.set_width(FRAME_WIDTH - 1)
        series.next_to(h_line, DOWN, buff=2.0)

        plusses = series.select_parts("+")
        denoms = VGroup(*(series.select_part(dt) for dt in denom_texs))
        plus_indices = [series.submobjects.index(plus[0]) for plus in plusses]
        denom_indices = [series.submobjects.index(denom[0]) for denom in denoms]
        coefs = VGroup()
        overs = VGroup()
        for i, j, k in zip((-1, *plus_indices), denom_indices, plus_indices):
            coefs.add(series[i + 1:j - 1])
            overs.add(series[j - 1])

        for n, coef, denom in zip(n_range, coefs, denoms):
            if sympy.isprime(n):
                color = YELLOW
            elif len(sympy.factorint(n)) == 1:
                color = TEAL
            else:
                color = WHITE
            coef.set_color(color)
            denom.set_color(color)

        coefs.save_state()
        coefs.shift(DOWN)

        numbers = VGroup(*(Integer(n, font_size=36) for n in n_range))
        arrows = VGroup()
        for number, coef_part in zip(numbers, coefs):
            number.next_to(coef_part, UP, buff=LARGE_BUFF)
            arrows.add(Arrow(number, coef_part, stroke_width=2))
        arrows.set_stroke(GREY_B)

        vm_def = Tex("n \\rightarrow \\log p & \\text { if } n=p^{k} \\text { for some prime } p \\text { and integer } k \\geq 1")
        vm_def.scale(0.5)
        vm_def.next_to(h_line, DOWN)
        vm_def.to_edge(RIGHT)
        details = Text("(Why this sequence? That's a story for another day...)")
        details.scale(0.5)
        details.set_color(GREY_B)
        details.next_to(vm_def, DOWN)

        self.play(
            ShowIncreasingSubsets(numbers),
            ShowIncreasingSubsets(arrows),
            ShowIncreasingSubsets(coefs),
            FadeIn(vm_def, time_span=(1, 2)),
            run_time=3,
            rate_func=linear,
        )
        self.play(FadeIn(details, 0.5 * DOWN))
        self.wait(3)
        self.play(
            coefs.animate.restore(),
            *(
                ReplacementTransform(number, denom)
                for number, denom in zip(numbers, denoms)
            ),
            *(FadeOut(arrow, scale=0.2) for arrow in arrows),
            # CHANGE: time_range -> time_span (current name of Animation's argument)
            Write(overs, time_span=(0.75, 1.75)),
            Write(plusses, time_span=(0.75, 1.75)),
        )
        self.add(series)
        self.wait()

        # Name Dirichlet
        series.generate_target()
        series.target.shift(0.5 * UP)
        brace = Brace(series.target, DOWN)
        name = Text("Dirichlet series")
        name.next_to(brace, DOWN)

        self.play(
            MoveToTarget(series),
            GrowFromCenter(brace),
        )
        self.play(Write(name))
        self.wait(2)

        # Move everything up
        func_name = Tex("f(s) = -\\zeta'(s) / \\zeta(s)", font_size=36)
        func_name.next_to(brace, DOWN)
        func_name.set_opacity(0)

        self.play(LaggedStart(
            FadeOut(h_line, 3 * UP),
            FadeOut(titles[0], UP),
            FadeOut(titles[1], 3 * UP),
            FadeOut(vm_def, 2 * UP),
            FadeOut(details, 2 * UP),
            FadeOut(name, 3 * UP),
            VGroup(series, brace, func_name).animate.set_opacity(1).to_edge(UP),
            lag_ratio=0.01
        ))
        self.wait()

        # Complex plane
        kw = dict(background_line_style={"stroke_width": 1})
        in_plane, out_plane = planes = VGroup(
            ComplexPlane((-5, 5), (-4, 4), **kw),
            ComplexPlane((-3, 3), (-3, 3), **kw),
        )
        plane_labels = VGroup(Text("Input"), Text("Output"))
        for label, plane, vect in zip(plane_labels, planes, [DL, DR]):
            plane.set_height(4)
            plane.add_coordinate_labels(font_size=12)
            plane.to_corner(vect)
            label.scale(0.7)
            label.set_color(GREY_A)
            label.next_to(plane, UP)

        arrow = Arrow(in_plane.get_right(), out_plane.get_left(), path_arc=-45 * DEGREES)
        arrow.align_to(in_plane, UP).shift(DOWN)
        f_label = Tex("f(s)", font_size=36)
        f_label.next_to(arrow.pfp(0.5), DOWN)

        in_dot = GlowDot(in_plane.n2p(0.5), color=YELLOW)
        out_dot = GlowDot(out_plane.n2p(2), color=RED)

        def get_z():
            return in_plane.p2n(in_dot.get_center())

        def func(z):
            ep = 1e-3
            zeta = mpmath.zeta(z)
            dzeta = (mpmath.zeta(z + ep) - zeta) / ep
            return -dzeta / zeta

        out_dot.add_updater(lambda d: d.move_to(out_plane.n2p(func(get_z()))))

        v_line = ParametricCurve(lambda t: in_plane.n2p(complex(2, t)), t_range=(-4, 4, 0.01))
        v_line.set_stroke(YELLOW, 2)
        out_line = v_line.copy()
        out_line.set_stroke(RED, 2)
        out_line.add_updater(lambda m: m.set_points([
            out_plane.n2p(func(in_plane.p2n(p)))
            for p in v_line.get_points()
        ]))

        # Complex mapping
        self.disable_interaction(in_plane, out_plane)

        self.play(
            FadeIn(in_plane),
            FadeIn(out_plane),
            FadeIn(plane_labels),
            FadeIn(in_dot)
        )
        self.play(
            ShowCreation(arrow),
            FadeIn(f_label, RIGHT + 0.2 * UP),
            TransformFromCopy(in_dot, out_dot, path_arc=45 * DEGREES)
        )
        self.play(
            in_dot.animate.move_to(v_line.get_start()),
            run_time=2,
        )
        in_dot.add_updater(lambda d: d.move_to(v_line.get_end()))
        self.add(v_line, out_line)
        self.play(
            ShowCreation(v_line),
            ShowCreation(out_line),
            run_time=5,
        )
        self.wait()
        self.play(
            v_line.animate.move_to(in_plane.n2p(-1)),
            run_time=6
        )
        self.wait()
