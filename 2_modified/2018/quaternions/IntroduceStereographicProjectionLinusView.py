# ==============================================================================
# Scene:      IntroduceStereographicProjectionLinusView
# Source:     videos/_2018/quaternions.py (lines 2605-2815)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl IntroduceStereographicProjectionLinusView.py IntroduceStereographicProjectionLinusView -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - GL calls mob.copy(deep=...) (generate_target, play(mob.method)); accept the keyword in the Linus override
# ==============================================================================

from manim_imports_ext import *

def stereo_project_point(point, axis=0, r=1, max_norm=10000):
    point = fdiv(point * r, point[axis] + r)
    point[axis] = 0
    norm = get_norm(point)
    if norm > max_norm:
        point *= max_norm / norm
    return point


def stereo_project(mobject, axis=0, r=1, outer_r=10, **kwargs):
    epsilon = 1
    for submob in mobject.family_members_with_points():
        points = submob.get_points()
        n = len(points)
        for i in range(n):
            if points[i, axis] == -r:
                js = it.chain(
                    range(i + 1, n),
                    range(i - 1, -1, -1)
                )
                for j in js:
                    if points[j, axis] == -r:
                        continue
                    else:
                        vect = points[j] - points[i]
                        points[i] += epsilon * vect
                        break
        submob.apply_function(
            lambda p: stereo_project_point(p, axis, r, **kwargs)
        )

        # If all points are outside a certain range, this
        # shouldn't be displayed
        norms = np.apply_along_axis(get_norm, 1, submob.get_points())
        if np.all(norms > outer_r):
            # TODO, instead set opacity?
            # submob.get_points()[:, :] = 0
            submob.set_fill(opacity=0)
            submob.set_stroke(opacity=0)

    return mobject


class Linus(VGroup):
    CONFIG = {
        "body_config": {
            "stroke_width": 15,
            "stroke_color": GREY_B,
            "sheen": 0.4,
        },
        "height": 2,
    }

    def __init__(self, **kwargs):
        VGroup.__init__(self, **kwargs)
        self.body = self.get_body_line()
        self.eyes = Eyes(self.body)

        self.add(self.body, self.eyes)
        self.set_height(self.height)
        self.center()

    def change_mode(self, mode, thing_to_look_at=None):
        self.eyes.change_mode(mode, thing_to_look_at)
        if mode == "sad":
            self.become_squiggle()
        elif mode == "confused":
            self.become_squiggle(factor=-0.1)
        elif mode == "pleading":
            self.become_squiggle(factor=0.3)
        else:
            self.become_line()
        return self

    def change(self, *args, **kwargs):
        self.change_mode(*args, **kwargs)
        return self

    def look_at(self, thing_to_look_at=None):
        self.eyes.look_at(thing_to_look_at)
        return self

    def blink(self):
        self.eyes.blink()
        return self

    def get_squiggle(self, factor=0.2):
        sine_curve = FunctionGraph(
            lambda x: factor * np.sin(x),
            x_min=0, x_max=TAU,
        )
        sine_curve.rotate(TAU / 4)
        sine_curve.match_style(self.body)
        sine_curve.match_height(self.body)
        sine_curve.move_to(self.body, UP)
        return sine_curve

    def get_body_line(self, **kwargs):
        config = dict(self.body_config)
        config.update(kwargs)
        line = Line(ORIGIN, 1.5 * UP, **config)
        if hasattr(self, "body"):
            line.match_style(self.body)
            line.match_height(self.body)
            line.move_to(self.body, UP)
        return line

    def become_squiggle(self, **kwargs):
        self.body.become(self.get_squiggle(**kwargs))
        return self

    def become_line(self, **kwargs):
        self.body.become(self.get_body_line(**kwargs))
        return self

    # CHANGE: GL calls mob.copy(deep=...) (generate_target, play(mob.method)); accept the keyword in the Linus override
    def copy(self, deep=False):
        return self.deepcopy()


class PushPin(SVGMobject):
    CONFIG = {
        "file_name": "push_pin",
        "height": 0.5,
        "sheen": 0.7,
        "fill_color": GREY,
    }

    def __init__(self, **kwargs):
        SVGMobject.__init__(self, **kwargs)
        self.rotate(20 * DEGREES)

    def pin_to(self, point):
        self.move_to(point, DR)


class Hand(SVGMobject):
    CONFIG = {
        "file_name": "pinch_hand",
        "height": 0.5,
        "sheen": 0.2,
        "fill_color": ORANGE,
    }

    def __init__(self, **kwargs):
        SVGMobject.__init__(self, **kwargs)
        # self.rotate(30 * DEGREES)
        self.add(VectorizedPoint().next_to(self, UP, buff=0.17))


class CheckeredCircle(Circle):
    CONFIG = {
        "n_pieces": 16,
        "colors": [BLUE_E, BLUE_C],
        "stroke_width": 5,
    }

    def __init__(self, **kwargs):
        Circle.__init__(self, **kwargs)
        pieces = self.get_pieces(self.n_pieces)
        self.set_points(np.zeros((0, 3)))
        self.add(*pieces)
        n_colors = len(self.colors)
        for i, color in enumerate(self.colors):
            self[i::n_colors].set_color(color)


class IntroduceStereographicProjection(MovingCameraScene):
    CONFIG = {
        "n_sample_points": 16,
        "circle_config": {
            "n_pieces": 16,
            "radius": 2,
            "stroke_width": 7,
        },
        "example_angles": [
            30 * DEGREES,
            120 * DEGREES,
            240 * DEGREES,
            80 * DEGREES,
            -60 * DEGREES,
            135 * DEGREES,
        ]
    }

    def construct(self):
        self.setup_plane()
        self.draw_lines()
        self.describe_individual_points()
        self.remind_that_most_points_are_not_projected()

    def setup_plane(self):
        self.plane = self.get_plane()
        self.circle = self.get_circle()
        self.circle_shadow = self.get_circle_shadow()

        self.add(self.plane)
        self.add(self.circle_shadow)
        self.add(self.circle)

    def draw_lines(self):
        plane = self.plane
        circle = self.circle
        circle.save_state()
        circle.generate_target()
        self.project_mobject(circle.target)

        circle_points = self.get_sample_circle_points()
        dots = VGroup(*[Dot(p) for p in circle_points])
        dots.set_sheen(-0.2, DR)
        dots.set_stroke(GREY_D, 2, background=True)
        arrows = VGroup()
        for dot in dots:
            dot.scale(0.75)
            dot.generate_target()
            dot.target.move_to(
                self.project(dot.get_center())
            )
            arrow = Arrow(
                dot.get_center(),
                dot.target.get_center(),
            )
            arrows.add(arrow)
        neg_one_point = plane.number_to_point(-1)
        neg_one_dot = Dot(neg_one_point)
        neg_one_dot.set_fill(YELLOW)

        lines = self.get_lines()

        special_index = self.n_sample_points // 2 + 1
        line = lines[special_index]
        dot = dots[special_index]
        arrow = arrows[special_index]
        dot_target_outline = dot.target.copy()
        dot_target_outline.set_stroke(RED, 2)
        dot_target_outline.set_fill(opacity=0)
        dot_target_outline.scale(1.5)

        v_line = Line(UP, DOWN)
        v_line.set_height(FRAME_HEIGHT)
        v_line.set_stroke(RED, 5)

        self.play(LaggedStartMap(FadeInFromLarge, dots))
        self.play(FadeInFromLarge(neg_one_dot))
        self.add(lines, neg_one_dot, dots)
        self.play(LaggedStartMap(ShowCreation, lines))
        self.wait()
        self.play(
            lines.set_stroke, {"width": 0.5},
            line.set_stroke, {"width": 4},
        )
        self.play(ShowCreation(dot_target_outline))
        self.play(ShowCreationThenDestruction(v_line))
        self.play(MoveToTarget(dot))
        self.wait()
        self.play(
            lines.set_stroke, {"width": 1},
            FadeOut(dot_target_outline),
            MoveToTarget(circle),
            *map(MoveToTarget, dots),
            run_time=2,
        )
        self.wait()

        self.lines = lines
        self.dots = dots

    def describe_individual_points(self):
        plane = self.plane
        one_point, zero_point, i_point, neg_i_point, neg_one_point = [
            plane.number_to_point(n)
            for n in [1, 0, complex(0, 1), complex(0, -1), -1]
        ]
        i_pin = PushPin()
        i_pin.pin_to(i_point)
        neg_i_pin = PushPin()
        neg_i_pin.pin_to(neg_i_point)

        dot = Dot()
        dot.set_stroke(RED, 3)
        dot.set_fill(opacity=0)
        dot.scale(1.5)
        dot.move_to(one_point)

        arc1 = Arc(angle=TAU / 4, radius=2)
        arc2 = Arc(
            angle=85 * DEGREES, radius=2,
            start_angle=TAU / 4,
        )
        arc3 = Arc(
            angle=-85 * DEGREES, radius=2,
            start_angle=-TAU / 4,
        )
        VGroup(arc1, arc2, arc3).set_stroke(RED)

        frame = self.camera_frame
        frame_height_tracker = ValueTracker(frame.get_height())
        frame_height_growth = frame_height_tracker.add_updater(
            lambda m, dt: m.set_value(m.get_value + 0.5 * dt)
        )

        neg_one_tangent = VGroup(
            Line(ORIGIN, UP),
            Line(ORIGIN, DOWN),
        )
        neg_one_tangent.set_height(25)
        neg_one_tangent.set_stroke(YELLOW, 5)
        neg_one_tangent.move_to(neg_one_point)

        self.play(ShowCreation(dot))
        self.wait()
        self.play(dot.move_to, zero_point)
        self.wait()
        dot.move_to(i_point)
        self.play(ShowCreation(dot))
        self.play(FadeIn(i_pin, UL))
        self.wait()
        self.play(
            dot.move_to, neg_i_point,
            path_arc=-60 * DEGREES
        )
        self.play(FadeIn(neg_i_pin, UL))
        self.wait()
        self.play(
            dot.move_to, one_point,
            path_arc=-60 * DEGREES
        )
        frame.add_updater(
            lambda m: m.set_height(frame_height_tracker.get_value())
        )

        triplets = [
            (arc1, i_point, TAU / 4),
            (arc2, neg_one_point, TAU / 4),
            (arc3, neg_one_point, -TAU / 4),
        ]
        for arc, point, path_arc in triplets:
            self.play(
                ShowCreation(arc),
                dot.move_to, point, path_arc=path_arc,
                run_time=2
            )
            self.wait()
            self.play(
                ApplyFunction(self.project_mobject, arc, run_time=2)
            )
            self.wait()
            self.play(FadeOut(arc))
            self.wait()
            if arc is arc1:
                self.add(frame, frame_height_growth)
            elif arc is arc2:
                self.play(dot.move_to, neg_i_point)
        self.wait(2)
        self.play(*map(ShowCreation, neg_one_tangent))
        self.wait()
        self.play(FadeOut(neg_one_tangent))
        self.wait(2)
        frame.clear_updaters()
        self.play(
            frame.set_height, FRAME_HEIGHT,
            self.lines.set_stroke, {"width": 0.5},
            FadeOut(self.dots),
            FadeOut(dot),
            run_time=2,
        )

    def remind_that_most_points_are_not_projected(self):
        plane = self.plane
        circle = self.circle

        sample_values = [0, complex(1, 1), complex(-2, -1)]
        sample_points = [
            plane.number_to_point(value)
            for value in sample_values
        ]
        sample_dots = VGroup(*[Dot(p) for p in sample_points])
        sample_dots.set_fill(GREEN)

        self.play(
            FadeOut(self.lines),
            Restore(circle),
        )

        for value, dot in zip(sample_values, sample_dots):
            cross = Cross(dot)
            cross.scale(2)
            label = Integer(value)
            if value is sample_values[1]:
                label.next_to(dot, UL, SMALL_BUFF)
            else:
                label.next_to(dot, UR, SMALL_BUFF)
            self.play(
                FadeInFromLarge(dot, 3),
                FadeInFromDown(label)
            )
            self.play(ShowCreation(cross))
            self.play(*map(FadeOut, [dot, cross, label]))
        self.wait()
        self.play(
            FadeIn(self.lines),
            MoveToTarget(circle, run_time=2),
        )
        self.wait()

    # Helpers
    def get_plane(self):
        plane = ComplexPlane(
            unit_size=2,
            color=GREY,
            secondary_color=GREY_D,
            x_radius=FRAME_WIDTH,
            y_radius=FRAME_HEIGHT,
            stroke_width=2,
        )
        plane.add_coordinates()
        return plane

    def get_circle(self):
        circle = CheckeredCircle(
            **self.circle_config
        )
        circle.set_stroke(width=7)
        return circle

    def get_circle_shadow(self):
        circle_shadow = CheckeredCircle(
            **self.circle_config
        )
        circle_shadow.set_stroke(opacity=0.65)
        return circle_shadow

    def get_sample_circle_points(self):
        plane = self.plane
        n = self.n_sample_points
        rotater = 1
        if hasattr(self, "circle_shadow"):
            point = self.circle_shadow[0].get_points()[0]
            rotater = complex(*point[:2])
            rotater /= abs(rotater)
        numbers = [
            rotater * np.exp(complex(0, TAU * x / n))
            for x in range(-(n // 2) + 1, n // 2)
        ]
        return [
            plane.number_to_point(number)
            for number in numbers
        ]

    def get_lines(self):
        plane = self.plane
        neg_one_point = plane.number_to_point(-1)
        circle_points = self.get_sample_circle_points()

        lines = VGroup(*[
            Line(neg_one_point, point)
            for point in circle_points
        ])
        for line in lines:
            length = line.get_length()
            line.scale(20 / length, about_point=neg_one_point)
            line.set_stroke(YELLOW, np.clip(length, 0, 1))
        return lines

    def project(self, point):
        return stereo_project_point(point, axis=0, r=2)

    def project_mobject(self, mobject):
        return stereo_project(mobject, axis=0, r=2, outer_r=6)


class IntroduceStereographicProjectionLinusView(IntroduceStereographicProjection):
    def construct(self):
        self.describe_individual_points()
        self.point_at_infinity()
        self.show_90_degree_rotation()
        self.talk_through_90_degree_rotation()
        self.show_four_rotations()
        self.show_example_angles()

    def describe_individual_points(self):
        plane = self.plane = self.get_plane()
        circle = self.circle = self.get_circle()
        linus = self.linus = self.get_linus()

        angles = np.arange(-135, 180, 45) * DEGREES
        sample_numbers = [
            np.exp(complex(0, angle))
            for angle in angles
        ]
        sample_points = [
            plane.number_to_point(number)
            for number in sample_numbers
        ]
        projected_sample_points = [
            self.project(point)
            for point in sample_points
        ]
        dots = VGroup(*[Dot() for x in range(8)])
        dots.set_fill(WHITE)
        dots.set_stroke(BLACK, 1)

        def generate_dot_updater(circle_piece):
            return lambda d: d.move_to(circle_piece.get_points()[0])

        for dot, piece in zip(dots, circle[::(len(circle) // 8)]):
            dot.add_updater(generate_dot_updater(piece))

        stot = "(\\sqrt{2} / 2)"
        labels_tex = [
            "-{}-{}i".format(stot, stot),
            "-i",
            "{}-{}i".format(stot, stot),
            "1",
            "{}+{}i".format(stot, stot),
            "i",
            "-{}+{}i".format(stot, stot),
        ]
        labels = VGroup(*[Tex(tex) for tex in labels_tex])
        vects = it.cycle([RIGHT, RIGHT])
        arrows = VGroup()
        for label, point, vect in zip(labels, projected_sample_points, vects):
            arrow = Arrow(vect, ORIGIN)
            arrow.next_to(point, vect, 2 * SMALL_BUFF)
            arrows.add(arrow)
            label.set_stroke(width=0, background=True)
            if stot in label.get_tex():
                label.set_height(0.5)
            else:
                label.set_height(0.5)
                label.set_stroke(WHITE, 2, background=True)
            label.next_to(arrow, vect, SMALL_BUFF)

        frame = self.camera_frame
        frame.set_height(12)

        self.add(linus)
        self.add(circle, *dots)
        self.play(
            ApplyFunction(self.project_mobject, circle),
            run_time=2
        )
        self.play(linus.change, "confused")
        self.wait()
        for i in [1, 0]:
            self.play(
                LaggedStartMap(GrowArrow, arrows[i::2]),
                LaggedStartMap(Write, labels[i::2])
            )
            self.play(Blink(linus))

        self.dots = dots

    def point_at_infinity(self):
        circle = self.circle
        linus = self.linus

        label = OldTexText(
            "$-1$ is \\\\ at $\\pm \\infty$"
        )
        label.scale(1.5)
        label.next_to(circle, LEFT, buff=1.25)
        arrows = VGroup(*[
            Vector(3 * v + 0.0 * RIGHT).next_to(label, v, buff=MED_LARGE_BUFF)
            for v in [UP, DOWN]
        ])
        arrows.set_color(YELLOW)

        self.play(
            Write(label),
            linus.change, "awe", label,
            *map(GrowArrow, arrows)
        )

        self.neg_one_label = VGroup(label, arrows)

    def show_90_degree_rotation(self):
        angle_tracker = ValueTracker(0)
        circle = self.circle
        linus = self.linus
        hand = Hand()
        hand.flip()
        one_dot = self.dots[0]
        hand.add_updater(
            lambda h: h.move_to(one_dot.get_center(), RIGHT)
        )

        def update_circle(circle):
            angle = angle_tracker.get_value()
            new_circle = self.get_circle()
            new_circle.rotate(angle)
            self.project_mobject(new_circle)
            circle.become(new_circle)

        circle.add_updater(update_circle)

        self.play(
            FadeIn(hand),
            one_dot.set_fill, RED,
        )
        for angle in 90 * DEGREES, 0:
            self.play(
                ApplyMethod(
                    angle_tracker.set_value, angle,
                    run_time=3,
                ),
                linus.change, "confused", hand
            )
            self.wait()
            self.play(Blink(linus))

        self.hand = hand
        self.angle_tracker = angle_tracker

    def talk_through_90_degree_rotation(self):
        linus = self.linus
        dots = self.dots
        one_dot = dots[0]
        i_dot = dots[2]
        neg_i_dot = dots[-2]

        kwargs1 = {
            "path_arc": -90 * DEGREES,
            "buff": SMALL_BUFF,
        }
        kwargs2 = dict(kwargs1)
        kwargs2["path_arc"] = -40 * DEGREES
        arrows = VGroup(
            Arrow(one_dot, i_dot, **kwargs1),
            Arrow(i_dot, 6 * UP + LEFT, **kwargs2),
            Arrow(6 * DOWN + LEFT, neg_i_dot, **kwargs2),
            Arrow(neg_i_dot, one_dot, **kwargs1)
        )
        arrows.set_stroke(WHITE, 3)
        one_to_i, i_to_neg_1, neg_one_to_neg_i, neg_i_to_one = arrows

        for arrow in arrows:
            self.play(
                ShowCreation(arrow),
                linus.look_at, arrow
            )
            self.wait(2)

        self.arrows = arrows

    def show_four_rotations(self):
        angle_tracker = self.angle_tracker
        linus = self.linus
        hand = self.hand
        linus.add_updater(lambda l: l.look_at(hand))
        linus.add_updater(lambda l: l.eyes.next_to(l.body, UP, 0))

        for angle in np.arange(TAU / 4, 5 * TAU / 4, TAU / 4):
            self.play(
                ApplyMethod(
                    angle_tracker.set_value, angle,
                    run_time=3,
                ),
            )
            self.wait()
        self.play(FadeOut(self.arrows))

    def show_example_angles(self):
        angle_tracker = self.angle_tracker
        angle_tracker.set_value(0)

        for angle in self.example_angles:
            self.play(
                ApplyMethod(
                    angle_tracker.set_value, angle,
                    run_time=4,
                ),
            )
            self.wait()

    #
    def get_linus(self):
        linus = Linus()
        linus.move_to(3 * RIGHT)
        linus.to_edge(DOWN)
        linus.look_at(ORIGIN)
        return linus
