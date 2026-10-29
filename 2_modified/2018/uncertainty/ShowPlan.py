# ==============================================================================
# Scene:      ShowPlan
# Source:     videos/_2018/uncertainty.py (lines 495-644)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl ShowPlan.py ShowPlan -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - the line endpoints can swap order while the path_arc animation interpolates the wrapper line, giving a negative sigma; a standard deviation is a magnitude, so use abs()
# ==============================================================================

from manim_imports_ext import *
import warnings

warnings.warn("""
    Warning: This file makes use of
    ContinualAnimation, which has since
    been deprecated
""")


class GaussianDistributionWrapper(Line):
    """
    This is meant to encode a 2d normal distribution as
    a mobject (so as to be able to have it be interpolated
    during animations).  It is a line whose center is the mean
    mu of a distribution, and whose radial vector (center to end)
    is the distribution's standard deviation
    """
    CONFIG = {
        "stroke_width" : 0,
        "mu" : ORIGIN,
        "sigma" : RIGHT,
    }
    def __init__(self, **kwargs):
        Line.__init__(self, ORIGIN, RIGHT, **kwargs)
        self.change_parameters(self.mu, self.sigma)

    def change_parameters(self, mu = None, sigma = None):
        curr_mu, curr_sigma = self.get_parameters()
        mu = mu if mu is not None else curr_mu
        sigma = sigma if sigma is not None else curr_sigma
        self.put_start_and_end_on(mu - sigma, mu + sigma)
        return self

    def get_parameters(self):
        """ Return mu_x, mu_y, sigma_x, sigma_y"""
        center, end = self.get_center(), self.get_end()
        return center, end-center

    def get_random_points(self, size = 1):
        mu, sigma = self.get_parameters()
        return np.array([
            np.array([
                # CHANGE: the line endpoints can swap order while the path_arc animation interpolates the wrapper line, giving a negative sigma; a standard deviation is a magnitude, so use abs()
                np.random.normal(mu_coord, abs(sigma_coord))
                for mu_coord, sigma_coord in zip(mu, sigma)
            ])
            for x in range(size)
        ])


class ProbabalisticMobjectCloud(ContinualAnimation):
    CONFIG = {
        "fill_opacity" : 0.25,
        "n_copies" : 100,
        "gaussian_distribution_wrapper_config" : {},
        "time_per_change" : 1./60,
        "start_up_time" : 0,
    }
    def __init__(self, prototype, **kwargs):
        digest_config(self, kwargs)
        fill_opacity = self.fill_opacity or prototype.get_fill_opacity()
        if "mu" not in self.gaussian_distribution_wrapper_config:
            self.gaussian_distribution_wrapper_config["mu"] = prototype.get_center()
        self.gaussian_distribution_wrapper = GaussianDistributionWrapper(
            **self.gaussian_distribution_wrapper_config
        )
        self.time_since_last_change = np.inf
        group = VGroup(*[
            prototype.copy().set_fill(opacity = fill_opacity)
            for x in range(self.n_copies)
        ])
        ContinualAnimation.__init__(self, group, **kwargs)
        self.update_mobject(0)

    def update_mobject(self, dt):
        self.time_since_last_change += dt
        if self.time_since_last_change < self.time_per_change:
            return
        self.time_since_last_change = 0

        group = self.mobject
        points = self.gaussian_distribution_wrapper.get_random_points(len(group))
        for mob, point in zip(group, points):
            self.update_mobject_by_point(mob, point)
        return self

    def update_mobject_by_point(self, mobject, point):
        mobject.move_to(point)
        return self


class ProbabalisticDotCloud(ProbabalisticMobjectCloud):
    CONFIG = {
        "color" : BLUE,
    }
    def __init__(self, **kwargs):
        digest_config(self, kwargs)
        dot = Dot(color = self.color)
        ProbabalisticMobjectCloud.__init__(self, dot)


class RadarDish(SVGMobject):
    CONFIG = {
        "file_name" : "radar_dish",
        "fill_color" : GREY_B,
        "stroke_color" : WHITE,
        "stroke_width" : 1,
        "height" : 1,
    }


class Plane(SVGMobject):
    CONFIG = {
        "file_name" : "plane",
        "color" : GREY_B,
        "height" : 1,
    }
    def __init__(self, **kwargs):
        SVGMobject.__init__(self, **kwargs)
        self.rotate(-TAU/4)


class RadarPulseSingleton(ContinualAnimation):
    CONFIG = {
        "speed" : 3.0,
        "direction" : RIGHT,
        "start_up_time" : 0,
        "fade_in_time" : 0.5,
        "color" : WHITE,
        "stroke_width" : 3,
    }
    def __init__(self, radar_dish, target, **kwargs):
        digest_config(self, kwargs)
        self.direction = self.direction/get_norm(self.direction)
        self.radar_dish = radar_dish
        self.target = target
        self.reflection_distance = None
        self.arc = Arc(
            start_angle = -30*DEGREES,
            angle = 60*DEGREES,
        )
        self.arc.set_height(0.75*radar_dish.get_height())
        self.arc.move_to(radar_dish, UP+RIGHT)
        self.start_points = np.array(self.arc.get_points())
        self.start_center = self.arc.get_center()
        self.finished = False

        ContinualAnimation.__init__(self, self.arc, **kwargs)
        
    def update_mobject(self, dt):
        arc = self.arc
        total_distance = self.speed*self.internal_time
        arc.set_points(self.start_points)
        arc.shift(total_distance*self.direction)

        if self.internal_time < self.fade_in_time:
            alpha = np.clip(self.internal_time/self.fade_in_time, 0, 1)
            arc.set_stroke(self.color, alpha*self.stroke_width)

        if self.reflection_distance is None:
            #Check if reflection is happening
            arc_point = arc.get_edge_center(self.direction)
            target_point = self.target.get_edge_center(-self.direction)
            arc_distance = np.dot(arc_point, self.direction)
            target_distance = np.dot(target_point, self.direction)
            if arc_distance > target_distance:
                self.reflection_distance = target_distance
        #Don't use elif in case the above code creates reflection_distance
        if self.reflection_distance is not None:
            delta_distance = total_distance - self.reflection_distance
            point_distances = np.dot(self.direction, arc.get_points().T)
            diffs = point_distances - self.reflection_distance
            shift_vals = np.outer(-2*np.maximum(diffs, 0), self.direction)
            arc.set_points(arc.get_points() + shift_vals)

            #Check if done
            arc_point = arc.get_edge_center(-self.direction)
            if np.dot(arc_point, self.direction) < np.dot(self.start_center, self.direction):
                self.finished = True
                self.arc.fade(1)

    def is_finished(self):
        return self.finished


class RadarPulse(ContinualAnimation):
    CONFIG = {
        "n_pulse_singletons" : 8,
        "frequency" : 0.05,
        "colors" : [BLUE, YELLOW]
    }
    def __init__(self, *args, **kwargs):
        digest_config(self, kwargs)
        colors = color_gradient(self.colors, self.n_pulse_singletons)
        self.pulse_singletons = [
            RadarPulseSingleton(*args, color = color, **kwargs)
            for color in colors
        ]
        pluse_mobjects = VGroup(*[ps.mobject for ps in self.pulse_singletons])
        ContinualAnimation.__init__(self, pluse_mobjects, **kwargs)
        
    def update_mobject(self, dt):
        for i, ps in enumerate(self.pulse_singletons):
            ps.internal_time = self.internal_time - i*self.frequency
            ps.update_mobject(dt)

    def is_finished(self):
        return all([ps.is_finished() for ps in self.pulse_singletons])


class ShowPlan(PiCreatureScene):
    def construct(self):
        self.add_title()
        words = self.get_words()
        self.play_sound_anims(words[0])
        self.play_doppler_anims(words[1])
        self.play_quantum_anims(words[2])

    def add_title(self):
        title = OldTexText("The plan")
        title.scale(1.5)
        title.to_edge(UP)
        h_line = Line(LEFT, RIGHT).scale(FRAME_X_RADIUS)
        h_line.next_to(title, DOWN)
        self.add(title, h_line)

    def get_words(self):
        trips = [
            ("sound waves", "(time vs. frequency)", YELLOW),
            ("Doppler radar", "(distance vs. velocity)", GREEN),
            ("quantum particles", "(position vs. momentum)", BLUE),
        ]
        words = VGroup()
        for topic, tradeoff, color in trips:
            word = OldTexText("Uncertainty for", topic, tradeoff)
            word[1:].set_color(color)
            word[2].scale(0.75)
            word[2].next_to(word[1], DOWN, buff = 1.5*SMALL_BUFF)
            words.add(word)
        words.arrange(DOWN, aligned_edge = LEFT, buff = MED_LARGE_BUFF)
        words.to_edge(LEFT)

        return words

    def play_sound_anims(self, word):
        morty = self.pi_creature
        wave = FunctionGraph(
            lambda x : 0.3*np.sin(15*x)*np.sin(0.5*x),
            x_min = 0, x_max = 30,
            step_size = 0.001,
        )
        wave.next_to(word, RIGHT)
        rect = BackgroundRectangle(wave, fill_opacity = 1)
        rect.stretch(2, 1)
        rect.next_to(wave, LEFT, buff = 0)
        always_shift(wave, direction=LEFT, rate=5)
        wave_fader = UpdateFromAlphaFunc(
            wave, 
            lambda w, a : w.set_stroke(width = 3*a)
        )
        checkmark = self.get_checkmark(word)

        self.add(wave)
        self.add_foreground_mobjects(rect, word)
        self.play(
            Animation(word),
            wave_fader,
            morty.change, "raise_right_hand", word
        )
        self.wait(2)
        wave_fader.rate_func = lambda a : 1-smooth(a)
        self.add_foreground_mobjects(checkmark)
        self.play(
            Write(checkmark),
            morty.change, "happy",
            wave_fader, 
        )
        self.remove_foreground_mobjects(rect, word)
        self.add(word)
        self.wait()

    def play_doppler_anims(self, word):
        morty = self.pi_creature

        radar_dish = RadarDish()
        radar_dish.next_to(word, DOWN, aligned_edge = LEFT)
        target = Plane()
        # target.match_height(radar_dish)
        target.next_to(radar_dish, RIGHT, buff = LARGE_BUFF)
        always_shift(target, direction = RIGHT, rate = 1.25)

        pulse = RadarPulse(radar_dish, target)

        checkmark = self.get_checkmark(word)

        self.add(target)
        self.play(
            Write(word),
            DrawBorderThenFill(radar_dish),
            UpdateFromAlphaFunc(
                target, lambda m, a : m.set_fill(opacity = a)
            ),
            morty.change, "pondering",
            run_time = 1
        )
        self.add(pulse)
        count = it.count() #TODO, this is not a great hack...
        while not pulse.is_finished() and next(count) < 15:
            self.play(
                morty.look_at, pulse.mobject,
                run_time = 0.5
            )
        self.play(
            Write(checkmark),
            UpdateFromAlphaFunc(
                target, lambda m, a : m.set_fill(opacity = 1-a)
            ),
            FadeOut(radar_dish),
            morty.change, "happy"
        )
        self.wait()

    def play_quantum_anims(self, word):
        morty = self.pi_creature
        dot_cloud = ProbabalisticDotCloud()
        gdw = dot_cloud.gaussian_distribution_wrapper
        gdw.next_to(word, DOWN, MED_LARGE_BUFF)
        gdw.rotate(5*DEGREES)
        gdw.save_state()
        gdw.scale(0)


        checkmark = self.get_checkmark(word)
        ish = OldTexText("$\\dots$ish")
        ish.next_to(checkmark, RIGHT, -SMALL_BUFF, DOWN)

        self.add(dot_cloud)
        self.play(
            Write(word),
            FadeIn(dot_cloud.mobject),
            morty.change, "confused",
        )
        self.play(gdw.restore, run_time = 2)
        self.play(Write(checkmark))
        self.wait()
        self.play(
            Write(ish), 
            morty.change, 'maybe'
        )
        self.wait(6)


    ##

    def get_checkmark(self, word):
        checkmark = OldTex("\\checkmark")
        checkmark.set_color(GREEN)
        checkmark.scale(1.25)
        checkmark.next_to(word[1], UP+RIGHT, buff = 0)
        return checkmark
