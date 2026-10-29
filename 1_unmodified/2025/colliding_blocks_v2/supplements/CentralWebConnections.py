# ==============================================================================
# Scene:      CentralWebConnections
# Source:     videos/_2025/colliding_blocks_v2/supplements.py (lines 1259-1293)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl CentralWebConnections.py CentralWebConnections -w -m --fps 15
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


class CentralWebConnections(WebOfConnections):
    n_iterations = 13
    n_neighbors = 10
    n_examples = 5

    def construct(self):
        # Test
        point_list = list(self.dots.get_points())
        dots = GlowDot(ORIGIN, radius=0.15).replicate(self.n_examples)

        for dot in dots:
            path = TracedPath(dot.get_center, stroke_width=1, stroke_color=WHITE)
            path.set_stroke(opacity=0.5)
            tail = TracingTail(dot, time_traced=2.0)
            self.add(dot, path, tail)

        dots.set_opacity(0)
        dots[0].set_opacity(1)
        self.wait()

        for n in range(self.n_iterations):
            for dot in dots:
                dot_center = dot.get_center()
                indices = np.argsort([get_norm(p - dot_center) for p in point_list])
                choice = np.random.randint(0, self.n_neighbors - 1)
                new_center = point_list[indices[choice]]
                point_list.pop(indices[choice])

                dot.target = dot.generate_target()
                dot.target.move_to(new_center)
                dot.target.set_opacity(1)
                if n > 0:
                    self.add(dot.copy().set_opacity(0.5))

            self.play(LaggedStartMap(MoveToTarget, dots), lag_ratio=0.5, run_time=3)
