# ==============================================================================
# Scene:      IntegralError
# Source:     videos/_2022/visual_proofs/lies.py (lines 1789-1892)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl IntegralError.py IntegralError -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - VFadeInThenOut without buff=0 or color=RED (kwargs that used to be ignored and now give TypeError)
# ==============================================================================

from manim_imports_ext import *

class IntegralError(InteractiveScene):
    def construct(self):
        # (Coped from above)
        axes = Axes((-1, 4), (-1, 10), width=12, height=6)
        graph = axes.get_graph(lambda x: x**2)
        graph.set_stroke(TEAL, 2)
        all_rects = VGroup(*(
            axes.get_riemann_rectangles(graph, (0, 3), dx).set_stroke(BLACK, np.round(4 * dx, 1), behind=False)
            for dx in [2**(-n) for n in range(2, 9)]
        ))
        rects = all_rects[0]
        last_rects = all_rects[-1].copy()
        last_rects.set_stroke(width=0)

        self.add(axes, graph)
        self.add(rects)

        # Mention error
        error = last_rects.copy()
        error.set_fill(RED, 1)

        error_label = Text("Error", font_size=72, color=RED)
        error_label.move_to(rects, UP).shift(UP)
        error_arrows = VGroup(*(
            Arrow(error_label, rect.get_top() + 0.2 * UP, stroke_width=2, tip_width_ratio=8)
            for rect in rects
        ))
        error_arrows.set_color(RED)

        self.add(error, rects)
        self.play(
            FadeIn(error, lag_ratio=0.5, run_time=2),
            Write(error_label, stroke_color=RED),
            LaggedStart(*(
                ShowCreation(arrow)
                for arrow in error_arrows
            ), lag_ratio=0.2, run_time=3)
        )
        self.wait()

        # Error boxes
        all_error_boxes = VGroup()
        for rg in all_rects:
            boxes = VGroup()
            for rect in rg:
                box = Rectangle(stroke_width=0, fill_opacity=0.5, fill_color=RED)
                box.replace(Line(
                    axes.i2gp(axes.x_axis.p2n(rect.get_left()), graph),
                    axes.i2gp(axes.x_axis.p2n(rect.get_right()), graph),
                ), stretch=True)
                boxes.add(box)
            all_error_boxes.add(boxes)
        self.play(
            FadeIn(all_error_boxes[0], lag_ratio=0.1),
            error.animate.set_opacity(0.25),
            FadeOut(error_arrows),
        )
        for rg, ebg in zip(all_rects, all_error_boxes):
            for rect, box in zip(rg, ebg):
                rect.add(box)
        self.remove(all_error_boxes)
        self.add(rects)

        # Inequality
        error_label.generate_target()
        error_label.target.scale(0.7)
        sum_squares = Tex("< \\sum \\Delta", isolate="\\Delta")
        rhs = VGroup(OldTex("="), DecimalNumber(num_decimal_places=4))
        rhs.arrange(RIGHT)
        rhs[1].set_value(0.3417)

        group = VGroup(error_label.target, sum_squares, rhs)
        group.arrange(RIGHT)
        group.to_edge(UP)

        pre_box_sym = rects[-1].submobjects[0]
        box_sym = pre_box_sym.copy()
        box_sym.replace(sum_squares[2], dim_to_match=1)
        sum_squares.replace_submobject(2, box_sym)

        self.play(
            MoveToTarget(error_label),
            Write(sum_squares[:2]),
            TransformFromCopy(pre_box_sym, box_sym)
        )
        self.add(rhs)
        self.play(
            CountInFrom(rhs[1], 0),
            LaggedStart(*(
                # CHANGE: VFadeInThenOut does not accept buff and color (before they were silently ignored)
                VFadeInThenOut(r.copy().set_fill(opacity=1))
                for r in all_error_boxes[0]
            ), lag_ratio=0.2),
            run_time=2
        )
        self.wait()

        # Iterations
        for new_rects in all_rects[1:]:
            self.play(
                Transform(rects, new_rects),
                ChangeDecimalToValue(rhs[1], rhs[1].get_value() / 4),
                run_time=3,
            )
            self.wait(0.5)
