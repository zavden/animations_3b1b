# ==============================================================================
# Scene:      DotProductOfUnitVectors
# Source:     videos/_2026/spheres_talk/random_puzzles.py (lines 450-569)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl DotProductOfUnitVectors.py DotProductOfUnitVectors -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class DotProductOfUnitVectors(InteractiveScene):
    random_seed = 2

    def construct(self):
        # Set up
        plane = NumberPlane((-4, 4), (-2, 2))
        plane.set_height(12)
        plane.background_lines.set_stroke(BLUE, 1, 0.5)
        plane.faded_lines.set_stroke(BLUE, 0.5, 0.25)
        unit_size = plane.x_axis.get_unit_size()

        circle = Circle(radius=unit_size)
        circle.set_stroke(GREY_C, 2)

        self.add(plane, circle)

        # Vectors
        v1, v2 = vects = Vector(unit_size * RIGHT, thickness=6).replicate(2)
        colors = [PINK, YELLOW]
        for vect, color, char in zip(vects, colors, "vw"):
            vect.set_fill(color)
            vect.label = Tex(R"\vec{\textbf{" + char + R"}}")
            vect.label.match_color(vect)
            vect.label.set_backstroke(BLACK, 5)
            vect.label.scale(2)
            vect.angle_tracker = ValueTracker(0)

        v1.angle_tracker.set_value(0.0)
        v2.angle_tracker.set_value(0.6)

        def update_vector(vector):
            vector.put_start_and_end_on(ORIGIN, circle.pfp(vector.angle_tracker.get_value() % 1))
            vector.label.move_to(vector.get_end() + 0.2 * vector.get_vector())

        v1.add_updater(update_vector)
        v2.add_updater(update_vector)

        self.add(v1, v2, v1.label, v2.label)

        self.play(v1.angle_tracker.animate.set_value(0.4), run_time=3)
        self.wait()

        # Show projection
        proj_group = always_redraw(lambda: self.get_projection_group(v1, v2))
        proj_group.suspend_updating()
        dashed_line, proj_line, proj_brace, label = proj_group

        self.play(LaggedStart(
            ShowCreation(dashed_line),
            FadeIn(proj_line),
            GrowFromCenter(proj_brace),
            AnimationGroup(
                TransformFromCopy(v1.label, label[0]),
                TransformFromCopy(v2.label, label[1]),
                Write(label[2])
            ),
            lag_ratio=0.5,
        ))
        self.wait()

        # Wander
        proj_group.resume_updating()
        self.add(proj_group)

        self.play(
            v1.angle_tracker.animate.set_value(0.2),
            run_time=3
        )
        self.wait()


        self.play(
            v2.angle_tracker.animate.set_value(0.25),
            run_time=3
        )
        self.wait()
        for value in [-0.23, 0.2]:
            self.play(
                v1.angle_tracker.animate.set_value(value),
                run_time=5
            )
            self.wait()

        # Randomness
        self.remove(proj_group)
        for n in range(50):
            v1.angle_tracker.set_value(random.random())
            v2.angle_tracker.set_value(random.random())
            self.wait(0.2)

    def get_projection_group(self, v1, v2):
        # Test
        dp = np.dot(v1.get_vector(), v2.get_vector()) / (v1.get_length() * v2.get_length())
        proj_line = Line(
            v2.get_start(),
            interpolate(v2.get_start(), v2.get_end(), dp)
        )
        proj_line.set_stroke(WHITE, 8)
        orientation = cross(v1.get_vector(), v2.get_vector())[2]
        proj_brace = LineBrace(
            proj_line,
            buff=SMALL_BUFF,
            # direction=UP if orientation > 0 else DOWN
            direction=UP if dp > 0 else DOWN
        )
        label = VGroup(v1.label, v2.label).copy()
        label.scale(0.5)
        label.arrange(RIGHT, buff=0.25)
        label.add(Tex(R"\cdot").move_to(label))
        angle = (proj_line.get_angle() + (PI if orientation > 0 else 0))
        angle = (angle + PI / 2) % PI - PI / 2
        label.rotate(angle)
        label.move_to(proj_brace.get_center() + 3 * (proj_brace.get_center() - proj_line.get_center()))

        dashed_line = DashedLine(v1.get_end(), proj_line.get_end())
        dashed_line.set_stroke(WHITE, 1)

        result = VGroup(dashed_line, proj_line, proj_brace, label)

        return result
