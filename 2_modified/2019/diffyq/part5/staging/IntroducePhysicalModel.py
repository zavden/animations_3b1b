# ==============================================================================
# Scene:      IntroducePhysicalModel
# Source:     videos/_2019/diffyq/part5/staging.py (lines 146-506)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl IntroducePhysicalModel.py IntroducePhysicalModel -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Align the first glyph of tip_label with submobject_to_align: the tip has no indexable submobjects.
# ==============================================================================

from manim_imports_ext import *

T_COLOR = GREY_B


VELOCITY_COLOR = GREEN


POSITION_COLOR = BLUE


CONST_COLOR = YELLOW


tex_config = {
    "tex_to_color_map": {
        "{t}": T_COLOR,
        "{0}": T_COLOR,
        "e^": WHITE,
        "=": WHITE,
    }
}


class IntroductionOfExp(Scene):
    def construct(self):
        questions = VGroup(
            OldTexText("What", "is", "$e^{t}$", "?"),
            OldTexText("What", "properties", "does", "$e^{t}$", "have?"),
            OldTexText(
                "What", "property", "defines", "$e^{t}$", "?",
                tex_to_color_map={"defines": BLUE}
            ),
        )
        questions.scale(2)
        questions[0].next_to(questions[1], UP, LARGE_BUFF)
        questions[2][-1].next_to(questions[2][-2], RIGHT, SMALL_BUFF)
        questions.to_edge(UP)
        for question in questions:
            part = question.get_part_by_tex("e^{t}")
            part[1].set_color(T_COLOR)

        top_cross = Cross(questions[0])

        deriv_ic = self.get_deriv_and_ic()
        deriv_ic.save_state()
        deriv_ic.scale(2 / 1.5)
        deriv_ic.to_edge(DOWN, buff=LARGE_BUFF)
        derivative, ic = deriv_ic
        derivative.save_state()
        derivative.set_x(0)

        self.play(FadeInFromDown(questions[0]))
        self.wait()
        self.play(
            ShowCreation(top_cross),
            LaggedStart(
                *[
                    TransformFromCopy(
                        questions[0].get_part_by_tex(tex),
                        questions[1].get_part_by_tex(tex),
                    )
                    for tex in ("What", "e^{t}")
                ],
                *[
                    FadeIn(questions[1][i])
                    for i in [1, 2, 4]
                ]
            )
        )
        self.wait()
        self.play(
            TransformFromCopy(
                questions[1].get_part_by_tex("$e^{t}$"),
                derivative[3:7],
            ),
            FadeIn(derivative[:2]),
            FadeIn(derivative.get_part_by_tex("=")),
        )
        self.play(
            ReplacementTransform(
                questions[1][0],
                questions[2][0],
            ),
            FadeOut(questions[1][1]),
            FadeIn(questions[2][1]),
            FadeOut(questions[1][2]),
            FadeIn(questions[2][2]),
            ReplacementTransform(
                questions[1][3],
                questions[2][3],
            ),
            FadeOut(questions[1][4]),
            FadeIn(questions[2][4]),
        )
        self.wait()
        self.play(
            TransformFromCopy(
                derivative[3:7:3],
                derivative[-5:],
                path_arc=-60 * DEGREES,
            ),
        )
        self.wait()
        self.play(
            Restore(derivative),
            FadeIn(ic, LEFT)
        )
        self.wait()
        self.play(
            FadeOut(questions[0]),
            FadeOut(top_cross),
            FadeOut(questions[2]),
            Restore(deriv_ic),
        )
        self.wait()

    def get_deriv_and_ic(self, const=None):
        if const:
            const_str = "{" + str(const) + "}"
            mult_str = "\\cdot"
        else:
            const_str = "{}"
            mult_str = "{}"
        args = [
            "{d \\over d{t}}",
            "e^{",
            const_str,
            "{t}}",
            "=",
            const_str,
            mult_str,
            "e^{",
            const_str,
            "{t}}"
        ]
        derivative = OldTex(
            *args,
            **tex_config
        )
        if const:
            derivative.set_color_by_tex(const_str, CONST_COLOR)

        ic = OldTex("e^{0} = 1", **tex_config)
        group = VGroup(derivative, ic)
        group.arrange(RIGHT, buff=LARGE_BUFF)
        ic.align_to(derivative.get_part_by_tex("e^"), DOWN)
        group.scale(1.5)
        group.to_edge(UP)
        return group


class IntroducePhysicalModel(IntroductionOfExp):
    CONFIG = {
        "number_line_config": {
            "x_min": 0,
            "x_max": 100,
            "unit_size": 1.5,
            "big_tick_numbers": [0],
            "numbers_to_show": list(range(0, 15)),
            "label_direction": UP,
        },
        "number_line_y": -2,
        "const": 1,
        "const_str": "",
        "num_decimal_places": 2,
        "output_label_config": {
            "show_ellipsis": True,
        },
    }

    def construct(self):
        self.setup_number_line()
        self.setup_movers()
        self.show_number_line()
        self.show_formulas()
        self.let_time_pass()

    def setup_number_line(self):
        nl = self.number_line = NumberLine(
            **self.number_line_config,
        )
        nl.to_edge(LEFT)
        nl.set_y(self.number_line_y)
        nl.add_numbers()

    def setup_movers(self):
        self.setup_value_trackers()
        self.setup_vectors()
        self.setup_vector_labels()
        self.setup_tip()
        self.setup_tip_label()
        self.setup_output_label()

    def setup_value_trackers(self):
        number_line = self.number_line

        input_tracker = ValueTracker(0)
        get_input = input_tracker.get_value

        def complex_number_to_point(z):
            zero = number_line.n2p(0)
            unit = number_line.n2p(1) - zero
            perp = rotate_vector(unit, TAU / 4)
            z = complex(z)
            return zero + unit * z.real + perp * z.imag

        number_line.cn2p = complex_number_to_point

        def get_output():
            return np.exp(self.const * get_input())

        def get_output_point():
            return number_line.n2p(get_output())

        output_tracker = ValueTracker(1)
        output_tracker.add_updater(
            lambda m: m.set_value(get_output())
        )

        self.get_input = get_input
        self.get_output = get_output
        self.get_output_point = get_output_point

        self.add(
            input_tracker,
            output_tracker,
        )
        self.input_tracker = input_tracker
        self.output_tracker = output_tracker

    def setup_tip(self):
        tip = ArrowTip(start_angle=-PI / 2)
        tip.set_height(0.6)
        tip.set_width(0.1, stretch=True)
        tip.add_updater(lambda m: m.move_to(
            self.get_output_point(), DOWN
        ))
        # tip.set_color(WHITE)
        tip.set_fill(GREY, 1)

        self.tip = tip

    def setup_tip_label(self):
        tip = self.tip
        const_str = self.const_str
        ndp = self.num_decimal_places

        args = ["e^{"]
        if const_str:
            args += [const_str, "\\cdot"]
        args += ["0." + ndp * "0"]

        tip_label = OldTex(*args, arg_separator="")
        if const_str:
            tip_label[1].set_color(CONST_COLOR)

        template_decimal = tip_label[-1]
        # parens = tip_label[-3::2]
        template_decimal.set_opacity(0)
        tip_label.add_updater(lambda m: m.next_to(
            tip, UP,
            buff=2 * SMALL_BUFF,
            # CHANGE: align the first glyph of the label, not a submobject of the tip.
            submobject_to_align=m[0]
        ))
        decimal = DecimalNumber(num_decimal_places=ndp)
        decimal.set_color(T_COLOR)
        decimal.match_height(template_decimal)
        decimal.add_updater(lambda m: m.set_value(self.get_input()))
        decimal.add_updater(
            lambda m: m.move_to(template_decimal, LEFT)
        )
        tip_label.add(decimal)

        self.tip_label = tip_label

    def setup_output_label(self):
        label = VGroup(
            OldTex("="),
            DecimalNumber(1, **self.output_label_config)
        )
        label.set_color(POSITION_COLOR)
        label.add_updater(
            lambda m: m[1].set_value(
                self.get_output()
            )
        )
        label.add_updater(
            lambda m: m.arrange(RIGHT, buff=SMALL_BUFF)
        )
        label.add_updater(
            lambda m: m.next_to(
                self.tip_label, RIGHT,
                buff=SMALL_BUFF,
                aligned_edge=DOWN,
            )
        )

        self.output_label = label

    def setup_vectors(self):
        number_line = self.number_line

        position_vect = Vector(color=POSITION_COLOR)
        velocity_vect = Vector(color=VELOCITY_COLOR)

        position_vect.add_updater(
            lambda m: m.put_start_and_end_on(
                number_line.cn2p(0),
                number_line.cn2p(self.get_output()),
            )
        )

        def update_velocity_vect(vect):
            vect.put_start_and_end_on(
                number_line.cn2p(0),
                number_line.cn2p(self.const * self.get_output())
            )
            vect.shift(
                number_line.cn2p(self.get_output()) - number_line.n2p(0)
            )
            return vect

        velocity_vect.add_updater(update_velocity_vect)

        self.position_vect = position_vect
        self.velocity_vect = velocity_vect

    def setup_vector_labels(self):
        position_vect = self.position_vect
        velocity_vect = self.velocity_vect

        max_width = 1.5
        p_label = OldTexText("Position")
        p_label.set_color(POSITION_COLOR)
        p_label.vect = position_vect
        v_label = OldTexText("Velocity")
        v_label.set_color(VELOCITY_COLOR)
        v_label.vect = velocity_vect

        # for label in [p_label, v_label]:
        #     label.add_background_rectangle()

        def update_label(label):
            label.set_width(min(
                max_width,
                0.8 * label.vect.get_length(),
            ))
            direction = normalize(label.vect.get_vector())
            perp_direction = rotate_vector(direction, -TAU / 4)
            label.next_to(
                label.vect.get_center(),
                np.round(perp_direction),
                buff=MED_SMALL_BUFF,
            )
        p_label.add_updater(update_label)
        v_label.add_updater(update_label)

        self.position_label = p_label
        self.velocity_label = v_label

    def show_number_line(self):
        number_line = self.number_line
        self.play(
            LaggedStartMap(
                FadeIn,
                number_line.numbers.copy(),
                remover=True,
            ),
            Write(number_line),
            run_time=2
        )
        self.wait()

    def show_formulas(self):
        deriv, ic = self.get_deriv_and_ic()
        eq_index = deriv.index_of_part_by_tex("=")
        lhs = deriv[:eq_index - 1]
        rhs = deriv[eq_index + 1:]

        rhs_rect = SurroundingRectangle(rhs)
        lhs_rect = SurroundingRectangle(lhs)
        rects = VGroup(rhs_rect, lhs_rect)
        rhs_rect.set_stroke(POSITION_COLOR, 2)
        lhs_rect.set_stroke(VELOCITY_COLOR, 2)

        rhs_word = OldTexText("Position")
        lhs_word = OldTexText("Velocity")
        words = VGroup(rhs_word, lhs_word)
        for word, rect in zip(words, rects):
            word.match_color(rect)
            word.next_to(rect, DOWN)

        self.add(deriv, ic)

        self.play(
            ShowCreation(rhs_rect),
            FadeIn(rhs_word, UP),
            ShowCreation(self.position_vect)
        )
        self.add(
            self.tip,
            self.number_line,
            self.position_vect,
        )
        self.number_line.numbers.set_stroke(BLACK, 3, background=True)
        self.play(
            Transform(
                rhs.copy(),
                self.tip_label.copy().clear_updaters(),
                remover=True,
            ),
            GrowFromPoint(self.tip, rhs.get_bottom()),
            TransformFromCopy(rhs_word, self.position_label),
        )
        self.add(self.tip_label)
        self.wait()
        self.play(
            ShowCreation(lhs_rect),
            FadeIn(lhs_word, UP),
        )
        self.wait()
        self.play(
            TransformFromCopy(
                self.position_vect,
                self.velocity_vect,
                path_arc=PI,
            )
        )
        self.play(
            TransformFromCopy(
                lhs_word,
                self.velocity_label,
            )
        )
        self.wait()

    def let_time_pass(self):
        # Sort of a quick and dirty implementation,
        # not the best for reusability

        rate = 0.25
        t_tracker = self.input_tracker
        t_tracker.add_updater(
            lambda m, dt: m.increment_value(rate * dt)
        )

        nl = self.number_line
        zero_point = nl.n2p(0)

        nl_copy = nl.copy()
        nl_copy.submobjects = []
        nl_copy.stretch(100, 0, about_point=zero_point)
        nl.add(nl_copy)

        # For first zoom
        xs1 = range(25, 100, 25)
        nl.add(*[
            nl.get_tick(x, size=1.5)
            for x in xs1
        ])
        nl.add_numbers(
            *xs1,
            buff=2,
            height=5,
        )

        # For second zoom
        xs2 = range(200, 1000, 200)
        nl.add(*[
            nl.get_tick(x, size=15)
            for x in xs2
        ])
        nl.add_numbers(
            *xs2,
            height=50,
            buff=20,
        )

        # For third zoom
        xs3 = range(2000, 10000, 2000)
        nl.add(*[
            nl.get_tick(x, size=150)
            for x in xs3
        ])
        nl.add_numbers(
            *xs3,
            height=300,
            buff=200,
        )
        for n in nl.numbers:
            n[1].scale(0.5)

        self.add(self.tip)

        self.add(self.output_label)
        self.play(VFadeIn(self.output_label))
        self.wait(5)
        self.play(
            nl.scale, 0.1, {"about_point": zero_point},
            run_time=1,
        )
        self.wait(6)
        self.play(
            nl.scale, 0.1, {"about_point": zero_point},
            run_time=1,
        )
        self.wait(8)
        self.play(
            nl.scale, 0.1, {"about_point": zero_point},
            run_time=1,
        )
        self.wait(12)
