# ==============================================================================
# Scene:      IntersectingCircles
# Source:     videos/_2024/puzzles/added_dimension.py (lines 2994-3128)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl IntersectingCircles.py IntersectingCircles -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class IntersectingCircles(InteractiveScene):
    def construct(self):
        # Add circles
        circles = Circle(radius=2).replicate(4)
        circles.set_stroke(BLUE_B, 2)
        circles[3].set_stroke(YELLOW, 3)
        circles.tri_intersection = ORIGIN  # To change
        circles.pair_intersections = np.zeros((3, 3))  # To change

        vectors = [RIGHT, UL, DL]
        vector_trackers = VGroup(VectorizedPoint(vect) for vect in vectors)

        def update_circles(circles):
            self.place_circles_by_vectors(
                circles,
                [vt.get_center() for vt in vector_trackers]
            )

        circles.add_updater(update_circles)

        dots = GlowDots(circles.pair_intersections)
        dots.set_color(WHITE)
        dots.add_updater(lambda m: m.set_points(circles.pair_intersections))

        circles[3].set_opacity(0)
        self.play(LaggedStartMap(ShowCreation, circles, lag_ratio=0.7))
        self.play(FadeIn(dots))
        self.wait()
        circles[3].set_stroke(opacity=1)
        self.play(ShowCreation(circles[3]))
        self.add(circles)
        self.wait()

        self.play(
            vector_trackers[2].animate.move_to(LEFT + 0.5 * DOWN),
            run_time=2
        )
        self.wait()
        self.play(
            vector_trackers[0].animate.move_to(RIGHT + 0.5 * DOWN),
            run_time=2
        )
        self.wait()
        self.play(
            vector_trackers[0].animate.move_to(RIGHT),
            run_time=2
        )
        self.wait()
        self.play(circles[3].animate.set_opacity(0))
        self.wait()

        # Draw radial lines
        centers = Dot(radius=0.05).replicate(3)
        centers.set_color(WHITE)

        def update_centers(centers):
            for center, circle in zip(centers, circles):
                center.move_to(circle)

        centers.add_updater(update_centers)

        radial_lines = self.get_radial_lines(circles, [vt.get_center() for vt in vector_trackers])

        self.play(
            LaggedStartMap(FadeOut, circles[:3].copy(), lag_ratio=0.5, scale=0),
            FadeIn(centers, lag_ratio=0.5)
        )
        self.wait()
        self.play(ShowCreation(radial_lines[:3], lag_ratio=0.75))
        self.wait()
        for i in range(3, 8, 2):
            self.play(ShowCreation(radial_lines[i:i + 2], lag_ratio=0.5, run_time=1))
            self.wait()
        self.wait()
        self.play(
            LaggedStart(
                (FadeTransform(radial_lines[i1].copy(), radial_lines[i2])
                for i1, i2 in [(5, 9), (8, 10), (4, 11)]),
                lag_ratio=0.75,
                run_time=3
            ),
        )
        self.wait()

        # Animate about
        radial_lines.add_updater(lambda m: m.become(
            self.get_radial_lines(circles, [vt.get_center() for vt in vector_trackers])
        ))

        self.add(circles, centers, radial_lines)
        self.play(
            vector_trackers[1].animate.move_to(UP),
            run_time=3
        )
        self.play(
            vector_trackers[1].animate.move_to(UL),
            run_time=3
        )
        circles[3].set_stroke(opacity=1)
        self.play(ShowCreation(circles[3]))
        self.wait()

    def place_circles_by_vectors(self, circles, vectors):
        radius = circles[0].get_radius()
        radial_vectors = np.array([radius * normalize(vect) for vect in vectors])
        for circle, radial_vector in zip(circles, radial_vectors):
            circle.move_to(radial_vector)
        circles[3].move_to(sum(radial_vectors)),

        circles.tri_intersection = ORIGIN
        circles.pair_intersections = np.array([
            sum(pair) for pair in it.combinations(list(radial_vectors[:3]), 2)
        ])

        return circles

    def get_radial_lines(self, circles, vectors):
        radius = circles[0].get_radius()
        radial_vectors = np.array([radius * normalize(vect) for vect in vectors])

        result = VGroup()
        for vect in radial_vectors:
            result.add(Line(ORIGIN, vect))
        for v1 in radial_vectors:
            for v2 in radial_vectors:
                if np.all(v1 == v2):
                    continue
                result.add(Line(v1, v1 + v2))
        total_sum = sum(radial_vectors)
        for vect in radial_vectors:
            result.add(DashedLine(total_sum - vect, total_sum))

        result.set_stroke(WHITE, 2)
        result[-3:].set_stroke(RED, 2)
        return result
