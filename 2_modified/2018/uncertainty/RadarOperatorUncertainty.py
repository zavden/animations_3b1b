# ==============================================================================
# Scene:      RadarOperatorUncertainty
# Source:     videos/_2018/uncertainty.py (lines 2251-2305)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl RadarOperatorUncertainty.py RadarOperatorUncertainty -w -m --fps 15
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


class RadarOperatorUncertainty(Scene):
    def construct(self):
        dish = RadarDish()
        dish.scale(3)
        dish.move_to(4*RIGHT + 2*DOWN)
        dish_words = OldTexText("3b1b industrial \\\\ enterprises")
        dish_words.scale(0.25)
        dish_words.set_stroke(BLACK, 0.5)
        dish_words.set_color(BLACK)
        dish_words.move_to(dish, DOWN)
        dish_words.shift(SMALL_BUFF*(UP+2*LEFT))
        dish.add(dish_words)
        randy = Randolph()
        randy.next_to(dish, LEFT, aligned_edge = DOWN)
        bubble = randy.get_bubble(
            width = 7,
            height = 4,
        )

        echo_object = Square()
        echo_object.move_to(dish)
        echo_object.shift(FRAME_X_RADIUS*RIGHT)
        pulse = RadarPulse(dish, echo_object, speed = 6)

        plane = Plane().scale(0.5)
        plane.move_to(bubble.get_bubble_center()+LEFT)
        plane_cloud = ProbabalisticMobjectCloud(
            plane, 
            fill_opacity = 0.3,
            n_copies = 10,
        )
        plane_gdw = plane_cloud.gaussian_distribution_wrapper

        vector_cloud = ProbabalisticVectorCloud(
            center_func = plane_gdw.get_center,
        )
        vector_gdw = vector_cloud.gaussian_distribution_wrapper
        vector_gdw.scale(0.05)
        vector_gdw.move_to(plane_gdw)
        vector_gdw.shift(2*RIGHT)

        self.add(randy, dish, bubble, plane_cloud, pulse)
        self.play(randy.change, "confused")
        self.wait(3)
        self.add(vector_cloud)
        for i in range(3):
            for plane_factor, vector_factor, freq in (0.05, 10, 0.01), (20, 0.1, 0.1):
                pulse.internal_time = 0
                pulse.frequency = freq
                self.play(
                    randy.change, "pondering", plane,
                    plane_gdw.scale, plane_factor,
                    vector_gdw.scale, vector_factor,
                )
                self.wait(2)
