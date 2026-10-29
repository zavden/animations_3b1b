# ==============================================================================
# Scene:      ReferenceTheIntegral
# Source:     videos/_2025/laplace/main_supplements.py (lines 260-533)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ReferenceTheIntegral.py ReferenceTheIntegral -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ReferenceTheIntegral(TeacherStudentsScene):
    def construct(self):
        # React to the preview
        morty = self.teacher
        stds = self.students

        self.play(
            morty.change("guilty"),
            self.change_students("confused", "concentrating", "pleading", look_at=self.screen)
        )
        self.wait(4)

        # Show expression
        t2c = {"{s}": YELLOW, "{t}": BLUE}
        lt_def = Tex(R"F({s}) = \int^\infty_0 f({t}) e^{\minus {s} {t}} d{t}", t2c=t2c)
        lt_def.move_to(self.hold_up_spot, DOWN)
        lt_def.shift(0.5 * DOWN)

        self.play(
            morty.change("raise_right_hand", look_at=lt_def),
            FadeIn(lt_def, UP),
            self.change_students("confused", "tease", "happy", look_at=lt_def)
        )
        self.wait(2)

        # Highlight integral
        int_rect = SurroundingRectangle(lt_def[R"\int^\infty_0"])
        body_rect = SurroundingRectangle(lt_def[R"f({t}) e^{\minus {s} {t}}"])
        VGroup(int_rect, body_rect).set_stroke(TEAL, 2)
        arrow = Vector(0.75 * DOWN, thickness=6)
        arrow.set_fill(TEAL)
        arrow.next_to(int_rect, UP)

        self.play(
            morty.change("hesitant", int_rect),
            ShowCreation(int_rect),
            GrowArrow(arrow),
            self.change_students("pondering", "happy", "tease"),
        )
        self.wait(2)

        # Show complex plane
        s_plane = ComplexPlane((-2, 2), (-2, 2))
        s_plane.add_coordinate_labels(font_size=16)
        s_plane.set_width(2.5)
        s_plane.next_to(body_rect, UP, LARGE_BUFF)
        s_plane.shift_onto_screen()
        s_plane.to_edge(UP, SMALL_BUFF)

        s = complex(-0.1, 1.5)
        t_max = 20
        func_path = ParametricCurve(
            lambda t: s_plane.n2p(2 * math.cos(t) * np.exp(s * t)),
            t_range=(1e-3, t_max, 0.1),
        )
        func_path.set_stroke(YELLOW, 2)
        dot = GlowDot()
        dot.move_to(func_path.get_start())
        tail = TracedPath(dot.get_center, stroke_color=YELLOW, time_traced=5)
        tail.add_updater(lambda m: m.set_stroke(YELLOW, width=(0, 3)))
        for t in range(30):
            tail.update(1 / 30)

        self.play(
            morty.change("raise_left_hand", s_plane),
            self.change_students("erm", "confused", "sassy", s_plane),
            arrow.animate.rotate(PI).scale(0.75).next_to(body_rect, UP).set_anim_args(path_arc=90 * DEG),
            ReplacementTransform(int_rect, body_rect),
        )
        self.add(tail)
        self.play(
            FadeIn(s_plane),
            MoveAlongPath(dot, func_path, run_time=10, rate_func=linear),
        )

        # Clear the board
        self.play(
            VFadeOut(tail),
            FadeOut(body_rect),
            FadeOut(arrow),
            FadeOut(s_plane),
            FadeOut(dot),
            lt_def.animate.move_to(2 * UP),
            morty.change("tease", look_at=2 * UP),
            self.change_students("pondering", "pondering", "pondering", look_at=2 * UP)
        )
        self.wait()

        # Remove f(t)
        lt_def.save_state()
        ft = lt_def[R"f({t})"][0]
        ft_rect = SurroundingRectangle(ft, buff=0.05)
        ft_rect.set_stroke(RED, 2)
        self.play(
            ShowCreation(ft_rect)
        )
        self.play(
            VGroup(ft_rect, ft).animate.to_corner(UL).set_stroke(width=0).fade(0.5),
            lt_def[R"e^{\minus {s} {t}} d{t}"].animate.align_to(ft, LEFT).shift(SMALL_BUFF * LEFT),
            lt_def["F({s}) = "].animate.set_fill(opacity=0),
        )
        self.wait(5)

        # Bring back the definition
        exp_int = VGroup(*lt_def[R"\int^\infty_0"][0], *lt_def[R"e^{\minus {s} {t}} d{t}"]).copy()
        exp_int_rhs = Tex(R"= \frac{1}{{s}}", t2c=t2c)
        exp_int_rhs.next_to(exp_int, RIGHT)
        exp_int_rhs.save_state()
        exp_int_rhs.move_to(morty.get_corner(UL)).set_fill(opacity=0)
        morty.body.insert_n_curves(500)
        exp_int.add(*exp_int_rhs)

        ft2, arrow, fancy_L = new_def_lhs = VGroup(
            Tex(R"f({t})", t2c=t2c),
            Vector(1.5 * RIGHT),
            Tex(R"\mathcal{L}"),
        )
        arrow.next_to(lt_def[R"\int"], LEFT)
        fancy_L.next_to(arrow, UP, SMALL_BUFF)
        ft2.next_to(arrow, LEFT)

        lt_def.saved_state[:5].set_opacity(0)

        self.play(
            morty.change("raise_right_hand", exp_int_rhs),
            Restore(exp_int_rhs)
        )
        self.wait(2)
        self.play(
            exp_int.animate.scale(0.5).fade(0.5).to_corner(UR),
            Restore(lt_def),
            self.change_students("confused", "erm", "sassy", look_at=exp_int),
            morty.change("guilty", stds[2].eyes),
            Write(new_def_lhs),
        )
        self.wait()
        self.play(
            TransformFromCopy(ft2, ft, path_arc=PI / 2)
        )
        self.wait(3)

        # Substitute in an exponential
        exp1, exp2 = exp_examples = Tex(R"e^{1.5{t}}", t2c=t2c).replicate(2)
        ft.refresh_bounding_box()
        exp1.move_to(ft2)
        exp2.move_to(ft)
        exp_examples.align_to(lt_def["e"], DOWN)

        self.play(
            LaggedStart(
                FadeOut(ft2, 0.5 * UP),
                FadeIn(exp1, 0.5 * UP),
                FadeOut(ft, 0.5 * UP),
                FadeIn(exp2, 0.5 * UP),
                lag_ratio=0.25
            ),
            morty.change("raise_right_hand"),
            self.change_students("pondering", "thinking", "tease")
        )
        self.wait(4)

        # Collapse the inside
        lt_def["f({t})"].set_fill(opacity=0)
        new_int = Tex(R"\int^\infty_0 e^{(1.5 - {s}){t}} d{t}", t2c=t2c)
        new_int.move_to(lt_def[R"\int"], LEFT).shift(1.0 * DOWN)
        new_int2 = Tex(R"\int^\infty_0 e^{\minus({s} - 1.5){t}} d{t}", t2c=t2c)
        new_int2.move_to(new_int)

        self.play(
            VGroup(exp_examples, arrow, fancy_L, lt_def).animate.to_edge(UP),
            FadeIn(new_int, DOWN),
            self.change_students("pondering", "pondering", "pondering", new_int),
            morty.change("tease", new_int),
        )
        self.wait()
        self.play(TransformMatchingTex(new_int, new_int2, path_arc=90 * DEG))
        self.wait()

        # Show the answer
        exp_int.target = exp_int.generate_target()
        exp_int.target.scale(1.5, about_edge=UR)
        exp_int.target.set_opacity(1)
        exp_int_rect = SurroundingRectangle(exp_int.target, buff=MED_SMALL_BUFF)
        exp_int_rect.set_stroke(YELLOW, 2)

        example_rhs = Tex(R"= {1 \over {s} - 1.5}", t2c=t2c)
        example_rhs.next_to(new_int2[-1], RIGHT)

        self.play(
            morty.change('raise_left_hand', exp_int),
            MoveToTarget(exp_int),
            ShowCreation(exp_int_rect),
            self.change_students("pondering", "thinking", "happy", look_at=exp_int),
        )
        self.wait()
        self.play(
            TransformMatchingShapes(exp_int[-4:], example_rhs),
            FadeOut(exp_int[:-4]),
            exp_int_rect.animate.surround(example_rhs, buff=SMALL_BUFF),
            morty.change("raise_right_hand"),
            run_time=1.5,
        )
        self.wait()

        # Label it as pole
        words = Text("Pole at 1.5")
        words.next_to(exp_int_rect, UP)
        words.match_x(example_rhs[1:])
        words.set_color(YELLOW)

        self.play(
            Write(words),
            exp_int_rect.animate.surround(example_rhs[1:], buff=SMALL_BUFF),
            morty.change("tease", words),
        )
        self.wait(3)
        self.play(
            FadeOut(exp_int_rect),
            FadeOut(words),
        )

        # Make it general
        srcs = VGroup(exp1, exp2, new_int2, example_rhs)
        trgs = VGroup(
            Tex(R"e^{a{t}}", t2c=t2c),
            Tex(R"e^{a{t}}", t2c=t2c),
            Tex(R"\int^\infty_0 e^{\minus(s - a){t}} d{t}", t2c=t2c),
            Tex(R"= {1 \over {s} - a}", t2c=t2c),
        )
        example_rects = VGroup(
            SurroundingRectangle(src["1.5"], buff=0.05)
            for src in srcs
        )
        example_rects.set_stroke(TEAL, 2)
        for src, trg in zip(srcs, trgs):
            trg.move_to(src)

        self.play(Write(example_rects))
        self.wait()
        self.play(
            FadeOut(example_rects),
            LaggedStart(
                (TransformMatchingTex(src, trg, key_map={"1.5": "a"})
                for src, trg in zip(srcs, trgs)),
                lag_ratio=0.2,
                run_time=1.5,
            )
        )
        self.wait()

        # Write conclusion
        new_rhs = trgs[3]

        self.play(
            FadeOut(trgs[2]),
            new_rhs.animate.next_to(lt_def, RIGHT),
            self.change_students("thinking", "happy", "tease", look_at=new_rhs),
            morty.change("raise_right_hand", new_rhs),
        )

        big_arrow = Arrow(trgs[0].get_bottom(), new_rhs.get_bottom(), path_arc=90 * DEG, thickness=5)
        words = TexText(R"Exponentials $\longrightarrow$ Poles")
        words.next_to(big_arrow, DOWN)

        self.play(
            Write(big_arrow),
            FadeIn(words, lag_ratio=0.1),
        )
        self.look_at(words)
        self.wait(3)

        # Clear
        self.remove(self.background)
        self.remove(self.pi_creatures)
