# ==============================================================================
# Scene:      PrimesNearMillion
# Source:     videos/_2024/antp/main.py (lines 370-475)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl PrimesNearMillion.py PrimesNearMillion -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *
import sympy

class PrimesNearMillion(InteractiveScene):
    def construct(self):
        # Add line
        T = int(1e6)
        radius = 800
        spacing = 50
        labeled_numbers = list(range(T - radius, T + radius, spacing))
        number_line = NumberLine(
            (T - radius, T + radius),
            width=250,
            tick_size=0.075,
        )
        number_line.ticks[::spacing // 5].stretch(2, 1)
        # number_line.stretch(0.2, 0)
        number_line.add_numbers(labeled_numbers, font_size=48, buff=0.5)
        self.add(number_line)

        # Primes
        primes = np.array(list(sympy.primerange(T - radius, T + radius)))
        dots = GlowDots(number_line.n2p(primes))
        dots.set_glow_factor(2)
        dots.set_radius(0.35)
        self.add(dots)

        # Highlight twins
        arcs = VGroup()
        for p1, p2 in zip(primes, primes[1:]):
            if p1 + 2 == p2:
                arc = Line(
                    number_line.n2p(p1),
                    number_line.n2p(p2),
                    path_arc=-PI
                )
                arc.set_stroke(YELLOW, 3)
                plus_2 = Tex("+2", font_size=24)
                plus_2.set_fill(YELLOW)
                plus_2.next_to(arc, UP, SMALL_BUFF)
                arcs.add(arc, plus_2)

        # Pan
        line_group = Group(number_line, dots, arcs)
        line_group.shift(1.5 * DOWN + -number_line.n2p(1e6))
        line_group.add_updater(lambda m, dt: m.shift(2 * dt * LEFT))
        self.add(line_group)

        # Words
        t2c = {"T": BLUE}
        kw = dict(font_size=90, t2c=t2c)
        words = TexText("How dense are primes?", **kw)
        lhs = TexText("Prime density near $T$", **kw)
        approx = Tex(R"\approx", **kw)
        approx.rotate(PI / 2)
        rhs = Tex(R"1 / \ln(T)", **kw)
        group = VGroup(lhs, approx, rhs)
        group.arrange(DOWN, buff=0.5)
        group.to_edge(UP)
        words.move_to(lhs)

        example = TexText("(e.g. $T = 1{,}000{,}000$)", font_size=60, t2c=t2c)
        example.next_to(lhs, DOWN, LARGE_BUFF)
        arrow = Arrow(
            lhs["T"].get_bottom(),
            example.get_right(),
            stroke_width=8,
            stroke_color=BLUE,
            path_arc=-PI / 2,
            buff=0.2,
        )

        self.add(words)
        self.wait(13)
        self.play(
            FadeTransform(words, lhs, run_time=1),
            ShowCreation(arrow),
            FadeIn(example, time_span=(1, 2)),
        )
        self.wait(5)
        self.play(
            FadeOut(arrow),
            FadeOut(example),
            Write(approx),
            FadeIn(rhs[:-2], DOWN),
            FadeIn(rhs[-1], DOWN),
            TransformFromCopy(lhs["T"], rhs["T"]),
        )
        self.wait(45)

    def old_zooming(self):
        sf = 0.1
        self.play(
            number_line.animate.scale(sf, about_point=ORIGIN),
            dots.animate.scale(sf, about_point=ORIGIN).set_radius(0.1),
            rate_func=rush_from,
            run_time=17
        )
        self.wait()

        # Zoom in to twin prime
        zoom_point = number_line.n2p(1000210)
        frame = self.frame

        self.play(
            frame.animate.move_to(zoom_point).set_height(0.60),
            dots.animate.set_radius(0.03),
            run_time=5
        )
