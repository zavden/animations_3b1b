# ==============================================================================
# Scene:      IntegralExampleWithErrorBoxes
# Source:     videos/_2022/visual_proofs/lies.py (lines 1895-1896)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl IntegralExampleWithErrorBoxes.py IntegralExampleWithErrorBoxes -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class IntegralExample(InteractiveScene):
    def construct(self):
        # Setup
        axes = Axes((-1, 4), (-1, 10), width=12, height=6)
        graph = axes.get_graph(lambda x: x**2)
        graph.set_stroke(TEAL, 2)
        all_rects = VGroup(*(
            axes.get_riemann_rectangles(graph, (0, 3), dx).set_stroke(BLACK, np.round(4 * dx, 1), behind=False)
            for dx in [2**(-n) for n in range(2, 8)]
        ))
        rects = all_rects[0]
        last_rects = all_rects[-1].copy()
        last_rects.set_stroke(width=0)

        self.add(axes)
        self.play(ShowCreation(graph))
        self.play(FadeIn(last_rects, lag_ratio=0.1))
        self.wait()
        self.play(FadeIn(rects, lag_ratio=0.1), FadeOut(last_rects))
        self.wait()
        self.play(LaggedStart(*(
            ApplyMethod(rect.set_color, YELLOW, rate_func=there_and_back)
            for rect in rects
        ), lag_ratio=0.5, run_time=4))

        # Iterations
        for new_rects in all_rects[1:]:
            self.play(Transform(rects, new_rects))
            self.wait(0.5)

        # Zoom
        frame = self.camera.frame

        self.play(frame.animate.move_to(graph.pfp(0.5)).set_height(0.1), run_time=3)
        self.wait()
        self.play(frame.animate.to_default_state(), run_time=3)
        self.wait()


class IntegralExampleWithErrorBoxes(IntegralExample):
    show_error_boxes = True
