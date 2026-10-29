# ==============================================================================
# Scene:      LinearAsASuperpositionOfCircular
# Source:     videos/_2023/optics_puzzles/cylinder.py (lines 1168-1318)
# Category:   1 · Renders unmodified
# Includes code copied from: _2023/optics_puzzles/objects.py
#
# Run from this folder:
#     manimgl LinearAsASuperpositionOfCircular.py LinearAsASuperpositionOfCircular -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *


# ----- From _2023/optics_puzzles/objects.py -----

class Molecule(Group):
    # List of characters
    atoms = []

    # List of 3d coordinates
    coordinates = np.zeros((0, 3))

    # List of pairs of indices
    bonds = []

    atom_to_color = {
        "H": WHITE,
        "O": RED,
        "C": GREY,
    }
    atom_to_radius = {
        "H": 0.1,
        "O": 0.2,
        "C": 0.19,
    }
    ball_config = dict(shading=(0.25, 0.5, 0.5), glow_factor=0.25)
    stick_config = dict(stroke_width=1, stroke_color=GREY_A, flat_stroke=False)

    def __init__(self, height=2.0, **kwargs):
        coords = np.array(self.coordinates)
        radii = np.array([self.atom_to_radius[atom] for atom in self.atoms])
        rgbas = np.array([color_to_rgba(self.atom_to_color[atom]) for atom in self.atoms])

        balls = DotCloud(coords, **self.ball_config)
        balls.set_radii(radii)
        balls.set_rgba_array(rgbas)

        sticks = VGroup()
        for i, j in self.bonds:
            c1, c2 = coords[[i, j], :]
            r1, r2 = radii[[i, j]]
            unit_vect = normalize(c2 - c1)

            sticks.add(Line(
                c1 + r1 * unit_vect, c2 - r2 * unit_vect,
                **self.stick_config
            ))

        super().__init__(balls, sticks, **kwargs)

        self.apply_depth_test()
        self.balls = balls
        self.sticks = sticks
        self.set_height(height)


class Sucrose(Molecule):
    atoms = [
        "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O",
        "C", "C", "C", "C", "C", "C", "C", "C", "C", "C", "C", "C",
        "H", "H", "H", "H", "H", "H", "H", "H", "H", "H", "H", "H", "H", "H", "H", "H", "H", "H", "H", "H", "H", "H",
    ]
    coordinates = np.array([
        [-1.468 ,  0.4385, -0.9184],
        [-0.6033, -0.8919,  0.8122],
        [ 0.9285,  0.4834, -0.3053],
        [-3.0702, -2.0054,  1.1933],
        [-4.62  ,  0.6319,  0.7326],
        [ 1.2231,  0.2156,  2.5658],
        [ 3.6108, -1.7286,  0.6379],
        [ 3.15  ,  1.8347,  1.1537],
        [-1.9582, -1.848 , -2.43  ],
        [-1.3845,  3.245 , -0.8933],
        [ 3.8369,  0.2057, -2.5044],
        [-1.4947, -0.8632, -0.3037],
        [-2.9301, -1.0229,  0.1866],
        [-3.229 ,  0.3737,  0.6887],
        [-2.5505,  1.2243, -0.3791],
        [ 0.7534, -0.7453,  0.3971],
        [ 1.6462, -0.7853,  1.639 ],
        [ 3.1147, -0.5553,  1.2746],
        [ 3.2915,  0.6577,  0.3521],
        [ 2.2579,  0.7203, -0.7858],
        [-1.0903, -1.9271, -1.3122],
        [-2.0027,  2.5323,  0.1653],
        [ 2.5886, -0.1903, -1.9666],
        [-3.6217, -1.2732, -0.6273],
        [-2.8148,  0.5301,  1.6917],
        [-3.2289,  1.4361, -1.215 ],
        [ 1.0588, -1.5992, -0.2109],
        [ 1.5257, -1.753 ,  2.1409],
        [ 3.6908, -0.4029,  2.1956],
        [ 4.31  ,  0.675 , -0.0511],
        [ 2.2441,  1.7505, -1.1644],
        [-1.1311, -2.9324, -0.8803],
        [-0.0995, -1.7686, -1.74  ],
        [-1.2448,  2.3605,  0.9369],
        [-2.799 ,  3.1543,  0.5841],
        [ 1.821 , -0.1132, -2.7443],
        [ 2.6532, -1.2446, -1.6891],
        [-3.98  , -1.9485,  1.5318],
        [-4.7364,  1.5664,  0.9746],
        [ 0.2787,  0.0666,  2.7433],
        [ 4.549 , -1.5769,  0.4327],
        [ 3.3427,  2.6011,  0.5871],
        [-1.6962, -2.5508, -3.0488],
        [-0.679 ,  2.6806, -1.2535],
        [ 3.7489,  1.1234, -2.8135],
    ])
    bonds = [
        (0, 11),
        (0, 14),
        (1, 11),
        (1, 15),
        (2, 15),
        (2, 19),
        (3, 12),
        (3, 37),
        (4, 13),
        (4, 38),
        (5, 16),
        (5, 39),
        (6, 17),
        (6, 40),
        (7, 18),
        (7, 41),
        (8, 20),
        (8, 42),
        (9, 21),
        (9, 43),
        (10, 22),
        (10, 44),
        (11, 12),
        (11, 20),
        (12, 13),
        (12, 23),
        (13, 14),
        (13, 24),
        (14, 21),
        (14, 25),
        (15, 16),
        (15, 26),
        (16, 17),
        (16, 27),
        (17, 18),
        (17, 28),
        (18, 19),
        (18, 29),
        (19, 22),
        (19, 30),
        (20, 31),
        (20, 32),
        (21, 33),
        (21, 34),
        (22, 35),
        (22, 36),
    ]



# ----- From _2023/optics_puzzles/cylinder.py -----

class LinearAsASuperpositionOfCircular(InteractiveScene):
    rotation_rate = 0.25
    amplitude = 2.0

    def construct(self):
        # Set up planes
        plane_config = dict(
            background_line_style=dict(stroke_color=GREY, stroke_width=1),
            faded_line_style=dict(stroke_color=GREY, stroke_width=0.5, stroke_opacity=0.5),
        )
        planes = VGroup(
            ComplexPlane((-1, 1), (-1, 1), **plane_config),
            ComplexPlane((-1, 1), (-1, 1), **plane_config),
            ComplexPlane((-2, 2), (-2, 2), **plane_config),
        )
        planes[:2].arrange(DOWN, buff=2.0).set_height(FRAME_HEIGHT - 1.5).next_to(ORIGIN, LEFT, 1.0)
        planes[2].set_height(6).next_to(ORIGIN, RIGHT, 1.0)
        # planes.arrange(RIGHT, buff=1.5)
        self.add(planes)

        # Set up trackers
        phase_trackers = ValueTracker(0).replicate(2)
        phase1_tracker, phase2_tracker = phase_trackers

        def update_phase(m, dt):
            m.increment_value(TAU * self.rotation_rate * dt)

        def slow_changer(m, dt):
            m.increment_value(-0.5 * TAU * self.rotation_rate * dt)

        for tracker in phase_trackers:
            tracker.add_updater(update_phase)

        self.add(*phase_trackers)

        def get_z1():
            return 0.5 * self.amplitude * np.exp((PI / 2 + phase1_tracker.get_value()) * 1j)

        def get_z2():
            return 0.5 * self.amplitude * np.exp((PI / 2 - phase2_tracker.get_value()) * 1j)

        def get_sum():
            return get_z1() + get_z2()

        # Vectors
        vects = VGroup(
            self.get_vector(planes[0], get_z1, color=RED),
            self.get_vector(planes[1], get_z2, color=YELLOW),
            self.get_vector(planes[2], get_sum, color=BLUE),
            self.get_vector(planes[2], get_z1, color=RED),
            self.get_vector(planes[2], get_sum, get_base=get_z1, color=YELLOW),
        )

        self.add(*vects)

        # Polarization line
        pol_line = Line(UP, DOWN)
        pol_line.set_stroke(YELLOW, 1)
        pol_line.match_height(planes[2])
        pol_line.move_to(planes[2])

        def update_pol_line(line):
            if abs(vects[2].get_length()) > 1e-3:
                line.set_angle(vects[2].get_angle())
                line.move_to(planes[2].n2p(0))
            return line

        pol_line.add_updater(update_pol_line)

        self.add(pol_line, *planes, *vects)

        # Write it as an equation
        plus = Tex("+", font_size=72)
        equals = Tex("=", font_size=72)
        plus.move_to(planes[0:2])
        # equals.move_to(planes[1:3])
        equals.move_to(ORIGIN)

        self.add(plus, equals)

        # Slow down annotation
        arcs = VGroup(
            Arrow(LEFT, RIGHT, path_arc=-PI, stroke_width=2),
            Arrow(RIGHT, LEFT, path_arc=-PI, stroke_width=2),
        )
        arcs.move_to(planes[0])
        slow_word = Text("Slow down!")
        slow_word.next_to(planes[0], DOWN)
        sucrose = Sucrose(height=1)
        sucrose.balls.scale_radii(0.25)
        sucrose.fade(0.5)
        sucrose.move_to(planes[0])
        slow_group = Group(slow_word, arcs, sucrose)

        def slow_down():
            self.play(FadeIn(slow_group, run_time=0.25))
            phase1_tracker.add_updater(slow_changer)
            self.wait(0.75)
            phase1_tracker.remove_updater(slow_changer)
            self.play(FadeOut(slow_group))

        # Highlight constituent parts
        back_rects = VGroup(*(BackgroundRectangle(plane) for plane in planes))
        back_rects.set_fill(opacity=0.5)

        self.wait(8)

        self.add(back_rects[1])
        VGroup(vects[1], vects[2], vects[4]).set_stroke(opacity=0.25)
        self.wait(8)
        self.remove(back_rects[1])

        self.add(back_rects[0])
        vects.set_stroke(opacity=1)
        VGroup(vects[0], vects[2]).set_stroke(opacity=0.25)
        self.wait(8)
        vects.set_stroke(opacity=1)
        self.remove(back_rects)
        self.wait(4)

        # Rotation labels
        for tracker in phase_trackers:
            tracker.set_value(0)

        rot_labels = VGroup(*(
            TexText("Total rotation: 0.00")
            for _ in range(2)
        ))
        for rot_label, plane, tracker in zip(rot_labels, planes, phase_trackers):
            rot_label.set_height(0.2)
            rot_label.set_color(GREY_B)
            rot_label.next_to(plane, UP)
            dec = rot_label.make_number_changeable("0.00", edge_to_fix=LEFT)
            dec.phase_tracker = tracker
            dec.add_updater(lambda m: m.set_value(m.phase_tracker.get_value() / TAU))

        self.add(rot_labels)

        # Let it play, occasionally kink
        self.wait(9)
        for _ in range(20):
            slow_down()
            self.wait(3 * random.random())

    def get_vector(self, plane, get_z, get_base=lambda: 0, color=BLUE):
        vect = Vector(UP, stroke_color=color)
        vect.add_updater(lambda m: m.put_start_and_end_on(
            plane.n2p(get_base()),
            plane.n2p(get_z())
        ))
        return vect
