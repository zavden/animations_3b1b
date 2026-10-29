# ==============================================================================
# Scene:      MeanProductExample
# Source:     videos/_2021/quick_eigen.py (lines 1114-1313)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl MeanProductExample.py MeanProductExample -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

EIGEN_COLORS = [TEAL_A, TEAL_D]


MEAN_COLOR = BLUE_B


PROD_COLOR = BLUE_D


class MeanProductExample(Scene):
    def construct(self):
        # Number line and midpoint
        number_line = NumberLine((0, 14))
        number_line.add_numbers()
        number_line.set_width(FRAME_WIDTH - 1)
        number_line.to_edge(UP, buff=1.5)
        nl = number_line

        mean = 7
        m_dot = Dot(nl.n2p(mean))
        m_dot.set_color(MEAN_COLOR)
        m_label = OldTex("m", color=MEAN_COLOR)
        m_label.next_to(m_dot, UP, buff=MED_SMALL_BUFF)
        label7 = OldTex("7", color=MEAN_COLOR)

        # Distance tracking
        d_tracker = ValueTracker(4)

        def get_l1_point():
            return nl.n2p(mean - d_tracker.get_value())

        def get_l2_point():
            return nl.n2p(mean + d_tracker.get_value())

        l1_dot, l2_dot = (Dot(color=TEAL) for x in range(2))
        l1_label = OldTex("\\lambda_1", color=EIGEN_COLORS[0])
        l2_label = OldTex("\\lambda_2", color=EIGEN_COLORS[1])
        l1_arrow, l2_arrow = (Arrow(color=WHITE) for x in range(2))

        l1_dot.add_updater(lambda m: m.move_to(get_l1_point()))
        l2_dot.add_updater(lambda m: m.move_to(get_l2_point()))
        always(l1_label.next_to, l1_dot, UP, buff=MED_SMALL_BUFF)
        always(l2_label.next_to, l2_dot, UP, buff=MED_SMALL_BUFF)
        m_label.match_y(l1_label)
        l1_arrow.add_updater(lambda m: m.set_points_by_ends(
            m_label.get_left() + SMALL_BUFF * LEFT, l1_label.get_right() + SMALL_BUFF * RIGHT,
        ))
        l2_arrow.add_updater(lambda m: m.set_points_by_ends(
            m_label.get_right() + SMALL_BUFF * RIGHT, l2_label.get_left() + SMALL_BUFF * LEFT,
        ))

        minus_d = OldTex("-d")
        plus_d = OldTex("+d")
        always(minus_d.next_to, l1_arrow, UP, SMALL_BUFF)
        always(plus_d.next_to, l2_arrow, UP, SMALL_BUFF)
        plus_qm = OldTex("+??")
        minus_qm = OldTex("-??")
        always(plus_qm.move_to, plus_d)
        always(minus_qm.move_to, minus_d)

        VGroup(plus_d, minus_d).set_opacity(0)

        label7.move_to(m_label)
        self.add(number_line)
        self.add(m_dot)
        self.add(label7)
        self.add(l1_dot)
        self.add(l2_dot)
        self.add(l1_label)
        self.add(l2_label)
        self.add(l1_arrow)
        self.add(l2_arrow)
        self.add(minus_d)
        self.add(plus_d)
        self.add(minus_qm)
        self.add(plus_qm)

        d_tracker.add_updater(lambda m: m.set_value(4 - 2.5 * np.sin(0.25 * self.time)))
        self.add(d_tracker)
        self.wait(20)
        self.play(
            UpdateFromAlphaFunc(
                Mobject(),
                lambda m, a: VGroup(plus_d, minus_d).set_opacity(a),
                remover=True
            ),
            UpdateFromAlphaFunc(
                Mobject(),
                lambda m, a: VGroup(plus_qm, minus_qm).set_opacity(1 - a),
                remover=True
            ),
        )
        self.remove(plus_qm, minus_qm)
        self.wait(5)

        # Write the product
        kw = {"tex_to_color_map": {"\\,7": MEAN_COLOR, "d": GREY_A, "=": WHITE, "-": WHITE}}
        texs = VGroup(*(OldTex(tex, **kw) for tex in [
            "(\\,7 + d\\,)(\\,7 - d\\,)",
            "\\,7^2 - d^2 = ",
            "40 =",
            "d^2 = \\,7^2 - 40",
            "d^2 = 9",
            "d = 3",
        ]))
        texs[:3].arrange(LEFT)
        texs[1].align_to(texs[2], DOWN)
        texs[:3].next_to(nl, DOWN, MED_LARGE_BUFF).to_edge(LEFT, buff=LARGE_BUFF)
        for t1, t2 in zip(texs[2:], texs[3:]):
            t2.next_to(t1, DOWN, MED_LARGE_BUFF)
            t2.shift((t1.get_part_by_tex("=").get_x() - t2.get_part_by_tex("=").get_x()) * RIGHT)

        texs[0].save_state()
        texs[0].move_to(texs[1], UL)

        self.play(Write(VGroup(texs[2], texs[0])))
        self.wait(3)
        self.play(Restore(texs[0]))
        self.play(TransformMatchingShapes(texs[0].copy(), texs[1], path_arc=45 * DEGREES))
        self.wait(3)

        self.play(LaggedStart(
            TransformFromCopy(texs[2][0], texs[3][6], path_arc=-45 * DEGREES),
            TransformFromCopy(texs[2][1], texs[3][2]),
            TransformFromCopy(texs[1][:3], texs[3][3:6]),
            TransformFromCopy(texs[1][3:5], texs[3][0:2], path_arc=45 * DEGREES),
            lag_ratio=0.1
        ))
        self.wait(2)
        self.play(FadeIn(texs[4], DOWN))
        self.wait()
        self.play(FadeIn(texs[5], DOWN))

        # Show final d geometrically
        d_tracker.clear_updaters()
        self.play(d_tracker.animate.set_value(3), rate_func=rush_into)
        minus_d.clear_updaters()
        plus_d.clear_updaters()

        plus_3 = OldTex("+3").move_to(plus_d)
        minus_3 = OldTex("-3").move_to(minus_d)
        self.play(
            LaggedStart(
                FadeOut(minus_d, 0.25 * UP),
                FadeOut(plus_d, 0.25 * UP),
                lag_ratio=0.25
            ),
            LaggedStart(
                FadeIn(minus_3, 0.25 * UP),
                FadeIn(plus_3, 0.25 * UP),
                lag_ratio=0.25
            )
        )
        self.wait()

        # Highlight solutions
        rects = VGroup(
            SurroundingRectangle(VGroup(l1_label, nl.numbers[4])),
            SurroundingRectangle(VGroup(l2_label, nl.numbers[10])),
        )
        self.play(LaggedStartMap(ShowCreation, rects), lag_ratio=0.3)
        self.wait(2)
        self.play(LaggedStartMap(FadeOut, rects), lag_ratio=0.3)

        # Replace with general variables
        ms = VGroup(m_label.copy())
        sevens = VGroup(label7)
        ps = VGroup()
        fourties = VGroup()
        for tex in texs[:-2]:
            for fourty in tex.get_parts_by_tex("40"):
                fourties.add(fourty)
                ps.add(OldTex("p").set_color(PROD_COLOR).move_to(fourty).shift(0.1 * DOWN))
            for seven in tex.get_parts_by_tex("7"):
                sevens.add(seven)
                m = OldTex("m").set_color(MEAN_COLOR)
                m.scale(0.95)
                m.move_to(seven, DR)
                m.shift(0.04 * RIGHT)
                ms.add(m)
        ps[0].shift(0.05 * RIGHT)
        ps[1].shift(0.1 * LEFT)

        for g1, g2 in ((sevens, ms), (fourties, ps)):
            self.play(
                LaggedStartMap(FadeOut, g1, shift=0.25 * UP, lag_ratio=0.3),
                LaggedStartMap(FadeIn, g2, shift=0.25 * UP, lag_ratio=0.3),
                texs[-2:].animate.set_opacity(0)
            )
        self.remove(texs[-2:])
        self.wait()
        self.play(FlashUnder(texs[3]))
        self.wait()

        plus_form, minus_form = [
            OldTex(
                c + "\\sqrt{\\,m^2 - p}",
                tex_to_color_map={"m": MEAN_COLOR, "p": PROD_COLOR},
                font_size=24,
            ).move_to(d, DOWN)
            for c, d in [("+", plus_d), ("-", minus_d)]
        ]
        pre_group = VGroup(*texs[3][4:6], ms[-1], ps[-1])
        self.play(
            TransformMatchingShapes(pre_group.copy(), minus_form),
            TransformMatchingShapes(pre_group.copy(), plus_form),
            FadeOut(VGroup(minus_3, plus_3), shift=0.25 * UP),
        )
        self.wait()
