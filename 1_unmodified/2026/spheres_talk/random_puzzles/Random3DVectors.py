# ==============================================================================
# Scene:      Random3DVectors
# Source:     videos/_2026/spheres_talk/random_puzzles.py (lines 572-644)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl Random3DVectors.py Random3DVectors -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class Random3DVectors(InteractiveScene):
    def construct(self):
        # Set up
        frame = self.frame
        radius = 2
        axes = ThreeDAxes(unit_size=radius)
        sphere = Sphere(radius=radius)
        mesh = SurfaceMesh(sphere, resolution=(51, 26))
        mesh.set_stroke(WHITE, 2, 0.1)

        v1, v2 = vects = Vector(RIGHT, thickness=4).replicate(2)
        colors = [PINK, YELLOW]
        for vect, color in zip(vects, colors):
            vect.set_fill(color)
            vect.always.set_perpendicular_to_camera(frame)
            self.set_vector_randomly(vect, radius)

        frame.reorient(-38, 74, 0, (0.04, -0.01, -0.06), 4.82)
        self.add(axes, mesh)
        self.add(vects)

        # Add dot product label
        def get_dp():
            vect1 = v1.get_vector()
            vect2 = v2.get_vector()
            return np.dot(vect1, vect2) / (get_norm(vect1) * get_norm(vect2))

        dp_label = Tex(R"\vec{\textbf{v}} \cdot \vec{\textbf{w}} = 0.00")
        dp_label[R"\vec{\textbf{v}}"].set_color(PINK)
        dp_label[R"\vec{\textbf{w}}"].set_color(YELLOW)
        num = dp_label.make_number_changeable("0.00")
        num.f_always.set_value(get_dp)

        dp_label.fix_in_frame()
        dp_label.to_corner(UL)
        self.add(dp_label)

        # Randomize
        frame.add_ambient_rotation(2 * DEG)
        for n in range(100):
            for vect in vects:
                self.set_vector_randomly(vect, radius)
            self.wait(0.2)

        # Only one random vector
        v2.put_start_and_end_on(ORIGIN, radius * OUT)
        v2.set_fill(opacity=0.5)

        dot = GlowDot()
        dot.set_color(v1.get_color())
        dot_ghosts = Group()

        def project(points):
            points[:, :2] = 0
            return points

        z_line = Line(ORIGIN, OUT)
        z_line.set_stroke(WHITE, 8)
        self.add(dot, dot_ghosts, z_line)

        for n in range(100):
            self.set_vector_randomly(v1, radius)
            z_line.set_points_as_corners([ORIGIN, v1.get_end()[2] * OUT])
            dot.move_to(v1.get_end())
            dot_ghosts.add(dot.copy())
            for ghost in dot_ghosts:
                ghost.set_opacity(ghost.get_opacity() * 0.9)
            self.wait(0.2)

    def set_vector_randomly(self, vect, radius):
        point = radius * normalize(np.random.normal(0, 1, 3))
        vect.put_start_and_end_on(ORIGIN, point)
        return vect
