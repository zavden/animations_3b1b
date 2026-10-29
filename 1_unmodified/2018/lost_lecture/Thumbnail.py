# ==============================================================================
# Scene:      Thumbnail
# Source:     videos/_2018/lost_lecture.py (lines 4226-4298)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl Thumbnail.py Thumbnail -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

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


class Thumbnail(ShowEmergingEllipse):
    CONFIG = {
        "num_lines": 50,
    }

    def construct(self):
        background = ImageMobject("Feynman_teaching")
        background.set_width(FRAME_WIDTH)
        background.scale(1.05)
        background.to_corner(UR, buff=0)
        background.shift(2 * UP)

        self.add(background)

        circle = self.get_circle()
        circle.set_stroke(width=6)
        circle.set_height(6.5)
        circle.to_corner(UL)
        circle.set_fill(BLACK, 0.9)
        lines = self.get_lines()
        lines.set_stroke(YELLOW, 5)
        lines.set_color_by_gradient(YELLOW, RED)
        ghost_lines = self.get_ghost_lines(lines)
        for line in lines:
            line.rotate(90 * DEGREES)
        ellipse = self.get_ellipse()
        ellipse.set_stroke(BLUE, 6)
        sun = ImageMobject("sun", height=0.5)
        sun.move_to(self.get_eccentricity_point())

        circle_group = VGroup(circle, ghost_lines, lines, ellipse, sun)
        self.add(circle_group)

        l1 = Line(
            circle.point_from_proportion(0.175),
            6.25 * RIGHT + 0.75 * DOWN
        )
        l2 = Line(
            circle.point_from_proportion(0.75),
            6.25 * RIGHT + 2.5 * DOWN
        )
        l2a = VMobject().pointwise_become_partial(l2, 0, 0.56)
        l2b = VMobject().pointwise_become_partial(l2, 0.715, 1)
        expand_lines = VGroup(l1, l2a, l2b)

        expand_lines.set_stroke("RED", 5)
        self.add(expand_lines)
        self.add(circle_group)

        small_group = circle_group.copy()
        small_group.scale(0.2)
        small_group.stretch(1.35, 1)
        small_group.move_to(6.2 * RIGHT + 1.6 * DOWN)
        for mob in small_group:
            if isinstance(mob, VMobject) and mob.get_stroke_width() > 1:
                mob.set_stroke(width=1)
        small_group[0].set_fill(opacity=0.25)
        self.add(small_group)

        title = OldTexText(
            "Feynman's \\\\", "Lost \\\\", "Lecture",
            alignment=""
        )
        title.scale(2.4)
        for part in title:
            part.add_to_back(
                part.copy().set_stroke(BLACK, 12).set_fill(BLACK, 1)
            )
        title.to_corner(UR)
        title[2].to_edge(RIGHT)
        title[1].shift(0.9 * RIGHT)
        title.shift(0.5 * LEFT)
        self.add(title)
