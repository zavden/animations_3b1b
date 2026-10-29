# ==============================================================================
# Scene:      FundamentalTheorem
# Source:     videos/_2017/eoc/old_chapter1.py (lines 2209-2392)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl FundamentalTheorem.py FundamentalTheorem -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Python 2 integer division: np.linspace needs an int
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


class FundamentalTheorem(CircleScene):
    CONFIG = {
        "circle_corner" : ORIGIN,
        "radius" : 1.5,
        "area_color" : BLUE,
        "circum_color" : WHITE,
        "unwrapped_tip" : 2.5*UP,
        "include_pi_creature" : False
    }
    def setup(self):
        CircleScene.setup(self)
        group = VGroup(
            self.circle, self.radius_line,
            self.radius_brace, self.radius_label
        )
        self.remove(*group)
        group.shift(DOWN)

        self.foreground_group = VGroup(
            self.radius_line,
            self.radius_brace,
            self.radius_label,
        )

    def create_pi_creature(self):
        morty = Mortimer()
        morty.scale(0.7)
        morty.to_corner(DOWN+RIGHT)
        return morty

    def construct(self):
        self.add_derivative_terms()
        self.add_integral_terms()
        self.think_about_it()
        self.bring_in_circle()
        self.show_outer_ring()
        self.show_all_rings()
        self.emphasize_oposites()

    def add_derivative_terms(self):
        symbolic = OldTex(
            "\\frac{d(\\pi R^2)}{dR} =", "2\\pi R"
        )
        VGroup(*symbolic[0][2:5]).set_color(self.area_color)
        VGroup(*symbolic[0][7:9]).set_color(self.dR_color)
        symbolic[1].set_color(self.circum_color)

        geometric = OldTex("\\frac{d \\quad}{dR}=")
        VGroup(*geometric[2:4]).set_color(self.dR_color)
        radius = geometric[0].get_height()
        area_circle = Circle(
            stroke_width = 0,
            fill_color = self.area_color,
            fill_opacity = 0.5,
            radius = radius
        )
        area_circle.next_to(geometric[0], buff = SMALL_BUFF)
        circum_circle = Circle(
            color = self.circum_color,
            radius = radius
        )
        circum_circle.next_to(geometric, RIGHT)
        geometric.add(area_circle, circum_circle)
        self.derivative_terms = VGroup(symbolic, geometric)
        self.derivative_terms.arrange(
            DOWN, buff = LARGE_BUFF, aligned_edge = LEFT
        )
        self.derivative_terms.next_to(ORIGIN, LEFT, buff = LARGE_BUFF)

        self.play(
            Write(self.derivative_terms),
            self.pi_creature.change_mode, "hooray"
        )
        self.wait()

    def add_integral_terms(self):
        symbolic = OldTex(
            "\\int_0^R", "2\\pi r", "\\cdot", "dr", "=", "\\pi R^2"
        )
        symbolic.set_color_by_tex("2\\pi r", self.circum_color)
        symbolic.set_color_by_tex("dr", self.dR_color)
        symbolic.set_color_by_tex("\\pi R^2", self.area_color)

        geometric = symbolic.copy()
        area_circle = Circle(
            radius = geometric[-1].get_width()/2,
            stroke_width = 0,
            fill_color = self.area_color,
            fill_opacity = 0.5
        )
        area_circle.move_to(geometric[-1])
        circum_circle = Circle(
            radius = geometric[1].get_width()/2,
            color = self.circum_color
        )
        circum_circle.move_to(geometric[1])
        geometric.submobjects[1] = circum_circle
        geometric.submobjects[-1] = area_circle

        self.integral_terms = VGroup(symbolic, geometric)
        self.integral_terms.arrange(
            DOWN, 
            buff = LARGE_BUFF, 
            aligned_edge = LEFT
        )
        self.integral_terms.next_to(ORIGIN, RIGHT, buff = LARGE_BUFF)

        self.play(Write(self.integral_terms))
        self.wait()

    def think_about_it(self):
        for mode in "confused", "pondering", "surprised":
            self.change_mode(mode)
            self.wait()

    def bring_in_circle(self):
        self.play(
            FadeOut(self.derivative_terms[0]),
            FadeOut(self.integral_terms[0]),
            self.derivative_terms[1].to_corner, UP+LEFT, MED_LARGE_BUFF,
            self.integral_terms[1].to_corner, UP+RIGHT, MED_LARGE_BUFF,
            self.pi_creature.change_mode, "speaking"
        )
        self.introduce_circle()

    def show_outer_ring(self):
        self.increase_radius(numerical_dr = False)
        self.foreground_group.add(self.nudge_line, self.nudge_arrow)
        self.wait()
        ring_copy = self.outer_ring.copy()
        ring_copy.save_state()
        self.unwrap_ring(ring_copy, to_edge = LEFT)
        brace = Brace(ring_copy, UP)
        brace.stretch_in_place(0.95, 0)
        deriv = brace.get_text("$\\dfrac{dA}{dR}$")
        VGroup(*deriv[:2]).set_color(self.outer_ring.get_color())
        VGroup(*deriv[-2:]).set_color(self.dR_color)
        self.play(
            GrowFromCenter(brace),
            Write(deriv),
            self.pi_creature.change_mode, "happy"
        )
        self.to_fade = VGroup(deriv, brace)
        self.to_restore = ring_copy        

    def show_all_rings(self):
        rings = VGroup(*[
            self.get_ring(radius = r, dR = self.dR)
            for r in np.arange(0, self.radius, self.dR)
        ])
        rings.set_color_by_gradient(BLUE_E, GREEN_E)
        rings.save_state()
        integrand = self.integral_terms[1][1]
        for ring in rings:
            Transform(ring, integrand).update(1)

        self.play(
            ApplyMethod(
                rings.restore,
                lag_ratio = 0.5,
                run_time = 5
            ),
            Animation(self.foreground_group),
        )

    def emphasize_oposites(self):
        self.play(
            FadeOut(self.to_fade),
            self.to_restore.restore,
            Animation(self.foreground_group),
            run_time = 2
        )
        arrow = DoubleArrow(
            self.derivative_terms[1],
            self.integral_terms[1],
        )
        opposites = OldTexText("Opposites")
        opposites.next_to(arrow, DOWN)

        self.play(
            ShowCreation(arrow),
            Write(opposites)
        )
        self.wait()
