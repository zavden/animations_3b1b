# ==============================================================================
# Scene:      SugarIsChiral
# Source:     videos/_2023/optics_puzzles/annotations.py (lines 1062-1146)
# Category:   1 · Renders unmodified
# Includes code copied from: _2023/optics_puzzles/objects.py
#
# Run from this folder:
#     manimgl SugarIsChiral.py SugarIsChiral -w -m --fps 15
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



# ----- From _2023/optics_puzzles/annotations.py -----

class SugarIsChiral(InteractiveScene):
    default_frame_orientation = (-33, 85)
    title = R"Sucrose $\text{C}_{12}\text{H}_{22}\text{O}_{11}$ "
    subtitle = "(D-Glucose + D-Fructose)"
    molecule_height = 3

    def construct(self):
        axes = ThreeDAxes()
        axes.set_stroke(opacity=0.5)
        # self.add(axes)

        # Set up
        frame = self.frame
        title = VGroup(
            TexText(self.title),
            TexText(self.subtitle),
        )
        title[1].scale(0.7).set_color(GREY_A)
        title.arrange(DOWN)
        title.fix_in_frame()
        title.to_edge(UP, buff=0.25)

        sucrose = Sucrose()
        sucrose.set_height(self.molecule_height)

        # Introduce
        frame.reorient(24, 74, 0)
        self.add(title)
        self.play(
            FadeIn(sucrose, scale=5),
        )
        self.play(
            self.frame.animate.reorient(-16, 75, 0).set_anim_args(run_time=6)
        )
        self.add(sucrose)
        self.wait()

        # Show mirror image
        mirror = Square(side_length=6)
        mirror.set_fill(BLUE, 0.35)
        mirror.set_stroke(width=0)
        mirror.rotate(PI / 2, UP)
        mirror.set_shading(0, 1, 0)
        mirror.stretch(3, 1)

        sucrose.target = sucrose.generate_target()
        sucrose.target.next_to(mirror, LEFT, buff=1.0)

        self.add(mirror, sucrose)
        self.play(
            frame.animate.move_to(0.75 * OUT),
            MoveToTarget(sucrose),
            FadeIn(mirror),
            title.animate.scale(0.75).match_x(sucrose.target).set_y(1.75),
            run_time=1.5,
        )

        mirror_image = sucrose.copy()
        mirror_image.target = mirror_image.generate_target()
        mirror_image.target.stretch(-1, 0, about_point=mirror.get_center())

        mirror_words = Text("(mirror image)", font_size=36, color=GREY_A)
        mirror_words.fix_in_frame()
        mirror_words.match_x(mirror_image.target)
        mirror_words.match_y(title)

        self.add(mirror_image, mirror, sucrose)
        self.play(
            MoveToTarget(mirror_image),
            FadeIn(mirror_words),
        )

        # Chiral definition
        definition = TexText(R"Chiral $\rightarrow$ Cannot be superimposed onto its mirror image")
        definition.fix_in_frame()
        definition.to_edge(UP)

        sucrose.add_updater(lambda m, dt: m.rotate(10 * DEGREES * dt, axis=OUT))
        mirror_image.add_updater(lambda m, dt: m.rotate(-10 * DEGREES * dt, axis=OUT))
        self.play(Write(definition))
        self.play(
            self.frame.animate.reorient(-8, 76, 0),
            run_time=15,
        )
        self.wait(15)
