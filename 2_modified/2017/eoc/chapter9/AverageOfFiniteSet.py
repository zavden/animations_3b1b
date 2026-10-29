# ==============================================================================
# Scene:      AverageOfFiniteSet
# Source:     videos/_2017/eoc/chapter9.py (lines 358-439)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl AverageOfFiniteSet.py AverageOfFiniteSet -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Grant's repo renamed TexMobject->Tex here (new GL class); the 2017 code needs the Cairo-style OldTex
# ==============================================================================

from manim_imports_ext import *

class AverageOfFiniteSet(Scene):
    CONFIG = {
        "lengths" : [1, 4, 2, 5]
    }
    def construct(self):
        lengths = self.lengths
        lines = VGroup(*[
            Line(ORIGIN, length*RIGHT)
            for length in lengths
        ])
        colors = Color(BLUE).range_to(RED, len(lengths))
        lines.set_color_by_gradient(*colors)
        lines.arrange(RIGHT)
        lines.generate_target()
        lines.target.arrange(RIGHT, buff = 0)
        for mob in lines, lines.target:
            mob.shift(UP)
        brace = Brace(lines.target, UP)

        labels = VGroup(*[
            OldTex(str(d)).next_to(line, UP).set_color(line.get_color())
            for d, line in zip(lengths, lines)
        ])
        # CHANGE: Grant's repo renamed TexMobject->Tex here (new GL class); the 2017 code needs the Cairo-style OldTex
        plusses = [OldTex("+") for x in range(len(lengths)-1)]
        symbols = VGroup(*
            # CHANGE: Grant's repo renamed TexMobject->Tex here (new GL class); the 2017 code needs the Cairo-style OldTex
            plusses + [OldTex("=")]
        )
        symbols.set_fill(opacity = 0)

        labels.generate_target()
        symbols.generate_target()
        symbols.target.set_fill(opacity = 1)
        sum_eq = VGroup(*it.chain(*list(zip(labels.target, symbols.target))))
        sum_eq.arrange(RIGHT)
        sum_eq.next_to(brace, UP)

        sum_mob = OldTex(str(sum(lengths)))
        sum_mob.next_to(sum_eq, RIGHT)

        dividing_lines = VGroup(*[
            DashedLine(p + MED_SMALL_BUFF*UP, p + MED_LARGE_BUFF*DOWN)
            for alpha in np.linspace(0, 1, len(lengths)+1)
            for p in [interpolate(
                lines.target.get_left(),
                lines.target.get_right(),
                alpha
            )]
        ])

        lower_braces = VGroup(*[
            Brace(VGroup(*dividing_lines[i:i+2]), DOWN)
            for i in range(len(lengths))
        ])
        averages = VGroup(*[
            lb.get_text("$%d/%d$"%(sum(lengths), len(lengths)))
            for lb in lower_braces
        ])
        circle = Circle(color = YELLOW)
        circle.replace(averages[1], stretch = True)
        circle.scale(1.5)

        self.add(lines)
        self.play(FadeIn(
            labels,
            lag_ratio = 0.5,
            run_time = 3
        ))
        self.wait()
        self.play(
            GrowFromCenter(brace),
            *list(map(MoveToTarget, [lines, labels, symbols])),
            run_time = 2
        )
        self.play(Write(sum_mob))
        self.wait()
        self.play(ShowCreation(dividing_lines, run_time = 2))
        self.play(*it.chain(
            list(map(Write, averages)),
            list(map(GrowFromCenter, lower_braces))
        ))
        self.play(ShowCreation(circle))
        self.wait(2)
