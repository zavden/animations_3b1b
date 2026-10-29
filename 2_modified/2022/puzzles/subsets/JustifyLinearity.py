# ==============================================================================
# Scene:      JustifyLinearity
# Source:     videos/_2022/puzzles/subsets.py (lines 3339-3512)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl JustifyLinearity.py JustifyLinearity -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Scene.play no longer accepts path_arc=: it is passed to the animations that move (Transform/MoveToTarget/set_anim_args)
# ==============================================================================

from manim_imports_ext import *

class JustifyLinearity(InteractiveScene):
    n_terms = 8

    def construct(self):
        # Create polynomials
        x_poly = self.get_polynomial("{x}", BLUE)
        x_poly.to_edge(UP)

        zeta_polys = VGroup(*(
            self.get_polynomial("\\zeta", YELLOW, exp_multiple=n)
            for n in range(5)
        ))
        zeta_polys.arrange(DOWN, buff=0.65, aligned_edge=LEFT)
        zeta_polys.next_to(x_poly, DOWN, LARGE_BUFF)
        x_poly.align_to(zeta_polys, LEFT)
        polys = VGroup(x_poly, *zeta_polys)

        # Align parts
        low_poly = polys[-1]
        for poly in polys[:-1]:
            for i1, i2 in zip(poly.sep_indices, low_poly.sep_indices):
                shift = (low_poly[i2].get_x(LEFT) - poly[i1].get_x(LEFT)) * RIGHT
                poly[i1].shift(shift / 2)
                poly[i1 + 1:].shift(shift)

        # Discuss complexity
        simple_examples = VGroup(*(
            Tex(f"f(x) = x^{{{n}}}", tex_to_color_map={"x": BLUE}, font_size=36)
            for n in range(1, 6)
        ))
        simple_examples.arrange(DOWN, aligned_edge=LEFT)
        simple_examples.move_to(4 * RIGHT + DOWN)
        simple_box = SurroundingRectangle(simple_examples, buff=MED_SMALL_BUFF)
        simple_box.set_fill(GREY_E, 1)
        simple_box.set_stroke(WHITE, 1)
        simple_label = Text("Simple examples")
        simple_label.next_to(simple_box, UP, SMALL_BUFF)
        simple_box.match_width(simple_label, stretch=True)
        simple_group = VGroup(simple_box, simple_label, simple_examples)

        randy = Randolph(height=2)
        randy.align_to(simple_box, DOWN)
        randy.to_edge(LEFT)

        self.add(simple_group)
        self.play(
            PiCreatureSays(
                randy, OldTexText("But $f$ is more\\\\complicated than that!", font_size=36),
                bubble_config=dict(width=4, height=2),
                target_mode="pleading",
            )
        )
        self.play(
            Write(x_poly),
            randy.change("sad", x_poly),
        )
        self.play(Blink(randy))
        self.wait()

        # Prepare for grid sum
        lhss = VGroup(*(
            poly[:poly.sep_indices[0]]
            for poly in zeta_polys
        ))
        lhss.save_state()
        plusses = Tex("+", font_size=36).replicate(len(lhss) - 1)
        group = VGroup(*it.chain(*zip(lhss, plusses)))
        group.add(lhss[-1])
        group.arrange(RIGHT, buff=MED_SMALL_BUFF)
        group.next_to(x_poly, DOWN, LARGE_BUFF)

        plusses.generate_target()
        for plus, lhs1, lhs2 in zip(plusses.target, lhss.saved_state, lhss.saved_state[1:]):
            plus.move_to(midpoint(lhs1.get_bottom(), lhs2.get_top()))
            plus.scale(0.7)

        self.play(
            Write(group),
            FadeOut(VGroup(randy.bubble, randy.bubble.content)),
            simple_group.animate.to_edge(DOWN),
        )
        self.wait()
        for mob in x_poly, group:
            self.play(
                FlashAround(mob, time_width=2, run_time=2, color=mob[2].get_fill_color()),
                randy.change("pondering", mob),
            )
            self.wait()
        self.play(
            # CHANGE: Scene.play no longer accepts path_arc; it is passed to the two animations that move
            lhss.animate.restore().set_anim_args(path_arc=-90 * DEGREES),
            MoveToTarget(plusses, path_arc=-90 * DEGREES),
            FadeOut(randy),
            FadeOut(simple_group),
        )
        self.wait()

        # Write all right hand sides
        anims = []
        for poly in zeta_polys:
            anims.append(FadeTransformPieces(
                x_poly[x_poly.sep_indices[0]:].copy(),
                poly[poly.sep_indices[0]:],
            ))
        self.play(LaggedStart(*anims, lag_ratio=0.1, run_time=2))
        self.wait()

        # Highlight columns
        lower_sum = VGroup()
        lp = polys[-1]
        for j in range(len(x_poly.sep_indices) - 1):
            polys.generate_target()
            col = VGroup()
            for poly in polys.target:
                col.add(poly[poly.sep_indices[j] + 1:poly.sep_indices[j + 1]])
            polys.target.set_fill(opacity=0.5)
            col.set_fill(opacity=1)

            if j % 5 == 0:
                term = Tex(f"5c_{j}", font_size=36)
            else:
                term = Tex("0", font_size=36)
            i1, i2 = lp.sep_indices[j:j + 2]
            term.next_to(VGroup(lp[i1], lp[i2]), DOWN, buff=0.7)
            plus = Tex("+", font_size=36)
            plus.next_to(lp[i1], DOWN, buff=0.7)
            if j == 0:
                plus.set_opacity(0)
            else:
                plus.move_to(midpoint(lower_sum.get_right(), term.get_left()))
            lower_sum.add(plus, term)

            self.play(
                FlashAround(col, time_width=2),
                MoveToTarget(polys),
                plusses.animate.set_fill(opacity=0.5),
            )
            self.wait()
            self.play(
                Write(plus),
                *(
                    FadeTransform(piece.copy(), term)
                    for piece in col[1:]
                )
            )
            self.wait()
        self.play(polys.animate.set_opacity(1))
        self.wait()

    def get_polynomial(self, input_tex, color, exp_multiple=None, font_size=36):
        if exp_multiple is not None:
            tex = f"f({input_tex}^{exp_multiple}) ="
        else:
            tex = f"f({input_tex}) = "
            exp_multiple = 1
        tex += "c_0 + "
        for n in range(1, self.n_terms):
            tex += f"c_{{{n}}}{input_tex}^{{{exp_multiple * n}}} + "
        tex += "\\cdots"
        result = Tex(
            tex,
            tex_to_color_map={
                input_tex: color,
                "+": WHITE,
                "=": WHITE,
            },
            font_size=font_size,
        )
        result.sep_indices = [
            result.submobjects.index(part.family_members_with_points()[0])
            for part in (*result.get_parts_by_tex("="), *result.get_parts_by_tex("+"))
        ]
        # result.arrange(RIGHT, aligned_edge=DOWN)
        return result
