# ==============================================================================
# Scene:      RootsOfUnity
# Source:     videos/_2022/convolutions/discrete.py (lines 2468-2531)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl RootsOfUnity.py RootsOfUnity -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class RootsOfUnity(InteractiveScene):
    def construct(self):
        # Add plane
        plane = ComplexPlane((-2, 2), (-2, 2))
        plane.scale(2.0 / 1.5)
        plane.to_corner(UL)
        plane.add_coordinate_labels([1, 1j], font_size=24)

        circle = Circle(radius=plane.x_axis.get_unit_size())
        circle.move_to(plane.n2p(0))
        circle.set_stroke(YELLOW, 2)

        N = 8
        roots = [np.exp(TAU * 1j * k / N) for k in range(N)]
        root_dots = Group(*(GlowDot(plane.n2p(root)) for root in roots))
        root_lines = VGroup(*(Line(plane.n2p(0), d.get_center()) for d in root_dots))
        root_lines.set_stroke(YELLOW, 1)

        self.add(plane)
        self.add(root_lines[0], root_dots[0])
        self.play(
            ShowCreation(circle),
            Rotate(Group(root_lines[0], root_dots[0]), TAU, about_point=plane.n2p(0)),
            run_time=2,
        )
        self.wait()

        # Show powers
        kw = dict(tex_to_color_map={R"\omega": YELLOW}, font_size=36)
        max_power = 3 * N
        powers = VGroup(*(
            OldTex(Rf"\omega^{{{k}}}", **kw)
            for k in range(max_power)
        ))
        powers.set_backstroke(BLACK, 3)
        for power, line in zip(powers, it.cycle(root_lines)):
            vect = line.get_vector()
            vect += UP if line.get_vector()[1] > -0.1 else DOWN
            vect += RIGHT if line.get_vector()[0] > -0.1 else LEFT
            power.next_to(line.get_end(), normalize(vect), buff=SMALL_BUFF)

        shown_powers = VGroup(powers[0])
        moving_power = powers[0].copy()
        for k in range(max_power - 1):
            shown_powers.generate_target()
            shown_powers.target.set_opacity(0.8)
            if k > N - 1:
                shown_powers.target[(k + 1) % N].set_opacity(0)

            kw = dict(path_arc=TAU / N)
            self.play(
                Transform(moving_power, powers[k + 1], **kw),
                Transform(root_lines[k % N].copy(), root_lines[(k + 1) % N], remover=True, **kw),
                Transform(root_dots[k % N].copy(), root_dots[(k + 1) % N], remover=True, **kw),
                MoveToTarget(shown_powers, **kw),
            )
            self.add(root_lines[:k + 2], root_dots[:k + 2])
            if k < N - 1:
                shown_powers.add(powers[k + 1])
        self.play(
            FadeOut(moving_power),
            powers[:N].animate.set_opacity(1)
        )
        self.wait()
