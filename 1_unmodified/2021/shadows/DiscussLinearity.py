# ==============================================================================
# Scene:      DiscussLinearity
# Source:     videos/_2021/shadows.py (lines 1595-1794)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl DiscussLinearity.py DiscussLinearity -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class DiscussLinearity(Scene):
    def construct(self):
        # Set background
        background = FullScreenRectangle()
        self.add(background)
        panels = Rectangle(4, 4).replicate(3)
        panels.set_fill(BLACK, 1)
        panels.set_stroke(WHITE, 2)
        panels.set_height(FRAME_HEIGHT - 1)
        panels.arrange(RIGHT, buff=LARGE_BUFF)
        panels.set_width(FRAME_WIDTH - 1)
        panels.center()
        self.add(panels)

        # Arrows
        arrows = VGroup(*(
            Arrow(
                p1.get_top(), p2.get_top(), path_arc=-0.6 * PI
            ).scale(0.75, about_edge=DOWN)
            for p1, p2 in zip(panels, panels[1:])
        ))
        arrows.space_out_submobjects(0.8)
        arrows.rotate(PI, RIGHT, about_point=panels.get_center())
        arrow_labels = VGroup(
            Text("Rotation", font_size=30),
            Text("Flat projection", font_size=30),
        )
        arrow_labels.set_backstroke()
        for arrow, label in zip(arrows, arrow_labels):
            label.next_to(arrow.pfp(0.5), UP, buff=0.35)

        shape_labels = VGroup(
            Text("Some shape"),
            Text("Any shape"),
        )
        shape_labels.next_to(panels[0].get_top(), UP, SMALL_BUFF)

        # self.play(Write(shape_labels[0], run_time=1))
        # self.wait()

        for arrow, label in zip(arrows, arrow_labels):
            self.play(
                ShowCreation(arrow),
                FadeIn(label, lag_ratio=0.1)
            )
            self.wait()

        # Linear!
        lin_text = Text(
            "Both are linear transformations!",
            t2c={"linear": YELLOW}
        )
        lin_text.next_to(panels, UP, MED_SMALL_BUFF)

        self.play(FadeIn(lin_text, lag_ratio=0.1))
        self.wait()

        # Stretch words
        uniform_words = Text("Uniform stretching here", font_size=36).replicate(2)
        for words, panel in zip(uniform_words, panels[0::2]):
            words.next_to(panel.get_top(), DOWN, SMALL_BUFF)
            words.set_color(YELLOW)
            words.set_backstroke()
            self.play(
                FadeIn(words, lag_ratio=0.1),
            )
            self.wait()

        # Transition
        lin_part = lin_text.get_part_by_text("linear")
        lin_copies = lin_part.copy().replicate(2)
        lin_copies.scale(0.6)
        for lin_copy, arrow in zip(lin_copies, arrows):
            lin_copy.next_to(arrow.pfp(0.5), DOWN, buff=0.15)

        self.play(
            TransformFromCopy(lin_part.replicate(2), lin_copies),
            LaggedStart(
                FadeOut(lin_text, lag_ratio=0.1),
                *map(FadeOut, uniform_words)
            )
        )

        # Areas
        area_labels = VGroup(
            Text("Area(shape)", t2c={"shape": BLUE}),
            Text("Area(shadow)", t2c={"shadow": BLUE_E}),
        )
        area_exprs = VGroup(
            OldTex("A").set_color(BLUE),
            OldTex("(\\text{some factor})", "\\cdot ", "A"),
        )
        area_exprs[1][2].set_color(BLUE)
        area_exprs[1][0].set_color(GREY_C)
        equals = VGroup()
        for label, expr, panel in zip(area_labels, area_exprs, panels[0::2]):
            label.match_x(panel)
            label.to_edge(UP, buff=MED_SMALL_BUFF)
            eq = OldTex("=")
            eq.rotate(PI / 2)
            eq.next_to(label, DOWN, buff=0.15)
            equals.add(eq)
            expr.next_to(eq, DOWN, buff=0.15)

        self.play(
            *map(Write, area_labels),
            run_time=1
        )
        self.play(
            *(FadeIn(eq, 0.5 * DOWN) for eq in equals),
            *(FadeIn(expr, DOWN) for expr in area_exprs),
        )
        self.wait()

        f_rot = OldTex("f(\\text{Rot})")
        f_rot.set_color(GREY_B)
        times_A = area_exprs[1][1:]
        f_rot.next_to(times_A, LEFT, buff=0.2)
        times_A.generate_target()
        VGroup(f_rot, times_A.target).match_x(panels[2])

        self.play(
            FadeTransform(area_exprs[1][0], f_rot),
            MoveToTarget(times_A)
        )
        self.play(ShowCreationThenFadeAround(f_rot, run_time=2))
        self.wait(1)

        # Determinant
        factor = area_exprs[1].get_part_by_tex('factor')
        rect = SurroundingRectangle(factor, buff=SMALL_BUFF)
        rect.set_stroke(YELLOW, 2)

        rot = Matrix([["v_1", "w_1"], ["v_2", "w_2"], ["v_3", "w_3"]], h_buff=1.0)
        rot.set_column_colors(GREEN, RED)
        proj = Matrix([["1", "0", "0"], ["0", "1", "0"]], h_buff=0.6)
        prod = VGroup(proj, rot)
        prod.arrange(RIGHT, buff=SMALL_BUFF)
        prod.set_height(0.8)
        det = OldTex(
            "\\text{det}", "\\Big(", "\\Big)",
            tex_to_color_map={
                "\\text{det}": YELLOW,
                # "rot": BLUE_D,
                # "proj": BLUE_B,
            },
            font_size=36
        )
        det[1:].match_height(prod, stretch=True)
        det.to_edge(UP)
        prod.next_to(det[1], RIGHT, SMALL_BUFF)
        det[2].next_to(prod, RIGHT, SMALL_BUFF)
        det.add(prod)
        det.center().to_edge(UP, buff=0.25)
        det_rect = SurroundingRectangle(det, buff=SMALL_BUFF)
        det_rect.set_stroke(YELLOW, 1)

        rot_brace = Brace(rot, DOWN, buff=SMALL_BUFF)
        details = Text("Need to work out rotation matrix...", font_size=20)
        details.next_to(rot_brace, DOWN, SMALL_BUFF)
        details.set_color(GREY_A)

        arrow = Arrow(rect.get_corner(UL), det.get_right())
        arrow.set_color(YELLOW)

        self.play(ShowCreation(rect))
        self.play(
            FadeTransform(rect.copy(), det_rect),
            FadeTransform(factor.copy(), det),
            ShowCreation(arrow)
        )
        self.wait()
        self.play(
            FadeOut(det_rect),
            GrowFromCenter(rot_brace),
            FadeIn(details),
        )
        self.wait()
        self.play(LaggedStart(*map(FadeOut, (
            *det, rot_brace, details
        )), lag_ratio=0.3, run_time=2))

        # Any shape
        ind_words = Text("Independent of the shape!", font_size=30)
        ind_words.move_to(det)
        ind_words.set_color(GREEN)

        self.play(
            arrow.animate.match_points(Arrow(factor.get_corner(UL), ind_words.get_corner(DR))),
            Write(ind_words, run_time=1),
        )
        self.wait()
        self.play(LaggedStart(*map(FadeOut, (ind_words, arrow, rect))))
        self.wait()

        # Cross out right
        cross = Cross(VGroup(equals[1], f_rot, times_A))
        cross.insert_n_curves(20)
        self.play(ShowCreation(cross))
        self.wait(3)
