# ==============================================================================
# Scene:      WaysToCombine
# Source:     videos/_2022/convolutions/discrete.py (lines 119-342)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl WaysToCombine.py WaysToCombine -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - list(array) -> array.tolist() in the OldTex of a, b, a+b...: numpy 2 prints np.int64(1) instead of 1
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

def get_aligned_pairs(group1, group2, n):
    return VGroup(*(
        VGroup(m1, m2)
        for m1 in group1
        for m2 in group2
        if m1.index + m2.index == n
    ))


def kinked_function(x):
    if x < -2:
        return 0
    elif x < -1:
        return -x - 2
    elif x < 1:
        return x
    elif x < 2:
        return -x + 2
    else:
        return 0


class WaysToCombine(InteractiveScene):
    def construct(self):
        # Functions
        v_line = Line(UP, DOWN).set_height(FRAME_HEIGHT)
        v_line.set_stroke(WHITE, 2)

        axes1, axes2, axes3 = all_axes = VGroup(*(
            Axes((-3, 3), (-1, 1), height=2.0, width=FRAME_WIDTH * 0.5 - 1)
            for x in range(3)
        ))
        all_axes.arrange(DOWN, buff=LARGE_BUFF)
        all_axes.set_height(FRAME_HEIGHT - 1)
        all_axes.move_to(midpoint(ORIGIN, RIGHT_SIDE))

        def f(x):
            return kinked_function(x)

        def g(x):
            return np.exp(-0.5 * x**2)

        f_graph = axes1.get_graph(f).set_stroke(BLUE, 2)
        g_graph = axes2.get_graph(g).set_stroke(YELLOW, 2)
        sum_graph = axes3.get_graph(lambda x: f(x) + g(x)).set_stroke(TEAL, 2)
        prod_graph = axes3.get_graph(lambda x: f(x) * g(x)).set_stroke(TEAL, 2)
        x_samples = np.linspace(*axes1.x_range[:2], 100)
        f_samples = list(map(f, x_samples))
        g_samples = list(map(g, x_samples))
        conv_samples = np.convolve(f_samples, g_samples, mode='same')
        conv_samples *= 0.1  # Artificially scale down
        conv_points = axes3.c2p(x_samples, conv_samples)
        conv_graph = VMobject().set_points_smoothly(conv_points)
        conv_graph.set_stroke(TEAL, 2)

        kw = dict(font_size=30, tex_to_color_map={"f": BLUE, "g": YELLOW})
        f_label = Tex("f(x)", **kw).move_to(axes1.get_corner(UL), UL)
        g_label = Tex("g(x)", **kw).move_to(axes2.get_corner(UL), UL)
        sum_label = Tex("[f + g](x)", **kw).move_to(axes3.get_corner(UL), UL)
        prod_label = Tex(R"[f \cdot g](x)", **kw).move_to(axes3.get_corner(UL), UL)
        conv_label = Tex(R"[f * g](x)", **kw).move_to(axes3.get_corner(UL), UL)
        graph_labels = VGroup(f_label, g_label, sum_label, prod_label, conv_label)

        # Sequences
        seq1 = np.array([1, 2, 3, 4])
        seq2 = np.array([5, 6, 7, 8])
        kw = dict(
            font_size=48,
            tex_to_color_map={"a": BLUE, "b": YELLOW},
            isolate=[",", "[", "]"]
        )
        seq1_tex, seq2_tex, sum_seq, prod_seq, conv_seq = seqs = VGroup(
            # CHANGE: numpy 2 displays np.int64(1) in list(array); .tolist() gives Python integers
            OldTex(f"a = {seq1.tolist()}", **kw),
            OldTex(f"b = {seq2.tolist()}", **kw),
            OldTex(f"a + b = {(seq1 + seq2).tolist()}", **kw),
            OldTex(Rf"a \cdot b = {(seq1 * seq2).tolist()}", **kw),
            OldTex(Rf"a * b = {np.convolve(seq1, seq2).tolist()}", **kw),
        )
        seqs.move_to(midpoint(ORIGIN, LEFT_SIDE))
        seq1_tex.match_y(axes1)
        seq2_tex.match_y(axes2)
        for seq in seqs[2:]:
            seq.match_y(axes3)

        # Operation labels
        op_labels = VGroup()
        left_op_labels = VGroup(*map(Text, ["Addition", "Multiplication", "Convolution"]))
        left_op_labels.set_color(TEAL)
        for left_op_label, seq, graph_label in zip(left_op_labels, seqs[2:], graph_labels[2:]):
            left_op_label.next_to(seq, UP, MED_LARGE_BUFF, aligned_edge=LEFT)
            right_op_label = left_op_label.copy().scale(0.7)
            right_op_label.next_to(graph_label, UP, aligned_edge=LEFT)
            op_labels.add(VGroup(left_op_label, right_op_label))

        # Introduce
        kw = dict(lag_ratio=0.7)
        self.play(
            LaggedStartMap(Write, seqs[:2], **kw),
            run_time=2,
        )
        self.play(
            FadeIn(v_line),
            LaggedStartMap(FadeIn, all_axes[:2], **kw),
            LaggedStartMap(ShowCreation, VGroup(f_graph, g_graph), **kw),
            LaggedStartMap(FadeIn, graph_labels[:2], **kw),
            run_time=2
        )
        self.wait()

        # Ways to combine?
        all_boxes = VGroup(*(SurroundingRectangle(m[2:]) for m in seqs[:3]))
        all_boxes.set_stroke(width=2)
        boxes = all_boxes[:2]
        boxes[0].set_color(BLUE)
        boxes[1].set_color(YELLOW)
        mystery_box = all_boxes[2]
        mystery_box.set_color(GREEN)
        q_marks = Text("????")
        q_marks.space_out_submobjects(1.5)
        q_marks.move_to(mystery_box)
        box_arrows = VGroup(*(
            Arrow(box.get_right(), mystery_box.get_corner(UR), path_arc=-PI / 3)
            for box in boxes
        ))

        self.play(
            *map(Write, box_arrows),
            FadeIn(boxes),
            *(
                Transform(
                    box.copy().set_stroke(width=0, opacity=0),
                    mystery_box.copy(),
                    path_arc=-PI / 3,
                    remover=True
                )
                for box in boxes
            )
        )
        self.add(mystery_box)
        comb_graph = sum_graph.copy()
        self.play(
            Write(q_marks),
            ReplacementTransform(axes1.copy(), axes3),
            Transform(axes2.copy(), axes3.copy(), remover=True),
            ReplacementTransform(f_graph.copy(), comb_graph),
            Transform(g_graph.copy(), comb_graph.copy(), remover=True),
        )
        self.play(Transform(comb_graph, prod_graph))
        self.play(Transform(comb_graph, conv_graph))
        self.play(LaggedStartMap(FadeOut, VGroup(
            *boxes, *box_arrows, mystery_box, q_marks, comb_graph
        )))

        # Sums and products
        tuples = [
            (sum_seq, sum_label, axes3, sum_graph, op_labels[0]),
            (prod_seq, prod_label, axes3, prod_graph, op_labels[1])
        ]
        for seq, label, axes, graph, op_label in tuples:
            self.play(LaggedStart(
                TransformMatchingShapes(
                    VGroup(*seq1_tex[:2], *seq2_tex[:2]).copy(),
                    seq[:4]
                ),
                TransformMatchingShapes(graph_labels[:2].copy(), label),
                FadeIn(op_label, DOWN)
            ))
            self.add(axes)
            # Go point by point
            value_rects = VGroup(*(
                VGroup(*map(SurroundingRectangle, s[-8::2]))
                for s in [seq1_tex, seq2_tex, seq]
            ))
            dots = Group(*(GlowDot(color=WHITE) for x in range(3)))
            self.play(
                *map(FadeIn, [seq[4], seq[-1]]),
                *(
                    VFadeInThenOut(rects, lag_ratio=0.5)
                    for rects in value_rects
                ),
                LaggedStart(*(
                    FadeIn(seq[n:n + 2 if n < 11 else n + 1])
                    for n in range(5, 12, 2)
                ), lag_ratio=0.5),
                run_time=2
            )
            self.play(
                ShowCreation(graph, rate_func=linear),
                UpdateFromFunc(dots[2], lambda m: m.move_to(graph.get_end())),
                *(
                    UpdateFromAlphaFunc(dot, lambda d, a: d.set_opacity(min(10 * a * (1 - a), 1)))
                    for dot in dots
                ),
                *(
                    MoveAlongPath(dot, graph)
                    for dot, graph in zip(dots, [f_graph, g_graph])
                ),
                run_time=4
            )
            self.wait()
            self.play(*map(FadeOut, [seq, label, graph, op_label]))

        # Convolutions
        self.play(LaggedStart(
            TransformMatchingShapes(
                VGroup(*seq1_tex[:2], *seq2_tex[:2]).copy(),
                conv_seq[:4],
            ),
            FadeIn(op_labels[2][0], DOWN),
            TransformMatchingShapes(graph_labels[:2].copy(), conv_label),
            FadeIn(op_labels[2][1], DOWN),
        ))
        self.play(FadeIn(conv_seq[4:], lag_ratio=0.2, run_time=2))

        # Hint at computation
        nums1 = seq1_tex[3::2]
        nums2 = seq2_tex[3::2]
        for mobs in nums1, nums2:
            for i, mob in enumerate(mobs):
                mob.index = i
        nums3 = conv_seq[5::2]

        nums1.set_color(BLUE)
        nums2.set_color(YELLOW)

        last_group = VGroup()
        for n, num3 in enumerate(nums3):
            rect = SurroundingRectangle(num3, buff=SMALL_BUFF)
            rect.set_stroke(TEAL, 2)
            rect.round_corners()
            pairs = get_aligned_pairs(nums1, nums2, n)
            lines = VGroup(*(Line(m1, m2) for m1, m2 in pairs))
            lines.set_stroke(TEAL, 2)

            group = VGroup(rect, lines)
            self.play(FadeIn(group), FadeOut(last_group), run_time=0.25)
            self.wait(0.25)
            last_group = group
        self.play(FadeOut(last_group, run_time=0.5))
        self.wait()

        # Conv graph
        self.play(ShowCreation(conv_graph, run_time=3))
        self.wait()
        self.play(MoveAlongPath(GlowDot(color=WHITE), conv_graph, run_time=5, remover=True))
        self.wait()
