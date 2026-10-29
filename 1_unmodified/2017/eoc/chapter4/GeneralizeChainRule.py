# ==============================================================================
# Scene:      GeneralizeChainRule
# Source:     videos/_2017/eoc/chapter4.py (lines 1865-2080)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl GeneralizeChainRule.py GeneralizeChainRule -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

SINE_COLOR = BLUE


X_SQUARED_COLOR = GREEN


class GeneralizeChainRule(Scene):
    def construct(self):
        example = OldTex(
            "\\frac{d}{dx}", "\\sin(", "x^2", ")", "=",
            "\\cos(", "x^2", ")", "\\,2x",
        )
        general = OldTex(
            "\\frac{d}{dx}", "g(", "h(x)", ")", "=",
            "{dg \\over ", " dh}", "(", "h(x)", ")", "{dh \\over", " dx}", "(x)"
        )
        example.to_edge(UP, buff = LARGE_BUFF)
        example.shift(RIGHT)
        general.next_to(example, DOWN, buff = 1.5*LARGE_BUFF)
        for mob in example, general:
            mob.set_color(SINE_COLOR)
            mob[0].set_color(WHITE)
            for tex in "x^2", "2x", "(x)", "{dh", " dx}":
                mob.set_color_by_tex(tex, X_SQUARED_COLOR, substring = True)

        example_outer = VGroup(*example[1:4])
        example_inner = example[2]
        d_example_outer = VGroup(*example[5:8])
        d_example_inner = example[6]
        d_example_d_inner = example[8]

        general_outer = VGroup(*general[1:4])
        general_inner = general[2]
        d_general_outer = VGroup(*general[5:10])
        d_general_inner = general[8]
        d_general_d_inner = VGroup(*general[10:13])

        example_outer_brace = Brace(example_outer)
        example_inner_brace = Brace(example_inner, UP, buff = SMALL_BUFF)
        d_example_outer_brace = Brace(d_example_outer)
        d_example_inner_brace = Brace(d_example_inner, buff = SMALL_BUFF)
        d_example_d_inner_brace = Brace(d_example_d_inner, UP, buff = SMALL_BUFF)

        general_outer_brace = Brace(general_outer)
        general_inner_brace = Brace(general_inner, UP, buff = SMALL_BUFF)
        d_general_outer_brace = Brace(d_general_outer)
        d_general_inner_brace = Brace(d_general_inner, buff = SMALL_BUFF)
        d_general_d_inner_brace = Brace(d_general_d_inner, UP, buff = SMALL_BUFF)

        for brace in example_outer_brace, general_outer_brace:
            brace.text = brace.get_text("Outer")
        for brace in example_inner_brace, general_inner_brace:
            brace.text = brace.get_text("Inner")
        for brace in d_example_outer_brace, d_general_outer_brace:
            brace.text = brace.get_text("d(Outer)")
            brace.text.shift(SMALL_BUFF*LEFT)
        for brace in d_example_d_inner_brace, d_general_d_inner_brace:
            brace.text = brace.get_text("d(Inner)", buff = SMALL_BUFF)

        #d(out)d(in) for example
        self.add(example)
        braces = VGroup(
            example_outer_brace, 
            example_inner_brace, 
            d_example_outer_brace
        )
        for brace in braces:
            self.play(GrowFromCenter(brace))
            self.play(Write(brace.text, run_time = 1))
            self.wait()
        self.wait()
        self.play(*it.chain(*[
            [mob.scale, 1.2, mob.set_color, YELLOW]
            for mob in (example_inner, d_example_inner)
        ]), rate_func = there_and_back)
        self.play(Transform(
            example_inner.copy(), d_example_inner,
            path_arc = -np.pi/2,
            remover = True
        ))
        self.wait()
        self.play(
            GrowFromCenter(d_example_d_inner_brace),
            Write(d_example_d_inner_brace.text)
        )
        self.play(Transform(
            VGroup(*reversed(example_inner.copy())),
            d_example_d_inner,
            path_arc = -np.pi/2,
            run_time = 2,
            remover = True
        ))
        self.wait()

        #Generalize
        self.play(*list(map(FadeIn, general[:5])))
        self.wait()
        self.play(
            Transform(example_outer_brace, general_outer_brace),
            Transform(example_outer_brace.text, general_outer_brace.text),
            Transform(example_inner_brace, general_inner_brace),
            Transform(example_inner_brace.text, general_inner_brace.text),
        )
        self.wait()
        self.play(
            Transform(d_example_outer_brace, d_general_outer_brace),
            Transform(d_example_outer_brace.text, d_general_outer_brace.text),
        )
        self.play(Write(d_general_outer))
        self.wait(2)
        self.play(
            Transform(d_example_d_inner_brace, d_general_d_inner_brace),
            Transform(d_example_d_inner_brace.text, d_general_d_inner_brace.text),
        )
        self.play(Write(d_general_d_inner))
        self.wait(2)

        #Name chain rule
        name = OldTexText("``Chain rule''")
        name.scale(1.2)
        name.set_color(YELLOW)
        name.to_corner(UP+LEFT)
        self.play(Write(name))
        self.wait()

        #Point out dh bottom
        morty = Mortimer().flip()
        morty.to_corner(DOWN+LEFT)
        d_general_outer_copy = d_general_outer.copy()
        morty.set_fill(opacity = 0)
        self.play(
            morty.set_fill, None, 1,
            morty.change_mode, "raise_left_hand",
            morty.look, UP+LEFT,
            d_general_outer_copy.next_to, 
            morty.get_corner(UP+LEFT), UP, MED_LARGE_BUFF,
            d_general_outer_copy.shift_onto_screen
        )
        self.wait()        
        circle = Circle(color = YELLOW)
        circle.replace(d_general_outer_copy[1])
        circle.scale(1.4)
        self.play(ShowCreation(circle))
        self.play(Blink(morty))
        self.wait()
        inner = d_general_outer_copy[3]
        self.play(
            morty.change_mode, "hooray",
            morty.look_at, inner,
            inner.shift, UP
        )
        self.play(inner.shift, DOWN)
        self.wait()
        self.play(morty.change_mode, "pondering")
        self.play(Blink(morty))
        self.wait()
        self.play(*list(map(FadeOut, [
            d_general_outer_copy, inner, circle
        ])))

        #Show cancelation
        braces = [
            d_example_d_inner_brace,
            d_example_outer_brace,
            example_inner_brace,
            example_outer_brace,
        ]
        texts = [brace.text for brace in braces]
        self.play(*list(map(FadeOut, braces+texts)))

        to_collapse = VGroup(VGroup(*general[7:10]), general[12])
        dg_dh = VGroup(*general[5:7])
        dh_dx = VGroup(*general[10:12])
        to_collapse.generate_target()
        points = VGroup(*list(map(VectorizedPoint, 
            [m.get_left() for m in to_collapse]
        )))
        self.play(
            Transform(to_collapse, points),
            dh_dx.next_to, dg_dh,
            morty.look_at, dg_dh,
        )
        self.wait()
        for mob in list(dg_dh)+list(dh_dx):
            circle = Circle(color = YELLOW)
            circle.replace(mob)
            circle.scale(1.3)
            self.play(ShowCreation(circle))
            self.wait()
            self.play(FadeOut(circle))

        strikes = VGroup()
        for dh in dg_dh[1], dh_dx[0]:
            strike = OldTex("/")
            strike.stretch(2, dim = 0)
            strike.rotate(-np.pi/12)
            strike.move_to(dh)
            strike.set_color(RED)
            strikes.add(strike)
        self.play(Write(strikes))
        self.play(morty.change_mode, "hooray")
        equals_dg_dx = OldTex("= \\frac{dg}{dx}")
        equals_dg_dx.next_to(dh_dx)
        self.play(Write(equals_dg_dx))
        self.play(Blink(morty))
        self.wait(2)

        ##More than a notational trick
        self.play(
            PiCreatureSays(morty, """
                This is more than a
                notational trick
            """),
            VGroup(
                dg_dh, dh_dx, equals_dg_dx, strikes,
                *general[:5]
            ).shift, DOWN,
            FadeOut(example)
        )
        self.wait()
        self.play(Blink(morty))
        self.wait()
