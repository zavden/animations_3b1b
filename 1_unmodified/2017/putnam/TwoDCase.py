# ==============================================================================
# Scene:      TwoDCase
# Source:     videos/_2017/putnam.py (lines 248-779)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl TwoDCase.py TwoDCase -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class TwoDCase(Scene):
    CONFIG = {
        "center" : ORIGIN,
        "random_seed" : 4,
        "radius" : 2.5,
        "center_color" : BLUE,
        "point_color" : YELLOW,
        "positive_triangle_color" : BLUE,
        "negative_triangle_color" : RED,
        "triangle_fill_opacity" : 0.25,
        "n_initial_random_choices" : 9,
        "n_p3_random_moves" : 4,
    }
    def construct(self):
        self.add_title()
        self.add_circle()
        self.choose_three_random_points()
        self.simplify_further()
        self.fix_two_points_in_place()
        self.note_special_region()
        self.draw_lines_through_center()
        self.ask_about_probability_p3_lands_in_this_arc()
        self.various_arc_sizes_for_p1_p2_placements()
        self.ask_about_average_arc_size()
        self.fix_p1_in_place()
        self.overall_probability()

    def add_title(self):
        title = OldTexText("2D Case")
        title.to_corner(UP+LEFT)
        self.add(title)
        self.set_variables_as_attrs(title)

    def add_circle(self):
        circle = Circle(radius = self.radius, color = WHITE)
        center_dot = Dot(color = self.center_color).center()
        radius = DashedLine(ORIGIN, circle.radius*RIGHT)
        VGroup(circle, center_dot, radius).shift(self.center)

        self.add(center_dot)
        self.play(ShowCreation(radius))
        self.play(
            ShowCreation(circle),
            Rotating(radius, angle = 2*np.pi, about_point = self.center),
            rate_func = smooth,
            run_time = 2,
        )
        self.play(ShowCreation(
            radius,
            rate_func = lambda t : smooth(1-t),
            remover = True
        ))
        self.wait()

        self.set_variables_as_attrs(circle, center_dot)

    def choose_three_random_points(self):
        point_mobs = self.get_point_mobs()
        point_labels = self.get_point_mob_labels()
        triangle = self.get_triangle()
        self.point_labels_update = self.get_labels_update(point_mobs, point_labels)
        self.triangle_update = self.get_triangle_update(point_mobs, triangle)
        self.update_animations = [
            self.triangle_update,
            self.point_labels_update,
        ]
        for anim in self.update_animations:
            anim.update(0)

        question = OldTexText(
            "Probability that \\\\ this triangle \\\\",
            "contains the center", "?",
            arg_separator = "",
        )
        question.set_color_by_tex("center", self.center_color)
        question.scale(0.8)
        question.to_corner(UP+RIGHT)
        self.question = question

        self.play(LaggedStartMap(DrawBorderThenFill, point_mobs))
        self.play(FadeIn(triangle))
        self.wait()
        self.play(LaggedStartMap(Write, point_labels))
        self.wait()
        self.play(Write(question))
        for x in range(self.n_initial_random_choices):
            self.change_point_mobs_randomly()
            self.wait()
        angles = self.get_point_mob_angles()
        target_angles = [5*np.pi/8, 7*np.pi/8, 0]
        self.change_point_mobs([ta - a for a, ta in zip(angles, target_angles)])
        self.wait()

    def simplify_further(self):
        morty = Mortimer().flip()
        morty.scale(0.75)
        morty.to_edge(DOWN)
        morty.shift(3.5*LEFT)

        bubble = SpeechBubble(
            direction = RIGHT,
            height = 3, width = 3
        )
        bubble.pin_to(morty)
        bubble.to_edge(LEFT, SMALL_BUFF)
        bubble.write("Simplify \\\\ more!")

        self.play(FadeIn(morty))
        self.play(
            morty.change, "hooray",
            ShowCreation(bubble),
            Write(bubble.content)
        )
        self.play(Blink(morty))
        self.wait()
        self.play(
            morty.change, "happy",
            morty.fade, 1,
            *list(map(FadeOut, [bubble, bubble.content]))
        )
        self.remove(morty)

    def fix_two_points_in_place(self):
        push_pins = VGroup()
        for point_mob in self.point_mobs[:-1]:
            push_pin = SVGMobject(file_name = "push_pin")
            push_pin.set_height(0.5)
            push_pin.move_to(point_mob.get_center(), DOWN)
            line = Line(ORIGIN, UP)
            line.set_stroke(WHITE, 2)
            line.set_height(0.1)
            line.move_to(push_pin, UP)
            line.shift(0.3*SMALL_BUFF*(2*DOWN+LEFT))
            push_pin.add(line)
            push_pin.set_fill(GREY_B)
            push_pin.save_state()
            push_pin.shift(UP)
            push_pin.fade(1)
            push_pins.add(push_pin)

        self.play(LaggedStartMap(
            ApplyMethod, push_pins,
            lambda mob : (mob.restore,)
        ))
        self.add_foreground_mobjects(push_pins)
        d_thetas = 2*np.pi*np.random.random(self.n_p3_random_moves)
        for d_theta in d_thetas:
            self.change_point_mobs([0, 0, d_theta])
            self.wait()

        self.set_variables_as_attrs(push_pins)

    def note_special_region(self):
        point_mobs = self.point_mobs
        angles = self.get_point_mob_angles()

        all_arcs = self.get_all_arcs()
        arc = all_arcs[-1]
        arc_lines = VGroup()
        for angle in angles[:2]:
            line = Line(LEFT, RIGHT).scale(SMALL_BUFF)
            line.shift(self.radius*RIGHT)
            line.rotate(angle + np.pi)
            line.shift(self.center)
            line.set_stroke(arc.get_color())
            arc_lines.add(line)

        self.play(ShowCreation(arc_lines))
        self.change_point_mobs([0, 0, angles[0]+np.pi-angles[2]])
        self.change_point_mobs(
            [0, 0, arc.angle],
            ShowCreation(arc, run_time = 2)
        )
        self.change_point_mobs([0, 0, np.pi/4 - angles[1]])
        self.change_point_mobs([0, 0, 0.99*np.pi], run_time = 4)
        self.wait()

        self.set_variables_as_attrs(all_arcs, arc, arc_lines)

    def draw_lines_through_center(self):
        point_mobs = self.point_mobs
        angles = self.get_point_mob_angles()
        all_arcs = self.all_arcs

        lines = self.get_center_lines()

        self.add_foreground_mobjects(self.center_dot)
        for line in lines:
            self.play(ShowCreation(line))
        self.play(FadeIn(all_arcs), Animation(point_mobs))
        self.remove(self.circle)
        self.wait()
        self.play(
            all_arcs.space_out_submobjects, 1.5,
            Animation(point_mobs),
            rate_func = there_and_back,
            run_time = 1.5,
        )
        self.wait()
        self.change_point_mobs(
            [0, 0, np.mean(angles[:2])+np.pi-angles[2]]
        )
        self.wait()
        for x in range(3):
            self.change_point_mobs([0, 0, np.pi/2])
        self.wait()

    def ask_about_probability_p3_lands_in_this_arc(self):
        arc = self.arc

        arrow = Vector(LEFT, color = BLUE)
        arrow.next_to(arc.get_center(), RIGHT, MED_LARGE_BUFF)
        question = OldTexText("Probability of landing \\\\ in this arc?")
        question.scale(0.8)
        question.next_to(arrow, RIGHT)
        question.shift_onto_screen()
        question.shift(SMALL_BUFF*UP)

        answer = OldTex(
            "{\\text{Length of arc}", "\\over",
            "\\text{Circumference}}"
        )
        answer.set_color_by_tex("arc", BLUE)
        answer.scale(0.8)
        answer.next_to(arrow, RIGHT)
        equals = OldTex("=")
        equals.rotate(np.pi/2)
        equals.next_to(answer, UP, buff = 0.35)

        self.play(FadeIn(question), GrowArrow(arrow))
        self.have_p3_jump_around_randomly(15)
        self.play(
            question.next_to, answer, UP, LARGE_BUFF,
            Write(equals),
            FadeIn(answer)
        )
        self.have_p3_jump_around_randomly(4)
        angles = self.get_point_mob_angles()
        self.change_point_mobs(
            [0, 0, 1.35*np.pi - angles[2]],
            run_time = 0,
        )
        self.wait()

        question.add(equals)
        self.arc_prob_question = question
        self.arc_prob = answer
        self.arc_size_arrow = arrow

    def various_arc_sizes_for_p1_p2_placements(self):
        arc = self.arc

        self.triangle.save_state()
        self.play(*list(map(FadeOut, [
            self.push_pins, self.triangle, self.arc_lines
        ])))
        self.update_animations.remove(self.triangle_update)
        self.update_animations += [
            self.get_center_lines_update(self.point_mobs, self.center_lines),
            self.get_arcs_update(self.all_arcs)
        ]

        #90 degree angle
        self.change_point_mobs_to_angles([np.pi/2, np.pi], run_time = 1)
        elbow = VGroup(
            Line(DOWN, DOWN+RIGHT),
            Line(DOWN+RIGHT, RIGHT),
        )
        elbow.scale(0.25)
        elbow.shift(self.center)
        ninety_degrees = OldTex("90^\\circ")
        ninety_degrees.next_to(elbow, DOWN+RIGHT, buff = 0)
        proportion = DecimalNumber(0.25)
        proportion.set_color(self.center_color)
        # proportion.next_to(arc.point_from_proportion(0.5), DOWN, MED_LARGE_BUFF)
        proportion.next_to(self.arc_size_arrow, DOWN)
        def proportion_update_func(alpha):
            angles = self.get_point_mob_angles()
            diff = abs(angles[1]-angles[0])/(2*np.pi)
            return min(diff, 1-diff)
        proportion_update = ChangingDecimal(proportion, proportion_update_func)

        self.play(ShowCreation(elbow), FadeIn(ninety_degrees))
        self.wait()
        self.play(
            ApplyMethod(
                arc.rotate, np.pi/12,
                rate_func = wiggle,
            )
        )
        self.play(LaggedStartMap(FadeIn, proportion, run_time = 1))
        self.wait()

        #Non right angles
        angle_pairs = [
            (0.26*np.pi, 1.24*np.pi), 
            (0.73*np.pi, 0.78*np.pi),
            (0.5*np.pi, np.pi),
        ]
        self.update_animations.append(proportion_update)
        for angle_pair in angle_pairs:
            self.change_point_mobs_to_angles(
                angle_pair,
                VGroup(elbow, ninety_degrees).fade, 1,
            )
            self.remove(elbow, ninety_degrees)
            self.wait()

        self.set_variables_as_attrs(proportion, proportion_update)

    def ask_about_average_arc_size(self):
        proportion = self.proportion
        brace = Brace(proportion, DOWN, buff = SMALL_BUFF)
        average = brace.get_text("Average?", buff = SMALL_BUFF)

        self.play(
            GrowFromCenter(brace),
            Write(average)
        )
        for x in range(6):
            self.change_point_mobs_to_angles(
                2*np.pi*np.random.random(2)
            )
        self.change_point_mobs_to_angles(
            [1.2*np.pi, 0.3*np.pi]
        )
        self.wait()

        self.set_variables_as_attrs(brace, average)

    def fix_p1_in_place(self):
        push_pin = self.push_pins[0]
        P1, P2, P3 = point_mobs = self.point_mobs

        self.change_point_mobs_to_angles([0.9*np.pi])
        push_pin.move_to(P1.get_center(), DOWN)
        push_pin.save_state()
        push_pin.shift(UP)
        push_pin.fade(1)
        self.play(push_pin.restore)
        for angle in [0.89999*np.pi, -0.09999*np.pi, 0.4*np.pi]:
            self.change_point_mobs_to_angles(
                [0.9*np.pi, angle],
                run_time = 4,
            )
        self.play(FadeOut(self.average[-1]))

    def overall_probability(self):
        point_mobs = self.point_mobs
        triangle = self.triangle

        one_fourth = OldTex("1/4")
        one_fourth.set_color(BLUE)
        one_fourth.next_to(self.question, DOWN)

        self.triangle_update.update(1)
        self.play(
            FadeIn(triangle),
            Animation(point_mobs)
        )
        self.update_animations.append(self.triangle_update)
        self.have_p3_jump_around_randomly(8, wait_time = 0.25)
        self.play(ReplacementTransform(
            self.proportion.copy(), VGroup(one_fourth)
        ))
        self.have_p3_jump_around_randomly(32, wait_time = 0.25)

    #####

    def get_point_mobs(self):
        points = np.array([
            self.center + rotate_vector(self.radius*RIGHT, theta)
            for theta in 2*np.pi*np.random.random(3)
        ])
        for index in 0, 1, 0:
            if self.points_contain_center(points):
                break
            points[index] -= self.center
            points[index] *= -1
            points[index] += self.center
        point_mobs = self.point_mobs = VGroup(*[
            Dot().move_to(point) for point in points            
        ])
        point_mobs.set_color(self.point_color)
        return point_mobs

    def get_point_mob_labels(self):
        point_labels = VGroup(*[
            OldTex("P_%d"%(i+1))
            for i in range(len(self.point_mobs))
        ])
        point_labels.set_color(self.point_mobs.get_color())
        self.point_labels = point_labels
        return point_labels

    def get_triangle(self):
        triangle = self.triangle = RegularPolygon(n = 3)
        triangle.set_fill(WHITE, opacity = self.triangle_fill_opacity)
        return triangle

    def get_center_lines(self):
        angles = self.get_point_mob_angles()
        lines = VGroup()
        for angle in angles[:2]:
            line = DashedLine(
                self.radius*RIGHT, self.radius*LEFT
            )
            line.rotate(angle)
            line.shift(self.center)
            line.set_color(self.point_color)
            lines.add(line)
        self.center_lines = lines
        return lines

    def get_labels_update(self, point_mobs, labels):
        def update_labels(labels):
            for point_mob, label in zip(point_mobs, labels):
                label.move_to(point_mob)
                vect = point_mob.get_center() - self.center
                vect /= get_norm(vect)
                label.shift(MED_LARGE_BUFF*vect)
            return labels
        return UpdateFromFunc(labels, update_labels)

    def get_triangle_update(self, point_mobs, triangle):
        def update_triangle(triangle):
            points = [pm.get_center() for pm in point_mobs]
            triangle.set_points_as_corners(points)
            if self.points_contain_center(points):
                triangle.set_color(self.positive_triangle_color)
            else:
                triangle.set_color(self.negative_triangle_color)
            return triangle
        return UpdateFromFunc(triangle, update_triangle)

    def get_center_lines_update(self, point_mobs, center_lines):
        def update_lines(center_lines):
            for point_mob, line in zip(point_mobs, center_lines):
                point = point_mob.get_center() - self.center
                line.rotate(
                    angle_of_vector(point) - line.get_angle()
                )
                line.move_to(self.center)
            return center_lines
        return UpdateFromFunc(center_lines, update_lines)

    def get_arcs_update(self, all_arcs):
        def update_arcs(arcs):
            new_arcs = self.get_all_arcs()
            Transform(arcs, new_arcs).update(1)
            return arcs
        return UpdateFromFunc(all_arcs, update_arcs)

    def get_all_arcs(self):
        angles = self.get_point_mob_angles()
        all_arcs = VGroup()
        for da0, da1 in it.product(*[[0, np.pi]]*2):
            arc_angle = (angles[1]+da1) - (angles[0]+da0)
            arc_angle = (arc_angle+np.pi)%(2*np.pi)-np.pi
            arc = Arc(
                start_angle = angles[0]+da0,
                angle = arc_angle,
                radius = self.radius,
                stroke_width = 5,
            )
            arc.shift(self.center)
            all_arcs.add(arc)
        all_arcs.set_color_by_gradient(RED, MAROON_B, PINK, BLUE)
        self.all_arcs = all_arcs
        return all_arcs

    def points_contain_center(self, points):
        p0, p1, p2 = points
        v1 = p1 - p0
        v2 = p2 - p0
        c = self.center - p0
        M = np.matrix([v1[:2], v2[:2]]).T
        M_inv = np.linalg.inv(M)
        coords = np.dot(M_inv, c[:2])
        return np.all(coords > 0) and (np.sum(coords.flatten()) <= 1)

    def get_point_mob_theta_change_anim(self, point_mob, d_theta):
        curr_theta = angle_of_vector(point_mob.get_center() - self.center)
        d_theta = (d_theta + np.pi)%(2*np.pi) - np.pi
        new_theta = curr_theta + d_theta

        def update_point(point_mob, alpha):
            theta = interpolate(curr_theta, new_theta, alpha)
            point_mob.move_to(self.center + self.radius*(
                np.cos(theta)*RIGHT + np.sin(theta)*UP
            ))
            return point_mob
        return UpdateFromAlphaFunc(point_mob, update_point, run_time = 2)

    def change_point_mobs(self, d_thetas, *added_anims, **kwargs):
        anims = it.chain(
            self.update_animations,
            [
                self.get_point_mob_theta_change_anim(pm, dt)
                for pm, dt in zip(self.point_mobs, d_thetas)
            ],
            added_anims
        )
        self.play(*anims, **kwargs)
        for update in self.update_animations:
            update.update(1)
 
    def change_point_mobs_randomly(self, *added_anims, **kwargs):
        d_thetas = 2*np.pi*np.random.random(len(self.point_mobs))
        self.change_point_mobs(d_thetas, *added_anims, **kwargs)

    def change_point_mobs_to_angles(self, target_angles, *added_anims, **kwargs):
        angles = self.get_point_mob_angles()
        n_added_targets = len(angles) - len(target_angles)
        target_angles = list(target_angles) + list(angles[-n_added_targets:])
        self.change_point_mobs(
            [ta-a for a, ta in zip(angles, target_angles)],
            *added_anims, **kwargs
        )

    def get_point_mob_angles(self):
        point_mobs = self.point_mobs
        points = [pm.get_center() - self.center for pm in point_mobs]
        return np.array(list(map(angle_of_vector, points)))

    def have_p3_jump_around_randomly(self, n_jumps, wait_time = 0.75, run_time = 0):
        for x in range(n_jumps):
            self.change_point_mobs(
                [0, 0, 2*np.pi*random.random()],
                run_time = run_time
            )
            self.wait(wait_time)
