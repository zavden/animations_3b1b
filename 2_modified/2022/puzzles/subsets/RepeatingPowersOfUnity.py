# ==============================================================================
# Scene:      RepeatingPowersOfUnity
# Source:     videos/_2022/puzzles/subsets.py (lines 3254-3336)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl RepeatingPowersOfUnity.py RepeatingPowersOfUnity -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Scene.play no longer accepts path_arc=: it is passed to the animations that move (Transform/MoveToTarget/set_anim_args)
# ==============================================================================

from manim_imports_ext import *

class RepeatingPowersOfUnity(InteractiveScene):
    n_steps = 25

    def construct(self):
        # Setup plane
        plane = ComplexPlane((-2, 2), (-2, 2))
        plane.set_height(FRAME_HEIGHT - 0.5)
        plane.add_coordinate_labels(font_size=24)
        for coord in plane.coordinate_labels:
            coord.shift_onto_screen(buff=SMALL_BUFF)
            coord.set_fill(WHITE)
        plane.to_edge(LEFT, buff=0.1)
        self.disable_interaction(plane)

        unit_circle = Circle(radius=plane.x_axis.get_unit_size())
        unit_circle.move_to(plane.get_origin())
        unit_circle.set_stroke(GREY_C, 2)
        self.disable_interaction(unit_circle)

        complex_plane_title = Text("Complex plane", font_size=42)
        complex_plane_title.next_to(plane.get_corner(UL), DR, buff=SMALL_BUFF)
        complex_plane_title.set_backstroke(width=8)

        self.add(plane)
        self.add(unit_circle)
        self.add(complex_plane_title)

        # Setup roots
        roots = [np.exp(complex(0, n * TAU / 5)) for n in range(5)]
        root_points = list(map(plane.n2p, roots))
        root_dots = Group(*(
            GlowDot(point)
            for point in root_points
        ))
        root_lines = VGroup(*(
            Arrow(
                plane.get_origin(), point, buff=0,
                stroke_width=2,
                stroke_color=YELLOW,
                stroke_opacity=0.7
            )
            for point in root_points
        ))
        self.disable_interaction(root_dots)

        pentagon = Polygon(*root_points)
        pentagon.set_stroke(TEAL, 2)
        pentagon.set_fill(TEAL, 0.25)
        self.add(pentagon)

        # Labels
        zeta_labels = VGroup()
        for n in range(self.n_steps):
            label = Tex("\\zeta^2")
            label[0].set_color(YELLOW)
            exp = Integer(n)
            exp.match_height(label[1])
            exp.move_to(label[1], DL)
            label.replace_submobject(1, exp)
            point = root_points[n % 5]
            vect = normalize(point - plane.get_origin())
            if n % 5 == 0:
                vect = UR
            label.next_to(point, vect, buff=SMALL_BUFF)
            zeta_labels.add(label)
        zeta_labels.set_backstroke(width=4)

        # Animations
        line = root_lines[0].copy()
        dot = root_dots[0].copy()
        label = zeta_labels[0].copy()

        self.add(line, dot, label)
        self.wait()

        for n in range(1, self.n_steps):
            self.play(
                # CHANGE: Scene.play no longer accepts path_arc; it is passed to each Transform
                Transform(line, root_lines[n % 5], path_arc=TAU / 5),
                Transform(dot, root_dots[n % 5], path_arc=TAU / 5),
                Transform(label, zeta_labels[n], path_arc=TAU / 5),
            )
            self.wait()
