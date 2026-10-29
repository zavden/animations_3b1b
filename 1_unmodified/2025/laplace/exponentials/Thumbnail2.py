# ==============================================================================
# Scene:      Thumbnail2
# Source:     videos/_2025/laplace/exponentials.py (lines 1652-1716)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl Thumbnail2.py Thumbnail2 -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class Thumbnail2(InteractiveScene):
    def construct(self):
        # Test
        theta = 140 * DEG
        z = np.exp(theta * 1j)

        plane_color = BLUE
        path_color = YELLOW
        vect_color = WHITE

        plane = ComplexPlane(
            (-4, 4),
            (-2, 2)
        )
        plane.set_height(10)
        plane.center()
        plane.add_coordinate_labels(font_size=24)
        plane.axes.set_stroke(WHITE, 3)
        plane.background_lines.set_stroke(plane_color, 4)
        plane.faded_lines.set_stroke(plane_color, 3, 0.35)

        unit_size = plane.x_axis.get_unit_size()

        arrow = Arrow(
            plane.n2p(1),
            plane.n2p(z),
            buff=0,
            path_arc=theta,
            thickness=12,
            fill_color=YELLOW,
        )
        arrow.scale(0.965, about_point=plane.n2p(1))
        arrow.set_fill(border_width=3)

        path = Arc(0, theta, radius=unit_size)
        path.set_stroke(path_color, width=(2, 30))
        dot = Group(TrueDot(radius=0.2), GlowDot(radius=0.75))
        dot.set_color(path_color)
        dot.move_to(path.get_end())

        n_vects = 8
        vectors = VGroup(
            Vector(2.5 * UP, thickness=8).set_fill(vect_color, opacity**2).put_start_on(plane.n2p(1)).rotate(phi, about_point=plane.n2p(0))
            for phi, opacity in zip(np.linspace(0, theta, n_vects), np.linspace(0.5, 1, n_vects))
        )
        vectors.set_fill(border_width=3)

        circle = Circle(radius=unit_size)
        circle.set_stroke(GREY, 5)

        d_line = DashedLine(plane.n2p(0), plane.n2p(z))
        d_line.set_stroke(WHITE, 3)
        arc = Arc(0, theta, radius=0.5)
        arc.set_stroke(WHITE, 5)
        theta_label = Tex(R"\theta", font_size=72)
        theta_label.next_to(arc.pfp(0.5), UR, SMALL_BUFF)

        self.add(plane)
        self.add(circle)
        self.add(d_line)
        self.add(vectors)
        self.add(path)
        self.add(dot)
        self.add(arc)
        self.add(theta_label)
