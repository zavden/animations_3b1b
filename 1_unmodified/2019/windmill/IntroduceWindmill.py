# ==============================================================================
# Scene:      IntroduceWindmill
# Source:     videos/_2019/windmill.py (lines 1443-1650)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl IntroduceWindmill.py IntroduceWindmill -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class WindmillScene(Scene):
    CONFIG = {
        "dot_config": {
            "fill_color": GREY_B,
            "radius": 0.05,
            "background_stroke_width": 2,
            "background_stroke_color": BLACK,
        },
        "windmill_style": {
            "stroke_color": RED,
            "stroke_width": 2,
            "background_stroke_width": 3,
            "background_stroke_color": BLACK,
        },
        "windmill_length": 2 * FRAME_WIDTH,
        "windmill_rotation_speed": 0.25,
        # "windmill_rotation_speed": 0.5,
        # "hit_sound": "pen_click.wav",
        "hit_sound": "pen_click.wav",
        "leave_shadows": False,
    }

    def get_random_point_set(self, n_points=11, width=6, height=6):
        return np.array([
            [
                -width / 2 + np.random.random() * width,
                -height / 2 + np.random.random() * height,
                0
            ]
            for n in range(n_points)
        ])

    def get_dots(self, points):
        return VGroup(*[
            Dot(point, **self.dot_config)
            for point in points
        ])

    def get_windmill(self, points, pivot=None, angle=TAU / 4):
        line = Line(LEFT, RIGHT)
        line.set_length(self.windmill_length)
        line.set_angle(angle)
        line.set_style(**self.windmill_style)

        line.point_set = points

        if pivot is not None:
            line.pivot = pivot
        else:
            line.pivot = points[0]

        line.rot_speed = self.windmill_rotation_speed

        line.add_updater(lambda l: l.move_to(l.pivot))
        return line

    def get_pivot_dot(self, windmill, color=YELLOW):
        pivot_dot = Dot(color=YELLOW)
        pivot_dot.add_updater(lambda d: d.move_to(windmill.pivot))
        return pivot_dot

    def start_leaving_shadows(self):
        self.leave_shadows = True
        self.add(self.get_windmill_shadows())

    def get_windmill_shadows(self):
        if not hasattr(self, "windmill_shadows"):
            self.windmill_shadows = VGroup()
        return self.windmill_shadows

    def next_pivot_and_angle(self, windmill):
        curr_angle = windmill.get_angle()
        pivot = windmill.pivot
        non_pivots = list(filter(
            lambda p: not np.all(p == pivot),
            windmill.point_set
        ))

        angles = np.array([
            -(angle_of_vector(point - pivot) - curr_angle) % PI
            for point in non_pivots
        ])

        # Edge case for 2 points
        tiny_indices = angles < 1e-6
        if np.all(tiny_indices):
            return non_pivots[0], PI

        angles[tiny_indices] = np.inf
        index = np.argmin(angles)
        return non_pivots[index], angles[index]

    def rotate_to_next_pivot(self, windmill, max_time=None, added_anims=None):
        """
        Returns animations to play following the contact, and total run time
        """
        new_pivot, angle = self.next_pivot_and_angle(windmill)
        change_pivot_at_end = True

        if added_anims is None:
            added_anims = []

        run_time = angle / windmill.rot_speed
        if max_time is not None and run_time > max_time:
            ratio = max_time / run_time
            rate_func = (lambda t: ratio * t)
            run_time = max_time
            change_pivot_at_end = False
        else:
            rate_func = linear

        for anim in added_anims:
            if anim.run_time > run_time:
                anim.run_time = run_time

        self.play(
            Rotate(
                windmill,
                -angle,
                rate_func=rate_func,
                run_time=run_time,
            ),
            *added_anims,
        )

        if change_pivot_at_end:
            self.handle_pivot_change(windmill, new_pivot)

        # Return animations to play
        return [self.get_hit_flash(new_pivot)], run_time

    def handle_pivot_change(self, windmill, new_pivot):
        windmill.pivot = new_pivot
        self.add_sound(self.hit_sound)
        if self.leave_shadows:
            new_shadow = windmill.copy()
            new_shadow.fade(0.5)
            new_shadow.set_stroke(width=1)
            new_shadow.clear_updaters()
            shadows = self.get_windmill_shadows()
            shadows.add(new_shadow)

    def let_windmill_run(self, windmill, time):
        # start_time = self.get_time()
        # end_time = start_time + time
        # curr_time = start_time
        anims_from_last_hit = []
        while time > 0:
            anims_from_last_hit, last_run_time = self.rotate_to_next_pivot(
                windmill,
                max_time=time,
                added_anims=anims_from_last_hit,
            )
            time -= last_run_time
            # curr_time = self.get_time()

    def add_dot_color_updater(self, dots, windmill, **kwargs):
        for dot in dots:
            dot.add_updater(lambda d: self.update_dot_color(
                d, windmill, **kwargs
            ))

    def update_dot_color(self, dot, windmill, color1=BLUE, color2=GREY_BROWN):
        perp = rotate_vector(windmill.get_vector(), TAU / 4)
        dot_product = np.dot(perp, dot.get_center() - windmill.pivot)
        if dot_product > 0:
            dot.set_color(color1)
        # elif dot_product < 0:
        else:
            dot.set_color(color2)
        # else:
        #     dot.set_color(WHITE)

        dot.set_stroke(
            # interpolate_color(dot.get_fill_color(), WHITE, 0.5),
            WHITE,
            width=2,
            background=True
        )

    def get_hit_flash(self, point):
        flash = Flash(
            point,
            line_length=0.1,
            flash_radius=0.2,
            run_time=0.5,
            remover=True,
        )
        flash_mob = flash.mobject
        for submob in flash_mob:
            submob.reverse_points()
        return Uncreate(
            flash.mobject,
            run_time=0.25,
            lag_ratio=0,
        )

    def get_pivot_counters(self, windmill, counter_height=0.25, buff=0.2, color=WHITE):
        points = windmill.point_set
        counters = VGroup()
        for point in points:
            counter = Integer(0)
            counter.set_color(color)
            counter.set_height(counter_height)
            counter.next_to(point, UP, buff=buff)
            counter.point = point
            counter.windmill = windmill
            counter.is_pivot = False
            counter.add_updater(self.update_counter)
            counters.add(counter)
        return counters

    def update_counter(self, counter):
        dist = get_norm(counter.point - counter.windmill.pivot)
        counter.will_be_pivot = (dist < 1e-6)
        if (not counter.is_pivot) and counter.will_be_pivot:
            counter.increment_value()
        counter.is_pivot = counter.will_be_pivot

    def get_orientation_arrows(self, windmill, n_tips=20):
        tips = VGroup(*[
            ArrowTip(start_angle=0)
            for x in range(n_tips)
        ])
        tips.stretch(0.75, 1)
        tips.scale(0.5)

        tips.rotate(windmill.get_angle())
        tips.match_color(windmill)
        tips.set_stroke(BLACK, 1, background=True)
        for tip, a in zip(tips, np.linspace(0, 1, n_tips)):
            tip.shift(
                windmill.point_from_proportion(a) - tip.get_points()[0]
            )
        return tips

    def get_left_right_colorings(self, windmill, opacity=0.3):
        rects = VGroup(VMobject(), VMobject())
        rects.const_opacity = opacity

        def update_regions(rects):
            p0, p1 = windmill.get_start_and_end()
            v = p1 - p0
            vl = rotate_vector(v, 90 * DEGREES)
            vr = rotate_vector(v, -90 * DEGREES)
            p2 = p1 + vl
            p3 = p0 + vl
            p4 = p1 + vr
            p5 = p0 + vr
            rects[0].set_points_as_corners([p0, p1, p2, p3])
            rects[1].set_points_as_corners([p0, p1, p4, p5])
            rects.set_stroke(width=0)
            rects[0].set_fill(BLUE, rects.const_opacity)
            rects[1].set_fill(GREY_BROWN, rects.const_opacity)
            return rects

        rects.add_updater(update_regions)
        return rects


class IntroduceWindmill(WindmillScene):
    CONFIG = {
        "final_run_time": 60,
        "windmill_rotation_speed": 0.5,
    }

    def construct(self):
        self.add_points()
        self.exclude_colinear()
        self.add_line()
        self.switch_pivots()
        self.continue_and_count()

    def add_points(self):
        points = self.get_random_point_set(8)
        points[-1] = midpoint(points[0], points[1])
        dots = self.get_dots(points)
        dots.set_color(YELLOW)
        dots.set_height(3)
        braces = VGroup(
            Brace(dots, LEFT),
            Brace(dots, RIGHT),
        )

        group = VGroup(dots, braces)
        group.set_height(4)
        group.center().to_edge(DOWN)

        S, eq = S_eq = OldTex("\\mathcal{S}", "=")
        S_eq.scale(2)
        S_eq.next_to(braces, LEFT)

        self.play(
            FadeIn(S_eq),
            FadeIn(braces[0], RIGHT),
            FadeIn(braces[1], LEFT),
        )
        self.play(
            LaggedStartMap(FadeInFromLarge, dots)
        )
        self.wait()
        self.play(
            S.next_to, dots, LEFT,
            {"buff": 2, "aligned_edge": UP},
            FadeOut(braces),
            FadeOut(eq),
        )

        self.S_label = S
        self.dots = dots

    def exclude_colinear(self):
        dots = self.dots

        line = Line(dots[0].get_center(), dots[1].get_center())
        line.scale(1.5)
        line.set_stroke(WHITE)

        words = OldTexText("Not allowed!")
        words.scale(2)
        words.set_color(RED)
        words.next_to(line.get_center(), RIGHT)

        self.add(line, dots)
        self.play(
            ShowCreation(line),
            FadeIn(words, LEFT),
            dots[-1].set_color, RED,
        )
        self.wait()
        self.play(
            FadeOut(line),
            FadeOut(words),
        )
        self.play(
            FadeOut(
                dots[-1], 3 * RIGHT,
                path_arc=-PI / 4,
                rate_func=running_start,
            )
        )
        dots.remove(dots[-1])
        self.wait()

    def add_line(self):
        dots = self.dots
        points = np.array(list(map(Mobject.get_center, dots)))
        p0 = points[0]

        windmill = self.get_windmill(points, p0, angle=60 * DEGREES)
        pivot_dot = self.get_pivot_dot(windmill)

        l_label = OldTex("\\ell")
        l_label.scale(1.5)
        p_label = OldTex("P")

        l_label.next_to(
            p0 + 2 * normalize(windmill.get_vector()),
            RIGHT,
        )
        l_label.match_color(windmill)
        p_label.next_to(p0, RIGHT)
        p_label.match_color(pivot_dot)

        arcs = VGroup(*[
            Arc(angle=-45 * DEGREES, radius=1.5)
            for x in range(2)
        ])
        arcs[1].rotate(PI, about_point=ORIGIN)
        for arc in arcs:
            arc.add_tip(tip_length=0.2)
        arcs.rotate(windmill.get_angle())
        arcs.shift(p0)

        self.add(windmill, dots)
        self.play(
            GrowFromCenter(windmill),
            FadeIn(l_label, DL),
        )
        self.wait()
        self.play(
            TransformFromCopy(pivot_dot, p_label),
            GrowFromCenter(pivot_dot),
            dots.set_color, WHITE,
        )
        self.wait()
        self.play(*map(ShowCreation, arcs))
        self.wait()

        # Rotate to next pivot
        next_pivot, angle = self.next_pivot_and_angle(windmill)
        self.play(
            *[
                Rotate(
                    mob, -0.99 * angle,
                    about_point=p0,
                    rate_func=linear,
                )
                for mob in [windmill, arcs, l_label]
            ],
            VFadeOut(l_label),
        )
        self.add_sound(self.hit_sound)
        self.play(
            self.get_hit_flash(next_pivot)
        )
        self.wait()

        self.pivot2 = next_pivot
        self.pivot_dot = pivot_dot
        self.windmill = windmill
        self.p_label = p_label
        self.arcs = arcs

    def switch_pivots(self):
        windmill = self.windmill
        pivot2 = self.pivot2
        p_label = self.p_label
        arcs = self.arcs

        q_label = OldTex("Q")
        q_label.set_color(YELLOW)
        q_label.next_to(pivot2, DR, buff=SMALL_BUFF)

        self.rotate_to_next_pivot(windmill)
        self.play(
            FadeIn(q_label, LEFT),
            FadeOut(p_label),
            FadeOut(arcs),
        )
        self.wait()
        flashes, run_time = self.rotate_to_next_pivot(windmill)
        self.remove(q_label)
        self.add_sound(self.hit_sound)
        self.play(*flashes)
        self.wait()
        self.let_windmill_run(windmill, 10)

    def continue_and_count(self):
        windmill = self.windmill
        pivot_dot = self.pivot_dot

        p_label = OldTex("P")
        p_label.match_color(pivot_dot)
        p_label.next_to(pivot_dot, DR, buff=0)

        l_label = OldTex("\\ell")
        l_label.scale(1.5)
        l_label.match_color(windmill)
        l_label.next_to(
            windmill.get_center() + -3 * normalize(windmill.get_vector()),
            DR,
            buff=SMALL_BUFF,
        )

        self.play(FadeIn(p_label, UL))
        self.play(FadeIn(l_label, LEFT))
        self.wait()

        self.add(
            windmill.copy().fade(0.75),
            pivot_dot.copy().fade(0.75),
        )
        pivot_counters = self.get_pivot_counters(windmill)
        self.add(pivot_counters)
        windmill.rot_speed *= 2

        self.let_windmill_run(windmill, self.final_run_time)
