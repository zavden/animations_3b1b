# ==============================================================================
# Scene:      ShowSimpleWeb
# Source:     videos/_2025/colliding_blocks_v2/supplements.py (lines 1296-1317)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ShowSimpleWeb.py ShowSimpleWeb -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class WebOfConnections(InteractiveScene):
    n_points = 1000

    def setup(self):
        super().setup()

        # Points
        points = np.random.uniform(-1, 1, (self.n_points, 3))

        curr_norms = np.linalg.norm(points, axis=1)
        target_norms = curr_norms**1.5
        points *= (target_norms / curr_norms)[:, np.newaxis]

        points = points[curr_norms < 1]
        points = np.vstack([[ORIGIN], points])  # Ensure origin is in there
        points *= 25

        dots = DotCloud(points)
        dots.stretch(0.2, 2, about_point=ORIGIN)
        dots.set_radius(0.02)
        self.dots = dots

        # Web of connections
        web = VGroup()
        for p1, p2 in it.combinations(dots.get_points(), 2):
            if random.random() < np.exp(-0.8 * get_norm(p1 - p2)):
                line = Line(p1, p2, stroke_color=WHITE, stroke_width=1, stroke_opacity=random.random())
                web.add(line)
        self.web = web

        # Zoom out over connections
        self.frame.add_updater(lambda m: m.set_height(2 + 0.5 * self.time))
        self.frame.add_updater(lambda m, dt: m.increment_theta(0.5 * dt * DEG))
        self.frame.add_updater(lambda m, dt: m.increment_phi(dt * DEG))


class ShowSimpleWeb(WebOfConnections):
    def construct(self):
        # Test
        self.web.sort(lambda p: get_norm(p))

        self.add(self.dots, self.web)
        self.wait(30)

        # Dense web
        dense_web = VGroup()
        for p1, p2 in it.combinations(self.dots.get_points(), 2):
            if random.random() < np.exp(-0.2 * get_norm(p1 - p2)):
                line = Line(
                    p1,
                    p2,
                    stroke_color=WHITE,
                    stroke_width=0.5,
                    stroke_opacity=random.random()**10
                )
                dense_web.add(line)
        self.play(ShowCreation(dense_web, lag_ratio=1 / len(dense_web), run_time=5))
        self.wait(5)
