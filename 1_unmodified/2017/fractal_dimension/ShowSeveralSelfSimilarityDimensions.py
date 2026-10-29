# ==============================================================================
# Scene:      ShowSeveralSelfSimilarityDimensions
# Source:     videos/_2017/fractal_dimension.py (lines 1493-1550)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ShowSeveralSelfSimilarityDimensions.py ShowSeveralSelfSimilarityDimensions -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ShowSeveralSelfSimilarityDimensions(Scene):
    def construct(self):
        vects = [
            4*LEFT,
            ORIGIN,
            4*RIGHT,
        ]
        fractal_classes = [
            PentagonalFractal,
            QuadraticKoch,
            DiamondFractal,
        ]
        max_orders = [
            4,
            4,
            5,
        ]
        dimensions = [
            1.668,
            1.500,
            1.843,
        ]

        title = OldTexText("``Self-similarity dimension''")
        title.to_edge(UP)
        title.set_color(YELLOW)
        self.add(title)


        def get_curves(order):
            curves = VGroup()
            for Class, vect in zip(fractal_classes, vects):
                curve = Class(order = order)
                curve.set_width(2),
                curve.shift(vect)
                curves.add(curve)
            return curves
        curves = get_curves(1)
        self.add(curves)

        for curve, dimension, u in zip(curves, dimensions, [1, -1, 1]):
            label = OldTexText("%.3f-dimensional"%dimension)
            label.scale(0.85)
            label.next_to(curve, u*UP, buff = LARGE_BUFF)
            self.add(label)

        self.wait()

        for order in  range(2, max(max_orders)+1):
            anims = []
            for curve, max_order in zip(curves, max_orders):
                if order <= max_order:
                    new_curve = curve.__class__(order = order)
                    new_curve.replace(curve)
                    anims.append(Transform(curve, new_curve))
            self.play(*anims, run_time = 2)
        self.wait()
        self.curves = curves
