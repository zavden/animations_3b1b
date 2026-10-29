# ==============================================================================
# Scene:      NudgeSideLengthOfSquare
# Source:     videos/_2017/eoc/chapter3.py (lines 362-775)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl NudgeSideLengthOfSquare.py NudgeSideLengthOfSquare -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - in Cairo Scene.__init__ ran construct(); GL needs cairo_nested_scene(Class, **kw) to build a scene inside another
# ==============================================================================

from manim_imports_ext import *

class NudgeSideLengthOfSquare(PiCreatureScene):
    CONFIG = {
        "square_width" : 3,
        "alt_square_width" : 5,
        "dx" : 0.25,
        "alt_dx" : 0.01,
        "square_color" : GREEN,
        "square_fill_opacity" : 0.75,
        "three_color" : GREEN,
        "dx_color" : BLUE_B,
        "is_recursing_on_dx" : False,
        "is_recursing_on_square_width" : False,
    }
    def construct(self):
        ApplyMethod(self.pi_creature.change_mode, "speaking").update(1)
        self.add_function_label()
        self.introduce_square()
        self.increase_area()
        self.write_df_equation()
        self.set_color_shapes()
        self.examine_thin_rectangles()
        self.examine_tiny_square()
        self.show_smaller_dx()
        self.rule_of_thumb()
        self.write_out_derivative()

    def add_function_label(self):
        label = OldTex("f(x) = x^2")
        label.next_to(ORIGIN, RIGHT, buff = (self.square_width-3)/2.)
        label.to_edge(UP)
        self.add(label)
        self.function_label = label

    def introduce_square(self):
        square = Square(
            side_length = self.square_width,
            stroke_width = 0,
            fill_opacity = self.square_fill_opacity,
            fill_color = self.square_color,
        )
        square.to_corner(UP+LEFT, buff = LARGE_BUFF)
        x_squared = OldTex("x^2")
        x_squared.move_to(square)

        braces = VGroup()
        for vect in RIGHT, DOWN:
            brace = Brace(square, vect)
            text = brace.get_text("$x$")
            brace.add(text)
            braces.add(brace)

        self.play(
            DrawBorderThenFill(square),
            self.pi_creature.change_mode, "plain"
        )
        self.play(*list(map(GrowFromCenter, braces)))
        self.play(Write(x_squared))
        self.change_mode("pondering")
        self.wait()

        self.square = square
        self.side_braces = braces

    def increase_area(self):
        color_kwargs = {
            "fill_color" : YELLOW,
            "fill_opacity" : self.square_fill_opacity,
            "stroke_width" : 0,
        }
        right_rect = Rectangle(
            width = self.dx,
            height = self.square_width,
            **color_kwargs
        )
        bottom_rect = right_rect.copy().rotate(-np.pi/2)
        right_rect.next_to(self.square, RIGHT, buff = 0)
        bottom_rect.next_to(self.square, DOWN, buff = 0)
        corner_square = Square(
            side_length = self.dx,
            **color_kwargs
        )
        corner_square.next_to(self.square, DOWN+RIGHT, buff = 0)

        right_line = Line(
            self.square.get_corner(UP+RIGHT),
            self.square.get_corner(DOWN+RIGHT),
            stroke_width = 0
        )
        bottom_line = Line(
            self.square.get_corner(DOWN+RIGHT),
            self.square.get_corner(DOWN+LEFT),
            stroke_width = 0
        )
        corner_point = VectorizedPoint(
            self.square.get_corner(DOWN+RIGHT)
        )

        little_braces = VGroup()
        for vect in RIGHT, DOWN:
            brace = Brace(
                corner_square, vect, 
                buff = SMALL_BUFF,
            )
            text = brace.get_text("$dx$", buff = SMALL_BUFF)
            text.set_color(self.dx_color)
            brace.add(text)
            little_braces.add(brace)

        right_brace, bottom_brace = self.side_braces
        self.play(
            Transform(right_line, right_rect),
            Transform(bottom_line, bottom_rect),
            Transform(corner_point, corner_square),
            right_brace.next_to, right_rect, RIGHT, SMALL_BUFF,
            bottom_brace.next_to, bottom_rect, DOWN, SMALL_BUFF,
        )
        self.remove(corner_point, bottom_line, right_line)
        self.add(corner_square, bottom_rect, right_rect)
        self.play(*list(map(GrowFromCenter, little_braces)))
        self.wait()
        self.play(*it.chain(*[
            [mob.shift, vect*SMALL_BUFF]
            for mob, vect in [
                (right_rect, RIGHT),
                (bottom_rect, DOWN),
                (corner_square, DOWN+RIGHT),
                (right_brace, RIGHT),
                (bottom_brace, DOWN),
                (little_braces, DOWN+RIGHT)
            ]
        ]))
        self.change_mode("thinking")
        self.wait()
        self.right_rect = right_rect
        self.bottom_rect = bottom_rect
        self.corner_square = corner_square
        self.little_braces = little_braces

    def write_df_equation(self):
        right_rect = self.right_rect
        bottom_rect = self.bottom_rect
        corner_square = self.corner_square

        df_equation = VGroup(
            OldTex("df").set_color(right_rect.get_color()),
            OldTex("="),
            right_rect.copy(),
            OldTexText("+"),
            right_rect.copy(),
            OldTex("+"),
            corner_square.copy()
        )
        df_equation.arrange()
        df_equation.next_to(
            self.function_label, DOWN, 
            aligned_edge = LEFT,
            buff = SMALL_BUFF
        )
        df, equals, r1, plus1, r2, plus2, s = df_equation

        pairs = [
            (df, self.function_label[0]),
            (r1, right_rect), 
            (r2, bottom_rect), 
            (s, corner_square),
        ]
        for mover, origin in pairs:
            mover.save_state()
            Transform(mover, origin).update(1)
        self.play(df.restore)
        self.wait()
        self.play(
            *[
                mob.restore
                for mob in (r1, r2, s)
            ]+[
                Write(symbol)
                for symbol in (equals, plus1, plus2)
            ], 
            run_time = 2
        )
        self.change_mode("happy")
        self.wait()

        self.df_equation = df_equation

    def set_color_shapes(self):
        df, equals, r1, plus1, r2, plus2, s = self.df_equation

        tups = [
            (self.right_rect, self.bottom_rect, r1, r2),
            (self.corner_square, s)
        ]
        for tup in tups:
            self.play(
                *it.chain(*[
                    [m.scale, 1.2, m.set_color, RED]
                    for m in tup
                ]), 
                rate_func = there_and_back
            )
            self.wait()

    def examine_thin_rectangles(self):
        df, equals, r1, plus1, r2, plus2, s = self.df_equation

        rects = VGroup(r1, r2)
        thin_rect_brace = Brace(rects, DOWN)
        text = thin_rect_brace.get_text("$2x \\, dx$")
        VGroup(*text[-2:]).set_color(self.dx_color)
        text.save_state()
        alt_text = thin_rect_brace.get_text("$2(3)(0.01)$")
        alt_text[2].set_color(self.three_color)
        VGroup(*alt_text[-5:-1]).set_color(self.dx_color)

        example_value = OldTex("=0.06")
        example_value.next_to(alt_text, DOWN)

        self.play(GrowFromCenter(thin_rect_brace))
        self.play(
            Write(text),
            self.pi_creature.change_mode, "pondering"
        )
        self.wait()

        xs = VGroup(*[
            brace[-1] 
            for brace in self.side_braces
        ])
        dxs = VGroup(*[
            brace[-1]
            for brace in self.little_braces
        ])
        for group, tex, color in (xs, "3", self.three_color), (dxs, "0.01", self.dx_color):
            group.save_state()            
            group.generate_target()            
            for submob in group.target:
                number = OldTex(tex)
                number.set_color(color)
                number.move_to(submob, LEFT)
                Transform(submob, number).update(1)
        self.play(MoveToTarget(xs))
        self.play(MoveToTarget(dxs))
        self.wait()
        self.play(Transform(text, alt_text))
        self.wait()
        self.play(Write(example_value))
        self.wait()
        self.play(
            FadeOut(example_value),
            *[
                mob.restore
                for mob in (xs, dxs, text)
            ]
        )
        self.remove(text)
        text.restore()
        self.add(text)

        self.wait()
        self.dxs = dxs
        self.thin_rect_brace = thin_rect_brace
        self.thin_rect_area = text        

    def examine_tiny_square(self):
        text = OldTex("dx^2")
        VGroup(*text[:2]).set_color(self.dx_color)
        text.next_to(self.df_equation[-1], UP)
        text.save_state()
        alt_text = OldTexText("0.0001")
        alt_text.move_to(text)

        self.play(Write(text))
        self.change_mode("surprised")
        self.wait()
        self.play(
            MoveToTarget(self.dxs),
            self.pi_creature.change_mode, "plain"
        )
        for submob in self.dxs.target:
            number = OldTex("0.01")
            number.set_color(self.dx_color)
            number.move_to(submob, LEFT)
            Transform(submob, number).update(1)
        self.play(MoveToTarget(self.dxs))
        self.play(
            Transform(text, alt_text),
            self.pi_creature.change_mode, "raise_right_hand"
        )
        self.wait(2)
        self.play(*[
            mob.restore
            for mob in (self.dxs, text)
        ] + [
            self.pi_creature.change_mode, "erm"
        ])
        self.dx_squared = text

    def show_smaller_dx(self):
        self.mobjects_at_start_of_show_smaller_dx = [
            mob.copy() for mob in self.get_mobjects()
        ]
        if self.is_recursing_on_dx:
            return

        # CHANGE: in Cairo Scene.__init__ ran construct(); GL needs cairo_nested_scene(Class, **kw) to build a scene inside another
        alt_scene = cairo_nested_scene(self.__class__,
            skip_animations = True,
            dx = self.alt_dx,
            is_recursing_on_dx = True
        )
        for mob in self.get_mobjects():
            mob.save_state()
        self.play(*[
            Transform(*pair)
            for pair in zip(
                self.get_mobjects(),
                alt_scene.mobjects_at_start_of_show_smaller_dx,
            )
        ])
        self.wait()
        self.play(*[
            mob.restore
            for mob in self.get_mobjects()
        ])
        self.change_mode("happy")
        self.wait()

    def rule_of_thumb(self):
        circle = Circle(color = RED)
        dx_squared_group = VGroup(self.dx_squared, self.df_equation[-1])
        circle.replace(dx_squared_group, stretch = True)
        dx_squared_group.add(self.df_equation[-2])
        circle.scale(1.5)
        safe_to_ignore = OldTexText("Safe to ignore")
        safe_to_ignore.next_to(circle, DOWN, aligned_edge = LEFT)
        safe_to_ignore.set_color(circle.get_color())

        self.play(ShowCreation(circle))
        self.play(
            Write(safe_to_ignore, run_time = 2),
            self.pi_creature.change_mode, "raise_right_hand"
        )
        self.play(
            FadeOut(circle),
            FadeOut(safe_to_ignore),
            dx_squared_group.fade, 0.5,
            dx_squared_group.to_corner, UP+RIGHT,
            self.pi_creature.change_mode, "plain"
        )
        self.wait()

    def write_out_derivative(self):
        df, equals, r1, plus1, r2, plus2, s = self.df_equation
        frac_line = OldTex("-")
        frac_line.stretch_to_fit_width(df.get_width())
        frac_line.move_to(df)
        dx = VGroup(*self.thin_rect_area[-2:]) 
        x = self.thin_rect_area[1]

        self.play(
            Transform(r1, self.right_rect),
            Transform(r2, self.bottom_rect),
            FadeOut(plus1),
            FadeOut(self.thin_rect_brace)
        )
        self.play(
            self.thin_rect_area.next_to, VGroup(df, equals),
            RIGHT, MED_SMALL_BUFF, UP,
            self.pi_creature.change_mode, "thinking"
        )
        self.wait(2)
        self.play(
            ApplyMethod(df.next_to, frac_line, UP, SMALL_BUFF),
            ApplyMethod(dx.next_to, frac_line, DOWN, SMALL_BUFF),
            Write(frac_line),            
            path_arc = -np.pi
        )
        self.wait()

        brace_xs = [
            brace[-1]
            for brace in self.side_braces
        ]
        xs = list(brace_xs) + [x]
        for x_mob in xs:
            number = OldTex("(%d)"%self.square_width)
            number.move_to(x_mob, LEFT)
            number.shift(
                (x_mob.get_bottom()[1] - number[1].get_bottom()[1])*UP
            )
            x_mob.save_state()
            x_mob.target = number
        self.play(*list(map(MoveToTarget, xs)))
        self.wait(2)

        #Recursively transform to what would have happened
        #with a wider square width
        self.mobjects_at_end_of_write_out_derivative = self.get_mobjects()
        if self.is_recursing_on_square_width or self.is_recursing_on_dx:
            return
        # CHANGE: in Cairo Scene.__init__ ran construct(); GL needs cairo_nested_scene(Class, **kw) to build a scene inside another
        alt_scene = cairo_nested_scene(self.__class__,
            skip_animations = True,
            square_width = self.alt_square_width,
            is_recursing_on_square_width = True,
        )
        self.play(*[
            Transform(*pair)
            for pair in zip(
                self.mobjects_at_end_of_write_out_derivative,
                alt_scene.mobjects_at_end_of_write_out_derivative
            )
        ])
        self.change_mode("happy")
        self.wait(2)
