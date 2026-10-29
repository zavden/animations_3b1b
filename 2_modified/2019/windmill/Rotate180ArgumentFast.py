# ==============================================================================
# Scene:      Rotate180ArgumentFast
# Source:     videos/_2019/windmill.py (lines 3024-3027)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl Rotate180ArgumentFast.py Rotate180ArgumentFast -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Read the points of windmill.point_set: Scene has no get_points.
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


class Rotate180Argument(WindmillScene):
    CONFIG = {
        "n_points": 21,
        "random_seed": 3,
    }

    def construct(self):
        self.setup_windmill()
        self.add_total_rotation_label()
        self.rotate_180()
        self.show_parallel_lines()
        self.rotate_180()
        self.rotate_180()

    def setup_windmill(self):
        n = self.n_points
        points = self.get_random_point_set(n)
        points[:, 0] *= 1.5
        points += RIGHT
        points = sorted(points, key=lambda p: p[0])
        mid_point = points[n // 2]
        points[n // 2 - 1] += 0.2 * LEFT
        self.points = points

        self.dots = self.get_dots(points)
        self.windmill = self.get_windmill(points, mid_point)
        self.pivot_dot = self.get_pivot_dot(self.windmill)
        self.pivot_dot.set_color(WHITE)
        self.add_dot_color_updater(self.dots, self.windmill)
        self.rects = self.get_left_right_colorings(self.windmill)

        p_label = OldTex("P_0")
        p_label.next_to(mid_point, RIGHT, SMALL_BUFF)
        self.p_label = p_label

        self.add(
            self.rects,
            self.windmill,
            self.dots,
            self.pivot_dot,
            self.p_label,
        )

    def add_total_rotation_label(self):
        windmill = self.windmill

        words = OldTexText("Total rotation:")
        counter = Integer(0, unit="^\\circ")
        title = VGroup(words, counter)
        title.arrange(RIGHT)
        title.to_corner(UL)
        rot_arrow = Vector(UP)
        rot_arrow.set_color(RED)
        rot_arrow.next_to(title, DOWN)
        circle = Circle()
        circle.replace(rot_arrow, dim_to_match=1)
        circle.set_stroke(WHITE, 1)

        rot_arrow.add_updater(
            lambda m: m.set_angle(windmill.get_angle())
        )
        rot_arrow.add_updater(
            lambda m: m.move_to(circle)
        )

        def update_count(c):
            new_val = 90 - windmill.get_angle() * 360 / TAU
            while abs(new_val - c.get_value()) > 90:
                new_val += 360
            c.set_value(new_val)

        counter.add_updater(update_count)

        rect = SurroundingRectangle(
            VGroup(title, circle),
            buff=MED_LARGE_BUFF,
        )
        rect.set_fill(BLACK, 0.8)
        rect.set_stroke(WHITE, 1)
        title.shift(MED_SMALL_BUFF * LEFT)

        self.rotation_label = VGroup(
            rect, words, counter, circle, rot_arrow
        )

        self.add(self.rotation_label)

    def rotate_180(self):
        windmill = self.windmill
        self.add(self.pivot_dot)
        self.let_windmill_run(
            windmill,
            PI / windmill.rot_speed,
        )
        self.wait()

    def show_parallel_lines(self):
        # CHANGE: the points belong to the windmill, not to Scene.
        points = self.windmill.point_set
        rotation_label = self.rotation_label
        dots = self.dots
        windmill = self.windmill

        lines = VGroup()
        for point in points:
            line = Line(DOWN, UP)
            line.set_height(2 * FRAME_HEIGHT)
            line.set_stroke(RED, 1, opacity=0.5)
            line.move_to(point)
            lines.add(line)
        lines.shuffle()

        self.add(lines, dots, rotation_label)
        self.play(
            ShowCreation(lines, lag_ratio=0.5, run_time=3)
        )
        self.wait()

        self.rects.suspend_updating()
        for rect in self.rects:
            self.play(
                rect.set_opacity, 0,
                rate_func=there_and_back,
                run_time=2
            )
        self.rects.resume_updating()
        self.wait()

        pivot_tracker = VectorizedPoint(windmill.pivot)
        pivot_tracker.save_state()

        def update_pivot(w):
            w.pivot = pivot_tracker.get_center()
        windmill.add_updater(update_pivot)

        for x in range(4):
            point = random.choice(points)
            self.play(
                pivot_tracker.move_to, point
            )
            self.wait()
        self.play(Restore(pivot_tracker))
        self.play(FadeOut(lines))
        windmill.remove_updater(update_pivot)
        self.wait()


class Rotate180ArgumentFast(Rotate180Argument):
    CONFIG = {
        "windmill_rotation_speed": 0.5,
    }
