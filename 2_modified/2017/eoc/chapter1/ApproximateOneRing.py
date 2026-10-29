# ==============================================================================
# Scene:      ApproximateOneRing
# Source:     videos/_2017/eoc/chapter1.py (lines 699-982)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl ApproximateOneRing.py ApproximateOneRing -w -m --fps 15
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
        "fill_opacity" : 0.75,
        "radial_line_color" : MAROON_B,
        "outer_ring_color" : GREEN_E,
        "ring_colors" : [BLUE, GREEN],
        "dR" : 0.1,
        "dR_color" : YELLOW,
        "unwrapped_tip" : ORIGIN,
        "include_pi_creature" : False,
        "circle_corner" : UP+LEFT,
    }
    def setup(self):
        PiCreatureScene.setup(self)
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

        self.radius_group = VGroup(
            self.radius_line, self.radius_brace, self.radius_label
        )
        self.add(self.circle, *self.radius_group)

        if not self.include_pi_creature:
            self.remove(self.get_primary_pi_creature())

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

    def get_rings(self, **kwargs):
        dR = kwargs.get("dR", self.dR)
        colors = kwargs.get("colors", self.ring_colors)
        radii = np.arange(0, self.radius, dR)
        colors = color_gradient(colors, len(radii))

        rings = VGroup(*[
            self.get_ring(radius, dR = dR, color = color)
            for radius, color in zip(radii, colors)
        ])
        return rings

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
            path_arc = np.pi/2,
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
        if to_edge is not None:
            result.to_edge(to_edge)

        return result

    def create_pi_creature(self):
        self.pi_creature = Randolph(color = BLUE_C)
        self.pi_creature.to_corner(DOWN+LEFT)
        return self.pi_creature


class ApproximateOneRing(CircleScene, ReconfigurableScene):
    CONFIG = {
        "num_lines" : 24,
        "ring_index_proportion" : 0.6,
        "ring_shift_val" : 6*RIGHT,
        "ring_colors" : [BLUE, GREEN_E],
        "unwrapped_tip" : 2*RIGHT+0.5*UP,
    }
    def setup(self):
        CircleScene.setup(self)
        ReconfigurableScene.setup(self)

    def construct(self):
        self.force_skipping()

        self.write_radius_three()
        self.try_to_understand_area()
        self.slice_into_rings()
        self.isolate_one_ring()

        self.revert_to_original_skipping_status()
        self.straighten_ring_out()
        self.force_skipping()

        self.approximate_as_rectangle()

    def write_radius_three(self):
        three = OldTex("3")
        three.move_to(self.radius_label)

        self.look_at(self.circle)
        self.play(Transform(
            self.radius_label, three,
            path_arc = np.pi
        ))
        self.wait()

    def try_to_understand_area(self):
        line_sets = [
            VGroup(*[
                Line(
                    self.circle.point_from_proportion(alpha),
                    self.circle.point_from_proportion(func(alpha)),
                )
                for alpha in np.linspace(0, 1, self.num_lines)
            ])
            for func in [
                lambda alpha : 1-alpha,
                lambda alpha : (0.5-alpha)%1,
                lambda alpha : (alpha + 0.4)%1,
                lambda alpha : (alpha + 0.5)%1,
            ]
        ]
        for lines in line_sets:
            lines.set_stroke(BLACK, 2)
        lines = line_sets[0]

        self.play(
            ShowCreation(
                lines, 
                run_time = 2, 
                lag_ratio = 0.5
            ),
            Animation(self.radius_group),
            self.pi_creature.change_mode, "maybe"
        )
        self.wait(2)
        for new_lines in line_sets[1:]:
            self.play(
                Transform(lines, new_lines),
                Animation(self.radius_group)
            )
            self.wait()
        self.wait()
        self.play(FadeOut(lines), Animation(self.radius_group))

    def slice_into_rings(self):
        rings = self.get_rings()
        rings.set_stroke(BLACK, 1)

        self.play(
            FadeIn(
                rings,
                lag_ratio = 0.5,
                run_time = 3
            ),
            Animation(self.radius_group),
            self.pi_creature.change_mode, "pondering",
            self.pi_creature.look_at, self.circle
        )
        self.wait(2)
        for x in range(2):
            self.play(
                Rotate(rings, np.pi, in_place = True, run_time = 2),
                Animation(self.radius_group),
                self.pi_creature.change_mode, "happy"
            )
        self.wait(2)

        self.rings = rings

    def isolate_one_ring(self):
        rings = self.rings
        index = int(self.ring_index_proportion*len(rings))
        original_ring = rings[index]
        ring = original_ring.copy()

        radius = Line(ORIGIN, ring.R*RIGHT, color = WHITE)
        radius.rotate(np.pi/4)
        r_label = OldTex("r")
        r_label.next_to(radius.get_center(), UP+LEFT, SMALL_BUFF)
        area_q = OldTexText("Area", "?", arg_separator = "")
        area_q.set_color(YELLOW)


        self.play(
            ring.shift, self.ring_shift_val,
            original_ring.set_fill, None, 0.25,
            Animation(self.radius_group),
        )

        VGroup(radius, r_label).shift(ring.get_center())
        area_q.next_to(ring, RIGHT)

        self.play(ShowCreation(radius))
        self.play(Write(r_label))
        self.wait()
        self.play(Write(area_q))
        self.wait()
        self.play(*[
            ApplyMethod(
                r.set_fill, YELLOW, 
                rate_func = squish_rate_func(there_and_back, alpha, alpha+0.15),
                run_time = 3
            )
            for r, alpha in zip(rings, np.linspace(0, 0.85, len(rings)))
        ]+[
            Animation(self.radius_group)
        ])
        self.wait()
        self.change_mode("thinking")
        self.wait()

        self.original_ring = original_ring
        self.ring = ring
        self.ring_radius_group = VGroup(radius, r_label)
        self.area_q = area_q

    def straighten_ring_out(self):
        ring = self.ring.copy()
        trapezoid = OldTexText("Trapezoid?")
        rectangle_ish = OldTexText("Rectangle-ish")
        for text in trapezoid, rectangle_ish:
            text.next_to(
                self.pi_creature.get_corner(UP+RIGHT), 
                DOWN+RIGHT, buff = MED_LARGE_BUFF
            )

        self.unwrap_ring(ring, to_edge = RIGHT)
        self.change_mode("pondering")
        self.wait()
        self.play(Write(trapezoid))
        self.wait()
        self.play(trapezoid.shift, DOWN)
        strike = Line(
            trapezoid.get_left(), trapezoid.get_right(),
            stroke_color = RED,
            stroke_width = 8
        )
        self.play(
            Write(rectangle_ish),
            ShowCreation(strike),
            self.pi_creature.change_mode, "happy"
        )
        self.wait()
        self.play(*list(map(FadeOut, [trapezoid, strike])))

        self.unwrapped_ring = ring

    def approximate_as_rectangle(self):
        top_brace, side_brace = [
            Brace(
                self.unwrapped_ring, vect, buff = SMALL_BUFF,
                min_num_quads = 2,
            )
            for vect in (UP, LEFT)
        ]
        top_brace.scale(self.ring.R/(self.ring.R+self.dR))
        side_brace.set_stroke(WHITE, 0.5)


        width_label = OldTex("2\\pi", "r")
        width_label.next_to(top_brace, UP, SMALL_BUFF)
        dr_label = OldTex("dr")
        q_marks = OldTex("???")
        concrete_dr = OldTex("=0.1")
        concrete_dr.submobjects.reverse()
        for mob in dr_label, q_marks, concrete_dr:
            mob.next_to(side_brace, LEFT, SMALL_BUFF)
        dr_label.save_state()

        alt_side_brace = side_brace.copy()
        alt_side_brace.move_to(ORIGIN, UP+RIGHT)
        alt_side_brace.rotate(-np.pi/2)
        alt_side_brace.shift(
            self.original_ring.get_boundary_point(RIGHT)
        )
        alt_dr_label = dr_label.copy()
        alt_dr_label.next_to(alt_side_brace, UP, SMALL_BUFF)

        approx = OldTex("\\approx")
        approx.next_to(
            self.area_q.get_part_by_tex("Area"), 
            RIGHT,
            align_using_submobjects = True,
        )
        two_pi_r_dr = VGroup(width_label, dr_label).copy()
        two_pi_r_dr.generate_target()
        two_pi_r_dr.target.arrange(
            RIGHT, buff = SMALL_BUFF, aligned_edge = DOWN
        )
        two_pi_r_dr.target.next_to(approx, RIGHT, aligned_edge = DOWN)

        self.play(GrowFromCenter(top_brace))
        self.play(
            Write(width_label.get_part_by_tex("pi")),
            ReplacementTransform(
                self.ring_radius_group[1].copy(),
                width_label.get_part_by_tex("r")
            )
        )
        self.wait()
        self.play(
            GrowFromCenter(side_brace),
            Write(q_marks)
        )
        self.change_mode("confused")
        self.wait()
        for num_rings in 20, 7:
            self.show_alternate_width(num_rings)
        self.play(ReplacementTransform(q_marks, dr_label))
        self.play(
            ReplacementTransform(side_brace.copy(), alt_side_brace),
            ReplacementTransform(dr_label.copy(), alt_dr_label),
            run_time = 2
        )
        self.wait()
        self.play(
            dr_label.next_to, concrete_dr.copy(), LEFT, SMALL_BUFF, DOWN,
            Write(concrete_dr, run_time = 2),
            self.pi_creature.change_mode, "pondering"
        )
        self.wait(2)
        self.play(
            MoveToTarget(two_pi_r_dr),
            FadeIn(approx),
            self.area_q.get_part_by_tex("?").fade, 1,
        )
        self.wait()
        self.play(
            FadeOut(concrete_dr),
            dr_label.restore
        )
        self.show_alternate_width(
            40, 
            transformation_kwargs = {"run_time" : 4},
            return_to_original_configuration = False,
        )
        self.wait(2)
        self.look_at(self.circle)
        self.play(
            ApplyWave(self.rings, amplitude = 0.1),
            Animation(self.radius_group),
            Animation(alt_side_brace),
            Animation(alt_dr_label),
            run_time = 3,
            lag_ratio = 0.5
        )
        self.wait(2)

    def show_alternate_width(self, num_rings, **kwargs):
        self.transition_to_alt_config(
            dR = self.radius/num_rings, **kwargs
        )
