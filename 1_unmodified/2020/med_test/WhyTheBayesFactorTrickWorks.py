# ==============================================================================
# Scene:      WhyTheBayesFactorTrickWorks
# Source:     videos/_2020/med_test.py (lines 4146-4321)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl WhyTheBayesFactorTrickWorks.py WhyTheBayesFactorTrickWorks -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class WomanIcon(SVGMobject):
    CONFIG = {
        "fill_color": GREY_B,
        "stroke_width": 0,
    }

    def __init__(self, **kwargs):
        super().__init__("woman_icon", **kwargs)
        self.remove(self[0])


class WhyTheBayesFactorTrickWorks(Scene):
    def construct(self):
        # Setup before and after
        titles = VGroup(
            OldTexText("Before test"),
            OldTexText("After test"),
        )
        titles.scale(1.25)
        for title, u in zip(titles, [-1, 1]):
            title.set_x(u * FRAME_WIDTH / 4)
            title.to_edge(UP, buff=MED_SMALL_BUFF)
        h_line = Line(LEFT, RIGHT)
        h_line.set_width(FRAME_WIDTH)
        h_line.next_to(titles, DOWN)
        h_line.set_x(0)
        v_line = Line(UP, DOWN).set_height(FRAME_HEIGHT)
        lines = VGroup(h_line, v_line)
        lines.set_stroke(GREY, 2)

        self.add(titles)
        self.add(lines)

        # Show population before
        population = VGroup(*(WomanIcon() for x in range(100)))
        population.arrange_in_grid(h_buff=0.7, fill_rows_first=False)
        population.set_height(5)
        population[:10].set_fill(YELLOW)
        population[:10].shift(MED_SMALL_BUFF * LEFT)
        population.match_x(titles[0])
        population.to_edge(DOWN, buff=MED_LARGE_BUFF)

        w_tex = "(\\text{\\# With})"
        wo_tex = "(\\text{\\# Without})"
        t2c = {
            w_tex: YELLOW,
            wo_tex: GREY_B,
        }
        odds = OldTex(w_tex, ":", wo_tex, tex_to_color_map=t2c)
        odds.next_to(population, UP, buff=MED_LARGE_BUFF)
        odds.match_x(titles[0])

        self.add(population)
        self.add(odds)
        self.play(
            ShowCreationThenDestruction(Underline(odds[0])),
            LaggedStartMap(
                ShowCreationThenFadeOut,
                VGroup(*(
                    SurroundingRectangle(icon, stroke_width=1, buff=0.05)
                    for icon in population[:10]
                ))
            ),
        )
        self.play(
            ShowCreationThenDestruction(Underline(odds[2])),
            LaggedStartMap(
                ShowCreationThenFadeOut,
                VGroup(*(
                    SurroundingRectangle(icon, color=GREY, stroke_width=1, buff=0.05)
                    for icon in population[10:]
                )),
                lag_ratio=0.01
            ),
        )
        self.wait()

        # Turn odds into fraction
        frac = OldTex(
            w_tex, "\\over", wo_tex, tex_to_color_map=t2c,
            font_size=36
        )
        frac.next_to(h_line, DOWN, MED_LARGE_BUFF)
        frac.match_x(titles[0])

        self.play(
            ReplacementTransform(odds, frac),
            population.set_height, 4.5,
            population.next_to, frac, DOWN, MED_LARGE_BUFF,
        )
        self.wait()

        # Show filtration
        pop_copy = population.copy()
        pop_copy.match_x(titles[1])

        tp_cases = pop_copy[:9]
        fn_cases = pop_copy[9:10]
        fp_cases = pop_copy[10::10]
        tn_cases = VGroup(*(
            case
            for case in pop_copy[10:]
            if case not in fp_cases
        ))

        VGroup(fn_cases, tn_cases).set_opacity(0.1)
        VGroup(tp_cases, tp_cases).set_stroke(GREEN, 3, background=True)

        pos_boxes = VGroup()
        for case in it.chain(tp_cases, fp_cases):
            box = SurroundingRectangle(case, buff=0.025)
            box.set_stroke(GREEN, 0)
            plus = OldTex("+", font_size=24)
            plus.move_to(box.get_corner(UR))
            plus.shift(DR * plus.get_height() / 4)
            plus.set_color(GREEN)
            box.add(plus)
            pos_boxes.add(box)

        self.play(
            TransformFromCopy(population, pop_copy),
            path_arc=30 * DEGREES
        )
        self.play(LaggedStartMap(DrawBorderThenFill, pos_boxes))
        self.wait()

        # Final fraction
        t2c.update({
            "\\text{Cancer}": YELLOW,
            "\\text{No cancer}": GREY,
            "+": GREEN,
            "\\cdot": WHITE,
        })
        final_frac = OldTex(
            w_tex, "\\cdot P(+ \\,|\\, \\text{Cancer})",
            "\\over",
            wo_tex, "\\cdot P(+ \\,|\\, \\text{No cancer})",
            tex_to_color_map=t2c,
            font_size=36,
        )
        final_frac.match_x(pop_copy)
        final_frac.match_y(frac)

        left_brace = Brace(tp_cases, LEFT)
        right_brace = Brace(fp_cases, RIGHT, min_num_quads=1)
        big_left_brace = Brace(VGroup(tp_cases, fn_cases), LEFT)
        big_right_brace = Brace(VGroup(fp_cases, tn_cases), RIGHT)
        big_left_brace.set_opacity(0)
        big_right_brace.set_opacity(0)

        self.play(*(
            TransformFromCopy(
                frac.get_part_by_tex(tex),
                final_frac.get_part_by_tex(tex)
            )
            for tex in (w_tex, "\\over")
        ))
        self.wait()
        self.play(
            TransformFromCopy(big_left_brace, left_brace),
            Write(final_frac[1:7])
        )
        self.wait()
        self.play(*(
            TransformFromCopy(
                frac.get_part_by_tex(tex),
                final_frac.get_part_by_tex(tex)
            )
            for tex in (wo_tex,)
        ))
        self.play(
            TransformFromCopy(big_right_brace, right_brace),
            Write(final_frac[9:])
        )
        self.wait()
        self.add(final_frac)

        # Circle likelihood ratio
        likelihood_ratio = VGroup(
            final_frac[2:7],
            final_frac[10:]
        )
        lr_rect = SurroundingRectangle(likelihood_ratio)
        lr_rect.set_stroke(BLUE, 3)

        self.play(ShowCreation(lr_rect))
        self.wait()
