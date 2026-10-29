# ==============================================================================
# Scene:      ThinkOfHeisenbergUncertainty
# Source:     videos/_2018/uncertainty.py (lines 4274-4363)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl ThinkOfHeisenbergUncertainty.py ThinkOfHeisenbergUncertainty -w -m --fps 15
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


class ProbabalisticVectorCloud(ProbabalisticMobjectCloud):
    CONFIG = {
        "color" : RED,
        "n_copies" : 20,
        "fill_opacity" : 0.5,
        "center_func" : lambda : ORIGIN,
    }
    def __init__(self, **kwargs):
        digest_config(self, kwargs)
        vector = Vector(
            RIGHT, color = self.color,
            max_tip_length_to_length_ratio = 1,
        )
        ProbabalisticMobjectCloud.__init__(self, vector)

    def update_mobject_by_point(self, vector, point):
        vector.put_start_and_end_on(
            self.center_func(),
            point
        )


class ThinkOfHeisenbergUncertainty(PiCreatureScene):
    def construct(self):
        morty = self.pi_creature
        morty.center().to_edge(DOWN).shift(LEFT)

        dot_cloud = ProbabalisticDotCloud()
        dot_gdw = dot_cloud.gaussian_distribution_wrapper
        dot_gdw.set_width(1)
        dot_gdw.rotate(TAU/8)
        dot_gdw.move_to(FRAME_X_RADIUS*RIGHT/2),

        vector_cloud = ProbabalisticVectorCloud(
            center_func = dot_gdw.get_center
        )
        vector_gdw = vector_cloud.gaussian_distribution_wrapper
        vector_gdw.set_width(0.1)
        vector_gdw.rotate(TAU/8)
        vector_gdw.next_to(dot_gdw, UP+LEFT, LARGE_BUFF)

        time_tracker = ValueTracker(0)
        self.add()
        freq = 1
        continual_anims = [
            always_shift(time_tracker, direction = RIGHT, rate = 1),
            Mobject.add_updater(
                dot_gdw,
                lambda d : d.set_width(
                    (np.cos(freq*time_tracker.get_value()) + 1.1)/2
                )
            ),
            Mobject.add_updater(
                vector_gdw,
                lambda d : d.set_width(
                    (-np.cos(freq*time_tracker.get_value()) + 1.1)/2
                )
            ),
            dot_cloud, vector_cloud
        ]
        self.add(*continual_anims)

        position, momentum, time, frequency = list(map(TexText, [
            "Position", "Momentum", "Time", "Frequency"
        ]))
        VGroup(position, time).set_color(BLUE)
        VGroup(momentum, frequency).set_color(YELLOW)
        groups = VGroup()
        for m1, m2 in (position, momentum), (time, frequency):
            arrow = OldTex("\\updownarrow").scale(1.5)
            group = VGroup(m1, arrow, m2)
            group.arrange(DOWN)
            lp, rp = parens = OldTex("\\big(\\big)")
            parens.stretch(1.5, 1)
            parens.match_height(group)
            lp.next_to(group, LEFT, buff = SMALL_BUFF)
            rp.next_to(group, RIGHT, buff = SMALL_BUFF)
            group.add(parens)
            groups.add(group)
        arrow = OldTex("\\Leftrightarrow").scale(2)
        groups.submobjects.insert(1, arrow)
        groups.arrange(RIGHT)
        groups.next_to(morty, UP+RIGHT, LARGE_BUFF)
        groups.shift_onto_screen()


        self.play(PiCreatureBubbleIntroduction(
            morty, "Heisenberg \\\\ uncertainty \\\\ principle",
            bubble_type = ThoughtBubble,
            bubble_config = {"height" : 4, "width" : 4, "direction" : RIGHT},
            target_mode = "pondering"
        ))
        self.wait()
        self.play(morty.change, "confused", dot_gdw)
        self.wait(10)
        self.play(
            ApplyMethod(
                VGroup(dot_gdw, vector_gdw ).shift, 
                FRAME_X_RADIUS*RIGHT,
                rate_func = running_start
            )
        )
        self.remove(*continual_anims)
        self.play(
            morty.change, "raise_left_hand", groups,
            FadeIn(
                groups, 
                lag_ratio = 0.5,
                run_time = 3,
            )
        )
        self.wait(2)
