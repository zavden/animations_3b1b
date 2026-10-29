# ==============================================================================
# Scene:      RomeoAndJuliet
# Source:     videos/_2021/matrix_exp.py (lines 1501-1808)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl RomeoAndJuliet.py RomeoAndJuliet -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Arrow(..., thickness=X) -> FillArrow(...): the thickness in the 2021 code is in scene units and the current Arrow multiplies it by 0.015 (invisible arrows).
#   - get_romeo_juilet_name_labels(lovers) -> self.get_romeo_juilet_name_labels(lovers): `self.` was missing (NameError in the original).
#   - pi_creature.deepcopy().change(mode) -> .change_mode(mode): since 2022 PiCreature.change returns an animation; here the immediate change is needed.
#   - OldTex/OldTexText with {{ }}: manimgl removed that convention (Apr 2021) and no longer splits the text into parts; the double braces are removed and isolate=[...] is passed with the same pieces.
#   - make_character_dynamic: temporary copies are aligned (not the permanent ones nor pi) and pi takes the data from copy1 with become() before interpolating: manimgl's VMobject alignment (double stroke for missing subpaths, since 2023) inflated the mouth points and failed with ValueError.
#   - self.play(..., path_arc=...) and self.play(mob.method, args, ...): Scene.play no longer accepts path_arc or uncalled methods; mob.animate(path_arc=...).method(args) is used.
#   - arrow.character.scale.number_line -> arrow.character.scale_mob.number_line: the attribute is called scale_mob (AttributeError in the original: scale is Mobject's method).
# ==============================================================================

from manim_imports_ext import *

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
