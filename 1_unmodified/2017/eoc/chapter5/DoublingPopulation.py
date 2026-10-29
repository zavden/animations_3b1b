# ==============================================================================
# Scene:      DoublingPopulation
# Source:     videos/_2017/eoc/chapter5.py (lines 68-442)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl DoublingPopulation.py DoublingPopulation -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class DoublingPopulation(PiCreatureScene):
    CONFIG = {
        "time_color" : YELLOW,
        "pi_creature_grid_dimensions" : (8, 8),
        "pi_creature_grid_height" : 6,
    }
    
    def construct(self):
        self.remove(self.get_pi_creatures())
        self.introduce_expression()
        self.introduce_pi_creatures()
        self.count_through_days()
        self.ask_about_dM_dt()
        self.growth_per_day()
        self.relate_growth_rate_to_pop_size()

    def introduce_expression(self):
        f_x = OldTex("f(x)", "=", "2^x")
        f_t = OldTex("f(t)", "=", "2^t")
        P_t = OldTex("P(t)", "=", "2^t")
        M_t = OldTex("M(t)", "=", "2^t")
        functions = VGroup(f_x, f_t, P_t, M_t)
        for function in functions:
            function.scale(1.2)
            function.to_corner(UP+LEFT)
        for function in functions[1:]:
            for i, j in (0, 2), (2, 1):
                function[i][j].set_color(self.time_color)

        t_expression = OldTex("t", "=", "\\text{Time (in days)}")
        t_expression.to_corner(UP+RIGHT)
        t_expression[0].set_color(self.time_color)

        pop_brace, mass_brace = [
            Brace(function[0], DOWN)
            for function in (P_t, M_t)
        ]
        for brace, word in (pop_brace, "size"), (mass_brace, "mass"):
            text = brace.get_text("Population %s"%word)
            text.to_edge(LEFT)
            brace.text = text

        self.play(Write(f_x))
        self.wait()
        self.play(
            Transform(f_x, f_t),
            FadeIn(
                t_expression,
                run_time = 2,
                lag_ratio = 0.5
            )
        )
        self.play(Transform(f_x, P_t))
        self.play(
            GrowFromCenter(pop_brace),
            Write(pop_brace.text, run_time = 2)
        )
        self.wait(2)

        self.function = f_x
        self.pop_brace = pop_brace
        self.t_expression = t_expression
        self.mass_function = M_t
        self.mass_brace = mass_brace

    def introduce_pi_creatures(self):
        creatures = self.get_pi_creatures()
        total_num_days = self.get_num_days()
        num_start_days = 4

        self.reset()
        for x in range(num_start_days):
            self.let_one_day_pass()
        self.wait()
        self.play(
            Transform(self.function, self.mass_function),
            Transform(self.pop_brace, self.mass_brace),
            Transform(self.pop_brace.text, self.mass_brace.text),
        )
        self.wait()
        for x in range(total_num_days-num_start_days):
            self.let_one_day_pass()
            self.wait()
        self.joint_blink(shuffle = False)
        self.wait()

    def count_through_days(self):
        self.reset()
        brace = self.get_population_size_descriptor()
        days_to_let_pass = 3

        self.play(GrowFromCenter(brace))
        self.wait()
        for x in range(days_to_let_pass):
            self.let_one_day_pass()
            new_brace = self.get_population_size_descriptor()
            self.play(Transform(brace, new_brace))
            self.wait()

        self.population_size_descriptor = brace

    def ask_about_dM_dt(self):
        dM_dt_question = OldTex("{dM", "\\over dt}", "=", "???")
        dM, dt, equals, q_marks = dM_dt_question
        dM_dt_question.next_to(self.function, DOWN, buff = LARGE_BUFF)
        dM_dt_question.to_edge(LEFT)

        self.play(
            FadeOut(self.pop_brace),
            FadeOut(self.pop_brace.text),
            Write(dM_dt_question)
        )
        self.wait(3)
        for mob in dM, dt:
            self.play(Indicate(mob))
            self.wait()

        self.dM_dt_question = dM_dt_question

    def growth_per_day(self):
        day_to_day, frac = self.get_from_day_to_day_label()

        self.play(
            FadeOut(self.dM_dt_question),
            FadeOut(self.population_size_descriptor),
            FadeIn(day_to_day)
        )
        rect = self.let_day_pass_and_highlight_new_creatures(frac)

        for x in range(2):
            new_day_to_day, new_frac = self.get_from_day_to_day_label()
            self.play(*list(map(FadeOut, [rect, frac])))
            frac = new_frac
            self.play(Transform(day_to_day, new_day_to_day))
            rect = self.let_day_pass_and_highlight_new_creatures(frac)
        self.play(*list(map(FadeOut, [rect, frac, day_to_day])))

    def let_day_pass_and_highlight_new_creatures(self, frac):
        num_new_creatures = 2**self.get_curr_day()

        self.let_one_day_pass()
        new_creatures = VGroup(
            *self.get_on_screen_pi_creatures()[-num_new_creatures:]
        )
        rect = Rectangle(
            color = GREEN,
            fill_color = BLUE,
            fill_opacity = 0.3,
        )
        rect.replace(new_creatures, stretch = True)
        rect.stretch_to_fit_height(rect.get_height()+MED_SMALL_BUFF)
        rect.stretch_to_fit_width(rect.get_width()+MED_SMALL_BUFF)
        self.play(DrawBorderThenFill(rect))
        self.play(Write(frac))
        self.wait()
        return rect

    def relate_growth_rate_to_pop_size(self):
        false_deriv = OldTex(
            "{d(2^t) ", "\\over dt}", "= 2^t"
        )
        difference_eq = OldTex(
            "{ {2^{t+1} - 2^t} \\over", "1}", "= 2^t"
        )
        real_deriv = OldTex(
            "{ {2^{t+dt} - 2^t} \\over", "dt}", "= \\, ???"
        )
        VGroup(
            false_deriv[0][3], 
            false_deriv[2][-1],
            difference_eq[0][1],
            difference_eq[0][-2],
            difference_eq[2][-1],
            difference_eq[2][-1],
            real_deriv[0][1],
            real_deriv[0][-2],
        ).set_color(YELLOW)
        VGroup(
            difference_eq[0][3],
            difference_eq[1][-1],
            real_deriv[0][3],
            real_deriv[0][4],
            real_deriv[1][-2],
            real_deriv[1][-1],
        ).set_color(GREEN)

        expressions = [false_deriv, difference_eq, real_deriv]
        text_arg_list = [
            ("Tempting", "...",),
            ("Rate of change", "\\\\ over one full day"),
            ("Rate of change", "\\\\ in a small time"),
        ]
        for expression, text_args in zip(expressions, text_arg_list):
            expression.next_to(
                self.function, DOWN, 
                buff = LARGE_BUFF,
                aligned_edge = LEFT,
            )
            expression.brace = Brace(expression, DOWN)
            expression.brace_text = expression.brace.get_text(*text_args)

        time = self.t_expression[-1]
        new_time = OldTex("3")
        new_time.move_to(time, LEFT)

        fading_creatures = VGroup(*self.get_on_screen_pi_creatures()[8:])


        self.play(*list(map(FadeIn, [
            false_deriv, false_deriv.brace, false_deriv.brace_text
        ])))
        self.wait()
        self.play(
            Transform(time, new_time),
            FadeOut(fading_creatures)
        )
        self.wait()
        for x in range(3):
            self.let_one_day_pass(run_time = 2)
            self.wait(2)

        for expression in difference_eq, real_deriv:
            expression.brace_text[1].set_color(GREEN)
            self.play(
                Transform(false_deriv, expression),
                Transform(false_deriv.brace, expression.brace),
                Transform(false_deriv.brace_text, expression.brace_text),
            )
            self.wait(3)
        self.reset()
        for x in range(self.get_num_days()):
            self.let_one_day_pass()
        self.wait()

        rect = Rectangle(color = YELLOW)
        rect.replace(real_deriv)
        rect.stretch_to_fit_width(rect.get_width()+MED_SMALL_BUFF)
        rect.stretch_to_fit_height(rect.get_height()+MED_SMALL_BUFF)
        self.play(*list(map(FadeOut, [
            false_deriv.brace, false_deriv.brace_text
        ])))
        self.play(ShowCreation(rect))
        self.play(*[
            ApplyFunction(
                lambda pi : pi.change_mode("pondering").look_at(real_deriv),
                pi,
                run_time = 2,
                rate_func = squish_rate_func(smooth, a, a+0.5)
            )
            for pi in self.get_pi_creatures()
            for a in [0.5*random.random()]
        ])
        self.wait(3)

    ###########

    def create_pi_creatures(self):
        width, height = self.pi_creature_grid_dimensions
        creature_array = VGroup(*[
            VGroup(*[
                PiCreature(mode = "plain")
                for y in range(height)
            ]).arrange(UP, buff = MED_LARGE_BUFF)
            for x in range(width)
        ]).arrange(RIGHT, buff = MED_LARGE_BUFF)
        creatures = VGroup(*it.chain(*creature_array))
        creatures.set_height(self.pi_creature_grid_height)
        creatures.to_corner(DOWN+RIGHT)

        colors = color_gradient([BLUE, GREEN, GREY_BROWN], len(creatures))
        random.shuffle(colors)
        for creature, color in zip(creatures, colors):
            creature.set_color(color)

        return creatures

    def reset(self):
        time = self.t_expression[-1]
        faders = [time] + list(self.get_on_screen_pi_creatures())
        new_time = OldTex("0")
        new_time.next_to(self.t_expression[-2], RIGHT)
        first_creature = self.get_pi_creatures()[0]

        self.play(*list(map(FadeOut, faders)))
        self.play(*list(map(FadeIn, [first_creature, new_time])))
        self.t_expression.submobjects[-1] = new_time

    def let_one_day_pass(self, run_time = 2):
        all_creatures = self.get_pi_creatures()
        on_screen_creatures = self.get_on_screen_pi_creatures()
        low_i = len(on_screen_creatures)
        high_i = min(2*low_i, len(all_creatures))
        new_creatures = VGroup(*all_creatures[low_i:high_i])

        to_children_anims = []
        growing_anims = []
        for old_pi, pi in zip(on_screen_creatures, new_creatures):
            pi.save_state()
            child = pi.copy()
            child.scale(0.25, about_point = child.get_bottom())
            child.eyes.scale(1.5, about_point = child.eyes.get_bottom())
            pi.move_to(old_pi)
            pi.set_fill(opacity = 0)

            index = list(new_creatures).index(pi)
            prop = float(index)/len(new_creatures)
            alpha  = np.clip(len(new_creatures)/8.0, 0, 0.5)
            rate_func = squish_rate_func(
                smooth, alpha*prop, alpha*prop+(1-alpha)
            )

            to_child_anim = Transform(pi, child, rate_func = rate_func)
            to_child_anim.update(1)
            growing_anim = ApplyMethod(pi.restore, rate_func = rate_func)
            to_child_anim.update(0)

            to_children_anims.append(to_child_anim)
            growing_anims.append(growing_anim)

        time = self.t_expression[-1]
        total_new_creatures = len(on_screen_creatures) + len(new_creatures)
        new_time = OldTex(str(int(np.log2(total_new_creatures))))
        new_time.move_to(time, LEFT)

        growing_anims.append(Transform(time, new_time))

        self.play(*to_children_anims, run_time = run_time/2.0)
        self.play(*growing_anims, run_time = run_time/2.0)
        
    def get_num_pi_creatures_on_screen(self):
        mobjects = self.get_mobjects()
        return sum([
            pi in mobjects for pi in self.get_pi_creatures()
        ])

    def get_population_size_descriptor(self):
        on_screen_creatures = self.get_on_screen_pi_creatures()
        brace = Brace(on_screen_creatures, LEFT)
        n = len(on_screen_creatures)
        label = brace.get_text(
            "$2^%d$"%int(np.log2(n)),
            "$=%d$"%n,
        )
        brace.add(label)
        return brace

    def get_num_days(self):
        x, y = self.pi_creature_grid_dimensions
        return int(np.log2(x*y))

    def get_curr_day(self):
        return int(np.log2(len(self.get_on_screen_pi_creatures())))

    def get_from_day_to_day_label(self):
        curr_day = self.get_curr_day()
        top_words = OldTexText(
            "From day", str(curr_day), 
            "to", str(curr_day+1), ":"
        )
        top_words.set_width(4)
        top_words.next_to(
            self.function, DOWN,
            buff = MED_LARGE_BUFF,
            aligned_edge = LEFT,
        )
        top_words[1].set_color(GREEN)

        bottom_words = OldTex(
            str(2**curr_day),
            "\\text{ creatures}", "\\over {1 \\text{ day}}"
        )
        bottom_words[0].set_color(GREEN)
        bottom_words.next_to(top_words, DOWN, buff = MED_LARGE_BUFF)

        return top_words, bottom_words
