# ==============================================================================
# Scene:      KeyProperties
# Source:     videos/_2025/laplace/derivative_supplements.py (lines 118-234)
# Category:   1 · Renders unmodified
# Includes code copied from: _2025/laplace/derivatives.py
#
# Run from this folder:
#     manimgl KeyProperties.py KeyProperties -w -m --fps 15
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


class KeyProperties(InteractiveScene):
    def construct(self):
        # Add title
        title = Text("Key Properties", font_size=72)
        title.to_edge(UP, buff=MED_SMALL_BUFF)
        title.set_backstroke(BLACK, 3)
        underline = Underline(title, buff=-0.05)
        underline.scale(1.25)
        self.add(underline, title)

        # Create
        t2c = dict(tex_to_color)
        number_labels = VGroup(Tex(Rf"{n})", font_size=72) for n in range(1, 4))
        number_labels.arrange(DOWN, aligned_edge=LEFT, buff=1.5)
        number_labels.next_to(title, DOWN, LARGE_BUFF)
        number_labels.to_edge(LEFT)

        properties = VGroup(
            get_lt_group(
                Tex(R"e^{a{t}}", t2c=t2c, font_size=60),
                Tex(R"{1 \over {s} - a}", t2c=t2c)
            ),
            get_lt_group(
                Tex(R"a \cdot f({t}) + b \cdot g({t})", t2c=t2c),
                Tex(R"a \cdot F({s}) + b \cdot G({s})", t2c=t2c),
            ),
            get_lt_group(
                Tex(R"f'({t})", t2c=t2c),
                Tex(R"{s} F({s}) - f(0)", t2c=t2c),
            ),
        )
        exp_prop, lin_prop, deriv_prop = properties
        properties.scale(1.25)
        for num, prop in zip(number_labels, properties):
            prop.shift(num.get_right() + MED_SMALL_BUFF * RIGHT - prop[0].get_left())
        exp_prop.shift(SMALL_BUFF * UP)

        # Show first properties
        self.play(
            LaggedStartMap(FadeIn, number_labels[:2], shift=UP, lag_ratio=0.25),
            ShowCreation(underline),
        )
        self.wait()

        self.play(Write(exp_prop[0]))
        self.play(LaggedStart(
            GrowArrow(exp_prop[1]),
            FadeIn(exp_prop[2], 0.25 * RIGHT),
            Transform(exp_prop[0]["a"][0].copy(), exp_prop[3]["a"][0].copy(), remover=True),
            Write(exp_prop[3]),
            lag_ratio=0.5
        ))
        self.wait()

        # Show linearity
        f_rects = VGroup(
            SurroundingRectangle(lin_prop[0]["f({t})"], buff=SMALL_BUFF),
            SurroundingRectangle(lin_prop[3]["F({s})"], buff=SMALL_BUFF),
        )
        g_rects = VGroup(
            SurroundingRectangle(lin_prop[0]["g({t})"], buff=SMALL_BUFF),
            SurroundingRectangle(lin_prop[3]["G({s})"], buff=SMALL_BUFF),
        )
        VGroup(f_rects, g_rects).set_stroke(TEAL, 2)

        self.play(
            Write(lin_prop[0])
        )
        self.play(LaggedStart(
            GrowArrow(lin_prop[1]),
            FadeIn(lin_prop[2], 0.25 * RIGHT),
            TransformMatchingTex(
                lin_prop[0].copy(),
                lin_prop[3],
                key_map={"{t}": "{s}", "f": "F", "g": "G"},
                path_arc=45 * DEG,
                lag_ratio=0.01,
            )
        ))
        self.wait()
        self.play(ShowCreation(f_rects, lag_ratio=0))
        self.wait()
        self.play(ReplacementTransform(f_rects, g_rects, lag_ratio=0))
        self.wait()
        self.play(FadeOut(g_rects))

        # (Edited in, show combination transformed)

        # Show third property
        frame = self.frame
        morty = Mortimer().flip()
        morty.next_to(number_labels[2], DR, LARGE_BUFF)

        self.play(
            VFadeIn(morty),
            morty.change("raise_left_hand", number_labels[2]),
            properties[:2].animate.set_fill(opacity=0.5),
            number_labels[:2].animate.set_fill(opacity=0.5),
            Write(number_labels[2]),
            frame.animate.set_height(12, about_edge=UP)
        )
        self.wait()
        self.play(LaggedStart(
            Write(deriv_prop[0]),
            GrowArrow(deriv_prop[1]),
            FadeIn(deriv_prop[2], 0.25 * RIGHT),
            morty.change("pondering", deriv_prop[0]),
        ))
        self.play(Blink(morty))
        self.wait()
        morty.body.insert_n_curves(500)
        self.play(
            Write(deriv_prop[3]),
            morty.change("raise_right_hand", deriv_prop[3])
        )
        self.play(Blink(morty))
        self.wait()
