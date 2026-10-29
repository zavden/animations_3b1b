# ==============================================================================
# Scene:      ShowMomentumFormula
# Source:     videos/_2018/uncertainty.py (lines 3032-3200)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl ShowMomentumFormula.py ShowMomentumFormula -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - AnimationGroup has no sub_anims in GL; the target of ApplyMethod(particle.move_to, xi_words) is centered on xi_words
# ==============================================================================

from manim_imports_ext import *
import warnings

warnings.warn("""
    Warning: This file makes use of
    ContinualAnimation, which has since
    been deprecated
""")


class IntroduceDeBroglie(Scene):
    CONFIG = {
        "default_wave_frequency" : 1,
        "wave_colors" : [BLUE_D, YELLOW],
        "dispersion_factor" : 1,
        "amplitude" : 1,
    }
    def construct(self):
        text_scale_val = 0.8,

        #Overlay real tower in video editor
        eiffel_tower = Line(3*DOWN, 3*UP, stroke_width = 0)
        picture = ImageMobject("de_Broglie")
        picture.set_height(4)
        picture.to_corner(UP+LEFT)
        name = OldTexText("Louis de Broglie")
        name.next_to(picture, DOWN)

        picture.save_state()
        picture.scale(0)
        picture.move_to(eiffel_tower.get_top())


        broadcasts = [
            Broadcast(
                eiffel_tower.get_top(),
                big_radius = 10,
                n_circles = 10,
                lag_ratio = 0.9,
                run_time = 7,
                rate_func = squish_rate_func(smooth, a, a+0.3),
                color = WHITE,
            )
            for a in np.linspace(0, 0.7, 3)
        ]

        self.play(*broadcasts)
        self.play(picture.restore)
        self.play(Write(name))
        self.wait()

        #Time line
        time_line = NumberLine(
            x_min = 1900,
            x_max = 1935,
            tick_frequency = 1,
            big_tick_numbers = list(range(1900, 1941, 10)),
            color = BLUE_D
        )
        time_line.stretch_to_fit_width(FRAME_WIDTH - picture.get_width() - 2)
        time_line.add_numbers(*time_line.big_tick_numbers)
        time_line.next_to(picture, RIGHT, MED_LARGE_BUFF, DOWN)

        year_to_words = {
            1914 : "Wold War I begins",
            1915 : "Einstein field equations",
            1916 : "Lewis dot formulas",
            1917 : "Not a lot of physics...because war",
            1918 : "S'more Rutherford badassery",
            1919 : "Eddington confirms general relativity predictions",
            1920 : "World is generally stoked on general relativity",
            1921 : "Einstein gets long overdue Nobel prize",
            1922 : "Stern-Gerlach Experiment",
            1923 : "Compton scattering observed",
            1924 : "de Broglie's thesis"
        }
        arrow = Vector(DOWN, color = WHITE)
        arrow.next_to(time_line.number_to_point(1914), UP)
        words = OldTexText(year_to_words[1914])
        words.scale(text_scale_val)
        date = Integer(1914)
        date.next_to(arrow, UP, LARGE_BUFF)

        def get_year(alpha = 0):
            return int(time_line.point_to_number(arrow.get_end()))

        def update_words(words):
            text = year_to_words.get(get_year(), "Hi there")
            if text not in words.get_tex():
                words.__init__(text)
                words.scale(text_scale_val)
            words.move_to(interpolate(
                arrow.get_top(), date.get_bottom(), 0.5
            ))
        update_words(words)
        self.play(
            FadeIn(time_line),
            GrowArrow(arrow),
            Write(words),
            Write(date),
            run_time = 1
        )
        self.wait()
        self.play(
            arrow.next_to, time_line.number_to_point(1924), UP,
            ChangingDecimal(
                date, get_year,
                position_update_func = lambda m : m.next_to(arrow, UP, LARGE_BUFF)
            ),
            UpdateFromFunc(words, update_words),
            run_time = 3,
        )
        self.wait()

        #Transform time_line
        line = time_line
        self.play(
            FadeOut(time_line.numbers),
            VGroup(arrow, words, date).shift, MED_LARGE_BUFF*UP,
            *[
                ApplyFunction(
                    lambda m : m.rotate(TAU/4).set_stroke(width = 0),
                    mob,
                    remover = True
                )
                for mob in time_line.tick_marks
            ]
        )

        #Wave function
        particle = VectorizedPoint()
        axes = Axes(x_min = -1, x_max = 10)
        axes.match_width(line)
        axes.shift(line.get_center() - axes.x_axis.get_center())
        im_line = line.copy()
        im_line.set_color(YELLOW)
        wave_update_animation = self.get_wave_update_animation(
            axes, particle, line, im_line
        )

        for x in range(3):
            particle.move_to(axes.coords_to_point(-10, 0))
            self.play(
                ApplyMethod(
                    particle.move_to, axes.coords_to_point(22, 0),
                    rate_func=linear
                ),
                wave_update_animation,
                run_time = 3
            )
            self.wait()

    ###
    def get_wave_update_animation(self, axes, particle, re_line = None, im_line = None):
        line = Line(
            axes.x_axis.get_left(),
            axes.x_axis.get_right(),
        )
        if re_line is None:
            re_line = line.copy()
            re_line.set_color(self.wave_colors[0])
        if im_line is None:
            im_line = line.copy()
            im_line.set_color(self.wave_colors[1])
        lines = VGroup(im_line, re_line)
        def update_lines(lines):
            waves = self.get_wave_pair(axes, particle)
            for line, wave in zip(lines, waves):
                wave.match_style(line)
                Transform(line, wave).update(1)
        return UpdateFromFunc(lines, update_lines)

    def get_wave(
        self, axes, particle, 
        complex_to_real_func = lambda z : z.real,
        freq = None, 
        **kwargs):
        freq = freq or self.default_wave_frequency
        k0 = 1./freq
        t0 = axes.x_axis.point_to_number(particle.get_center())
        def func(x):
            dispersion = fdiv(1., self.dispersion_factor)*(np.sqrt(1./(1+t0**2)))
            wave_part = complex_to_real_func(np.exp(
                complex(0, TAU*freq*(x-dispersion))
            ))
            bell_part = np.exp(-dispersion*(x-t0)**2)
            amplitude = self.amplitude
            return amplitude*wave_part*bell_part
        graph = axes.get_graph(func)
        return graph

    def get_wave_pair(self, axes, particle, colors = None, **kwargs):
        if colors is None and "color" not in kwargs:
            colors = self.wave_colors
        return VGroup(*[
            self.get_wave(
                axes, particle, 
                C_to_R, color = color, 
                **kwargs
            )
            for C_to_R, color in zip(
                [lambda z : z.imag, lambda z : z.real], 
                colors
            )
        ])


class ShowMomentumFormula(IntroduceDeBroglie, TeacherStudentsScene):
    CONFIG = {
        "default_wave_frequency" : 2,
        "dispersion_factor" : 0.25,
        "p_color" : BLUE,
        "xi_color" : YELLOW,
        "amplitude" : 0.5,
    }
    def construct(self):
        self.introduce_formula()
        self.react_to_claim()

    def introduce_formula(self):
        formula = p, eq, h, xi = OldTex("p", "=", "h", "\\xi")
        formula.move_to(ORIGIN)
        formula.scale(1.5)

        word_shift_val = 1.75
        p_words = OldTexText("Momentum")
        p_words.next_to(p, UP, LARGE_BUFF).shift(word_shift_val*LEFT)
        p_arrow = Arrow(
            p_words.get_bottom(), p.get_corner(UP+LEFT),
            buff = SMALL_BUFF
        )
        added_p_words = OldTexText("(Classically $m \\times v$)")
        added_p_words.move_to(p_words, DOWN)
        VGroup(p, p_words, added_p_words, p_arrow).set_color(self.p_color)

        xi_words = OldTexText("Spatial frequency")
        added_xi_words = OldTexText("(cycles per unit \\emph{distance})")
        xi_words.next_to(xi, UP, LARGE_BUFF).shift(word_shift_val*RIGHT)
        xi_words.align_to(p_words)
        xi_arrow = Arrow(
            xi_words.get_bottom(), xi.get_corner(UP+RIGHT), 
            buff = SMALL_BUFF
        )
        added_xi_words.move_to(xi_words, DOWN)
        added_xi_words.align_to(added_p_words, DOWN)
        VGroup(xi, xi_words, added_xi_words, xi_arrow).set_color(self.xi_color)

        axes = Axes(
            x_min = 0, x_max = FRAME_WIDTH,
            y_min = -1, y_max = 1,
        )
        axes.center().to_edge(UP, buff = -0.5)
        # axes.next_to(formula, RIGHT)
        particle = VectorizedPoint()
        wave_update_animation = self.get_wave_update_animation(axes, particle)
        wave = wave_update_animation.mobject
        wave[0].set_stroke(width = 0)
        particle.next_to(wave, LEFT, buff = 2)
        wave_propagation = AnimationGroup(
            ApplyMethod(particle.move_to, axes.coords_to_point(30, 0)),
            wave_update_animation,
            run_time = 4,
            rate_func=linear,
        )
        stopped_wave_propagation = AnimationGroup(
            ApplyMethod(particle.move_to, xi_words),
            wave_update_animation,
            run_time = 3,
            rate_func=linear,
        )
        n_v_lines = 10
        v_lines = VGroup(*[
            DashedLine(UP, DOWN)
            for x in range(n_v_lines)
        ])
        v_lines.match_color(xi)
        v_lines.arrange(
            RIGHT,
            buff = float(axes.x_axis.unit_size)/self.default_wave_frequency
        )
        # CHANGE: AnimationGroup has no sub_anims in GL; the target of ApplyMethod(particle.move_to, xi_words) is centered on xi_words
        v_lines.move_to(xi_words)
        v_lines.align_to(wave)
        v_lines.shift(0.125*RIGHT)
        
        self.add(formula, wave)
        self.play(
            self.teacher.change, "raise_right_hand", 
            GrowArrow(p_arrow),
            Succession(
                Write, p_words,
                ApplyMethod, p_words.next_to, added_p_words, UP,
            ),
            FadeIn(
                added_p_words,
                rate_func = squish_rate_func(smooth, 0.5, 1),
                run_time = 2,
            ),
            wave_propagation
        )
        self.play(
            Write(xi_words),
            GrowArrow(xi_arrow),
            self.change_students("confused", "erm", "sassy"),
            stopped_wave_propagation
        )
        self.play(
            FadeIn(added_xi_words),
            xi_words.next_to, added_xi_words, UP,
        )
        self.play(
            LaggedStartMap(ShowCreation, v_lines),
            self.change_students(*["pondering"]*3)
        )
        self.play(LaggedStartMap(FadeOut, v_lines))
        self.wait()

        self.formula_labels = VGroup(
            p_words, p_arrow, added_p_words,
            xi_words, xi_arrow, added_xi_words, 
        )        
        self.set_variables_as_attrs(wave, wave_propagation, formula)

    def react_to_claim(self):
        formula_labels = self.formula_labels
        full_formula = VGroup(self.formula, formula_labels)
        full_formula.save_state()
        wave_propagation = self.wave_propagation

        student = self.students[2]
        self.student_says(
            "Hang on...",
            bubble_config = {"height" : 2, "width" : 2, "direction" : LEFT},
            target_mode = "sassy",
            index = 2,
            added_anims = [self.teacher.change, "plain"]
        )
        student.bubble.add(student.bubble.content)
        self.wait()
        kwargs = {
            "path_arc" : TAU/4,
            "lag_ratio" : 0.5,
            "lag_ratio" : 0.7,
            "run_time" : 1.5,
        }
        self.play(
            full_formula.scale, 0,
            full_formula.move_to, student.eyes.get_bottom()+SMALL_BUFF*DOWN,
            Animation(student.bubble),
            **kwargs
        )
        self.play(full_formula.restore, Animation(student.bubble), **kwargs)
        wave_propagation.update_config(
            rate_func = lambda a : interpolate(0.35, 1, a)
        )
        self.play(
            wave_propagation, 
            RemovePiCreatureBubble(student, target_mode = "confused"),
        )
        wave_propagation.update_config(rate_func = lambda t : t)
        self.student_says(
            "Physics is \\\\ just weird",
            bubble_config = {"height" : 2.5, "width" : 3},
            target_mode = "shruggie",
            index = 0,
            added_anims = [ApplyMethod(full_formula.shift, UP)]
        )
        self.wait()
        self.play(
            wave_propagation,
            ApplyMethod(full_formula.shift, DOWN),
            FadeOut(self.students[0].bubble),
            FadeOut(self.students[0].bubble.content),
            self.change_students(*3*["pondering"]),
            self.teacher.change, "pondering",
        )
        self.play(wave_propagation)
