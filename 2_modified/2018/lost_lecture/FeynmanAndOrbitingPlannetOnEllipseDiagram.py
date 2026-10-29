# ==============================================================================
# Scene:      FeynmanAndOrbitingPlannetOnEllipseDiagram
# Source:     videos/_2018/lost_lecture.py (lines 360-400)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl FeynmanAndOrbitingPlannetOnEllipseDiagram.py FeynmanAndOrbitingPlannetOnEllipseDiagram -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - same: comet is a member of the Orbiting group, so use the group as foreground
# ==============================================================================

from manim_imports_ext import *

# TODO, this is untested after turning it from a
# ContinualAnimation into a VGroup
class Orbiting(VGroup):
    CONFIG = {
        "rate": 7.5,
    }

    def __init__(self, planet, star, ellipse, **kwargs):
        VGroup.__init__(self, **kwargs)
        self.add(planet)
        self.planet = planet
        self.star = star
        self.ellipse = ellipse
        # Proportion of the way around the ellipse
        self.proportion = 0
        planet.move_to(ellipse.point_from_proportion(0))

        self.add_updater(lambda m, dt: m.update(dt))

    def update(self, dt):
        # time = self.internal_time

        planet = self.planet
        star = self.star
        ellipse = self.ellipse

        rate = self.rate
        radius_vector = planet.get_center() - star.get_center()
        rate *= 1.0 / get_norm(radius_vector)

        prop = self.proportion
        d_prop = 0.001
        ds = get_norm(op.add(
            ellipse.point_from_proportion((prop + d_prop) % 1),
            -ellipse.point_from_proportion(prop),
        ))

        delta_prop = (d_prop / ds) * rate * dt

        self.proportion = (self.proportion + delta_prop) % 1
        planet.move_to(
            ellipse.point_from_proportion(self.proportion)
        )


class ShowEmergingEllipse(Scene):
    CONFIG = {
        "circle_radius": 3,
        "circle_color": BLUE,
        "num_lines": 150,
        "lines_stroke_width": 1,
        "eccentricity_vector": 2 * RIGHT,
        "ghost_lines_stroke_color": GREY_B,
        "ghost_lines_stroke_width": 0.5,
        "ellipse_color": PINK,
    }

    def construct(self):
        circle = self.get_circle()
        e_point = self.get_eccentricity_point()
        e_dot = Dot(e_point, color=YELLOW)
        lines = self.get_lines()
        ellipse = self.get_ellipse()

        fade_rect = FullScreenFadeRectangle()

        line = lines[len(lines) // 5]
        line_dot = Dot(line.get_center(), color=YELLOW)
        line_dot.scale(0.5)

        ghost_line = self.get_ghost_lines(line)
        ghost_lines = self.get_ghost_lines(lines)

        rot_words = OldTexText("Rotate $90^\\circ$ \\\\ about center")
        rot_words.next_to(line_dot, RIGHT)

        elbow = self.get_elbow(line)

        eccentric_words = OldTexText("``Eccentric'' point")
        eccentric_words.next_to(circle.get_center(), DOWN)

        ellipse_words = OldTexText("Perfect ellipse")
        ellipse_words.next_to(ellipse, UP, SMALL_BUFF)

        for text in rot_words, ellipse_words:
            text.add_to_back(text.copy().set_stroke(BLACK, 5))

        shuffled_lines = VGroup(*lines)
        random.shuffle(shuffled_lines.submobjects)

        self.play(ShowCreation(circle))
        self.play(
            FadeIn(e_dot, LEFT),
            Write(eccentric_words, run_time=1)
        )
        self.wait()
        self.play(
            LaggedStartMap(ShowCreation, shuffled_lines),
            Animation(VGroup(e_dot, circle)),
            FadeOut(eccentric_words)
        )
        self.add(ghost_lines)
        self.add(e_dot, circle)
        self.wait()
        self.play(
            FadeIn(fade_rect),
            Animation(line),
            GrowFromCenter(line_dot),
            FadeInFromDown(rot_words),
        )
        self.wait()
        self.add(ghost_line)
        self.play(
            MoveToTarget(line, path_arc=90 * DEGREES),
            Animation(rot_words),
            ShowCreation(elbow)
        )
        self.wait()
        self.play(
            FadeOut(fade_rect),
            FadeOut(line_dot),
            FadeOut(rot_words),
            FadeOut(elbow),
            Animation(line),
            Animation(ghost_line)
        )
        self.play(
            LaggedStartMap(MoveToTarget, lines, run_time=4),
            Animation(VGroup(e_dot, circle))
        )
        self.wait()
        self.play(
            ShowCreation(ellipse),
            FadeInFromDown(ellipse_words)
        )
        self.wait()

    def get_circle(self):
        circle = self.circle = Circle(
            radius=self.circle_radius,
            color=self.circle_color
        )
        return circle

    def get_eccentricity_point(self):
        return self.circle.get_center() + self.eccentricity_vector

    def get_lines(self):
        center = self.circle.get_center()
        radius = self.circle.get_width() / 2
        e_point = self.get_eccentricity_point()
        lines = VGroup(*[
            Line(
                e_point,
                center + rotate_vector(radius * RIGHT, angle)
            )
            for angle in np.linspace(0, TAU, self.num_lines)
        ])
        lines.set_stroke(width=self.lines_stroke_width)
        for line in lines:
            line.generate_target()
            line.target.rotate(90 * DEGREES)
        return lines

    def get_ghost_lines(self, lines):
        return lines.copy().set_stroke(
            color=self.ghost_lines_stroke_color,
            width=self.ghost_lines_stroke_width
        )

    def get_elbow(self, line):
        elbow = VGroup(Line(UP, UL), Line(UL, LEFT))
        elbow.set_stroke(width=1)
        elbow.scale(0.2, about_point=ORIGIN)
        elbow.rotate(
            line.get_angle() - 90 * DEGREES,
            about_point=ORIGIN
        )
        elbow.shift(line.get_center())
        return elbow

    def get_ellipse(self):
        center = self.circle.get_center()
        e_point = self.get_eccentricity_point()
        radius = self.circle.get_width() / 2

        # Ellipse parameters
        a = radius / 2
        c = get_norm(e_point - center) / 2
        b = np.sqrt(a**2 - c**2)

        result = Circle(radius=b, color=self.ellipse_color)
        result.stretch(a / b, 0)
        result.move_to(Line(center, e_point))
        return result


class FeynmanAndOrbitingPlannetOnEllipseDiagram(ShowEmergingEllipse):
    def construct(self):
        circle = self.get_circle()
        lines = self.get_lines()
        ghost_lines = self.get_ghost_lines(lines)
        for line in lines:
            MoveToTarget(line).update(1)
        ellipse = self.get_ellipse()
        e_dot = Dot(self.get_eccentricity_point())
        e_dot.set_color(YELLOW)

        comet = ImageMobject("earth")
        comet.set_width(0.3)

        feynman = ImageMobject("Feynman")
        feynman.set_height(6)
        feynman.next_to(ORIGIN, LEFT)
        feynman.to_edge(UP)
        feynman_name = OldTexText("Richard Feynman")
        feynman_name.next_to(feynman, DOWN)
        feynman.save_state()
        feynman.shift(2 * DOWN)
        feynman_rect = BackgroundRectangle(
            feynman, fill_opacity=1
        )

        group = VGroup(circle, ghost_lines, lines, e_dot, ellipse)

        self.add(group)
        # CHANGE: same: comet is a member of the Orbiting group, so use the group as foreground
        orbit = Orbiting(comet, e_dot, ellipse)
        self.add(orbit)
        self.add_foreground_mobjects(orbit)
        self.wait()
        self.play(
            feynman.restore,
            MaintainPositionRelativeTo(feynman_rect, feynman),
            VFadeOut(feynman_rect),
            group.to_edge, RIGHT,
        )
        self.play(Write(feynman_name))
        self.wait()
        self.wait(10)
