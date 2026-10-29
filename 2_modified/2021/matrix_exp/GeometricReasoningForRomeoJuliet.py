# ==============================================================================
# Scene:      GeometricReasoningForRomeoJuliet
# Source:     videos/_2021/matrix_exp.py (lines 4486-4665)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl GeometricReasoningForRomeoJuliet.py GeometricReasoningForRomeoJuliet -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Arrow(..., thickness=X) -> FillArrow(...): the thickness in the 2021 code is in scene units and the current Arrow multiplies it by 0.015 (invisible arrows).
#   - Matrix/DecimalMatrix: `element_to_mobject_config` no longer exists: Matrix uses `element_config`; DecimalMatrix uses `num_decimal_places=` and `decimal_config=`.
#   - get_romeo_juilet_name_labels(lovers) -> self.get_romeo_juilet_name_labels(lovers): `self.` was missing (NameError in the original).
#   - pi_creature.deepcopy().change(mode) -> .change_mode(mode): since 2022 PiCreature.change returns an animation; here the immediate change is needed.
#   - OldTex/OldTexText with {{ }}: manimgl removed that convention (Apr 2021) and no longer splits the text into parts; the double braces are removed and isolate=[...] is passed with the same pieces.
#   - make_character_dynamic: temporary copies are aligned (not the permanent ones nor pi) and pi takes the data from copy1 with become() before interpolating: manimgl's VMobject alignment (double stroke for missing subpaths, since 2023) inflated the mouth points and failed with ValueError.
#   - self.play(..., path_arc=...) and self.play(mob.method, args, ...): Scene.play no longer accepts path_arc or uncalled methods; mob.animate(path_arc=...).method(args) is used.
#   - arrow.character.scale.number_line -> arrow.character.scale_mob.number_line: the attribute is called scale_mob (AttributeError in the original: scale is Mobject's method).
#   - Matrix: entry[0][-2] -> entry[-2] (the elements are flat Tex; the glyph t is entry[-2]); set_points_smoothly(true_smooth=True) -> approx=False.
#   - Circle.radius -> circle.get_radius() (the attribute no longer exists).
#   - Sector(outer_radius=...) -> Sector(radius=...) (Sector no longer accepts outer_radius).
#   - t_label[1].data['font_size'] *= 2 is removed: DecimalNumber no longer has that field and scale() doubles its font_size.
# ==============================================================================

from manim_imports_ext import *

def get_matrix_exponential(matrix, height=1.5, scalar_tex="t", **matrix_config):
    elem = matrix[0][0]
    if isinstance(elem, str):
        mat_class = Matrix
    elif isinstance(elem, int) or isinstance(elem, np.int64):
        mat_class = IntegerMatrix
    else:
        mat_class = DecimalMatrix

    matrix = mat_class(matrix, **matrix_config)
    base = OldTex("e")
    base.set_height(0.4 * height)
    matrix.set_height(0.6 * height)
    matrix.move_to(base.get_corner(UR), DL)
    result = VGroup(base, matrix)
    if scalar_tex:
        scalar = OldTex(scalar_tex)
        scalar.set_height(0.7 * base.get_height())
        scalar.next_to(matrix, RIGHT, buff=SMALL_BUFF, aligned_edge=DOWN)
        result.add(scalar)
    return result


def get_2d_equation(matrix=[["a", "b"], ["c", "d"]]):
    deriv = OldTex("d \\over dt", tex_to_color_map={"t": GREY_B})
    vect = Matrix(
        [["x(t)"], ["y(t)"]],
        bracket_h_buff=SMALL_BUFF,
        bracket_v_buff=SMALL_BUFF,
        # CHANGE: element_to_mobject_config no longer exists in Matrix/DecimalMatrix (see element_config / decimal_config)
        element_config={
            "tex_to_color_map": {"t": GREY_B},
            "isolate": ["(", ")"]
        }
    )
    deriv.match_height(vect)
    equals = OldTex("=")
    matrix_mob = Matrix(matrix, h_buff=0.8)
    matrix_mob.set_color(TEAL)
    matrix_mob.match_height(vect)
    equation = VGroup(deriv, vect, equals, matrix_mob, vect.deepcopy())
    equation.arrange(RIGHT)
    return equation


class RomeoAndJuliet(Scene):
    def construct(self):
        # Add Romeo and Juliet
        romeo, juliet = lovers = self.get_romeo_and_juliet()
        lovers.set_height(2)
        lovers.arrange(LEFT, buff=1)
        lovers.move_to(0.5 * DOWN)

        self.add(*lovers)
        self.make_romeo_and_juliet_dynamic(romeo, juliet)
        romeo.love_tracker.set_value(1.5)
        juliet.love_tracker.set_value(1.5)
        # CHANGE: `self.` was missing (NameError in the original: get_romeo_juilet_name_labels is a method of the scene)
        self.get_romeo_juilet_name_labels(lovers)

        for creature in lovers:
            self.play(
                creature.love_tracker.animate.set_value(2.5),
                Write(creature.name_label, run_time=1),
            )
        self.wait()

        # Add their scales
        juliet_scale = self.get_love_scale(juliet, LEFT, "x", BLUE_B)
        romeo_scale = self.get_love_scale(romeo, RIGHT, "y", BLUE)
        scales = [juliet_scale, romeo_scale]

        scale_labels = VGroup(
            OldTexText("Juliet's love for Romeo", font_size=30),
            OldTexText("Romeo's love for Juliet", font_size=30),
        )
        scale_arrows = VGroup()
        for scale, label in zip(scales, scale_labels):
            var = scale[2][0][0]
            label.next_to(var, UP, buff=0.7)
            # CHANGE: Arrow(thickness=...) -> FillArrow: thickness in scene units (the current Arrow multiplies it by 0.015)
            arrow = FillArrow(var, label, buff=0.1, thickness=0.025)
            scale_arrows.add(arrow)
            label.set_color(var.get_fill_color())

        for lover, scale, arrow, label, final_love in zip(reversed(lovers), scales, scale_arrows, scale_labels, [1, -1]):
            self.add(scale)
            self.play(FlashAround(scale[2][0][0]))
            self.play(
                lover.love_tracker.animate.set_value(5),
                GrowArrow(arrow),
                FadeIn(label, 0.5 * UP),
            )
            self.play(lover.love_tracker.animate.set_value(final_love), run_time=2)
            self.wait()

        # Juliet's rule
        frame = self.camera.frame
        equations = VGroup(
            # CHANGE: OldTex no longer splits on {{ }} (convention removed from manimgl in Apr 2021); they are removed and isolate=[...] is used with the same pieces
            OldTex("{dx \\over dt} = -y(t)", isolate=["=", "y(t)"]),
            OldTex("{dy \\over dt} = x(t)", isolate=["=", "x(t)"]),
        )
        juliet_eq, romeo_eq = equations
        juliet_eq.next_to(scale_labels[0], UR)
        juliet_eq.shift(0.5 * UP)

        self.play(
            frame.animate.move_to(0.7 * UP),
            Write(equations[0]),
        )
        self.wait()
        self.play(FlashAround(juliet_eq[0]))
        self.wait()
        y_rect = SurroundingRectangle(juliet_eq.get_parts_by_tex("y(t)"), buff=0.05)
        y_rect_copy = y_rect.copy()
        y_rect_copy.replace(romeo.scale_mob.dot, stretch=True)
        self.play(FadeIn(y_rect))
        self.wait()
        self.play(TransformFromCopy(y_rect, y_rect_copy))
        y_rect_copy.add_updater(lambda m: m.move_to(romeo.scale_mob.dot))
        self.wait()
        self.play(romeo.love_tracker.animate.set_value(-3))

        big_arrow = Arrow(
            juliet.scale_mob.number_line.get_bottom(),
            juliet.scale_mob.number_line.get_top(),
        )
        big_arrow.set_color(GREEN)
        big_arrow.next_to(juliet.scale_mob.number_line, LEFT)

        self.play(
            FadeIn(big_arrow),
            ApplyMethod(juliet.love_tracker.set_value, 5, run_time=3, rate_func=linear),
        )
        self.wait()
        self.play(romeo.love_tracker.animate.set_value(5))
        # CHANGE: Scene.play no longer accepts path_arc or uncalled methods; mob.animate(path_arc=...).method(args) is used
        self.play(
            big_arrow.animate(path_arc=PI).rotate(PI).set_color(RED),
            run_time=0.5,
        )
        self.play(juliet.love_tracker.animate.set_value(-5), rate_func=linear, run_time=5)
        self.play(FadeOut(y_rect), FadeOut(y_rect_copy))

        # Romeo's rule
        romeo_eq.next_to(scale_labels[1], UL)
        romeo_eq.shift(0.5 * UP)
        self.play(
            juliet_eq.animate.to_edge(LEFT),
            FadeOut(big_arrow),
        )
        self.play(FadeIn(romeo_eq, UP))
        self.wait()

        dy_rect = SurroundingRectangle(romeo_eq.get_part_by_tex("dy"))
        x_rect = SurroundingRectangle(romeo_eq.get_part_by_tex("x(t)"), buff=0.05)
        x_rect_copy = x_rect.copy()
        x_rect_copy.replace(juliet.scale_mob.dot, stretch=True)
        self.play(ShowCreation(dy_rect))
        self.wait()
        self.play(TransformFromCopy(dy_rect, x_rect))
        self.play(TransformFromCopy(x_rect, x_rect_copy))
        self.wait()

        big_arrow.next_to(romeo.scale_mob.number_line, RIGHT)
        self.play(FadeIn(big_arrow), LaggedStartMap(FadeOut, VGroup(dy_rect, x_rect)))
        self.play(romeo.love_tracker.animate.set_value(-3), run_time=4, rate_func=linear)
        x_rect_copy.add_updater(lambda m: m.move_to(juliet.scale_mob.dot))
        juliet.love_tracker.set_value(5)
        self.wait()
        # CHANGE: Scene.play no longer accepts path_arc or uncalled methods; mob.animate(path_arc=...).method(args) is used
        self.play(
            big_arrow.animate(path_arc=PI).rotate(PI).set_color(GREEN),
            run_time=0.5,
        )
        self.play(romeo.love_tracker.animate.set_value(5), rate_func=linear, run_time=5)
        self.play(FadeOut(x_rect_copy))
        self.wait()

        # Show constant change
        left_arrow = Arrow(UP, DOWN)
        left_arrow.character = juliet
        left_arrow.get_rate = lambda: -romeo.love_tracker.get_value()

        right_arrow = Arrow(DOWN, UP)
        right_arrow.character = romeo
        right_arrow.get_rate = lambda: juliet.love_tracker.get_value()

        def update_arrow(arrow):
            # CHANGE: the attribute is called scale_mob (scale is Mobject's method): AttributeError in the original
            nl = arrow.character.scale_mob.number_line
            rate = arrow.get_rate()
            if rate == 0:
                rate = 1e-6
            arrow.put_start_and_end_on(nl.n2p(0), nl.n2p(rate))
            arrow.next_to(nl, np.sign(nl.get_center()[0]) * RIGHT)
            if rate > 0:
                arrow.set_color(GREEN)
            else:
                arrow.set_color(RED)

        left_arrow.add_updater(update_arrow)
        right_arrow.add_updater(update_arrow)

        self.play(
            VFadeIn(left_arrow),
            ApplyMethod(big_arrow.scale, 0, remover=True, run_time=3),
            ApplyMethod(juliet.love_tracker.set_value, 0, run_time=3),
        )

        ps_point = Point(5 * UP)
        curr_time = self.time
        ps_point.add_updater(lambda m: m.move_to([
            -5 * np.sin(0.5 * (self.time - curr_time)),
            5 * np.cos(0.5 * (self.time - curr_time)),
            0,
        ]))
        juliet.love_tracker.add_updater(lambda m: m.set_value(ps_point.get_location()[0]))
        romeo.love_tracker.add_updater(lambda m: m.set_value(ps_point.get_location()[1]))
        self.add(ps_point)
        self.add(right_arrow)

        self.play(
            equations.animate.arrange(RIGHT, buff=LARGE_BUFF).to_edge(UP, buff=0),
            run_time=2,
        )
        # Just let this play out for a long time while other animations are played on top
        self.wait(5 * TAU)

    def get_romeo_and_juliet(self):
        romeo = PiCreature(color=BLUE_E, flip_at_start=True)
        juliet = PiCreature(color=BLUE_B)
        return VGroup(romeo, juliet)

    def make_romeo_and_juliet_dynamic(self, romeo, juliet):
        cutoff_values = [-5, -3, -1, 0, 1, 3, 5]
        modes = ["angry", "sassy", "hesitant", "plain", "happy", "hooray", "surprised"]
        self.make_character_dynamic(romeo, juliet, cutoff_values, modes)
        self.make_character_dynamic(juliet, romeo, cutoff_values, modes)

    def get_romeo_juilet_name_labels(self, lovers, font_size=36, spacing=1.2, buff=MED_SMALL_BUFF):
        name_labels = VGroup(*(
            Text(name, font_size=font_size)
            for name in ["Romeo", "Juliet"]
        ))
        for label, creature in zip(name_labels, lovers):
            label.next_to(creature, DOWN, buff)
            creature.name_label = label
        name_labels.space_out_submobjects(spacing)
        return name_labels

    def make_character_dynamic(self, pi_creature, lover, cutoff_values, modes):
        height = pi_creature.get_height()
        bottom = pi_creature.get_bottom()
        copies = [
            # CHANGE: PiCreature.change(...) now returns an animation (.animate); change_mode(...) is the immediate change
            pi_creature.deepcopy().change_mode(mode).set_height(height).move_to(bottom, DOWN)
            for mode in modes
        ]
        pi_creature.love_tracker = ValueTracker()

        def update_func(pi):
            love = pi.love_tracker.get_value()

            if love < cutoff_values[0]:
                pi.become(copies[0])
            elif love >= cutoff_values[-1]:
                pi.become(copies[-1])
            else:
                i = 1
                while cutoff_values[i] < love:
                    i += 1
                # CHANGE: manimgl's align_data_and_family now fills the missing subpaths with a double stroke (not with a point) and aligns
                # CHANGE: every frame, copies and pi separately inflated and misaligned the mouth points (ValueError when interpolating); they are aligned
                # CHANGE: temporary copies against each other and pi takes the data from copy1 (become) before interpolating
                copy1 = copies[i - 1].copy()
                copy2 = copies[i].copy()

                alpha = inverse_interpolate(cutoff_values[i - 1], cutoff_values[i], love)
                s_alpha = squish_rate_func(smooth, 0.25, 0.75)(alpha)

                # if s_alpha > 0:
                copy1.align_data_and_family(copy2)
                pi.become(copy1)
                fam = pi.family_members_with_points()
                f1 = copy1.family_members_with_points()
                f2 = copy2.family_members_with_points()
                for sm, sm1, sm2 in zip(fam, f1, f2):
                    sm.interpolate(sm1, sm2, s_alpha)

            pi.look_at(lover.get_top())
            if love < cutoff_values[1]:
                # Look away from the lover
                pi.look_at(2 * pi.eyes.get_center() - lover.eyes.get_center() + DOWN)

            return pi

        pi_creature.add_updater(update_func)

        def update_eyes(heart_eyes):
            love = pi_creature.love_tracker.get_value()
            l_alpha = np.clip(
                inverse_interpolate(cutoff_values[-1] - 0.5, cutoff_values[-1], love),
                0, 1
            )
            pi_creature.eyes.set_opacity(1 - l_alpha)
            heart_eyes.set_opacity(l_alpha)
            # heart_eyes.move_to(pi_creature.eyes)
            heart_eyes.match_x(pi_creature.mouth)

        heart_eyes = self.get_heart_eyes(pi_creature)
        heart_eyes.add_updater(update_eyes)
        pi_creature.heart_eyes = heart_eyes
        self.add(heart_eyes)
        return pi_creature

    def get_heart_eyes(self, creature):
        hearts = VGroup()
        for eye in creature.eyes:
            heart = SVGMobject("hearts")
            heart.set_fill(RED)
            heart.match_width(eye)
            heart.move_to(eye)
            heart.scale(1.25)
            heart.set_stroke(BLACK, 1)
            hearts.add(heart)
        hearts.set_opacity(0)
        return hearts

    def get_love_scale(self, creature, direction, var_name, color):
        number_line = NumberLine((-5, 5))
        number_line.rotate(90 * DEGREES)
        number_line.set_height(1.5 * creature.get_height())
        number_line.next_to(creature, direction, buff=MED_LARGE_BUFF)
        number_line.add_numbers(
            range(-4, 6, 2),
            font_size=18,
            color=GREY_B,
            buff=0.1,
            direction=LEFT,
        )

        dot = Dot(color=color)
        dot.add_updater(lambda m: m.move_to(number_line.n2p(creature.love_tracker.get_value())))

        label = VGroup(OldTex(var_name, "=", font_size=36), DecimalNumber(font_size=24))
        label.set_color(color)
        label[0].shift(label[1].get_left() + SMALL_BUFF * LEFT - label[0][1].get_right())
        label.next_to(number_line, UP)
        label[1].add_updater(lambda m: m.set_value(creature.love_tracker.get_value()).set_color(color))

        result = VGroup(number_line, dot, label)
        result.set_stroke(background=True)
        result.number_line = number_line
        result.dot = dot
        result.label = label
        creature.scale_mob = result

        return result


class RomeoJulietVectorSpace(RomeoAndJuliet):
    def construct(self):
        # Set up Romeo and Juliet
        romeo, juliet = lovers = self.get_romeo_and_juliet()
        lovers.set_height(2.0)
        lovers.arrange(LEFT, buff=3)
        name_labels = self.get_romeo_juilet_name_labels(lovers, font_size=36, spacing=1.1)
        self.make_romeo_and_juliet_dynamic(*lovers)

        self.add(*lovers)
        self.add(*name_labels)

        # Scales
        juliet_scale = self.get_love_scale(juliet, LEFT, "x", BLUE_B)
        romeo_scale = self.get_love_scale(romeo, RIGHT, "y", BLUE)
        scales = [juliet_scale, romeo_scale]
        self.add(*scales)

        # Animate in
        psp_tracker = Point()

        def get_psp():
            # Get phase space point
            return psp_tracker.get_location()

        juliet.love_tracker.add_updater(lambda m: m.set_value(get_psp()[0]))
        romeo.love_tracker.add_updater(lambda m: m.set_value(get_psp()[1]))
        self.add(romeo.love_tracker, juliet.love_tracker)

        psp_tracker.move_to([1, -3, 0])
        self.play(
            Rotate(psp_tracker, 90 * DEGREES, about_point=ORIGIN, run_time=3, rate_func=linear)
        )

        # Transition to axes
        axes = Axes(
            x_range=(-5, 5),
            y_range=(-5, 5),
            height=7,
            width=7,
            axis_config={
                "include_tip": False,
                "numbers_to_exclude": [],
            }
        )
        axes.set_x(-3)

        for axis in axes:
            axis.add_numbers(range(-4, 6, 2), color=GREY_B)
            axis.numbers[2].set_opacity(0)

        for pi in lovers:
            pi.clear_updaters()
            pi.generate_target()
            pi.target.set_height(0.75)
            pi.name_label.generate_target()
            pi.name_label.target.scale(0.5)
            group = VGroup(pi.target, pi.name_label.target)
            group.arrange(DOWN, buff=SMALL_BUFF)
            pi.target_group = group
            pi.scale_mob[2].clear_updaters()
            self.add(*pi.scale_mob)
        juliet.target_group.next_to(axes.x_axis.get_end(), RIGHT)
        romeo.target_group.next_to(axes.y_axis.get_corner(UR), RIGHT)
        romeo.target_group.shift_onto_screen(buff=MED_SMALL_BUFF)
        romeo.target.flip()
        juliet.target.flip()
        juliet.target.make_eye_contact(romeo.target)

        self.play(LaggedStart(
            juliet.scale_mob.number_line.animate.become(axes.x_axis),
            FadeOut(juliet.scale_mob.label),
            MoveToTarget(juliet),
            MoveToTarget(juliet.name_label),
            romeo.scale_mob.number_line.animate.become(axes.y_axis),
            FadeOut(romeo.scale_mob.label),
            MoveToTarget(romeo),
            MoveToTarget(romeo.name_label),
            run_time=3
        ))
        self.add(*romeo.scale_mob[:2], *juliet.scale_mob[:2])

        # Reset pi creatures
        self.remove(lovers)
        self.remove(romeo.heart_eyes)
        self.remove(juliet.heart_eyes)
        new_lovers = self.get_romeo_and_juliet()
        for new_pi, pi in zip(new_lovers, lovers):
            new_pi.flip()
            new_pi.replace(pi)
            new_pi.scale_mob = pi.scale_mob
        lovers = new_lovers
        romeo, juliet = new_lovers
        self.add(romeo, juliet)
        self.make_romeo_and_juliet_dynamic(romeo, juliet)
        juliet.love_tracker.add_updater(lambda m: m.set_value(get_psp()[0]))
        romeo.love_tracker.add_updater(lambda m: m.set_value(get_psp()[1]))
        self.add(romeo.love_tracker, juliet.love_tracker)

        # h_line and v_line
        ps_dot = Dot(color=BLUE)
        ps_dot.add_updater(lambda m: m.move_to(axes.c2p(*get_psp()[:2])))
        v_line = Line().set_stroke(BLUE_D, 2)
        h_line = Line().set_stroke(BLUE_B, 2)
        v_line.add_updater(lambda m: m.put_start_and_end_on(
            axes.x_axis.n2p(get_psp()[0]),
            axes.c2p(*get_psp()[:2]),
        ))
        h_line.add_updater(lambda m: m.put_start_and_end_on(
            axes.y_axis.n2p(get_psp()[1]),
            axes.c2p(*get_psp()[:2]),
        ))
        x_dec = DecimalNumber(0, font_size=24)
        x_dec.next_to(h_line, UP, SMALL_BUFF)
        y_dec = DecimalNumber(0, font_size=24)
        y_dec.next_to(v_line, RIGHT, SMALL_BUFF)

        romeo.scale_mob.dot.clear_updaters()
        juliet.scale_mob.dot.clear_updaters()
        self.play(
            ShowCreation(h_line.copy().clear_updaters(), remover=True),
            ShowCreation(v_line.copy().clear_updaters(), remover=True),
            ReplacementTransform(romeo.scale_mob.dot, ps_dot),
            ReplacementTransform(juliet.scale_mob.dot, ps_dot),
            ChangeDecimalToValue(x_dec, get_psp()[0]),
            VFadeIn(x_dec),
            ChangeDecimalToValue(y_dec, get_psp()[1]),
            VFadeIn(y_dec),
        )
        self.add(h_line, v_line, ps_dot)

        # Add coordinates
        equation = VGroup(
            Matrix([["x"], ["y"]], bracket_h_buff=SMALL_BUFF),
            OldTex("="),
            DecimalMatrix(
                np.reshape(get_psp()[:2], (2, 1)),
                # CHANGE: element_to_mobject_config no longer exists in Matrix/DecimalMatrix (see element_config / decimal_config)
                num_decimal_places=2, decimal_config={"font_size": 36, "include_sign": True}
            ),
        )
        equation[0].match_height(equation[2])
        equation.arrange(RIGHT)
        equation.to_corner(UR)
        equation.shift(MED_SMALL_BUFF * LEFT)

        self.play(
            FadeIn(equation[:2]),
            FadeIn(equation[2].get_brackets()),
            TransformFromCopy(x_dec, equation[2].get_entries()[0]),
            TransformFromCopy(y_dec, equation[2].get_entries()[1]),
        )
        equation[2].get_entries()[0].add_updater(lambda m: m.set_value(get_psp()[0]))
        equation[2].get_entries()[1].add_updater(lambda m: m.set_value(get_psp()[1]))

        self.play(FadeOut(x_dec), FadeOut(y_dec))

        # Play around in state space
        # CHANGE: Scene.play no longer accepts path_arc or uncalled methods; mob.animate(path_arc=...).method(args) is used
        self.play(psp_tracker.animate(path_arc=120 * DEGREES).move_to([3, -2, 0]), run_time=3)
        self.wait()
        # CHANGE: Scene.play no longer accepts path_arc or uncalled methods; mob.animate(path_arc=...).method(args) is used
        self.play(psp_tracker.animate(path_arc=0 * DEGREES).move_to([-5, -2, 0]), run_time=3, rate_func=there_and_back)
        self.wait()
        # CHANGE: Scene.play no longer accepts path_arc or uncalled methods; mob.animate(path_arc=...).method(args) is used
        self.play(psp_tracker.animate(path_arc=0 * DEGREES).move_to([3, 5, 0]), run_time=3, rate_func=there_and_back)
        self.wait()
        # CHANGE: Scene.play no longer accepts path_arc or uncalled methods; mob.animate(path_arc=...).method(args) is used
        self.play(psp_tracker.animate(path_arc=-120 * DEGREES).move_to([5, 3, 0]), run_time=2)
        self.wait()

        # Arrow vs. dot
        arrow = Arrow(axes.get_origin(), ps_dot.get_center(), buff=0, fill_color=BLUE)
        arrow.set_stroke(BLACK, 2, background=True)
        arrow_outline = arrow.copy()
        arrow_outline.set_fill(opacity=0)
        arrow_outline.set_stroke(YELLOW, 1)
        self.play(LaggedStart(
            FadeIn(arrow),
            FadeOut(ps_dot),
            ShowPassingFlash(arrow_outline, run_time=1, time_width=0.5),
            lag_ratio=0.5,
        ))
        self.wait()
        self.play(LaggedStart(
            FadeIn(ps_dot),
            FadeOut(arrow),
            FlashAround(ps_dot, buff=0.05),
        ))
        self.wait()
        self.play(FlashAround(equation))
        # CHANGE: Scene.play no longer accepts path_arc or uncalled methods; mob.animate(path_arc=...).method(args) is used
        self.play(psp_tracker.animate.move_to([4, 3, 0]), run_time=2)
        self.wait()

        # Function of time
        new_lhs = Matrix([["x(t)"], ["y(t)"]])
        new_lhs.match_height(equation[0])
        new_lhs.move_to(equation[0], RIGHT)

        self.play(
            FadeTransformPieces(equation[0], new_lhs),
        )
        self.remove(equation[0])
        self.add(new_lhs)
        equation.replace_submobject(0, new_lhs)

        # Initialize rotation
        curr_time = self.time
        curr_psp = get_psp()
        psp_tracker.add_updater(lambda m: m.move_to(np.dot(
            curr_psp,
            np.transpose(rotation_about_z(0.25 * (self.time - curr_time))),
        )))
        self.wait(5)

        # Rate of change
        deriv_lhs = Matrix([["x'(t)"], ["y'(t)"]], bracket_h_buff=SMALL_BUFF)
        deriv_lhs.match_height(equation[0])
        deriv_lhs.move_to(equation[0])
        deriv_lhs.set_color(RED_B)
        deriv_label = Text("Rate of change", font_size=24)
        deriv_label.match_width(deriv_lhs)
        deriv_label.match_color(deriv_lhs)
        deriv_label.next_to(deriv_lhs, DOWN, SMALL_BUFF)

        self.play(
            FadeIn(deriv_lhs),
            Write(deriv_label, run_time=1),
            equation.animate.shift(2.0 * deriv_lhs.get_height() * DOWN)
        )
        self.wait(5)

        deriv_vect = Arrow(fill_color=RED_B)
        deriv_vect.add_updater(
            lambda m: m.put_start_and_end_on(
                axes.get_origin(),
                axes.c2p(-0.5 * get_psp()[1], 0.5 * get_psp()[0])
            ).shift(
                ps_dot.get_center() - axes.get_origin()
            )
        )
        pre_vect = Arrow(LEFT, RIGHT)
        pre_vect.replace(deriv_label, dim_to_match=0)
        pre_vect.set_fill(RED_B, 0)
        moving_vect = pre_vect.copy()
        deriv_vect.set_opacity(0)
        self.add(deriv_vect)
        self.play(
            UpdateFromAlphaFunc(
                moving_vect,
                lambda m, a: m.interpolate(pre_vect, deriv_vect, a).set_fill(opacity=a),
                remover=True
            )
        )
        deriv_vect.set_fill(opacity=1)
        self.add(deriv_vect, ps_dot)
        self.wait(8)

        # Show equation
        rhs = VGroup(
            OldTex("="),
            Matrix([["-y(t)"], ["x(t)"]], bracket_h_buff=SMALL_BUFF)
        )
        rhs.match_height(deriv_lhs)
        rhs.arrange(RIGHT)
        rhs.next_to(deriv_lhs, RIGHT)

        self.play(FadeIn(rhs))
        self.wait()
        for i in range(2):
            self.play(FlashAround(
                VGroup(deriv_lhs.get_entries()[i], rhs[1].get_entries()[i]),
                run_time=3,
                time_width=4,
            ))
        self.wait(2)

        # Write with a matrix
        deriv_lhs.generate_target()
        new_eq = VGroup(
            deriv_lhs.target,
            OldTex("="),
            IntegerMatrix([[0, -1], [1, 0]], bracket_v_buff=MED_LARGE_BUFF),
            Matrix([["x(t)"], ["y(t)"]], bracket_h_buff=SMALL_BUFF),
        )
        new_eq[2].match_height(new_eq[0])
        new_eq[3].match_height(new_eq[0])
        new_eq.arrange(RIGHT)
        new_eq.to_corner(UR)

        self.play(
            MoveToTarget(deriv_lhs),
            MaintainPositionRelativeTo(deriv_label, deriv_lhs),
            ReplacementTransform(rhs[0], new_eq[1]),
            ReplacementTransform(rhs[1].get_brackets(), new_eq[3].get_brackets()),
            FadeIn(new_eq[2], scale=2),
            FadeTransform(rhs[1].get_entries()[1], new_eq[3].get_entries()[0]),
            FadeTransform(rhs[1].get_entries()[0], new_eq[3].get_entries()[1]),
        )
        self.wait(3)

        row_rect = SurroundingRectangle(new_eq[2].get_entries()[:2], buff=SMALL_BUFF)
        col_rect = SurroundingRectangle(new_eq[3].get_entries(), buff=SMALL_BUFF)
        both_rects = VGroup(row_rect, col_rect)
        both_rects.set_stroke(YELLOW, 2)

        self.play(*map(ShowCreation, both_rects))
        self.wait(3)
        self.play(row_rect.animate.move_to(new_eq[2].get_entries()[2:4]))
        self.wait(3)
        self.play(FadeOut(both_rects))

        # Write general form
        general_form = OldTex(
            "{d \\over dt}",
            "\\vec{\\textbf{v} }",
            "(t)",
            "=",
            "\\textbf{M}",
            "\\vec{\\textbf{v} }",
            "(t)",
        )
        general_form.set_color_by_tex("d \\over dt", RED_B)
        general_form.set_color_by_tex("\\textbf{v}", GREY_B)
        general_form.scale(1.2)
        general_form.next_to(new_eq, DOWN, LARGE_BUFF)
        general_form.shift(0.5 * RIGHT)
        gf_rect = SurroundingRectangle(general_form, buff=MED_SMALL_BUFF)
        gf_rect.set_stroke(YELLOW, 2)

        equation.clear_updaters()
        self.play(
            FadeIn(general_form),
            FadeOut(equation),
        )
        self.wait()
        self.play(ShowCreation(gf_rect))
        self.wait(4 * TAU)

        # Fade all else out
        self.play(FadeOut(VGroup(gf_rect, general_form, new_eq, deriv_lhs, deriv_label)))
        self.wait(4 * TAU)
        print(self.num_plays)


class AnalyzeRomeoAndJulietSpace(RomeoJulietVectorSpace):
    def construct(self):
        # Add axes
        axes = self.get_romeo_juliet_axes()
        ps_dot = axes.ps_dot
        ps_dot.set_opacity(0)
        ps_dot.move_to(axes.c2p(4, 3))

        ps_arrow = self.get_ps_arrow(axes, add_shadow=True)
        ps_arrow.update()
        self.add(ps_arrow)

        # Add equation
        matrix = [["0", "-1"], ["1", "0"]]
        equation = get_2d_equation(matrix)
        equation.to_corner(UR)

        implies = OldTex("\\Downarrow", font_size=72)
        implies.next_to(equation, DOWN, buff=0.3)

        initial_condition = Matrix([["x_0"], ["y_0"]], bracket_h_buff=0.1)
        initial_condition.match_height(equation)
        initial_condition.set_color(BLUE_B)
        ic_source = initial_condition.copy()
        ic_source.scale(0.5)
        ic_source.next_to(ps_arrow.get_end(), RIGHT, SMALL_BUFF)

        mat_exp = get_matrix_exponential(matrix, h_buff=0.8)
        solution = VGroup(equation[1].copy(), OldTex("="), mat_exp, initial_condition)
        solution[2][1].set_color(TEAL)
        solution.arrange(RIGHT)
        solution.scale(0.8)
        solution.next_to(implies, DOWN, buff=0.3)

        rot_matrix = Matrix(
            [["\\cos(t)", "-\\sin(t)"], ["\\sin(t)", "\\cos(t)"]],
            bracket_h_buff=0.2,
            h_buff=2.0
        )
        for entry in rot_matrix.get_entries():
            # CHANGE: the elements of Matrix are flat Tex (one glyph per child); before, entry[0] was the whole string
            entry[-2].set_color(GREY_B)
        rot_matrix.match_height(solution[0])
        solution2 = solution.deepcopy()
        solution2.replace_submobject(2, rot_matrix)
        solution2.arrange(RIGHT)
        solution2.next_to(solution, DOWN, buff=0.7)

        rot_matrix_brace = Brace(rot_matrix, DOWN)
        rot_label = OldTexText("Rotate by angle $t$")
        rot_label.next_to(rot_matrix_brace, DOWN, SMALL_BUFF)

        self.add(equation)
        self.play(FlashAround(equation, run_time=2))
        self.wait()
        self.play(
            Write(implies),
            TransformFromCopy(equation[1], solution[0], path_arc=-20 * DEGREES),
            TransformFromCopy(equation[2], solution[1]),
        )
        self.play(
            Write(mat_exp[0]),
            TransformFromCopy(equation[3], mat_exp[1]),
        )
        self.play(Write(mat_exp[2]))
        self.wait()
        self.play(
            FadeIn(ic_source),
            FlashAround(ic_source),
        )
        self.play(TransformFromCopy(ic_source, initial_condition))
        self.wait()
        self.play(
            *(
                TransformFromCopy(solution[i], solution2[i])
                for i in [0, 1, 3]
            ),
            FadeTransform(mat_exp.copy(), rot_matrix)
        )
        self.play(
            GrowFromCenter(rot_matrix_brace),
            FadeIn(rot_label),
        )
        self.wait()

        # Rotate vector
        start_angle = ps_arrow.get_angle()
        t_tracker = ValueTracker(0)
        get_t = t_tracker.get_value

        def get_arc():
            curr_time = get_t()
            arc = ParametricCurve(
                lambda s: axes.c2p(*tuple((1 + 0.2 * s) * np.array([
                    math.cos(start_angle + s * curr_time),
                    math.sin(start_angle + s * curr_time),
                ]))),
                t_range=(0, 1, 0.01)
            )
            arc.set_stroke(WHITE, 2)
            return arc

        arc = always_redraw(get_arc)
        t_label = VGroup(OldTex("t = ", font_size=30), DecimalNumber(font_size=24))
        t_label.arrange(RIGHT, buff=SMALL_BUFF)

        def update_t_label(label):
            point = arc.pfp(0.5)
            label[1].set_value(get_t())
            label.set_stroke(BLACK, 5, background=True)
            label.set_opacity(min(2 * get_t(), 1))
            if get_t() < 3.65:
                target_point = point + 0.75 * (point - axes.get_origin())
                label.shift(target_point - label[1].get_center())

        t_label.add_updater(update_t_label)

        curr_xy = np.array(axes.p2c(ps_dot.get_center()))

        def update_ps_dot(dot):
            rot_M = np.array(rotation_matrix_transpose(get_t(), OUT))[:2, :2]
            new_xy = np.dot(curr_xy, rot_M)
            dot.move_to(axes.c2p(*new_xy))

        ps_dot.add_updater(update_ps_dot)

        t_tracker.add_updater(lambda m, dt: m.increment_value(0.5 * dt))
        self.add(arc, t_label, t_tracker, ps_dot)
        self.play(VFadeIn(t_label))
        self.wait(16 * PI - 1)

    def get_romeo_juliet_axes(self, height=5):
        # Largely copied from RomeoJulietVectorSpace
        romeo, juliet = lovers = self.get_romeo_and_juliet()
        axes = Axes(
            x_range=(-5, 5),
            y_range=(-5, 5),
            height=height,
            width=height,
            axis_config={
                "include_tip": False,
                "numbers_to_exclude": [],
            }
        )
        axes.to_edge(LEFT)

        for axis in axes:
            axis.add_numbers(range(-4, 6, 2), color=GREY_A, font_size=12)
            axis.numbers[2].set_opacity(0)

        lovers.set_height(0.5)
        lovers.flip()
        juliet.next_to(axes.x_axis.get_end(), RIGHT)
        romeo.next_to(axes.y_axis.get_end(), UP)

        ps_dot = Dot(radius=0.04, fill_color=BLUE)
        ps_dot.move_to(axes.c2p(3, 1))

        def get_xy():
            # Get phase space point
            return axes.p2c(ps_dot.get_center())

        self.make_romeo_and_juliet_dynamic(romeo, juliet)
        juliet.love_tracker.add_updater(lambda m: m.set_value(get_xy()[0]))
        romeo.love_tracker.add_updater(lambda m: m.set_value(get_xy()[1]))
        self.add(romeo.love_tracker, juliet.love_tracker)

        name_labels = self.get_romeo_juilet_name_labels(lovers, font_size=12, spacing=1.0, buff=0.05)

        axes.lovers = lovers
        axes.name_labels = name_labels
        axes.ps_dot = ps_dot
        axes.add(lovers, name_labels, ps_dot)

        self.add(axes)
        self.add(*lovers)
        self.add(*(pi.heart_eyes for pi in lovers))

        return axes

    def get_ps_arrow(self, axes, color=BLUE, add_shadow=False):
        # CHANGE: Arrow(thickness=...) -> FillArrow: thickness in scene units (the current Arrow multiplies it by 0.015)
        arrow = FillArrow(
            LEFT, RIGHT,
            fill_color=color,
            thickness=0.04
        )
        arrow.add_updater(lambda m: m.put_start_and_end_on(
            axes.get_origin(), axes.ps_dot.get_center(),
        ))

        if add_shadow:
            ps_arrow_shadow = arrow.copy()
            ps_arrow_shadow.clear_updaters()
            ps_arrow_shadow.set_fill(BLUE, 0.5)
            self.add(ps_arrow_shadow)
        return arrow


class GeometricReasoningForRomeoJuliet(AnalyzeRomeoAndJulietSpace):
    def construct(self):
        # Setup
        axes = self.get_romeo_juliet_axes()
        ps_dot = axes.ps_dot
        ps_dot.set_opacity(0)
        ps_dot.move_to(axes.c2p(4, 3))

        ps_arrow = self.get_ps_arrow(axes)
        self.add(ps_arrow)

        matrix = [["0", "-1"], ["1", "0"]]
        equation = get_2d_equation(matrix)
        ddt, xy1, eq, mat, xy2 = equation
        equation.to_corner(UR)
        self.add(equation)

        # Show 90 degree rotation
        mat_brace = Brace(mat, DOWN, buff=SMALL_BUFF)
        mat_label = mat_brace.get_text("90-degree rotation matrix", font_size=30)
        mat_label.set_color(TEAL)

        self.play(
            GrowFromCenter(mat_brace),
            Write(mat_label, run_time=1)
        )
        self.wait()

        # Spiral around to various points
        curve = VMobject()
        curve.set_points_smoothly(
            [
                axes.c2p(x, y)
                for x, y in [(4, 3), (0, 2), (0, -1), (-3, -4), (-3, 2), (3, 1)]
            ],
            # CHANGE: set_points_smoothly no longer has true_smooth: approx=False is the exact smoothing
            approx=False
        )
        self.play(MoveAlongPath(ps_dot, curve, run_time=5))
        self.wait()

        # Rate of change
        deriv_vect = ps_arrow.copy()
        deriv_vect.clear_updaters()
        deriv_vect.set_color(RED)
        deriv_vect.shift(ps_arrow.get_vector())

        deriv_rect = SurroundingRectangle(VGroup(ddt, xy1))
        deriv_rect.set_stroke(RED, 2)

        d_line = DashedLine(ps_arrow.get_start(), ps_arrow.get_end())
        d_line.shift(ps_arrow.get_vector())
        d_line.set_stroke(WHITE, 1)

        arc = Arc(
            start_angle=ps_arrow.get_angle(),
            angle=90 * DEGREES,
            arc_center=ps_arrow.get_end(),
            radius=0.25
        )
        elbow = VMobject()
        elbow.set_points_as_corners([RIGHT, UR, UP])
        elbow.scale(0.25, about_point=ORIGIN)
        elbow.rotate(ps_arrow.get_angle(), about_point=ORIGIN)
        elbow.shift(ps_arrow.get_end())
        VGroup(elbow, arc).set_stroke(WHITE, 2)

        self.play(
            TransformFromCopy(ps_arrow, deriv_vect, path_arc=30 * DEGREES),
            ShowCreation(deriv_rect),
        )
        self.add(d_line, deriv_vect)
        self.play(
            ShowCreation(arc),
            Rotate(deriv_vect, 90 * DEGREES, about_point=ps_arrow.get_end()),
            run_time=2,
            rate_func=rush_into,
        )
        self.remove(arc)
        self.add(elbow)
        self.wait()

        # Show rotation
        ps_arrow.clear_updaters()
        ps_dot.add_updater(lambda m: m.move_to(ps_arrow.get_end()))
        rot_group = VGroup(ps_arrow, d_line, elbow, deriv_vect)
        circle = Circle(radius=ps_arrow.get_length())
        circle.set_stroke(GREY, 1)
        circle.move_to(axes.get_origin())

        self.play(
            Rotate(
                rot_group,
                angle=TAU - ps_arrow.get_angle(),
                about_point=axes.get_origin(),
                run_time=6,
                rate_func=linear,
            ),
            FadeIn(circle),
        )
        self.wait()

        # Show matching length
        self.play(
            deriv_vect.animate.put_start_and_end_on(ps_arrow.get_start(), ps_arrow.get_end()).shift(0.2 * UP),
            run_time=3,
            rate_func=there_and_back_with_pause,
        )
        self.wait()

        # Show one radian of arc
        # CHANGE: Circle.radius is no longer an attribute; get_radius() is used
        arc = Arc(
            0, 1,
            radius=circle.get_radius(),
            arc_center=axes.get_origin(),
        )
        arc.set_stroke(YELLOW, 3)
        # CHANGE: Sector no longer accepts outer_radius (its parameter is radius)
        sector = Sector(
            start_angle=0,
            angle=1,
            radius=circle.get_radius(),
        )
        sector.shift(axes.get_origin())
        sector.set_stroke(width=0)
        sector.set_fill(GREY_D, 1)

        t_label = VGroup(OldTex("t = ", font_size=30), DecimalNumber(0, font_size=20))
        t_label.arrange(RIGHT, buff=SMALL_BUFF)
        t_label.next_to(arc.pfp(0.5), UR, SMALL_BUFF)

        self.play(
            Rotate(rot_group, 1, about_point=axes.get_origin()),
            ShowCreation(arc),
            ChangeDecimalToValue(t_label[1], 1.0),
            VFadeIn(t_label),
            run_time=2,
            rate_func=linear,
        )
        self.add(sector, axes, ps_arrow, arc)
        self.play(FadeIn(sector))
        self.wait()

        radius = Line(axes.get_origin(), arc.get_start())
        radius.set_stroke(RED, 5)
        self.play(ShowCreation(radius))
        self.play(Rotate(radius, -PI / 2, about_point=radius.get_end()))
        radius.rotate(PI)
        self.play(radius.animate.match_points(arc))
        self.play(FadeOut(radius))
        self.wait()

        # One radian per unit time
        self.play(
            t_label.animate.shift(UP).scale(2),
        )
        # CHANGE: DecimalNumber no longer has data["font_size"]; scale() (above) already doubles its font_size, so the line is redundant
        for x in range(5):
            VGroup(sector, arc).rotate(1, about_point=axes.get_origin())
            self.play(
                Rotate(rot_group, 1, about_point=axes.get_origin()),
                ChangeDecimalToValue(t_label[1], t_label[1].get_value() + 1),
                run_time=2,
                rate_func=linear,
            )
        self.play(
            FadeOut(VGroup(sector, arc)),
            Rotate(rot_group, TAU - 6, about_point=axes.get_origin()),
            ChangeDecimalToValue(t_label[1], TAU),
            run_time=2 * (TAU - 6),
            rate_func=linear,
        )
        self.wait(2)

        t_label[1].set_value(0)
        self.play(
            Rotate(rot_group, PI, about_point=axes.get_origin()),
            ChangeDecimalToValue(t_label[1], PI),
            run_time=2 * PI,
            rate_func=linear,
        )
        self.wait(2)
