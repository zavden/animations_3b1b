# ==============================================================================
# Scene:      TableOfContents
# Source:     videos/_2025/cosmic_distance/supplements.py (lines 117-203)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl TableOfContents.py TableOfContents -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class TableOfContents(InteractiveScene):
    def construct(self):
        items = VGroup(
            Text("Rung 1: Earth"),
            Text("Rung 2: Moon"),
            Text("Rung 3: Sun"),
            Text("Rung 4: Shapes of orbits"),
            Text("Rung 5: Distances to planets"),
            Text("Rung 6: Speed of light"),
            Text("Rung 7: Nearby stars"),
            Text("Rung 8: Milky way"),
            Text("Rung 9: Nearby Galaxies"),
            Text("Rung 10: Distant galaxies"),
        )
        items.arrange(DOWN, aligned_edge=LEFT, buff=0.5)
        items.set_height(FRAME_HEIGHT - 1)
        items.to_edge(LEFT)

        self.play(LaggedStartMap(FadeIn, items, shift=0.5 * LEFT, lag_ratio=0.1))
        self.wait()

        # Slow pan through
        items.save_state()
        highlight_points = Group()

        def update_item(item):
            y_diff = item.get_y() - item.highlight_point.get_y()
            alpha = np.exp(-(2 * y_diff)**2)
            item.set_height(interpolate(0.3, item.start_height, alpha), about_edge=LEFT)
            item.set_opacity(interpolate(0.5, 1, alpha))

        for item in items:
            item.start_height = item.get_height()
            item.highlight_point = Point(item.get_center())
            item.add_updater(update_item)

            highlight_points.add(item.highlight_point)

        self.play(
            *(item.highlight_point.animate.set_y(items[0].get_y()) for item in items),
            run_time=2
        )
        self.play(
            *(item.highlight_point.animate.set_y(-4) for item in items),
            run_time=20,
            rate_func=linear
        )
        self.play(
            *(item.highlight_point.animate.match_y(item) for item in items),
            run_time=2
        )
        self.wait()

        # Show the two parts
        brace1 = Brace(items[:4], RIGHT)
        brace2 = Brace(items[4:], RIGHT)

        self.play(
            GrowFromCenter(brace1),
            *(item.highlight_point.animate.shift(DOWN) for item in items[4:])
        )
        self.wait()
        self.play(
            *(item.highlight_point.animate.shift(DOWN) for item in items[:4]),
            *(item.highlight_point.animate.shift(UP) for item in items[4:]),
            ReplacementTransform(brace1, brace2),
        )
        self.wait()
        self.play(
            FadeOut(brace2),
            # *(item.highlight_point.animate.shift(DOWN) for item in items[4:]),
            # *(item.highlight_point.animate.shift(UP) for item in items[:1]),
        )
        # self.wait()
        items.clear_updaters()

        # One by one
        for n in range(len(items)):
            items.target = items.generate_target()
            for k, item in enumerate(items.target):
                if k == n:
                    item.set_height(0.45, about_edge=LEFT).set_opacity(1)
                else:
                    item.set_height(0.25, about_edge=LEFT).set_opacity(0.5)
            self.play(MoveToTarget(items))
            self.wait()
        self.wait(2)
