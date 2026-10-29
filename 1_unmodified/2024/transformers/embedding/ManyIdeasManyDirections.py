# ==============================================================================
# Scene:      ManyIdeasManyDirections
# Source:     videos/_2024/transformers/embedding.py (lines 2695-2755)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ManyIdeasManyDirections.py ManyIdeasManyDirections -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

def get_direction_lines(axes, direction, n_lines=500, color=YELLOW, line_length=1.0, stroke_width=3):
    line = Line(ORIGIN, line_length * normalize(direction))
    line.insert_n_curves(20).set_stroke(width=(0, stroke_width, stroke_width, stroke_width, 0))
    lines = line.replicate(n_lines)
    lines.set_color(color)
    for line in lines:
        line.move_to(axes.c2p(
            random.uniform(*axes.x_range[:2]),
            random.uniform(*axes.y_range[:2]),
            random.uniform(*axes.z_range[:2]),
        ))
    return lines


class SimpleSpaceExample(InteractiveScene):
    def construct(self):
        # Setup axes
        frame = self.frame
        plane, axes = self.add_plane_and_axes()
        frame.reorient(14, 77, 0, (2.23, 0.25, 1.13), 4.46)

        # Show an initial vector in the space
        frame.add_ambient_rotation()
        vect = Arrow(axes.c2p(0, 0, 0), axes.c2p(2, -1, 1), buff=0)
        vect.set_color(BLUE)
        vect.always.set_perpendicular_to_camera(self.frame)
        label = Text("you", font_size=24)
        # label = Text("Photo", font_size=24).set_backstroke(BLACK, 5)
        label.rotate(PI / 2, RIGHT)
        label.next_to(vect.get_center(), OUT + LEFT, buff=0)

        self.play(
            ShowCreation(vect),
            FadeIn(label, vect.get_vector())
        )
        self.wait(5)

        # Many directions -> Different kinds of meaning
        ideas = VGroup(
            Text("Part of a command"),
            Text("Affectionate"),
            Text("Sadness"),
        )
        ideas.set_backstroke(BLACK, 3)
        ideas.scale(0.35)
        ideas.rotate(PI / 2, RIGHT)

        last_idea = VGroup()
        last_direction = 1.0 * normalize(cross(RIGHT, vect.get_vector()))
        for idea in ideas:
            direction = rotate_vector(last_direction, PI / 3, vect.get_vector())
            new_vect = self.get_added_vector(vect, direction)
            new_vect.set_perpendicular_to_camera(self.frame)
            idea.next_to(new_vect.get_center(), buff=0.1)
            lines = get_direction_lines(axes, new_vect.get_vector(), color=new_vect.get_color())
            self.play(
                FadeOut(last_idea),
                ShowCreation(new_vect),
                FadeIn(idea, new_vect.get_vector()),
                LaggedStartMap(ShowCreationThenFadeOut, lines, lag_ratio=2 / len(lines), run_time=2)
            )
            self.wait(1)
            last_idea = VGroup(new_vect, idea)
            last_direction = direction
        self.play(FadeOut(last_idea))
        self.wait(5)

        # Specific ideas added onto "you"
        ideas = VGroup(
            # Text("Astronaut"),
            # Text("Riding a Horse"),
            # Text("On the moon"),
            #
            Text("needs an adjective next"),
            Text("preceded by \"that which does not kill\""),
            Text("related to growth and strength"),
            #
            # Text("River bank"),
            # Text("Beginning of a story"),
            # Text("Establishing a setting"),
        )
        ideas.scale(0.4)
        ideas.rotate(PI / 2, RIGHT)
        directions = [
            (-0.25, -1, 0.75),
            (-0.5, -0.25, 0.5),
            (1.0, -0.5, 1.0),
        ]
        orientations = [
            (11, 92, 0, (2.69, 0.55, 1.12), 6.25),
            (-8, 83, 0, (2.73, 0.56, 1.24), 6.80),
            (-14, 79, 0, (2.49, 0.61, 1.41), 7.64),
        ]

        vects = VGroup(vect)
        concepts = VGroup(label)
        for idea, direction, orientation in zip(ideas, directions, orientations):
            point = vects[-1].get_end()
            new_vect = self.get_added_vector(vects[-1], direction)
            new_vect.always.set_perpendicular_to_camera(self.frame)
            idea.next_to(new_vect.get_center())
            self.play(
                frame.animate.reorient(*orientation),
                GrowArrow(new_vect),
                FadeIn(idea, 0.5 * new_vect.get_vector())
            )
            self.wait(2)
            vects.add(new_vect)
        self.wait(15)

    def add_plane_and_axes(
        self,
        x_range=(-4, 4),
        y_range=(-4, 4),
        z_range=(-3, 3),
    ):
        axes = ThreeDAxes(x_range, y_range, z_range)
        plane = NumberPlane(
            x_range, y_range,
            background_line_style=dict(
                stroke_color=GREY_D,
                stroke_width=1
            ),
            faded_line_ratio=1,
        )
        plane.axes.set_stroke(GREY_D, 0)

        self.add(plane, axes)
        return plane, axes

    def get_added_vector(self, last_vect, direction):
        point = last_vect.get_end()
        new_vect = Arrow(point, point + direction, buff=0)
        new_vect.set_color(random_bright_color())
        new_vect.set_flat_stroke(False)
        return new_vect


class ManyIdeasManyDirections(SimpleSpaceExample):
    random_seed = 2

    def construct(self):
        # Axes
        frame = self.frame
        plane, axes = self.add_plane_and_axes()
        frame.reorient(-17, 73, 0, (-0.06, 0.11, 0.31), 6.03)
        frame.add_ambient_rotation()

        # Many directions -> Different kinds of meaning
        ideas = VGroup(
            Text(word)
            for word in [
                "Typewriter",
                "Paradigm",
                "Whimsical",
                "Gelatinous",
                "Rainbow",
                "Serendipitous",
                "Algorithm",
                "Nebulous",
                "Spatula",
                "Lethargic",
                "Effervescent",
                "Asteroid",
                "Pungent",
                "Daydream",
                "Mercurial",
                "Cactus",
                "Diaphanous",
                "Hiccup",
                "Viscous",
                "Thunderclap",
            ]
        )
        ideas.set_backstroke(BLACK, 3)
        ideas.scale(0.5)
        ideas.rotate(PI / 2, RIGHT)

        last_idea = VGroup()
        last_direction = RIGHT + OUT
        for idea in ideas:
            direction = normalize(cross(last_direction, np.random.uniform(-1, 1, 3)))
            new_vect = Vector(direction)
            new_vect.set_perpendicular_to_camera(self.frame)
            new_vect.set_color(random_bright_color())
            idea.next_to(new_vect.get_end(), direction, buff=0.1)
            lines = get_direction_lines(axes, direction, color=new_vect.get_color(), n_lines=250, stroke_width=2)
            idea.set_fill(interpolate_color(new_vect.get_color(), WHITE, 0.5))
            self.play(
                FadeOut(last_idea),
                GrowArrow(new_vect),
                FadeIn(idea, new_vect.get_vector()),
                LaggedStartMap(ShowCreationThenFadeOut, lines, lag_ratio=1 / len(lines), run_time=1.5)
            )
            self.wait()
            last_idea = VGroup(new_vect, idea)
            last_direction = direction
        self.play(FadeOut(last_idea))
        self.wait(5)
