# ==============================================================================
# Scene:      GeneratingFunctionForPrimes
# Source:     videos/_2022/puzzles/subsets.py (lines 3738-3881)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl GeneratingFunctionForPrimes.py GeneratingFunctionForPrimes -w -m --fps 15
# ==============================================================================

import sympy
from manim_imports_ext import *

def von_mangoldt_str(n):
    factors = sympy.factorint(n)
    if len(factors) == 1:
        return f"\\ln({list(factors.keys())[0]})"
    else:
        return "0"


class GeneratingFunctionForPrimes(InteractiveScene):
    def construct(self):
        # Title
        title = Text("A prime generating function?")
        title.to_edge(UP, buff=MED_SMALL_BUFF)
        title.set_backstroke()
        underline = Underline(title, buff=-0.05)
        underline.stretch(1.25, 0)
        underline.insert_n_curves(20)
        underline.set_stroke(WHITE, [0, 3, 3, 3, 0])
        self.add(underline, title)

        # Attempt sequence
        n_range = range(1, 12)
        piece_groups = [
            [str(int(sympy.isprime(n))) + f"\\cdot x^{{{n}}} " for n in n_range],
            [str(int(sympy.isprime(n))) + f"\\cdot {{{n}}}^x " for n in n_range],
            [str(int(sympy.isprime(n))) + f"\\cdot {{{n}}}^s " for n in n_range],
            ["{ " + str(int(sympy.isprime(n))) + f" \\over  {{{n}}}^s }}" for n in n_range],
            ["{ " + von_mangoldt_str(n) + f" \\over  {{{n}}}^s }}" for n in n_range],
            [f"{{1 \\over  {{{n}}}^s }}" for n in range(1, 14)],
        ]
        lines = VGroup()
        for pieces in piece_groups:
            line = Tex(" + ".join([*pieces, "\\cdots"]), isolate=[*pieces, "+"])
            line.set_width(FRAME_WIDTH - 1)
            for n, piece in zip(it.count(1), pieces):
                part = line.select_part(piece)
                if sympy.isprime(n):
                    part.set_color(GREEN)
                elif len(sympy.factorint(n)) == 1 and "ln" in piece:
                    part.set_color(TEAL)
            lines.add(line)
            line.pieces = pieces

        lines[0].shift(2 * UP)
        lines[4].shift(2.5 * DOWN)

        arrows = VGroup(
            Arrow(lines[0], lines[1]),
            Arrow(lines[3], lines[4]),
        )
        for arrow in arrows:
            arrow.label = Text("or rather...", font_size=36)
            arrow.label.next_to(arrow, RIGHT)

        self.play(Write(lines[0]))
        self.wait()
        for i, l1, l2 in zip(it.count(), lines[0:4], lines[1:5]):
            added_anims = []
            if i in [1, 2]:
                self.remove(l1)
            elif i in [0, 3]:
                arrow = arrows[i // 3]
                added_anims.append(GrowArrow(arrow))
                added_anims.append(Write(arrow.label))
            self.play(
                *(
                    TransformMatchingShapes(l1.select_part(p1).copy(), l2.select_part(p2))
                    for p1, p2 in zip(l1.pieces, l2.pieces)
                ),
                ReplacementTransform(l1.select_parts("+").copy(), l2.select_parts("+")),
                ReplacementTransform(l1.select_parts("\\cdots").copy(), l2.select_parts("\\cdots")),
                *added_anims,
            )
            self.wait()

        # Sweep away
        series = lines[4]
        self.play(
            series.animate.move_to(UP),
            FadeOut(VGroup(lines[0], arrows[0], arrows[0].label), UP),
            FadeOut(VGroup(lines[3], arrows[1], arrows[1].label), 0.5 * UP),
        )
        self.wait()

        # Name Dirichlet series
        gf_part = title.select_part("generating function?")
        strike = Line().replace(gf_part, dim_to_match=0)
        strike.set_stroke(RED, 5)
        dirichlet = Text("Dirichlet series")
        dirichlet.set_color(BLUE)
        dirichlet.next_to(gf_part, DOWN)

        self.play(
            ShowCreation(strike),
        )
        self.play(FadeIn(dirichlet, DOWN))
        self.wait()

        # Von Mangoldt
        vm_name = Text("Von Mangoldt function: ")
        vm_def = VGroup(
            Tex("\\Lambda(n)= \\log p & \\text { if } n=p^{k} \\text { for some prime } p \\text { and integer } k \\geq 1"),
            Tex("\\Lambda(n)= 0 & \\text { otherwise }")
        )
        vm_def.arrange(DOWN, aligned_edge=LEFT)
        vm = VGroup(vm_name, vm_def)
        vm.arrange(RIGHT)
        vm_name.align_to(vm_def[0], DOWN)
        vm.set_width(FRAME_WIDTH - 1)
        vm.next_to(series, DOWN, LARGE_BUFF)

        self.play(Write(vm_name, run_time=1))
        self.wait()
        for part in vm_def:
            self.play(FadeIn(part))
            self.wait()

        self.play(
            FadeOut(vm),
            FadeOut(VGroup(title, underline, strike), 0.5 * UP),
            FadeOut(dirichlet, UP),
            series.animate.move_to(2 * UP),
        )

        # Contrast with zeta
        zeta_series = lines[5]
        zeta_series.center()
        zeta_series.set_color(WHITE)
        zeta_brace = Brace(zeta_series, DOWN, buff=SMALL_BUFF)
        zeta_sym = OldTex("\\zeta(s)")
        zeta_sym.next_to(zeta_brace, DOWN)
        zeta_group = VGroup(zeta_series, zeta_brace, zeta_sym)

        series_brace = Brace(series, DOWN, buff=SMALL_BUFF)
        series_label = Tex("-{\\zeta'(s) \\over \\zeta(s)}")
        series_label.next_to(series_brace, DOWN)

        self.play(FadeIn(zeta_series, DOWN))
        self.play(
            GrowFromCenter(zeta_brace),
            Write(zeta_sym)
        )
        self.wait()
        self.play(
            GrowFromCenter(series_brace),
            Write(series_label),
            zeta_group.animate.shift(1.5 * DOWN)
        )
        self.wait()

        # Show the complex plane
        pass
