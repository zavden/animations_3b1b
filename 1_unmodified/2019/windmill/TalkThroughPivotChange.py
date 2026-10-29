# ==============================================================================
# Scene:      TalkThroughPivotChange
# Source:     videos/_2019/windmill.py (lines 2714-2863)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl TalkThroughPivotChange.py TalkThroughPivotChange -w -m --fps 15
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


class TalkThroughPivotChange(WindmillScene):
    CONFIG = {
        "windmill_rotation_speed": 0.2,
    }

    def construct(self):
        self.setup_windmill()
        self.ask_about_pivot_change()
        self.show_above_and_below()
        self.change_pivot()

    def setup_windmill(self):
        points = self.points = np.array([
            DR, UR, UL, DL, 0.5 * LEFT
        ])
        points *= 3
        self.dots = self.get_dots(points)
        self.windmill = self.get_windmill(points, points[-1])
        self.pivot_dot = self.get_pivot_dot(self.windmill)
        self.pivot_dot.set_color(WHITE)
        self.add_dot_color_updater(self.dots, self.windmill)
        self.rects = self.get_left_right_colorings(self.windmill)

        self.add(
            self.rects,
            self.windmill,
            self.dots,
            self.pivot_dot,
        )

    def ask_about_pivot_change(self):
        windmill = self.windmill

        new_pivot, angle = self.next_pivot_and_angle(windmill)
        words = OldTexText("Think about\\\\pivot change")
        words.next_to(new_pivot, UP, buff=2)
        words.to_edge(LEFT)
        arrow = Arrow(words.get_bottom(), new_pivot, buff=0.2)

        self.play(
            Rotate(
                windmill, -0.9 * angle,
                run_time=3,
                rate_func=linear
            ),
            Write(words, run_time=1),
            ShowCreation(arrow),
        )
        self.wait()

        self.question = words
        self.question_arrow = arrow

    def show_above_and_below(self):
        windmill = self.windmill
        vect = normalize(windmill.get_vector())
        angle = windmill.get_angle()
        tips = self.get_orientation_arrows(windmill)
        top_half = Line(windmill.get_center(), windmill.get_end())
        low_half = Line(windmill.get_center(), windmill.get_start())
        top_half.set_stroke(YELLOW, 3)
        low_half.set_stroke(PINK, 3)
        halves = VGroup(top_half, low_half)

        top_words = OldTexText("Above pivot")
        low_words = OldTexText("Below pivot")
        all_words = VGroup(top_words, low_words)
        for words, half in zip(all_words, halves):
            words.next_to(ORIGIN, DOWN)
            words.rotate(angle, about_point=ORIGIN)
            words.shift(half.point_from_proportion(0.15))
            words.match_color(half)

        self.play(ShowCreation(tips))
        self.wait()
        self.add(top_half, tips)
        self.play(
            ShowCreationThenFadeOut(top_half),
            FadeIn(top_words, -vect),
        )
        self.add(low_half, tips)
        self.play(
            ShowCreationThenFadeOut(low_half),
            FadeIn(low_words, vect),
        )
        self.wait()

        windmill.add(tips)
        self.above_below_words = all_words

    def change_pivot(self):
        windmill = self.windmill
        dots = self.dots
        arrow = self.question_arrow

        blue_rect = SurroundingRectangle(dots[3])
        blue_rect.set_color(BLUE)
        new_pivot_word = OldTexText("New pivot")
        new_pivot_word.next_to(blue_rect, LEFT)
        old_pivot_word = OldTexText("Old pivot")
        old_pivot = windmill.pivot
        old_pivot_word.next_to(
            old_pivot, LEFT,
            buff=SMALL_BUFF + MED_SMALL_BUFF
        )

        self.play(
            FadeOut(self.above_below_words),
            ReplacementTransform(
                self.question,
                new_pivot_word,
            ),
            ReplacementTransform(arrow, blue_rect),
        )
        self.wait()
        anims, time = self.rotate_to_next_pivot(windmill)
        self.play(
            *anims,
            Rotate(
                windmill,
                angle=-windmill.rot_speed,
                rate_func=linear,
            )
        )
        self.wait()
        self.play(
            TransformFromCopy(new_pivot_word, old_pivot_word),
            blue_rect.move_to, old_pivot,
        )
        self.wait(2)

        # Hit new point
        brown_rect = SurroundingRectangle(dots[1])
        brown_rect.set_color(GREY_BROWN)

        self.play(TransformFromCopy(blue_rect, brown_rect))
        self.play(
            blue_rect.move_to, windmill.pivot,
            blue_rect.set_color, GREY_BROWN,
            old_pivot_word.move_to, new_pivot_word,
            FadeOut(new_pivot_word, DL)
        )
        self.let_windmill_run(windmill, 1)
        self.wait()
        self.play(
            FadeOut(old_pivot_word),
            FadeOut(blue_rect),
            FadeOut(brown_rect),
        )
        self.let_windmill_run(windmill, 20)
