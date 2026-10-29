# ==============================================================================
# Scene:      IntroduceConcentricRings
# Source:     videos/_2017/eoc/old_chapter1.py (lines 1661-2008)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl IntroduceConcentricRings.py IntroduceConcentricRings -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Grant's repo renamed TexMobject->Tex here (new GL class); the 2017 code needs the Cairo-style OldTex
#   - Python 2 integer division: np.linspace needs an int
#   - GL ApplyMethod takes the method kwargs as a trailing dict
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


class IntroduceConcentricRings(CircleScene):
    CONFIG = {
        "radius" : 2.5,
        "special_ring_index" : 10,
        "include_pi_creature" : True,
    }
    def construct(self):
        self.build_up_rings()
        self.add_up_areas()
        self.unwrap_special_ring()
        self.write_integral()
        self.ask_about_approx()

    def create_pi_creature(self):
        morty = Mortimer()
        morty.scale(0.7)
        morty.to_corner(DOWN+RIGHT)
        return morty

    def build_up_rings(self):
        self.circle.set_fill(opacity = 0)
        rings = VGroup(*[
            self.get_ring(r, self.dR)
            for r in np.arange(0, self.radius, self.dR)
        ])
        rings.set_color_by_gradient(BLUE_E, GREEN_E)
        rings.set_stroke(BLACK, width = 1)
        outermost_ring = rings[-1]
        dr_line = Line(
            rings[-2].get_top(), 
            rings[-1].get_top(),
            color = YELLOW
        )
        dr_text = OldTex("dr")
        dr_text.move_to(self.circle.get_corner(UP+RIGHT))
        dr_text.shift(LEFT)
        dr_text.set_color(YELLOW)
        dr_arrow = Arrow(dr_text, dr_line, buff = SMALL_BUFF)
        self.dr_group = VGroup(dr_text, dr_arrow, dr_line)


        foreground_group = VGroup(self.radius_brace, self.radius_label, self.radius_line)
        self.play(
            FadeIn(outermost_ring), 
            Animation(foreground_group)
        )
        self.play(
            Write(dr_text),
            ShowCreation(dr_arrow),
            ShowCreation(dr_line)
        )
        foreground_group.add(dr_line, dr_arrow, dr_text)        
        self.change_mode("pondering")
        self.wait()
        self.play(
            FadeIn(
                VGroup(*rings[:-1]),
                lag_ratio=1,
                run_time = 5
            ),
            Animation(foreground_group)
        )
        self.wait()

        self.foreground_group = foreground_group
        self.rings = rings

    def add_up_areas(self):
        start_rings = VGroup(*self.rings[:4])
        moving_rings = start_rings.copy()
        moving_rings.generate_target()
        moving_rings.target.set_stroke(width = 0)
        # CHANGE: Grant's repo renamed TexMobject->Tex here (new GL class); the 2017 code needs the Cairo-style OldTex
        plusses = VGroup(*[OldTex("+") for ring in moving_rings])
        area_sum = VGroup(*it.chain(*list(zip(
            [ring for ring in moving_rings.target],
            plusses
        ))))
        dots_equals_area = OldTex("\\dots", "=", "\\pi R^2")
        area_sum.add(*dots_equals_area)
        area_sum.arrange()
        area_sum.to_edge(RIGHT)
        area_sum.to_edge(UP, buff = MED_SMALL_BUFF)
        dots_equals_area[-1].shift(0.1*UP)
        self.area_sum_rhs = dots_equals_area[-1]

        # start_rings.set_fill(opacity = 0.3)
        self.play(
            MoveToTarget(
                moving_rings,
                lag_ratio = 0.5,
            ),
            Write(
                VGroup(plusses, dots_equals_area),
                rate_func = squish_rate_func(smooth, 0.5, 1)
            ),
            Animation(self.foreground_group),
            run_time = 5,
        )
        self.wait()
        self.area_sum = area_sum

    def unwrap_special_ring(self):
        rings = self.rings
        foreground_group = self.foreground_group
        special_ring = rings[self.special_ring_index]
        special_ring.save_state()

        radius = (special_ring.get_width()-2*self.dR)/2.
        radial_line = Line(ORIGIN, radius*RIGHT)
        radial_line.rotate(np.pi/4)
        radial_line.shift(self.circle.get_center())
        radial_line.set_color(YELLOW)
        r_label = OldTex("r")
        r_label.next_to(radial_line.get_center(), UP+LEFT, buff = SMALL_BUFF)

        rings.generate_target()
        rings.save_state()
        rings.target.set_fill(opacity = 0.3)
        rings.target.set_stroke(BLACK)
        rings.target[self.special_ring_index].set_fill(opacity = 1)
        self.play(
            MoveToTarget(rings),
            Animation(foreground_group)
        )
        self.play(ShowCreation(radial_line))
        self.play(Write(r_label))
        self.foreground_group.add(radial_line, r_label)
        self.wait()
        self.unwrap_ring(special_ring, to_edge = RIGHT)

        brace = Brace(special_ring, UP)
        brace.stretch_in_place(0.9, 0)
        two_pi_r = brace.get_text("$2\\pi r$")
        left_brace = OldTex("\\{")
        left_brace.stretch_to_fit_height(1.5*self.dR)
        left_brace.next_to(special_ring, LEFT, buff = SMALL_BUFF)
        dr = OldTex("dr")
        dr.next_to(left_brace, LEFT, buff = SMALL_BUFF)
        self.play(
            GrowFromCenter(brace),
            Write(two_pi_r)
        )
        self.play(GrowFromCenter(left_brace), Write(dr))
        self.wait()

        think_concrete = OldTexText("Think $dr = 0.1$")
        think_concrete.next_to(dr, DOWN+LEFT, buff = LARGE_BUFF)
        arrow = Arrow(think_concrete.get_top(), dr)
        self.play(
            Write(think_concrete),
            ShowCreation(arrow),
            self.pi_creature.change_mode, "speaking"
        )
        self.wait()

        less_wrong = OldTexText("""
            Approximations get
            less wrong
        """)
        less_wrong.next_to(self.pi_creature, LEFT, aligned_edge = UP)
        self.play(Write(less_wrong))
        self.wait()

        self.special_ring = special_ring
        self.radial_line = radial_line
        self.r_label = r_label
        self.to_fade = VGroup(
            brace, left_brace, two_pi_r, dr, 
            think_concrete, arrow, less_wrong
        )
        self.two_pi_r = two_pi_r.copy()
        self.dr = dr.copy()

    def write_integral(self):
        brace = Brace(self.area_sum)
        formula_q = brace.get_text("Nice formula?")
        int_sym, R, zero = def_int = OldTex("\\int", "_0", "^R")
        self.two_pi_r.generate_target()
        self.dr.generate_target()
        equals_pi_R_squared = OldTex("= \\pi R^2")
        integral_expression = VGroup(
            def_int, self.two_pi_r.target,
            self.dr.target, equals_pi_R_squared
        )
        integral_expression.arrange()
        integral_expression.next_to(brace, DOWN)
        self.integral_expression = VGroup(*integral_expression[:-1])

        self.play(
            GrowFromCenter(brace),
            Write(formula_q),
            self.pi_creature.change_mode, "pondering"
        )
        self.wait(2)

        last = VMobject()
        last.save_state()
        for ring in self.rings:
            ring.save_state()
            target = ring.copy()
            target.set_fill(opacity = 1)
            self.play(
                last.restore,
                Transform(ring, target),
                Animation(self.foreground_group),
                run_time = 0.5
            )
            last = ring
        self.play(last.restore)
        self.wait()

        ghost = self.rings.copy()
        for mob in self.area_sum_rhs, self.two_pi_r:
            ghost.set_fill(opacity = 0.1)
            self.play(Transform(ghost, mob))
            self.wait()
        self.remove(ghost)

        self.wait()
        self.play(FadeOut(formula_q))
        self.play(Write(int_sym))
        self.wait()
        self.rings.generate_target()
        self.rings.target.set_fill(opacity = 1)
        self.play(
            MoveToTarget(self.rings, rate_func = there_and_back),
            Animation(self.foreground_group)
        )
        self.wait()
        self.grow_and_shrink_r_line(zero, R)
        self.wait()
        self.play(
            MoveToTarget(self.two_pi_r),
            MoveToTarget(self.dr),
            run_time = 2
        )
        self.wait()
        self.play(
            FadeOut(self.to_fade),
            ApplyMethod(self.rings.restore, run_time = 2),
            Animation(self.foreground_group)
        )
        self.wait()
        self.play(Write(equals_pi_R_squared))
        self.wait()
        self.equals = equals_pi_R_squared[0]
        self.integral_terms = VGroup(
            self.integral_expression[1], 
            self.integral_expression[2], 
            self.int_lower_bound, 
            self.int_upper_bound,
            VGroup(*equals_pi_R_squared[1:])
        )

    def grow_and_shrink_r_line(self, zero_target, R_target):
        self.radial_line.get_center = self.circle.get_center
        self.radial_line.save_state()
        self.radial_line.generate_target()
        self.radial_line.target.scale(
            0.1 / self.radial_line.get_length()
        )
        self.r_label.generate_target()
        self.r_label.save_state()
        equals_0 = OldTex("=0")
        r_equals_0 = VGroup(self.r_label.target, equals_0)
        r_equals_0.arrange(buff = SMALL_BUFF)
        r_equals_0.next_to(self.radial_line.target, UP+LEFT, buff = SMALL_BUFF)
        self.play(
            MoveToTarget(self.radial_line),
            MoveToTarget(self.r_label),
            GrowFromCenter(equals_0)
        )
        self.play(equals_0[-1].copy().replace, zero_target)
        self.remove(self.get_mobjects_from_last_animation()[0])
        self.add(zero_target)
        self.wait()
        self.radial_line.target.scale(
            self.radius/self.radial_line.get_length()
        )
        equals_0.target = OldTex("=R")
        equals_0.target.next_to(
            self.radial_line.target.get_center_of_mass(),
            UP+LEFT, buff = SMALL_BUFF
        )
        self.r_label.target.next_to(equals_0.target, LEFT, buff = SMALL_BUFF)
        self.play(
            MoveToTarget(self.radial_line),
            MoveToTarget(self.r_label),
            MoveToTarget(equals_0)
        )
        self.play(equals_0[-1].copy().replace, R_target)
        self.remove(self.get_mobjects_from_last_animation()[0])
        self.add(R_target)
        self.wait()
        self.play(
            self.radial_line.restore,
            self.r_label.restore,
            FadeOut(equals_0)
        )
        self.int_lower_bound, self.int_upper_bound = zero_target, R_target

    def ask_about_approx(self):
        approx = OldTex("\\approx").replace(self.equals)
        self.equals.save_state()
        question = OldTexText(
            "Should this be\\\\",
            "an approximation?"
        )
        question.next_to(approx, DOWN, buff = 1.3*LARGE_BUFF)
        arrow = Arrow(question, approx, buff = MED_SMALL_BUFF)
        approach_words = OldTexText("Consider\\\\", "$dr \\to 0$")
        approach_words.move_to(question, RIGHT)
        int_brace = Brace(self.integral_expression)
        integral_word = int_brace.get_text("``Integral''")

        self.play(
            Transform(self.equals, approx),
            Write(question),
            ShowCreation(arrow),
            self.pi_creature.change_mode, "confused"
        )
        self.wait(2)
        self.play(*[
            # CHANGE: GL ApplyMethod takes the method kwargs as a trailing dict
            ApplyMethod(ring.set_stroke, ring.get_color(), {"width" : 1})
            for ring in self.rings
        ] + [
            FadeOut(self.dr_group),
            Animation(self.foreground_group)
        ])
        self.wait()
        self.play(
            Transform(question, approach_words),
            Transform(arrow, Arrow(approach_words, approx)),
            self.equals.restore,
            self.pi_creature.change_mode, "happy"
        )
        self.wait(2)
        self.play(
            self.integral_expression.set_color_by_gradient, BLUE, GREEN,
            GrowFromCenter(int_brace),
            Write(integral_word)
        )
        self.wait()
        for term in self.integral_terms:
            term.save_state()
            self.play(term.set_color, YELLOW)
            self.play(term.restore)
        self.wait(3)
