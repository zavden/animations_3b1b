# ==============================================================================
# Scene:      IntroduceEulersFormula
# Source:     videos/_2025/laplace/exponentials.py (lines 27-231)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl IntroduceEulersFormula.py IntroduceEulersFormula -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - The 8 YouTube thumbnails (downloaded at run time, from other channels) are replaced with local color cards with generic titles (yt_card_<id>.png)
#
# Placeholder assets (not Grant's originals):
#   - raster_images/yt_card_<id>.png with generic titles (_lib/assets/generated/replacements/visual/make_video_cards.py)
# ==============================================================================

from manim_imports_ext import *

class IntroduceEulersFormula(InteractiveScene):
    def construct(self):
        # Add plane
        plane = ComplexPlane(
            (-2, 2), (-2, 2),
            width=6, height=6,
        )
        plane.background_lines.set_stroke(BLUE, 1)
        plane.faded_lines.set_stroke(BLUE, 0.5, 0.5)
        plane.to_edge(LEFT)

        plane.add_coordinate_labels([1, -1])
        i_labels = VGroup(
            Tex(R"i", font_size=36).next_to(plane.n2p(1j), UL, SMALL_BUFF),
            Tex(R"-i", font_size=36).next_to(plane.n2p(-1j), DL, SMALL_BUFF),
        )
        plane.add(i_labels)

        self.add(plane)

        # Show pi
        pi_color = RED
        arc = Arc(0, PI, radius=plane.x_axis.get_unit_size(), arc_center=plane.n2p(0))
        arc.set_stroke(pi_color, 5)
        t_tracker = ValueTracker(0)
        t_dec = DecimalNumber(0)
        t_dec.set_color(pi_color)
        t_dec.add_updater(lambda m: m.set_value(t_tracker.get_value()))
        t_dec.add_updater(lambda m: m.move_to(plane.n2p(1.3 * np.exp(0.9 * t_tracker.get_value() * 1j))))

        pi = Tex(R"\pi", font_size=72)
        pi.set_color(pi_color)
        pi.set_backstroke(BLACK, 3)

        self.play(
            ShowCreation(arc),
            t_tracker.animate.set_value(PI),
            VFadeIn(t_dec, time_span=(0, 1)),
            run_time=2
        )
        pi.move_to(t_dec, DR)
        self.play(
            FadeOut(t_dec),
            FadeIn(pi),
            run_time=0.5
        )

        # Write formula
        formula = Tex(R"e^{\pi i} = -1", font_size=90, t2c={R"\pi": RED, "i": BLUE})
        formula.set_x(FRAME_WIDTH / 4).to_edge(UP)
        cliche = Text("Cliché?", font_size=72)
        cliche.next_to(formula, DOWN, LARGE_BUFF)

        randy = Randolph(height=2)
        randy.next_to(plane, RIGHT, LARGE_BUFF, aligned_edge=DOWN)
        randy.body.set_backstroke(BLACK)

        self.play(LaggedStart(
            TransformFromCopy(pi, formula[R"\pi"][0]),
            FadeTransform(i_labels[0].copy(), formula["i"][0]),
            Write(formula["="][0]),
            TransformFromCopy(plane.coordinate_labels[1], formula["-1"][0]),
            Write(formula["e"][0]),
            lag_ratio=0.2,
            run_time=3
        ))
        self.wait()

        self.play(
            LaggedStart(
                *(
                    # TransformFromCopy(formula[c1][0], cliche[c2][0])
                    FadeTransform(formula[c1][0].copy(), cliche[c2][0])
                    for c1, c2 in zip(
                        ["e", "1", "i", "e", R"\pi", "e", "1"],
                        "Cliché?",
                    )
                ),
                lag_ratio=0.1,
                run_time=3
            ),
            VFadeIn(randy),
            randy.says("This again?", mode="sassy", bubble_direction=LEFT)
        )
        self.play(Blink(randy))
        self.add(cliche)

        # Show many thumbnails
        plane_group = VGroup(plane, arc, pi)
        plane_group.set_z_index(-1)
        thumbnails = Group(
            # CHANGE: the YouTube thumbnail was downloaded at run time; now it is a local color card with the title (raster_images/yt_card_<id>.png, make_video_cards.py)
            Group(ImageMobject(f"yt_card_{slug}"))
            for slug in [
                "-dhHrg-KbJ0",  # Mathologer
                "f8CXG7dS-D0",  # Welch Labs
                "ZxYOEwM6Wbk",  # 3b1b
                "LE2uwd9V5vw",  # Khan Academy
                "CRj-sbi2i2I",  # Numberphile
                "v0YEaeIClKY",  # Other 3b1b
                "sKtloBAuP74",
                "IUTGFQpKaPU",  # Po shen lo
            ]
        )
        thumbnails.set_width(4)
        thumbnails.arrange(DOWN, buff=-0.8)
        thumbnails[4:].align_to(thumbnails, UP).shift(0.5 * DOWN)
        thumbnails.to_corner(UL)
        for n, tn in enumerate(thumbnails):
            tn.add_to_back(SurroundingRectangle(tn, buff=0).set_stroke(WHITE, 1))
            tn.shift(0.4 * n * RIGHT)

        self.play(
            FadeOut(randy.bubble, time_span=(0, 1)),
            randy.change("raise_left_hand", thumbnails).set_anim_args(time_span=(0, 1)),
            plane_group.animate.set_width(3.5).next_to(formula, DOWN, MED_LARGE_BUFF).set_anim_args(time_span=(0, 2)),
            FadeOut(cliche, 3 * RIGHT, lag_ratio=-0.02, time_span=(0.5, 2.0)),
            LaggedStartMap(FadeIn, thumbnails, shift=UP, lag_ratio=0.5),
            run_time=3
        )

        # Fail to explain
        thumbnails.generate_target()
        for tn, vect in zip(thumbnails.target, compass_directions(len(thumbnails))):
            vect[0] *= 1.5
            tn.set_height(1.75)
            tn.move_to(3 * vect)

        formula.generate_target()
        q_marks = Tex(R"???", font_size=90)
        VGroup(formula.target, q_marks).arrange(DOWN, buff=MED_LARGE_BUFF).center()

        self.play(
            MoveToTarget(thumbnails, lag_ratio=0.01, run_time=2),
            FadeOut(randy, DOWN),
            FadeOut(plane_group, DOWN),
            MoveToTarget(formula),
            Write(q_marks)
        )
        self.wait()
        self.play(LaggedStartMap(FadeOut, thumbnails, shift=DOWN, lag_ratio=0.5, run_time=4))
        self.wait()

        # Show constant meanings
        e_copy = formula["e"][0].copy()

        circle = Circle(radius=1)
        circle.to_edge(UP, buff=LARGE_BUFF)
        circle.set_stroke(WHITE, 1)
        arc = circle.copy().pointwise_become_partial(circle, 0, 0.5)
        arc.set_stroke(pi_color, 5)
        radius = Line(circle.get_center(), circle.get_right())
        radius.set_stroke(WHITE, 1)
        radius_label = Tex(R"1", font_size=24)
        radius_label.next_to(radius, DOWN, SMALL_BUFF)
        pi_label = Tex(R"\pi").set_color(pi_color)
        pi_label.next_to(circle, UP, buff=SMALL_BUFF)
        circle_group = VGroup(circle, arc, radius_label, radius, pi_label)

        i_eq = Tex(R"i^2 = -1", t2c={"i": BLUE}, font_size=90)
        i_eq.move_to(circle).set_x(5)

        self.play(
            formula.animate.shift(DOWN),
            FadeOut(e_copy, 3 * UP + 5 * LEFT),
            FadeOut(q_marks, DOWN)
        )
        self.play(
            TransformFromCopy(formula[R"\pi"][0], pi_label),
            LaggedStartMap(FadeIn, VGroup(circle, radius, radius_label)),
            ShowCreation(arc),
        )
        self.play(
            FadeTransform(formula["i"][0].copy(), i_eq["i"][0]),
            Write(i_eq[1:], time_span=(0.75, 1.75)),
        )
        self.wait()

        # Question marks over i
        i_rect = SurroundingRectangle(formula["i"], buff=0.05)
        i_rect.set_stroke(YELLOW, 2)
        q_marks = Tex(R"???", font_size=24)
        q_marks.match_color(i_rect)
        q_marks.next_to(i_rect, UP, SMALL_BUFF)

        self.play(
            ShowCreation(i_rect),
            FadeIn(q_marks, 0.25 * UP, lag_ratio=0.25)
        )
        self.wait()

        # Who cares (To overlay)
        frame = self.frame
        back_rect = FullScreenRectangle()
        back_rect.fix_in_frame()
        back_rect.set_z_index(-1),

        self.play(
            LaggedStartMap(FadeOut, VGroup(circle_group, i_eq, VGroup(i_rect, q_marks))),
            FadeOut(circle_group),
            frame.animate.set_y(-3.5),
            FadeIn(back_rect),
            formula.animate.set_fill(WHITE),
            run_time=2
        )
        self.wait()
