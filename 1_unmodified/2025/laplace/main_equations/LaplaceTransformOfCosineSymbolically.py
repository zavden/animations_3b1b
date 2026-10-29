# ==============================================================================
# Scene:      LaplaceTransformOfCosineSymbolically
# Source:     videos/_2025/laplace/main_equations.py (lines 1807-2132)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl LaplaceTransformOfCosineSymbolically.py LaplaceTransformOfCosineSymbolically -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class LaplaceTransformOfCosineSymbolically(InteractiveScene):
    def construct(self):
        # Add defining integral
        frame = self.frame
        t2c = {
            "{t}": BLUE,
            "{s}": YELLOW,
            R"\omega": PINK,
            R"int^\infty_0": WHITE,
        }
        key_strings = [
            R"int^\infty_0",
            R"e^{\minus{s}{t}} d{t}",
            "+",
            R"\frac{1}{2}",
            R"e^{i{t}}",
            R"e^{\minus i{t}}",
        ]
        kw = dict(isolate=key_strings, t2c=t2c)

        cos_t = Tex(R"\cos({t})", **kw)
        cos_t.to_corner(UL, buff=LARGE_BUFF)
        arrow = Vector(1.5 * RIGHT)
        arrow.next_to(cos_t)
        fancy_L = Tex(R"\mathcal{L}")
        fancy_L.next_to(arrow, UP, SMALL_BUFF)

        def lt_string(interior):
            return Rf"\int^\infty_0 " + interior + R"e^{\minus{s}{t}} d{t}"

        lt_def = Tex(lt_string(R"\cos({t})"), **kw)
        lt_def.next_to(arrow, RIGHT)

        self.add(cos_t)
        self.play(LaggedStart(
            GrowArrow(arrow),
            Write(fancy_L),
            Write(lt_def[R"\int^\infty_0"]),
            TransformFromCopy(cos_t, lt_def[R"\cos({t})"][0], path_arc=45 * DEG),
            Write(lt_def[R"e^{\minus{s}{t}} d{t}"]),
            lag_ratio=0.2,
        ))

        # Split up into exponential parts
        spilt_cos_str = R"\left( \frac{1}{2} e^{i{t}} + \frac{1}{2} e^{\minus i{t}} \right)"
        split_inside = Tex("=" + lt_string(spilt_cos_str), **kw)
        split_inside.next_to(lt_def, RIGHT)

        cos_rect = SurroundingRectangle(lt_def[R"\cos({t})"])
        cos_rect.set_stroke(TEAL, 2)

        self.play(ShowCreation(cos_rect))
        self.play(
            TransformMatchingTex(
                lt_def.copy(),
                split_inside,
                key_map={R"\cos({t})": spilt_cos_str},
                path_arc=30 * DEG,
                mismatch_animation=FadeTransform,
            ),
            cos_rect.animate.surround(split_inside[spilt_cos_str]).set_anim_args(path_arc=30 * DEG),
            run_time=1.5
        )
        self.play(FadeOut(cos_rect))
        self.wait()
        self.add(split_inside)

        # Rect growth
        self.play(cos_rect.animate.surround(split_inside[1:]).set_stroke(width=5))
        self.wait()
        self.play(FadeOut(cos_rect))

        # Linearity
        split_tex = " ".join([
            R"\frac{1}{2}", lt_string(R"e^{i{t}}"), R"\, + \,",
            R"\frac{1}{2}", lt_string(R"e^{\minus i{t}}"),
        ])
        split_outside = Tex(split_tex, **kw)
        side_eq = Tex(R"=", font_size=72).rotate(90 * DEG)
        side_eq.next_to(split_inside, DOWN, MED_LARGE_BUFF)
        split_outside.next_to(side_eq, DOWN, MED_LARGE_BUFF)
        split_outside.shift_onto_screen()

        srcs = VGroup()
        trgs = VGroup()
        for tex in key_strings:
            src = split_inside[tex]
            trg = split_outside[tex]
            if tex is key_strings[0]:
                src = VGroup(part[:3] for part in src)
                trg = VGroup(part[:3] for part in trg)
            srcs.add(src)
            trgs.add(trg)

        self.play(
            Write(side_eq),
            LaggedStart(
                (TransformFromCopy(*pair)
                for pair in zip(srcs[:3], trgs[:3])),
                lag_ratio=0.01,
                run_time=2
            ),
        )
        self.wait()
        self.play(
            TransformFromCopy(srcs[3][0], trgs[3][0]),
            TransformFromCopy(srcs[4][0], trgs[4][0])
        )
        self.wait()
        self.play(
            TransformFromCopy(srcs[3][1], trgs[3][1]),
            TransformFromCopy(srcs[5][0], trgs[5][0])
        )
        self.wait()

        # Collapse to poles
        exp_transform_parts = VGroup(
            split_outside[lt_string(R"e^{i{t}}")],
            split_outside[lt_string(R"e^{\minus i{t}}")],
        )
        pole_strings = [R"\frac{1}{{s} - i}", R"\frac{1}{{s} \, + \, i}"]
        half_string = R"\frac{1}{2}"
        pole_sum = Tex(
            R" \, ".join([half_string, pole_strings[0], "+", half_string, pole_strings[1]]),
            **kw
        )
        pole_sum.scale(1.25)
        pole_sum.move_to(split_outside).shift(0.2 * LEFT)

        split_inside_rect = SurroundingRectangle(split_inside[spilt_cos_str])
        exp_transform_rects = VGroup(
            SurroundingRectangle(part, buff=SMALL_BUFF)
            for part in exp_transform_parts
        )
        pole_rects = VGroup(
            SurroundingRectangle(pole_sum[tex], buff=SMALL_BUFF)
            for tex in pole_strings
        )

        VGroup(split_inside_rect, exp_transform_rects, pole_rects).set_stroke(TEAL, 2)

        self.play(ShowCreation(split_inside_rect))
        self.wait()
        self.play(LaggedStart(*(
            TransformFromCopy(split_inside_rect, rect)
            for rect in exp_transform_rects
        )))
        self.play(FadeOut(split_inside_rect))
        self.wait()
        for i, tex in enumerate([R"e^{i{t}}", R"e^{\minus i{t}}"]):
            self.play(
                ReplacementTransform(exp_transform_rects[i], pole_rects[i]),
                ReplacementTransform(split_outside[half_string][i], pole_sum[half_string][i]),
                FadeTransform(split_outside[lt_string(tex)], pole_sum[pole_strings[i]]),
                Transform(split_outside["+"][0], pole_sum["+"][0])
            )
            self.play(FadeOut(pole_rects[i]))
        self.remove(split_outside)
        self.add(pole_sum)
        self.play(pole_sum.animate.match_x(side_eq))

        # Read it as "pole at i", etc.
        pole_rects = VGroup(
            SurroundingRectangle(pole_sum[tex], buff=SMALL_BUFF)
            for tex in pole_strings
        )
        pole_rects.set_stroke(YELLOW, 2)
        pole_words = VGroup(
            TexText(Rf"Pole at \\ $s = {value}$", font_size=60, t2c={"Pole at": YELLOW, "s": YELLOW})
            for value in ["i", "-i"]
        )

        last_group = VGroup()
        for word, rect in zip(pole_words, pole_rects):
            word.next_to(rect, DOWN, MED_LARGE_BUFF)
            self.play(
                FadeIn(word, lag_ratio=0.1),
                ShowCreation(rect),
                FadeOut(last_group)
            )
            self.wait()
            last_group = VGroup(word, rect)

        self.play(FadeOut(last_group))

        # Add an omega
        old_group = VGroup(cos_t, lt_def, split_inside, pole_sum)
        new_group = VGroup(
            Tex(R"\cos(\omega{t})", **kw),
            Tex(lt_string(R"\cos(\omega{t})"), **kw),
            Tex("=" + lt_string(R"\left(\frac{1}{2} e^{i\omega{t}} + \frac{1}{2}e^{\minus i \omega {t}} \right)"), **kw),
            Tex(R" \, ".join([
                half_string, R"\frac{1}{{s} - \omega i}", "+",
                half_string, R"\frac{1}{{s} \, + \, \omega i}",
            ]), **kw)
        )
        for new, old in zip(new_group, old_group):
            new.match_width(old)
            new.move_to(old)

        omegas = VGroup()
        for new in new_group:
            omegas.add(*new[R"\omega"])

        omega_copies = omegas.copy()
        omegas.set_fill(opacity=0)
        omegas[0].set_fill(opacity=1)

        cos_omega = new_group[0]
        cos_omega.scale(1.25, about_edge=RIGHT)
        cos_omega_rect = SurroundingRectangle(cos_omega)
        cos_omega_rect.set_stroke(PINK, 2)

        self.play(
            ShowCreation(cos_omega_rect),
            TransformMatchingTex(cos_t, cos_omega),
            run_time=1
        )
        self.wait()
        self.play(
            LaggedStart(
                (TransformMatchingTex(old, new)
                for new, old in zip(new_group[1:], old_group[1:])),
                lag_ratio=0.05,
                run_time=1
            ),
            TransformFromCopy(
                omegas[0].replicate(len(omega_copies) - 1),
                omega_copies[1:],
                path_arc=30 * DEG,
                lag_ratio=0.1,
                run_time=2
            ),
        )
        self.remove(omega_copies)
        omegas.set_fill(opacity=1)
        self.add(new_group)
        self.play(FadeOut(cos_omega_rect))
        self.wait()

        # Simplify fraction
        lower_arrow = Tex(R"\longleftarrow", font_size=60)
        lower_arrow.next_to(pole_sum, LEFT)

        transform_kw = dict(
            matched_keys=[
                R"{s}^2 \,+\, \omega^2",
                R"{s} \,+\, \omega i",
                R"{s} - \omega i",
                R"\over",
            ],
            key_map={
                R"({s} - \omega i)({s} + \omega i)": R"{s}^2 \,+\, \omega^2"
            }
        )

        steps = VGroup(
            Tex(R"""
                \frac{1}{2}\left(
                {{s} \,+\, \omega i \over ({s} - \omega i)({s} + \omega i)} +
                {{s} - \omega i \over ({s} - \omega i)({s} + \omega i)}
                \right)
            """, **kw),
            Tex(R"""
                \frac{1}{2}\left(
                {{s} \,+\, \omega i \over {s}^2 \,+\, \omega^2} +
                {{s} - \omega i \over {s}^2 \,+\, \omega^2}
                \right)
            """, **kw),
            Tex(R"""
                \frac{1}{2} {{s} \,+\, \omega i \,+\, {s} - \omega i \over {s}^2 \,+\, \omega^2}
            """, **kw),
            Tex(R"""
                \frac{1}{2} {2{s} \over {s}^2 \,+\, \omega^2}
            """, **kw),
            Tex(R"{{s} \over {s}^2 \,+\, \omega^2}", **kw),
        )
        for step in steps:
            step.next_to(lower_arrow, LEFT)

        self.play(
            Write(lower_arrow),
            FadeTransform(pole_sum.copy(), steps[0]),
            frame.animate.set_height(8.5, about_edge=DR),
            run_time=2
        )
        for step1, step2 in zip(steps, steps[1:]):
            self.play(
                TransformMatchingTex(step1, step2, **transform_kw)
            )
            self.wait()

        # Circle answer
        answer = steps[-1]
        answer.target = answer.generate_target()
        answer.target.scale(1.5, about_edge=RIGHT)
        answer_rect = SurroundingRectangle(answer.target)
        answer_rect.set_stroke(TEAL, 3)
        self.play(
            ShowCreation(answer_rect),
            MoveToTarget(answer)
        )
        self.wait()

        # Highlight direct equality
        lt_def, int_of_expanded, imag_result = new_group[-3:]

        direct_equals = Tex(R"=", font_size=90)
        direct_equals.rotate(90 * DEG)
        direct_equals.next_to(lt_def, DOWN, MED_LARGE_BUFF)

        to_fade = VGroup(int_of_expanded, side_eq, imag_result)

        self.play(
            lower_arrow.animate.set_fill(opacity=0),
            to_fade.animate.set_fill(opacity=0.2),
            answer_rect.animate.surround(VGroup(lt_def, answer)),
            Write(direct_equals),
        )
        self.wait()
        self.play(
            lower_arrow.animate.set_fill(opacity=1).rotate(PI).set_anim_args(path_arc=PI),
            answer_rect.animate.surround(VGroup(answer, imag_result)),
            imag_result.animate.set_fill(opacity=1),
        )
        self.wait()
