# ==============================================================================
# Scene:      ReflectOnGeneratingFunctions
# Source:     videos/_2022/puzzles/subsets.py (lines 3610-3735)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl ReflectOnGeneratingFunctions.py ReflectOnGeneratingFunctions -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - ParametricCurve(t_range=(a, b)) -> t_range=(a, b, 0.1): manimgl unpacks t_range into 3 values (functions.py:39) and no longer fills in the step
#   - background_line_style without stroke_color raises KeyError (coordinate_systems.py:668, it is no longer merged with the default): stroke_color=BLUE_D is added
# ==============================================================================

from manim_imports_ext import *

def get_subsets(full_set):
    return list(it.chain(*(
        it.combinations(full_set, k)
        for k in range(len(full_set) + 1)
    )))


class ReflectOnGeneratingFunctions(InteractiveScene):
    def construct(self):
        # Sequence
        subsets = get_subsets(list(range(1, 16)))
        seq = [
            sum(sum(s) == n for s in subsets)
            for n in range(1, 15)
        ]
        seq_mobs = VGroup(*map(Integer, seq))
        seq_mobs.scale(0.9)
        seq_mobs.add(Tex("\\cdots"))
        seq_mobs.arrange(RIGHT, aligned_edge=DOWN)
        seq_mobs.arrange_to_fit_width(FRAME_WIDTH - 1)
        seq_mobs.move_to(UP)

        brace = Brace(seq_mobs, UP)
        brace_label = Text("Sequence we want to understand")
        brace_label.next_to(brace, UP)

        self.play(
            Write(brace_label, run_time=1),
            GrowFromCenter(brace),
            ShowIncreasingSubsets(seq_mobs),
        )
        self.wait()

        # Put into a polynomial
        poly_str = " + ".join((
            f"{s} x^{{{n}}}"
            for n, s in enumerate(seq)
        ))
        poly_str += "+ \\cdots"
        poly = Tex(
            poly_str,
            tex_to_color_map={"x": BLUE, "+": WHITE},
        )
        poly.set_width(FRAME_WIDTH - 1)
        poly.next_to(seq_mobs, DOWN, buff=LARGE_BUFF)

        plus_indices = [-1, *(poly.submobjects.index(p[0]) for p in poly.select_parts("+"))]
        coefs = VGroup(*[
            poly[i + 1:i + 1 + len(str(n))]
            for i, n in zip(plus_indices, seq)
        ])
        self.play(
            LaggedStart(*(
                Transform(sm.copy(), coef.copy(), remover=True)
                for sm, coef in zip(seq_mobs, coefs)
            )),
            LaggedStart(*(
                FadeIn(sm, scale=3.0)
                for sm in poly
                if not set(sm.get_family()).intersection(coefs.get_family())
            )),
            run_time=2
        )
        self.add(poly)
        self.wait()

        # Make way
        self.play(
            poly.animate.to_edge(UP),
            FadeOut(VGroup(seq_mobs, brace, brace_label), 2.5 * UP),
        )

        # Evaluate on complex plane
        in_plane = ComplexPlane((-3, 3), (-3, 3))
        out_plane = ComplexPlane(
            (-10, 10), (-10, 10),
            # CHANGE: NumberPlane requires stroke_color in background_line_style (before it was merged with the default value BLUE_D)
            background_line_style=dict(stroke_color=BLUE_D, stroke_width=1),
            faded_line_ratio=0,
        )
        plane_labels = VGroup(Text("Input"), Text("Output"))
        for plane, vect, label in zip([in_plane, out_plane], [DL, DR], plane_labels):
            plane.add_coordinate_labels(font_size=20)
            plane.set_height(5)
            plane.to_corner(vect)
            label.scale(0.75)
            label.set_color(GREY_A)
            label.next_to(plane, UP)

        arrow = Arrow(in_plane.get_right(), out_plane.get_left(), path_arc=-45 * DEGREES)
        arrow.shift(UP)

        in_dot = GlowDot(in_plane.n2p(-1), color=YELLOW)
        out_dot = GlowDot(out_plane.n2p(0), color=RED)

        self.play(
            FadeIn(in_plane),
            Write(plane_labels[0]),
            FadeIn(in_dot),
        )
        self.play(
            ShowCreation(arrow),
            FadeTransform(in_plane.copy(), out_plane, path_arc=-30 * DEGREES),
            TransformFromCopy(*plane_labels, path_arc=30 * DEGREES),
            TransformFromCopy(in_dot, out_dot, path_arc=30 * DEGREES),
        )
        self.add(out_dot)

        # Paths
        def get_z():
            return in_plane.p2n(in_dot.get_center())

        def func(z):
            return np.prod([1 + z**n for n in range(10)])

        out_dot.add_updater(lambda od: od.move_to(out_plane.n2p(func(get_z()))))

        # CHANGE: ParametricCurve unpacks t_range into (min, max, step) and no longer completes a 2-value t_range; the default step 0.1 is added
        arc = ParametricCurve(lambda t: in_plane.n2p(np.exp(complex(0, PI - t))), t_range=(0, TAU, 0.1))
        # arc_image = ParametricCurve(lambda t: out_plane.n2p(func(np.exp(complex(0, PI - t)))), t_range=(0, TAU, 0.01))
        # arc.set_stroke(YELLOW, 2)
        # arc_image.set_stroke(RED, 1)


        paths = [
            TracingTail(in_dot, stroke_color=YELLOW, stroke_width=(0, 3), time_traced=16),
            TracingTail(out_dot, stroke_color=RED, stroke_width=(0, 1.5), time_traced=16),
        ]
        self.add(*paths)
        self.wait(16)
        self.play(
            MoveAlongPath(in_dot, arc.copy()),
            run_time=16,
            rate_func=linear,
        )
        self.wait(10)
