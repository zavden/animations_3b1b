# ==============================================================================
# Scene:      SolutionsToPolynomials
# Source:     videos/_2020/monster.py (lines 1352-1659)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl SolutionsToPolynomials.py SolutionsToPolynomials -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

def permutation_animation(mobs, perm=None, arc=PI / 2, lag_factor=3, run_time=None):
    if perm is None:
        targets = list(mobs)
        random.shuffle(targets)
    else:
        targets = [mobs[i] for i in perm]

    kw = {"lag_ratio": lag_factor / len(mobs)}
    if run_time is not None:
        kw["run_time"] = run_time
    return LaggedStart(
        *[
            ApplyMethod(m1.move_to, m2, path_arc=arc)
            for m1, m2 in zip(mobs, targets)
        ],
        **kw
    )


class SolutionsToPolynomials(Scene):
    def construct(self):
        # Show quintic shuffling
        colors = list(Color(BLUE).range_to(YELLOW, 5))
        quintic = OldTex(
            "x^5 - x - 1",
            "=",
            "(x - r_0)",
            "(x - r_1)",
            "(x - r_2)",
            "(x - r_3)",
            "(x - r_4)",
            tex_to_color_map={
                f"r_{i}": colors[i]
                for i in range(5)
            }
        )
        root_syms = VGroup(*[quintic.get_part_by_tex(f"r_{i}") for i in range(5)])
        quintic.set_width(FRAME_WIDTH - 1)
        quintic.to_edge(UP)

        plane = ComplexPlane(x_range=(-2, 2), y_range=(-2, 2))
        plane.set_height(6)
        plane.to_edge(DOWN, buff=MED_SMALL_BUFF)
        plane.add_coordinate_labels()
        for label in plane.coordinate_labels:
            label.scale(0.7, about_edge=UR)

        def get_root_dots(roots, plane=plane, colors=colors):
            return VGroup(*[
                Dot(
                    plane.n2p(root),
                    radius=0.1,
                    color=color,
                ).set_stroke(BLACK, 2, background=True)
                for root, color in zip(roots, colors)
            ])

        root_dots = get_root_dots([
            1.1673,
            0.181232 + 1.08395j,
            0.181232 - 1.08395j,
            -0.764884 + 0.352472j,
            -0.764884 - 0.352472j,
        ])

        self.add(quintic)
        self.add(plane)
        self.play(LaggedStart(*[
            ReplacementTransform(rs.copy(), rd)
            for rs, rd in zip(root_syms, root_dots)
        ], run_time=3, lag_ratio=0.3))
        self.wait()

        root_syms.save_state()
        root_dots.save_state()

        for x in range(5):
            perm = list(range(5))
            random.shuffle(perm)
            self.play(*[
                permutation_animation(mob, perm, arc=30 * DEGREES, lag_factor=0.5)
                for mob in [root_syms, root_dots]
            ])
            self.wait(0.5)
        self.play(
            Restore(root_syms, path_arc=60 * DEGREES),
            Restore(root_dots, path_arc=60 * DEGREES),
        )

        # Down to quadratic
        quadratic_lhs = OldTex("x^2 - x - 1")
        quadratic_lhs.match_height(quintic[0])
        quadratic_lhs.move_to(quintic[0], RIGHT)

        self.play(
            FadeOut(quintic[0], UP),
            FadeIn(quadratic_lhs, DOWN),
            FadeOut(quintic[8:], UP),
            MaintainPositionRelativeTo(root_dots, plane),
            UpdateFromAlphaFunc(root_dots, lambda m, a: m.set_opacity(1 - a)),
            plane.to_edge, LEFT,
        )
        self.remove(root_dots)
        root_dots.set_opacity(1)
        root_dots.save_state()

        quad_root_dots = get_root_dots([
            (1 + u * np.sqrt(5)) / 2 for u in [-1, 1]
        ])

        self.play(LaggedStart(*[
            ReplacementTransform(root_sym.copy(), root_dot)
            for root_dot, root_sym in zip(quad_root_dots, root_syms)
        ]))
        self.wait()

        # Quadratic formula
        quadratic_formula = OldTex(
            "{-b \\pm \\sqrt{\\,b^2 - 4ac} \\over 2a}",
        )
        quadratic_formula.set_height(1.5)
        quadratic_formula.to_edge(RIGHT, buff=LARGE_BUFF)

        quad_form_name = OldTexText("Quadratic formula")
        quad_form_name.set_height(0.5)
        quad_form_name.next_to(quadratic_formula, DOWN, LARGE_BUFF)
        quad_form_name.set_color(GREY_B)

        self.play(
            Write(quadratic_formula),
            FadeIn(quad_form_name, DOWN)
        )
        self.wait()

        # Cubic
        cubic_lhs = OldTex("x^3 - x - 1")
        cubic_lhs.replace(quadratic_lhs)

        cubic_root_dots = get_root_dots([
            1.3247,
            -0.66236 + 0.56228j,
            -0.66236 - 0.56228j,
        ])

        cubic_formula = OldTex(
            r"\sqrt[3]{-\frac{q}{2}+\sqrt{\frac{q^{2}}{4}+\frac{p^{3}}{27}}}+\sqrt[3]{-\frac{q}{2}-\sqrt{\frac{q^{2}}{4}+\frac{p^{3}}{27}}}",
        )
        cubic_formula.replace(quadratic_formula, dim_to_match=1)
        cubic_formula.to_edge(RIGHT, buff=MED_SMALL_BUFF)
        cubic_formula.scale(0.8, about_edge=RIGHT)

        cubic_form_name = OldTexText("Cubic formula (reduced)")
        cubic_form_name.replace(quad_form_name, dim_to_match=1)
        cubic_form_name.match_style(quad_form_name)

        self.play(
            ReplacementTransform(quad_root_dots, cubic_root_dots),
            FadeIn(quintic[8:11], DOWN),
            FadeIn(cubic_lhs, DOWN),
            FadeOut(quadratic_lhs, UP),
        )
        self.play(
            LaggedStart(
                FadeOut(quadratic_formula, 2 * RIGHT),
                FadeOut(quad_form_name, 2 * RIGHT),
            ),
            LaggedStart(
                FadeIn(cubic_formula, 2 * LEFT),
                FadeIn(cubic_form_name, 2 * LEFT),
            ),
        )
        self.wait()

        # Quartic (largely copied from above)
        quartic_lhs = OldTex("x^4 - x - 1")
        quartic_lhs.replace(quadratic_lhs)

        quartic_root_dots = get_root_dots([
            1.2207,
            -0.72449,
            -0.24813 + 1.0340j,
            -0.24813 - 1.0340j,
        ])

        quartic_formula = OldTex(r"""
            r_{i}&=-\frac{b}{4 a}-S \pm \frac{1}{2} \sqrt{-4 S^{2}-2 p \pm \frac{q}{S}}\\\\
            &\text{Where}\\\\
            p&=\frac{8 a c-3 b^{2}}{8 a^{2}} \qquad \qquad
            q=\frac{b^{3}-4 a b c+8 a^{2} d}{8 a^{3}}\\\\
            S&=\frac{1}{2} \sqrt{-\frac{2}{3} p+\frac{1}{3 a}\left(Q+\frac{\Delta_{0}}{Q}\right)}\\\\
            Q&=\sqrt[3]{\frac{\Delta_{1}+\sqrt{\Delta_{1}^{2}-4 \Delta_{0}^{3}}}{2}}\\\\
            \Delta_{0}&=c^{2}-3 b d+12 a e\\\\
            \Delta_{1}&=2 c^{3}-9 b c d+27 b^{2} e+27 a d^{2}-72 a c e\\\\
        """)
        quartic_formula.set_height(6)
        quartic_formula.next_to(plane, RIGHT, LARGE_BUFF)

        self.play(
            FadeOut(cubic_formula, 2 * RIGHT),
            FadeOut(cubic_form_name, 2 * RIGHT),
            ReplacementTransform(cubic_root_dots, quartic_root_dots),
            FadeIn(quintic[11:14], DOWN),
            FadeIn(quartic_lhs, DOWN),
            FadeOut(cubic_lhs, UP),
        )
        self.play(
            Write(quartic_formula, run_time=3),
        )
        self.wait(2)

        # Back to quintic
        self.play(
            ReplacementTransform(quartic_root_dots, root_dots),
            FadeIn(quintic[0], DOWN),
            FadeOut(quartic_lhs, UP),
            FadeIn(quintic[14:], DOWN),
            FadeOut(quartic_formula, 0.1 * DOWN, lag_ratio=0.01),
        )

        # Wonder about the quintic
        mathy = PiCreature(color=GREY)
        mathy.flip()
        mathy.next_to(quintic, DOWN, buff=1.5)
        mathy.to_edge(RIGHT)

        self.play(
            VFadeIn(mathy),
            mathy.change, "confused", root_syms,
        )
        self.play(Blink(mathy))
        self.wait()
        self.play(
            mathy.change, "pondering", root_syms[3]
        )
        self.play(Blink(mathy))
        self.wait()

        mathy.add_updater(lambda m, sym=root_syms[3]: m.look_at(sym))

        # Show a few permutations
        s5_name = OldTex("S_5")
        s5_name.scale(1.5)
        s5_name.next_to(plane, RIGHT, MED_LARGE_BUFF, aligned_edge=UP)
        s5_name.shift(DOWN)

        s5_lines = VGroup()
        for dot in root_dots:
            line = Line(s5_name.get_left(), dot.get_center())
            line.match_color(dot)
            line.set_stroke(width=1)
            line.dot = dot
            line.start = line.get_start()
            s5_lines.add(line)

        s5_lines.set_stroke(opacity=0.5)

        self.play(
            FadeIn(s5_name),
            ShowCreation(s5_lines, lag_ratio=0.5),
        )
        for line in s5_lines:
            line.add_updater(lambda m: m.put_start_and_end_on(m.start, m.dot.get_center()))
        self.add(*s5_lines)

        for x in range(5):
            perm = list(range(5))
            random.shuffle(perm)
            self.play(*[
                permutation_animation(mob, perm, arc=30 * DEGREES, lag_factor=0.5)
                for mob in [root_syms, root_dots]
            ])
            self.wait(0.5)

        self.play(
            VFadeOut(s5_lines),
            Restore(root_syms),
            Restore(root_dots),
            FadeOut(mathy),
        )

        # No formula
        r0_value = OldTex(
            "r_0", "=", "1.1673\\dots",
        )
        r0_value.set_color_by_tex("r_0", BLUE)
        r0_value.scale(1.5)
        r0_value.next_to(plane, RIGHT, MED_LARGE_BUFF)
        r0_value.shift(DOWN)

        self.play(
            LaggedStart(*[
                AnimationGroup(
                    ShowCreationThenFadeAround(dot),
                    ShowCreationThenFadeAround(sym),
                )
                for sym, dot in zip(root_syms, root_dots)
            ], lag_ratio=0.3, run_time=3),
        )
        self.play(TransformFromCopy(root_syms[0], r0_value[0]))
        self.play(Write(r0_value[1:]))
        self.add(r0_value)
        self.wait()

        # Arithmetic symbols
        symbols = VGroup(*[
            OldTex(s)
            for s in ["+", "-", "\\times", "/", "\\sqrt[n]{\\qquad}"]
        ])
        symbols[:4].arrange_in_grid(2, 2)
        symbols[4].next_to(symbols[:4], RIGHT, MED_LARGE_BUFF)
        symbols.move_to(s5_name)
        symbols.to_edge(RIGHT)
        symbols_rect = SurroundingRectangle(symbols, buff=MED_SMALL_BUFF)
        symbols_rect.set_stroke(BLUE, 2)

        arrow = Arrow(symbols_rect.get_corner(DL), r0_value[2][3].get_top())
        cross = Cross(arrow)
        cross.stretch(0.5, 1)

        self.play(
            FadeIn(symbols, lag_ratio=0.2, run_time=1.5),
            ShowCreation(symbols_rect),
        )
        self.wait()
        self.play(GrowArrow(arrow))
        self.play(ShowCreation(cross))
        self.wait()
