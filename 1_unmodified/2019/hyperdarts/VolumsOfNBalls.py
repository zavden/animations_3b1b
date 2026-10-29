# ==============================================================================
# Scene:      VolumsOfNBalls
# Source:     videos/_2019/hyperdarts.py (lines 2210-2329)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl VolumsOfNBalls.py VolumsOfNBalls -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class VolumsOfNBalls(Scene):
    def construct(self):
        title, alt_title = [
            OldTexText(
                "Volumes of " + tex + "-dimensional balls",
                tex_to_color_map={tex: YELLOW},
            )
            for tex in ["$N$", "$2n$"]
        ]
        for mob in [title, alt_title]:
            mob.scale(1.5)
            mob.to_edge(UP)

        formulas = VGroup(*[
            OldTex(
                tex,
                tex_to_color_map={"R": WHITE}
            )
            for tex in [
                "2R",
                "\\pi R^2",
                "\\frac{4}{3} \\pi R^3",
                "\\frac{1}{2} \\pi^2 R^4",
                "\\frac{8}{15} \\pi^2 R^5",
                "\\frac{1}{6} \\pi^3 R^6",
                "\\frac{16}{105} \\pi^3 R^7",
                "\\frac{1}{24} \\pi^4 R^8",
                "\\frac{32}{945} \\pi^4 R^9",
                "\\frac{1}{120} \\pi^5 R^{10}",
                "\\frac{64}{10{,}395} \\pi^5 R^{11}",
                "\\frac{1}{720} \\pi^6 R^{12}",
            ]
        ])

        formulas.arrange(RIGHT, buff=LARGE_BUFF)
        formulas.scale(0.9)
        formulas.to_edge(LEFT)

        lines = VGroup()
        d_labels = VGroup()
        for dim, formula in zip(it.count(1), formulas):
            label = VGroup(Integer(dim), OldTex("D"))
            label.arrange(RIGHT, buff=0, aligned_edge=DOWN)
            label[0].set_color(YELLOW)
            label.move_to(formula)
            label.shift(UP)

            line = Line(UP, DOWN)
            line.set_stroke(WHITE, 1)
            line.next_to(formula, RIGHT, buff=MED_LARGE_BUFF)
            line.shift(0.5 * UP)

            d_labels.add(label)
            lines.add(line)
            # coefs.add(formula[0])
            formula[0].set_color(BLUE_B)
        lines.remove(lines[-1])
        line = Line(formulas.get_left(), formulas.get_right())
        line.set_stroke(WHITE, 1)
        line.next_to(d_labels, DOWN, MED_SMALL_BUFF)
        lines.add(line)

        chart = VGroup(lines, d_labels, formulas)
        chart.save_state()

        self.add(title)
        self.add(d_labels)
        self.add(lines)

        self.play(LaggedStartMap(FadeInFromDown, formulas, run_time=3, lag_ratio=0.1))
        self.play(chart.to_edge, RIGHT, {"buff": MED_SMALL_BUFF}, run_time=5)
        self.wait()
        self.play(Restore(chart))
        self.play(FadeOut(formulas[4:]))

        rect1 = SurroundingRectangle(formulas[2][0][-1])
        rect2 = SurroundingRectangle(formulas[3][0][-2:])
        self.play(ShowCreation(rect1))
        self.play(TransformFromCopy(rect1, rect2))
        self.play(FadeOut(VGroup(rect1, rect2)))

        arrows = VGroup(*[
            Arrow(
                formulas[i].get_bottom(),
                formulas[i + 1].get_bottom(),
                path_arc=150 * DEGREES,
            )
            for i in (1, 2)
        ])

        for arrow in arrows:
            self.play(ShowCreation(arrow))
        self.wait()
        self.play(
            FadeOut(arrows),
            FadeIn(formulas[4:]),
        )

        # General formula for even dimensions
        braces = VGroup(*[
            Brace(formula, DOWN)
            for formula in formulas[1::2]
        ])
        gen_form = OldTex("{\\pi^n \\over n!}", "R^{2n}")
        gen_form[0].set_color(BLUE_B)
        gen_form.scale(1.5)
        gen_form.to_edge(DOWN)

        self.play(
            formulas[::2].set_opacity, 0.25,
            ReplacementTransform(title, alt_title)
        )
        for brace in braces[:3]:
            self.play(GrowFromCenter(brace))
        self.wait()
        self.play(
            FadeOut(braces[:3]),
            FadeIn(gen_form, UP),
        )
        self.wait()
