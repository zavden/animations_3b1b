# ==============================================================================
# Scene:      CombinationOfExponentials
# Source:     videos/_2025/laplace/derivative_supplements.py (lines 251-283)
# Category:   1 · Renders unmodified
# Includes code copied from: _2025/laplace/derivatives.py
#
# Run from this folder:
#     manimgl CombinationOfExponentials.py CombinationOfExponentials -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *


# ----- From _2025/laplace/derivatives.py -----

tex_to_color = {
    "{t}": BLUE,
    "{s}": YELLOW,
}



# ----- From _2025/laplace/derivative_supplements.py -----

def get_lt_group(src, trg, arrow_length=1.5, arrow_thickness=4, buff=MED_SMALL_BUFF, label_font_size=48):
    arrow = Vector(arrow_length * RIGHT, thickness=arrow_thickness)
    arrow.next_to(src, RIGHT, buff=buff)
    trg.next_to(arrow, RIGHT, buff=buff)

    label = Tex(R"\mathcal{L}", font_size=label_font_size)
    label.next_to(arrow, UP, buff=SMALL_BUFF)

    return VGroup(src, arrow, label, trg)


class CombinationOfExponentials(InteractiveScene):
    def construct(self):
        # Test
        t2c = dict(tex_to_color)
        t2c["c_n"] = TEAL
        kw = dict(t2c=t2c, font_size=72)
        combination = Tex(R"\sum_n c_n e^{a_n{t}}", **kw)
        result = Tex(R"\sum_n {c_n \over {s} - a_n}", **kw)

        group = get_lt_group(
            combination,
            result,
            arrow_length=4,
            label_font_size=60,
            arrow_thickness=6
        )
        group.center()

        self.play(FadeIn(combination, lag_ratio=0.1))
        self.wait()
        self.play(LaggedStart(
            GrowArrow(group[1]),
            FadeIn(group[2], RIGHT),
            *(
                Transform(combination[tex][0].copy(), result[tex][0].copy(), remover=True)
                for tex in ["c_n", "a_n", R"\sum_n"]
            ),
            Write(result[R"\over {s} - "][0]),
            lag_ratio=0.2,
            run_time=2
        ))
        self.add(group)
        self.wait()
