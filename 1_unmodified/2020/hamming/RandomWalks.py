# ==============================================================================
# Scene:      RandomWalks
# Source:     videos/_2020/hamming.py (lines 6161-6268)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl RandomWalks.py RandomWalks -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class RandomWalks(Scene):
    CONFIG = {
        "random_seed": 1,
    }

    def construct(self):
        # Setup
        N_PATHS = 25
        frame = self.camera.frame
        frame.set_height(2 * FRAME_HEIGHT)
        frame.shift(2 * RIGHT)

        idea_spot = 10 * RIGHT + 3 * UP
        idea_dot = Dot(idea_spot)
        idea_dot.set_color(YELLOW)
        bulb = Lightbulb()
        bulb.next_to(idea_dot, UP)

        start_point = 7 * LEFT + 3 * DOWN
        start_dot = Dot(start_point, color=WHITE)
        start_dot.scale(2)

        self.add(idea_dot, bulb, start_dot)

        # Paths
        paths = VGroup(*[VGroup() for n in range(N_PATHS)])
        for path in paths:
            path.add(Line(start_point, start_point))
            path.set_stroke(WHITE, 3, 0.5)

        path_dots = VGroup()
        for path in paths:
            # dot = Randolph(
            #     mode="thinking", height=0.25,
            #     # color=random.choice([BLUE_B, BLUE_C, BLUE_D, GREY_BROWN])
            # )
            dot = Dot(color=BLUE)
            dot.set_stroke(BLACK, 3, background=True)
            dot.path = path
            dot.add_updater(lambda m: m.move_to(m.path[-1].get_end()))
            path_dots.add(dot)

        self.add(paths)
        self.add(path_dots)

        # Perform search
        magic_path = None
        while magic_path is None:
            new_segments = VGroup()
            for path in paths:
                start = path[-1].get_end()

                # Choose random direction based on loosely sniffing out idea spot
                R_vect = start - idea_spot
                R_vect = rotate_vector(10 * R_vect, TAU * random.random())
                point = idea_spot + R_vect
                to_point = point - start
                angle = angle_of_vector(to_point)
                if -3 * PI / 2 < angle <= -PI / 2:
                    vect = DOWN
                elif -PI / 2 < angle <= PI / 2:
                    vect = RIGHT
                elif PI / 2 < angle <= 3 * PI / 2:
                    vect = UP
                else:
                    vect = LEFT

                end = start + vect
                new_segment = Line(start, end)
                new_segment.match_style(path)

                new_segments.add(new_segment)
                path.add(new_segment)

                if np.isclose(end, idea_spot).all():
                    magic_path = path.copy()
            self.play(
                LaggedStartMap(ShowCreation, new_segments, lag_ratio=10 / N_PATHS),
                run_time=0.5,
            )
            self.add(paths)

        # Highlight magic path
        magic_path.set_stroke(YELLOW, 5, 1)
        self.play(
            paths.fade, 0.7,
            ShowCreation(magic_path, run_time=2),
        )
        self.wait()

        fake_path = VMobject()
        fake_path.start_new_path(start_point)
        for segment in magic_path:
            fake_path.add_line_to(segment.get_end())
        fake_path.match_style(magic_path)

        line = Line(start_point, idea_spot)
        line.match_style(magic_path)
        line.set_stroke(TEAL, 8)

        self.add(fake_path, start_dot)
        self.play(
            ApplyMethod(magic_path.set_opacity, 0.5),
            Transform(fake_path, line, run_time=2),
            paths.fade, 0.5,
            path_dots.fade, 0.5,
        )
        self.wait(4)
