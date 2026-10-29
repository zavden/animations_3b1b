# ==============================================================================
# Scene:      IntroduceHamilton
# Source:     videos/_2018/quaternions.py (lines 536-632)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl IntroduceHamilton.py IntroduceHamilton -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class IntroduceHamilton(Scene):
    def construct(self):
        hamilton = ImageMobject("Hamilton", height=6)
        hamilton.to_corner(UL)
        shamrock = SVGMobject(file_name="shamrock")
        shamrock.set_height(1)
        shamrock.set_color("#009a49")
        shamrock.set_fill(opacity=0.25)
        shamrock.next_to(hamilton.get_corner(UL), DR)
        shamrock.align_to(hamilton, UP)
        hamilton_name = OldTexText(
            "William Rowan Hamilton"
        )
        hamilton_name.match_width(hamilton)
        hamilton_name.next_to(hamilton, DOWN)

        quote = OldTexText(
            """\\huge ...Every morning in the early part of the above-cited
            month, on my coming down to breakfast, your (then)
            little brother William Edwin, and yourself, used to
            ask me,""",
            "``Well, Papa, can you multiply triplets''?",
            """Whereto I was always obliged to reply, with a sad
            shake of the head: ``No, I can only add and subtract
            them.''...""",
            alignment=""
        )
        quote.set_color_by_tex("Papa", YELLOW)
        quote = VGroup(*it.chain(*quote))
        quote.set_width(FRAME_WIDTH - hamilton.get_width() - 2)
        quote.to_edge(RIGHT)
        quote_rect = SurroundingRectangle(quote, buff=MED_SMALL_BUFF)
        quote_rect.set_stroke(WHITE, 2)
        quote_rect.stretch(1.1, 1)
        quote_label = OldTexText(
            "August 5, 1865 Letter\\\\from Hamilton to his son"
        )
        quote_label.next_to(quote_rect, UP)
        quote_label.set_color(BLUE)
        VGroup(quote, quote_rect, quote_label).to_edge(UP)

        plaque = ImageMobject("BroomBridgePlaque")
        plaque.set_width(FRAME_WIDTH / 2)
        plaque.to_edge(LEFT)
        plaque.shift(UP)
        equation = OldTex(
            "i^2 = j^2 = k^2 = ijk = -1",
            tex_to_color_map={"i": GREEN, "j": RED, "k": BLUE}
        )
        equation_rect = Rectangle(width=3.25, height=0.7)
        equation_rect.move_to(3.15 * LEFT + 0.25 * DOWN)
        equation_rect.set_color(WHITE)
        equation_arrow = Vector(DOWN)
        equation_arrow.match_color(equation_rect)
        equation_arrow.next_to(equation_rect, DOWN)
        equation.next_to(equation_arrow, DOWN)

        self.play(
            FadeInFromDown(hamilton),
            Write(hamilton_name),
        )
        self.play(DrawBorderThenFill(shamrock))
        self.wait()

        self.play(
            LaggedStartMap(
                FadeIn, quote,
                lag_ratio=0.2,
                run_time=4
            ),
            FadeInFromDown(quote_label),
            ShowCreation(quote_rect)
        )
        self.wait(3)
        self.play(
            ApplyMethod(
                VGroup(hamilton, shamrock, hamilton_name).to_edge, RIGHT,
                run_time=2,
                rate_func=squish_rate_func(smooth, 0.5, 1),
            ),
            LaggedStartMap(
                FadeOutAndShiftDown, VGroup(*it.chain(
                    quote, quote_rect, quote_label
                ))
            )
        )
        self.wait()
        self.play(FadeIn(plaque))
        self.play(
            ShowCreation(equation_rect),
            GrowArrow(equation_arrow)
        )
        self.play(ReplacementTransform(
            equation.copy().replace(equation_rect).fade(1),
            equation
        ))
        self.wait()
