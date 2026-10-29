# ==============================================================================
# Scene:      SeparateFractals
# Source:     videos/_2017/fractal_dimension.py (lines 1552-1575)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl SeparateFractals.py SeparateFractals -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Python 2 integer division in slice
#   - Cairo ran construct() inside Scene.__init__; use cairo_nested_scene to build the other scene
# ==============================================================================

from manim_imports_ext import *

def break_up(mobject, factor = 1.3):
    mobject.scale(factor)
    for submob in mobject:
        submob.scale(1./factor)
    return mobject


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


class SeparateFractals(Scene):
    def construct(self):
        # CHANGE: Cairo ran construct() inside Scene.__init__; use cairo_nested_scene to build the other scene
        last_sc = cairo_nested_scene(ShowSeveralSelfSimilarityDimensions, skip_animations = True)
        self.add(*last_sc.get_mobjects())
        quad_koch = last_sc.curves[1]
        length = len(quad_koch)
        new_quad_koch = VGroup(*[
            # CHANGE: Python 2 integer division in slice
            VGroup(*quad_koch[i*length//8:(i+1)*length//8])
            for i in range(8)
        ])
        curves = list(last_sc.curves)
        curves[1] = new_quad_koch
        curves = VGroup(*curves)
        curves.save_state()
        self.play(*[
            ApplyFunction(
                lambda m : break_up(m, 2),
                curve
            )
            for curve in curves
        ])
        self.wait(2)
        self.play(curves.restore)
        self.wait()
