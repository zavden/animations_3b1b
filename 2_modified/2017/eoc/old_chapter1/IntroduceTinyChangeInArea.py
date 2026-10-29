# ==============================================================================
# Scene:      IntroduceTinyChangeInArea
# Source:     videos/_2017/eoc/old_chapter1.py (lines 541-777)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl IntroduceTinyChangeInArea.py IntroduceTinyChangeInArea -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Python 2 integer division: np.linspace needs an int
#   - Cairo copy() kept .target; GL sets target=None: copy the target by hand
# ==============================================================================

from manim_imports_ext import *

class CircleScene(PiCreatureScene):
    CONFIG = {
        "radius" : 1.5,
        "stroke_color" : WHITE,
        "fill_color" : BLUE_E,
        "fill_opacity" : 0.5,
        "radial_line_color" : MAROON_B,
        "outer_ring_color" : GREEN_E,
        "dR" : 0.1,
        "dR_color" : YELLOW,
        "unwrapped_tip" : ORIGIN,
        "include_pi_creature" : False,
        "circle_corner" : UP+LEFT
    }
    def setup(self):
        self.circle = Circle(
            radius = self.radius,
            stroke_color = self.stroke_color,
            fill_color = self.fill_color,
            fill_opacity = self.fill_opacity,
        )
        self.circle.to_corner(self.circle_corner, buff = MED_LARGE_BUFF)
        self.radius_line = Line(
            self.circle.get_center(),
            self.circle.get_right(),
            color = self.radial_line_color
        )
        self.radius_brace = Brace(self.radius_line, buff = SMALL_BUFF)
        self.radius_label = self.radius_brace.get_text("$R$", buff = SMALL_BUFF)

        self.add(
            self.circle, self.radius_line, 
            self.radius_brace, self.radius_label
        )

        self.pi_creature = self.create_pi_creature()
        if self.include_pi_creature:
            self.add(self.pi_creature)
        else:
            self.pi_creature.set_fill(opacity = 0)

    def create_pi_creature(self):
        return Mortimer().to_corner(DOWN+RIGHT)

    def introduce_circle(self, added_anims = []):
        self.remove(self.circle)
        self.play(
            ShowCreation(self.radius_line),
            GrowFromCenter(self.radius_brace),
            Write(self.radius_label),
        )
        self.circle.set_fill(opacity = 0)

        self.play(
            Rotate(
                self.radius_line, 2*np.pi-0.001, 
                about_point = self.circle.get_center(),
            ),
            ShowCreation(self.circle),
            *added_anims,
            run_time = 2
        )
        self.play(
            self.circle.set_fill, self.fill_color, self.fill_opacity,
            Animation(self.radius_line),
            Animation(self.radius_brace),
            Animation(self.radius_label),
        )

    def increase_radius(self, numerical_dr = True, run_time = 2):
        radius_mobs = VGroup(
            self.radius_line, self.radius_brace, self.radius_label
        )
        nudge_line = Line(
            self.radius_line.get_right(),
            self.radius_line.get_right() + self.dR*RIGHT,
            color = self.dR_color
        )
        nudge_arrow = Arrow(
            nudge_line.get_center() + 0.5*RIGHT+DOWN,
            nudge_line.get_center(),
            color = YELLOW,
            buff = SMALL_BUFF,
            tip_length = 0.2,
        )
        if numerical_dr:
            nudge_label = OldTex("%.01f"%self.dR)
        else:
            nudge_label = OldTex("dr")
        nudge_label.set_color(self.dR_color)
        nudge_label.scale(0.75)
        nudge_label.next_to(nudge_arrow.get_start(), DOWN)

        radius_mobs.add(nudge_line, nudge_arrow, nudge_label)

        outer_ring = self.get_outer_ring()

        self.play(
            FadeIn(outer_ring),            
            ShowCreation(nudge_line),
            ShowCreation(nudge_arrow),
            Write(nudge_label),
            run_time = run_time/2.
        )
        self.wait(run_time/2.)
        self.nudge_line = nudge_line
        self.nudge_arrow = nudge_arrow
        self.nudge_label = nudge_label
        self.outer_ring = outer_ring
        return outer_ring

    def get_ring(self, radius, dR, color = GREEN):
        ring = Circle(radius = radius + dR).center()
        inner_ring = Circle(radius = radius)
        inner_ring.rotate(np.pi, RIGHT)
        ring.append_vectorized_mobject(inner_ring)
        ring.set_stroke(width = 0)
        ring.set_fill(color)
        ring.move_to(self.circle)
        ring.R = radius 
        ring.dR = dR
        return ring

    def get_outer_ring(self):
        return self.get_ring(
            radius = self.radius, dR = self.dR,
            color = self.outer_ring_color
        )

    def unwrap_ring(self, ring, **kwargs):
        self.unwrap_rings(ring, **kwargs)

    def unwrap_rings(self, *rings, **kwargs):
        added_anims = kwargs.get("added_anims", [])
        rings = VGroup(*rings)
        unwrapped = VGroup(*[
            self.get_unwrapped(ring, **kwargs)
            for ring in rings
        ])
        self.play(
            rings.rotate, np.pi/2,
            rings.next_to, unwrapped.get_bottom(), UP,
            run_time = 2,
            path_arc = np.pi/2
        )
        self.play(
            Transform(rings, unwrapped, run_time = 3),
            *added_anims
        )

    def get_unwrapped(self, ring, to_edge = LEFT, **kwargs):
        R = ring.R
        R_plus_dr = ring.R + ring.dR
        n_anchors = ring.get_num_curves()
        result = VMobject()
        result.set_points_as_corners([
            interpolate(np.pi*R_plus_dr*LEFT,  np.pi*R_plus_dr*RIGHT, a)
            # CHANGE: Python 2 integer division: np.linspace needs an int
            for a in np.linspace(0, 1, n_anchors//2)
        ]+[
            interpolate(np.pi*R*RIGHT+ring.dR*UP,  np.pi*R*LEFT+ring.dR*UP, a)
            # CHANGE: Python 2 integer division: np.linspace needs an int
            for a in np.linspace(0, 1, n_anchors//2)
        ])
        result.set_style_data(
            stroke_color = ring.get_stroke_color(),
            stroke_width = ring.get_stroke_width(),
            fill_color = ring.get_fill_color(),
            fill_opacity = ring.get_fill_opacity(),
        )
        result.move_to(self.unwrapped_tip, aligned_edge = DOWN)
        result.shift(R_plus_dr*DOWN)
        result.to_edge(to_edge)

        return result


class IntroduceTinyChangeInArea(CircleScene):
    CONFIG = {
        "include_pi_creature" : True,
    }
    def construct(self):
        new_area_form, minus, area_form = expression = OldTex(
            "\\pi (R + 0.1)^2", "-", "\\pi R^2"
        )
        VGroup(*new_area_form[4:7]).set_color(self.dR_color)
        expression_brace = Brace(expression, UP)
        change_in_area = expression_brace.get_text("Change in area")
        change_in_area.set_color(self.outer_ring_color)
        area_brace = Brace(area_form)
        area_word = area_brace.get_text("Area")
        area_word.set_color(BLUE)
        new_area_brace = Brace(new_area_form)
        new_area_word = new_area_brace.get_text("New area")
        group = VGroup(
            expression, expression_brace, change_in_area,
            area_brace, area_word, new_area_brace, new_area_word
        )
        group.to_edge(UP).shift(RIGHT)
        group.save_state()
        area_group = VGroup(area_form, area_brace, area_word)
        area_group.save_state()
        area_group.next_to(self.circle, RIGHT, buff = LARGE_BUFF)

        self.introduce_circle(
            added_anims = [self.pi_creature.change_mode, "speaking"]
        )
        self.play(Write(area_group))
        self.change_mode("happy")
        outer_ring = self.increase_radius()
        self.wait()
        self.play(
            area_group.restore,            
            GrowFromCenter(expression_brace),
            Write(new_area_form), 
            Write(minus), 
            Write(change_in_area),
            self.pi_creature.change_mode, "confused",
        )
        self.play(
            Write(new_area_word),
            GrowFromCenter(new_area_brace)
        )
        self.wait(2)
        self.play(
            group.fade, 0.7,
            self.pi_creature.change_mode, "happy"
        )
        self.wait()
        self.play(
            outer_ring.set_color, YELLOW,
            Animation(self.nudge_arrow),
            Animation(self.nudge_line),
            rate_func = there_and_back
        )
        self.show_unwrapping(outer_ring)
        self.play(group.restore)
        self.work_out_expression(group)
        self.second_unwrapping(outer_ring)
        insignificant = OldTexText("Insignificant")
        insignificant.set_color(self.dR_color)
        insignificant.move_to(self.error_words)
        self.play(Transform(self.error_words, insignificant))
        self.wait()

        big_rect = Rectangle(
            width = FRAME_WIDTH,
            height = FRAME_HEIGHT,
            fill_color = BLACK, 
            fill_opacity = 0.85,
            stroke_width = 0,
        )
        self.play(
            FadeIn(big_rect),
            area_form.set_color, BLUE,
            self.two_pi_R.set_color, GREEN,
            self.pi_creature.change_mode, "happy"
        )

    def show_unwrapping(self, outer_ring):
        almost_rect = outer_ring.copy()        
        self.unwrap_ring(
            almost_rect,
            added_anims = [self.pi_creature.change_mode, "pondering"]
        )

        circum_brace = Brace(almost_rect, UP).scale(0.95)
        dR_brace = OldTex("\\}")
        dR_brace.stretch(0.5, 1)
        dR_brace.next_to(almost_rect, RIGHT)
        two_pi_R = circum_brace.get_text("$2\\pi R$")
        dR = OldTex("$0.1$").scale(0.7).next_to(dR_brace, RIGHT)
        dR.set_color(self.dR_color)

        two_pi_R.generate_target()
        dR.generate_target()
        lp, rp = OldTex("()")
        change_in_area = OldTexText(
            "Change in area $\\approx$"
        )
        final_area = VGroup(
            change_in_area,
            two_pi_R.target, lp, dR.target.scale(1./0.7), rp
        )
        final_area.arrange(RIGHT, buff = SMALL_BUFF)
        final_area.next_to(almost_rect, DOWN, buff = MED_LARGE_BUFF)
        final_area.set_color(GREEN_A)
        final_area[3].set_color(self.dR_color)
        change_in_area.shift(0.1*LEFT)

        self.play(
            GrowFromCenter(circum_brace),
            Write(two_pi_R)
        )
        self.wait()
        self.play(
            GrowFromCenter(dR_brace),
            Write(dR)
        )
        self.wait()
        # CHANGE: Cairo copy() kept .target; GL sets target=None: copy the target by hand
        two_pi_R_copy = two_pi_R.copy()
        two_pi_R_copy.target = two_pi_R.target.copy()
        dR_copy = dR.copy()
        dR_copy.target = dR.target.copy()
        self.play(
            MoveToTarget(two_pi_R_copy),
            MoveToTarget(dR_copy),
            Write(change_in_area, run_time = 1),
            Write(lp),
            Write(rp),
        )
        self.remove(*self.get_mobjects_from_last_animation())
        self.add(final_area)
        self.play(
            self.pi_creature.change_mode, "happy",
            self.pi_creature.look_at, final_area
        )
        self.wait()
        group = VGroup(
            almost_rect, final_area, two_pi_R, dR,
            circum_brace, dR_brace
        )
        self.play(group.fade)

    def work_out_expression(self, expression_group):
        exp, exp_brace, title, area_brace, area_word, new_area_brace, new_area_word = expression_group
        new_area_form, minus, area_form = exp

        expanded = OldTex(
            "\\pi R^2", "+", "2\\pi R (0.1)", 
            "+", "\\pi (0.1)^2", "-", "\\pi R^2",
        )
        pi_R_squared, plus, two_pi_R_dR, plus2, pi_dR_squared, minus2, pi_R_squared2 = expanded
        for subset in two_pi_R_dR[4:7], pi_dR_squared[2:5]:
            VGroup(*subset).set_color(self.dR_color)
        expanded.next_to(new_area_form, DOWN, aligned_edge = LEFT, buff = MED_SMALL_BUFF)
        expanded.shift(LEFT/2.)

        faders = [area_brace, area_word, new_area_brace, new_area_word]
        self.play(*list(map(FadeOut, faders)))
        trips = [
            ([0, 2, 8], pi_R_squared, plus),
            ([8, 0, 2, 1, 4, 5, 6, 7], two_pi_R_dR, plus2),
            ([0, 1, 4, 5, 6, 7, 8], pi_dR_squared, VGroup()),
        ]
        to_remove = []
        for subset, target, writer in trips:
            starter = VGroup(
                *np.array(list(new_area_form.copy()))[subset]
            )
            self.play(
                Transform(starter, target, run_time = 2),
                Write(writer)
            )
            to_remove += self.get_mobjects_from_last_animation()
            self.wait()
        self.play(
            Transform(minus.copy(), minus2),
            Transform(area_form.copy(), pi_R_squared2),
        )
        to_remove += self.get_mobjects_from_last_animation()
        self.remove(*to_remove)
        self.add(self.pi_creature, *expanded)
        self.wait(2)
        self.play(*[
            ApplyMethod(mob.set_color, RED)
            for mob in (pi_R_squared, pi_R_squared2)
        ])
        self.wait()
        self.play(*[
            ApplyMethod(mob.fade, 0.7)
            for mob in (plus, pi_R_squared, pi_R_squared2, minus2)
        ]) 
        self.wait()

        approx_brace = Brace(two_pi_R_dR)
        error_brace = Brace(pi_dR_squared, buff = SMALL_BUFF)
        error_words = error_brace.get_text("Error", buff = SMALL_BUFF)
        error_words.set_color(RED)
        self.error_words = error_words

        self.play(
            GrowFromCenter(approx_brace),
            self.pi_creature.change_mode, "hooray"
        )
        self.wait()
        self.play(
            GrowFromCenter(error_brace),
            Write(error_words),
            self.pi_creature.change_mode, "confused"
        )
        self.wait()
        self.two_pi_R = VGroup(*two_pi_R_dR[:3])

    def second_unwrapping(self, outer_ring):
        almost_rect = outer_ring.copy()
        rect = Rectangle(
            width = 2*np.pi*self.radius,
            height = self.dR,
            fill_color = self.outer_ring_color,
            fill_opacity = 1,
            stroke_width = 0,
        )
        self.play(
            almost_rect.set_color, YELLOW,
            self.pi_creature.change_mode, "pondering"
        )
        self.unwrap_ring(almost_rect)
        self.wait()
        rect.move_to(almost_rect)
        self.play(FadeIn(rect))
        self.wait()

    def create_pi_creature(self):
        morty = Mortimer()
        morty.scale(0.7)
        morty.to_corner(DOWN+RIGHT)
        return morty
