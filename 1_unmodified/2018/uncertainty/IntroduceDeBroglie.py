# ==============================================================================
# Scene:      IntroduceDeBroglie
# Source:     videos/_2018/uncertainty.py (lines 2836-3030)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl IntroduceDeBroglie.py IntroduceDeBroglie -w -m --fps 15
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
