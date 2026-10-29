# ==============================================================================
# Scene:      LoveExample
# Source:     videos/_2019/diffyq/part1/staging.py (lines 2472-2852)
# Category:   1 · Renders unmodified
# Includes code copied from: _2019/diffyq/part1/shared_constructs.py
#
# Run from this folder:
#     manimgl LoveExample.py LoveExample -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *


# ----- From _2019/diffyq/part1/shared_constructs.py -----

class You(PiCreature):
    CONFIG = {
        "color": BLUE_C,
    }


def get_heart_var(index):
    heart = SuitSymbol("hearts")
    if index == 1:
        heart.set_color(BLUE_C)
    elif index == 2:
        heart.set_color(GREEN)
    heart.set_height(0.7)
    index = Integer(index)
    index.move_to(heart.get_corner(DR))
    heart.add(index)
    return heart


def get_heart_var_deriv(index):
    heart = get_heart_var(index)
    filler_tex = "T"
    deriv = OldTex("{d", filler_tex, "\\over", "dt}")
    deriv.scale(2)
    filler = deriv.get_part_by_tex(filler_tex)
    heart.match_height(filler)
    heart.move_to(filler)
    heart.scale(1.5, about_edge=UL)
    deriv.remove(filler)
    deriv.add(heart)
    deriv.heart = heart
    return deriv


def get_love_equation1():
    equation = VGroup(
        get_heart_var_deriv(1),
        OldTex("=").scale(2),
        OldTex("a").scale(2),
        get_heart_var(2)
    )
    equation.arrange(RIGHT)
    equation[-1].shift(SMALL_BUFF * DL)
    return equation


def get_love_equation2():
    equation = VGroup(
        get_heart_var_deriv(2),
        OldTex("=").scale(2),
        OldTex("-b").scale(2),
        get_heart_var(1),
    )
    equation.arrange(RIGHT)
    equation[-1].shift(SMALL_BUFF * DL)
    return equation



# ----- From _2019/diffyq/part1/staging.py -----

class LoveExample(PiCreatureScene):
    def construct(self):
        self.show_hearts()
        self.add_love_trackers()
        self.break_down_your_rule()
        self.break_down_their_rule()

    def create_pi_creatures(self):
        you = You()
        you.shift(FRAME_WIDTH * LEFT / 4)
        you.to_edge(DOWN)

        tau = TauCreature(color=GREEN)
        tau.flip()
        tau.shift(FRAME_WIDTH * RIGHT / 4)
        tau.to_edge(DOWN)

        self.you = you
        self.tau = tau
        return (you, tau)

    def show_hearts(self):
        you, tau = self.you, self.tau
        hearts = VGroup()
        n_hearts = 20
        for x in range(n_hearts):
            heart = SuitSymbol("hearts")
            heart.scale(0.5 + 2 * np.random.random())
            heart.shift(np.random.random() * 4 * RIGHT)
            heart.shift(np.random.random() * 4 * UP)
            hearts.add(heart)
        hearts.move_to(2 * DOWN)
        hearts.add_updater(lambda m, dt: m.shift(2 * dt * UP))

        self.add(hearts)
        self.play(
            LaggedStartMap(
                UpdateFromAlphaFunc, hearts,
                lambda heart: (
                    heart,
                    lambda h, a: h.set_opacity(
                        there_and_back(a)
                    ).shift(0.02 * UP)
                ),
                lag_ratio=0.01,
                run_time=3,
                suspend_mobject_updating=False,
            ),
            ApplyMethod(
                you.change, 'hooray', tau.eyes,
                run_time=2,
                rate_func=squish_rate_func(smooth, 0.5, 1)
            ),
            ApplyMethod(
                tau.change, 'hooray', you.eyes,
                run_time=2,
                rate_func=squish_rate_func(smooth, 0.5, 1)
            ),
        )
        self.remove(hearts)
        self.wait()

    def add_love_trackers(self):
        self.init_ps_point()
        self.add_love_decimals()
        self.add_love_number_lines()
        self.tie_creature_state_to_ps_point()

        self.play(Rotating(
            self.ps_point,
            radians=-7 * TAU / 8,
            about_point=ORIGIN,
            run_time=10,
            rate_func=linear,
        ))
        self.wait()

    def break_down_your_rule(self):
        label1 = self.love_1_label
        label2 = self.love_2_label
        ps_point = self.ps_point

        up_arrow = Vector(UP, color=GREEN)
        down_arrow = Vector(DOWN, color=RED)
        for arrow in (up_arrow, down_arrow):
            arrow.next_to(label1, RIGHT)

        self.play(GrowArrow(up_arrow))
        self.play(
            self.tau.love_eyes.scale, 1.25,
            self.tau.love_eyes.set_color, BLUE_C,
            rate_func=there_and_back,
        )
        self.play(
            ps_point.shift, 6 * RIGHT,
            run_time=2,
        )
        self.wait()
        ps_point.shift(13 * DOWN)
        self.play(
            FadeOut(up_arrow),
            GrowArrow(down_arrow),
        )
        self.play(
            ps_point.shift, 11 * LEFT,
            run_time=3,
        )
        self.wait()

        # Derivative
        equation = get_love_equation1()
        equation.shift(0.5 * UP)
        deriv, equals, a, h2 = equation

        self.play(
            Write(deriv[:-1]),
            Write(equals),
            Write(a),
            TransformFromCopy(label1[0], deriv.heart),
            TransformFromCopy(label2[0], h2),
        )
        self.wait()
        self.play(
            equation.scale, 0.5,
            equation.to_corner, UL,
            FadeOut(down_arrow)
        )

    def break_down_their_rule(self):
        label1 = self.love_1_label
        label2 = self.love_2_label
        ps_point = self.ps_point

        up_arrow = Vector(UP, color=GREEN)
        down_arrow = Vector(DOWN, color=RED)
        for arrow in (up_arrow, down_arrow):
            arrow.next_to(label2, RIGHT)

        # Derivative
        equation = get_love_equation2()
        equation.shift(0.5 * UP)
        deriv, equals, mb, h1 = equation

        self.play(
            Write(deriv[:-1]),
            Write(equals),
            Write(mb),
            TransformFromCopy(label1[0], h1),
            TransformFromCopy(label2[0], deriv.heart),
        )

        self.play(GrowArrow(up_arrow))
        self.play(
            ps_point.shift, 13 * UP,
            run_time=3,
        )
        self.wait()
        self.play(
            ps_point.shift, 11 * RIGHT,
        )
        self.play(
            FadeOut(up_arrow),
            GrowArrow(down_arrow),
        )
        self.play(
            ps_point.shift, 13 * DOWN,
            run_time=3,
        )
        self.wait()

    #
    def init_ps_point(self):
        self.ps_point = VectorizedPoint(np.array([5.0, 5.0, 0]))

    def get_love1(self):
        return self.ps_point.get_location()[0]

    def get_love2(self):
        return self.ps_point.get_location()[1]

    def set_loves(self, love1=None, love2=None):
        if love1 is not None:
            self.ps_point.set_x(love1)
        if love2 is not None:
            self.ps_point.set_x(love2)

    def add_love_decimals(self):
        self.love_1_label = self.add_love_decimal(
            1, self.get_love1, self.you.get_color(), -3,
        )
        self.love_2_label = self.add_love_decimal(
            2, self.get_love2, self.tau.get_color(), 3,
        )

    def add_love_decimal(self, index, value_func, color, x_coord):
        d = DecimalNumber(include_sign=True)
        d.add_updater(lambda d: d.set_value(value_func()))

        label = get_heart_var(index)
        label.move_to(x_coord * RIGHT)
        label.to_edge(UP)
        eq = OldTex("=")
        eq.next_to(label, RIGHT, SMALL_BUFF)
        eq.shift(SMALL_BUFF * UP)
        d.next_to(eq, RIGHT, SMALL_BUFF)

        self.add(label, eq, d)
        return VGroup(label, eq, d)

    def add_love_number_lines(self):
        nl1 = NumberLine(
            x_min=-8,
            x_max=8,
            unit_size=0.25,
            tick_frequency=2,
            number_scale_val=0.25,
        )
        nl1.set_stroke(width=1)
        nl1.next_to(self.love_1_label, DOWN)
        nl1.add_numbers(*range(-6, 8, 2))

        nl2 = nl1.copy()
        nl2.next_to(self.love_2_label, DOWN)

        dot1 = Dot(color=self.you.get_color())
        dot1.add_updater(lambda d: d.move_to(
            nl1.number_to_point(self.get_love1())
        ))
        dot2 = Dot(color=self.tau.get_color())
        dot2.add_updater(lambda d: d.move_to(
            nl2.number_to_point(self.get_love2())
        ))

        self.add(nl1, nl2, dot1, dot2)

    def get_love_eyes(self, eyes):
        hearts = VGroup()
        for eye in eyes:
            heart = SuitSymbol("hearts")
            heart.match_width(eye)
            heart.move_to(eye)
            heart.scale(1.25)
            heart.set_stroke(BLACK, 1)
            hearts.add(heart)
        hearts.add_updater(
            lambda m: m.move_to(eyes)
        )
        return hearts

    def tie_creature_state_to_ps_point(self):
        # Quite a mess, but I'm coding in a rush here...
        you = self.you
        you_copy = you.copy()
        tau = self.tau
        tau_copy = tau.copy()

        you.love_eyes = self.get_love_eyes(you.eyes)
        tau.love_eyes = self.get_love_eyes(tau.eyes)

        self.add(you.love_eyes)
        self.add(tau.love_eyes)

        you_height = you.get_height()
        tau_height = tau.get_height()

        you_bottom = you.get_bottom()
        tau_bottom = tau.get_bottom()

        def update_you(y):
            love = self.get_love1()

            cutoff_values = [
                -5, -3, -1, 1, 3, 5
            ]
            modes = [
                "angry", "sassy", "hesitant",
                "plain",
                "happy", "hooray", "surprised",
            ]

            if love < cutoff_values[0]:
                y.change(modes[0])
            elif love >= cutoff_values[-1]:
                y.change(modes[-1])
            else:
                i = 0
                while cutoff_values[i] < love:
                    i += 1
                m1 = modes[i - 1]
                m2 = modes[i]
                y.change(m1)
                you_copy.change(m2)
                for mob in y, you_copy:
                    mob.set_height(you_height)
                    mob.move_to(you_bottom, DOWN)

                alpha = inverse_interpolate(
                    cutoff_values[i - 1],
                    cutoff_values[i],
                    love,
                )
                s_alpha = squish_rate_func(smooth, 0.25, 1)(alpha)
                if s_alpha > 0:
                    y.align_data_and_family(you_copy)
                    f1 = y.family_members_with_points()
                    f2 = you_copy.family_members_with_points()
                    for sm1, sm2 in zip(f1, f2):
                        sm1.interpolate(sm1, sm2, s_alpha)
            y.look_at(tau.eyes)
            if love < -4:
                y.look_at(LEFT_SIDE)
            # y.move_to(
            #     you_bottom + 0.025 * love * RIGHT, DOWN,
            # )

            l_alpha = np.clip(
                inverse_interpolate(5, 5.5, love),
                0, 1
            )
            y.eyes.set_opacity(1 - l_alpha)
            y.love_eyes.set_opacity(l_alpha)

            return y

        def update_tau(t):
            love = self.get_love2()

            cutoff_values = [
                -5, -1.7, 1.7, 5
            ]
            modes = [
                "angry", "confused", "plain",
                "hooray", "hooray"
            ]

            if love < cutoff_values[0]:
                t.change(modes[0])
            elif love >= cutoff_values[-1]:
                t.change(modes[-1])
            else:
                i = 0
                while cutoff_values[i] < love:
                    i += 1
                m1 = modes[i - 1]
                m2 = modes[i]
                t.change(m1)
                tau_copy.change(m2)
                for mob in t, tau_copy:
                    mob.set_height(tau_height)
                    mob.move_to(tau_bottom, DOWN)

                alpha = inverse_interpolate(
                    cutoff_values[i - 1],
                    cutoff_values[i],
                    love,
                )
                s_alpha = squish_rate_func(smooth, 0.25, 1)(alpha)
                if s_alpha > 0:
                    t.align_data_and_family(tau_copy)
                    f1 = t.family_members_with_points()
                    f2 = tau_copy.family_members_with_points()
                    for sm1, sm2 in zip(f1, f2):
                        sm1.interpolate(sm1, sm2, s_alpha)
            # t.move_to(
            #     tau_bottom + 0.025 * love * LEFT, DOWN,
            # )
            t.look_at(you.eyes)
            if love < -4:
                t.look_at(RIGHT_SIDE)

            l_alpha = np.clip(
                inverse_interpolate(5, 5.5, love),
                0, 1
            )
            t.eyes.set_opacity(1 - l_alpha)
            t.love_eyes.set_opacity(l_alpha)

        you.add_updater(update_you)
        tau.add_updater(update_tau)

        self.pi_creatures = VGroup()
