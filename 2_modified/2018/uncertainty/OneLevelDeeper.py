# ==============================================================================
# Scene:      OneLevelDeeper
# Source:     videos/_2018/uncertainty.py (lines 4170-4203)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl OneLevelDeeper.py OneLevelDeeper -w -m --fps 15
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


class OneLevelDeeper(Scene):
    def construct(self):
        heisenberg = ImageMobject("Heisenberg")
        heisenberg.to_corner(UP+LEFT)
        self.add(heisenberg)

        hup_words = OldTexText("Heisenberg's uncertainty principle")
        wave_words = OldTexText("Interpretation of the wave function")
        arrow = Vector(UP)
        group = VGroup(hup_words, arrow, wave_words)
        group.arrange(DOWN)

        randomness = ProbabalisticMobjectCloud(
            OldTexText("Randomness"),
            n_copies = 5,
            time_per_change = 0.05
        )
        gdw = randomness.gaussian_distribution_wrapper
        gdw.rotate(TAU/4)
        gdw.set_height(1)
        # gdw.set_width(4)
        gdw.next_to(hup_words, UP, MED_LARGE_BUFF)

        self.add(hup_words, randomness)
        self.wait(4)
        self.play(
            FadeIn(wave_words),
            GrowArrow(arrow),
            ApplyMethod(
                gdw.next_to, wave_words, DOWN, MED_LARGE_BUFF,
                path_arc = TAU/2,
            )
        )
        self.wait(6)
