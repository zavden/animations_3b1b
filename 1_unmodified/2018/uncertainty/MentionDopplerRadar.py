# ==============================================================================
# Scene:      MentionDopplerRadar
# Source:     videos/_2018/uncertainty.py (lines 1649-1686)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl MentionDopplerRadar.py MentionDopplerRadar -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *
import warnings

warnings.warn("""
    Warning: This file makes use of
    ContinualAnimation, which has since
    been deprecated
""")


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


class MentionDopplerRadar(TeacherStudentsScene):
    def construct(self):
        words = OldTexText("Doppler Radar")
        words.next_to(self.teacher, UP)
        words.save_state()
        words.shift(DOWN).fade(1)
        dish = RadarDish()
        dish.next_to(self.students, UP, buff = 2, aligned_edge = LEFT)
        plane = Plane()
        plane.to_edge(RIGHT)
        plane.align_to(dish)
        always_shift(plane, LEFT, 1)
        plane.flip()
        pulse = RadarPulse(dish, plane)
        look_at_anims = [
            Mobject.add_updater(
                pi, lambda pi : pi.look_at(pulse.mobject)
            )
            for pi in self.get_pi_creatures()
        ]

        self.add(dish, plane, pulse, *look_at_anims)
        self.play(
            self.teacher.change, "hooray",
            words.restore
        )
        self.play_student_changes("pondering", "erm", "sassy")
        self.wait(2)
        self.play(
            self.teacher.change, "happy",
            self.change_students(*["thinking"]*3)
        )
        self.wait()
        dish.set_stroke(width = 0)
        self.play(UpdateFromAlphaFunc(
            VGroup(plane, dish),
            lambda m, a : m.set_fill(opacity = 1 - a)
        ))
