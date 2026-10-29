# ==============================================================================
# Scene:      RecapCircleSolution
# Source:     videos/_2017/eoc/chapter1.py (lines 1558-1791)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl RecapCircleSolution.py RecapCircleSolution -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Python 2 integer division: np.linspace needs an int
#   - GL arc has no self-element in its submobject list: the tip is arc.submobjects[-1] (Cairo arc[1])
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


class GraphRectangles(CircleScene, GraphScene):
    CONFIG = {
        "graph_origin" : 3.25*LEFT+2.5*DOWN,
        "x_min" : 0,
        "x_max" : 4,
        "x_axis_width" : 7,
        "x_labeled_nums" : list(range(5)),
        "x_axis_label" : "$r$",
        "y_min" : 0,
        "y_max" : 20,
        "y_tick_frequency" : 2.5,
        "y_labeled_nums" : list(range(5, 25, 5)),
        "y_axis_label" : "",
        "exclude_zero_label" : False,
        "num_rings_in_ring_sum_start" : 3,
        "tick_height" : 0.2,
    }
    def setup(self):
        CircleScene.setup(self)
        GraphScene.setup(self)
        self.setup_axes()
        self.remove(self.axes)

        # self.pi_creature.change_mode("pondering")
        # self.pi_creature.look_at(self.circle)
        # self.add(self.pi_creature)

        three = OldTex("3")
        three.move_to(self.radius_label)
        self.radius_label.save_state()
        Transform(self.radius_label, three).update(1)

    def construct(self):
        self.draw_ring_sum()
        self.draw_r_values()
        self.unwrap_rings_onto_graph()
        self.draw_graph()
        self.point_out_approximation()
        self.let_dr_approah_zero()
        self.compute_area_under_graph()
        self.show_circle_unwrapping()

    def draw_ring_sum(self):
        rings = self.get_rings()
        rings.set_stroke(BLACK, 1)
        ring_sum, draw_ring_sum_anims = self.get_ring_sum(rings)
        area_label = OldTex(
            "\\text{Area}", "\\approx", 
            "2\\pi", "r", "\\,dr"
        )
        area_label.set_color_by_tex("r", YELLOW, substring = False)
        area_label.next_to(ring_sum, RIGHT, aligned_edge = UP)
        area = area_label.get_part_by_tex("Area")
        arrow_start = area.get_corner(DOWN+LEFT)
        arrows = VGroup(*[
            Arrow(
                arrow_start,
                ring.target.get_boundary_point(
                    arrow_start - ring.target.get_center()
                ),
                color = ring.get_color()
            )
            for ring in rings
            if ring.target.get_fill_opacity() > 0
        ])
        
        self.add(rings, self.radius_group)
        self.remove(self.circle)
        self.wait()
        self.play(*draw_ring_sum_anims)
        self.play(Write(area_label, run_time = 2))
        self.play(ShowCreation(arrows))
        self.wait()

        self.ring_sum = ring_sum
        area_label.add(arrows)
        self.area_label = area_label
        self.rings = rings

    def draw_r_values(self):
        values_of_r = OldTexText("Values of ", "$r$")
        values_of_r.set_color_by_tex("r", YELLOW)
        values_of_r.next_to(
            self.x_axis, UP, 
            buff = 2*LARGE_BUFF,
            aligned_edge = LEFT
        )

        r_ticks = VGroup(*[
            Line(
                self.coords_to_point(r, -self.tick_height),
                self.coords_to_point(r, self.tick_height),
                color = YELLOW
            )
            for r in np.arange(0, 3, 0.1)
        ])
        arrows = VGroup(*[
            Arrow(
                values_of_r.get_part_by_tex("r").get_bottom(),
                tick.get_top(),
                buff = SMALL_BUFF,
                color = YELLOW,
                tip_length = 0.15
            )
            for tick in (r_ticks[0], r_ticks[-1])
        ])
        first_tick = r_ticks[0].copy()
        moving_arrow = arrows[0].copy()

        index = 2
        dr_brace = Brace(
            VGroup(*r_ticks[index:index+2]), 
            DOWN, buff = SMALL_BUFF
        )
        dr_label = OldTex("dr")
        dr_label.next_to(
            dr_brace, DOWN, 
            buff = SMALL_BUFF, 
            aligned_edge = LEFT
        )
        dr_group = VGroup(dr_brace, dr_label)

        self.play(
            FadeIn(values_of_r),
            FadeIn(self.x_axis),
        )
        self.play(
            ShowCreation(moving_arrow),
            ShowCreation(first_tick),
        )
        self.play(Indicate(self.rings[0]))
        self.wait()
        self.play(
            Transform(moving_arrow, arrows[-1]),
            ShowCreation(r_ticks, lag_ratio = 0.5),
            run_time = 2
        )
        self.play(Indicate(self.rings[-1]))
        self.wait()
        self.play(FadeIn(dr_group))
        self.wait()
        self.play(*list(map(FadeOut, [moving_arrow, values_of_r])))

        self.x_axis.add(r_ticks)
        self.r_ticks = r_ticks
        self.dr_group = dr_group
        
    def unwrap_rings_onto_graph(self):
        rings = self.rings
        graph = self.get_graph(lambda r : 2*np.pi*r)
        flat_graph = self.get_graph(lambda r : 0)
        rects, flat_rects = [
            self.get_riemann_rectangles(
                g, x_min = 0, x_max = 3, dx = self.dR,
                start_color = self.rings[0].get_fill_color(),
                end_color = self.rings[-1].get_fill_color(),
            )
            for g in (graph, flat_graph)
        ]
        self.graph, self.flat_rects = graph, flat_rects

        transformed_rings = VGroup()
        self.ghost_rings = VGroup()        
        for index, rect, r in zip(it.count(), rects, np.arange(0, 3, 0.1)):
            proportion = float(index)/len(rects)
            ring_index = int(len(rings)*proportion**0.6)
            ring = rings[ring_index]
            if ring in transformed_rings:
                ring = ring.copy()
            transformed_rings.add(ring)
            if ring.get_fill_opacity() > 0:
                ghost_ring = ring.copy()
                ghost_ring.set_fill(opacity = 0.25)
                self.add(ghost_ring, ring)
                self.ghost_rings.add(ghost_ring)

            ring.rect = rect

            n_anchors = ring.get_num_curves()            
            target = VMobject()
            target.set_points_as_corners([
                interpolate(ORIGIN,  DOWN, a)
                # CHANGE: Python 2 integer division: np.linspace needs an int
                for a in np.linspace(0, 1, n_anchors//2)
            ]+[
                interpolate(DOWN+RIGHT, RIGHT, a)
                # CHANGE: Python 2 integer division: np.linspace needs an int
                for a in np.linspace(0, 1, n_anchors//2)
            ])
            target.replace(rect, stretch = True)
            target.stretch_to_fit_height(2*np.pi*r)
            target.move_to(rect, DOWN)
            target.set_stroke(BLACK, 1)
            target.set_fill(ring.get_fill_color(), 1)
            ring.target = target
            ring.original_ring = ring.copy()

        foreground_animations = list(map(Animation, [self.x_axis, self.area_label]))
        example_ring = transformed_rings[2]

        self.play(
            MoveToTarget(
                example_ring,
                path_arc = -np.pi/2,
                run_time = 2
            ),
            Animation(self.x_axis),
        )
        self.wait(2)
        self.play(*[
            MoveToTarget(
                ring,
                path_arc = -np.pi/2,
                run_time = 4,
                rate_func = squish_rate_func(smooth, alpha, alpha+0.25)
            )
            for ring, alpha in zip(
                transformed_rings, 
                np.linspace(0, 0.75, len(transformed_rings))
            )
        ] + foreground_animations)
        self.wait()

        ##Demonstrate height of one rect
        highlighted_ring = transformed_rings[6].copy()
        original_ring = transformed_rings[6].original_ring
        original_ring.move_to(highlighted_ring, RIGHT)
        original_ring.set_fill(opacity = 1)
        highlighted_ring.save_state()

        side_brace = Brace(highlighted_ring, RIGHT)
        height_label = side_brace.get_text("2\\pi", "r")
        height_label.set_color_by_tex("r", YELLOW)

        self.play(
            transformed_rings.set_fill, None, 0.2,
            Animation(highlighted_ring),
            *foreground_animations
        )
        self.play(
            self.dr_group.arrange, DOWN,
            self.dr_group.next_to, highlighted_ring, 
            DOWN, SMALL_BUFF
        )
        self.wait()
        self.play(
            GrowFromCenter(side_brace),
            Write(height_label)
        )
        self.wait()
        self.play(Transform(highlighted_ring, original_ring))
        self.wait()
        self.play(highlighted_ring.restore)
        self.wait()
        self.play(
            transformed_rings.set_fill, None, 1,
            FadeOut(side_brace),
            FadeOut(height_label),
            *foreground_animations
        )
        self.remove(highlighted_ring)
        self.wait()

        ##Rescale
        self.play(*[
            ApplyMethod(
                ring.replace, ring.rect, 
                method_kwargs = {"stretch" : True}
            )
            for ring in transformed_rings
        ] + [
            Write(self.y_axis),
            FadeOut(self.area_label),
        ] + foreground_animations)
        self.remove(transformed_rings)
        self.add(rects)
        self.wait()

        self.rects = rects

    def draw_graph(self):
        graph_label = self.get_graph_label(
            self.graph, "2\\pi r", 
            direction = UP+LEFT,
            x_val = 2.5,
            buff = SMALL_BUFF
        )

        self.play(ShowCreation(self.graph))
        self.play(Write(graph_label))
        self.wait()
        self.play(*[
            Transform(
                rect, flat_rect,
                run_time = 2,
                rate_func = squish_rate_func(
                    lambda t : 0.1*there_and_back(t), 
                    alpha, alpha+0.5
                ),
                lag_ratio = 0.5
            )
            for rect, flat_rect, alpha in zip(
                self.rects, self.flat_rects,
                np.linspace(0, 0.5, len(self.rects))
            )
        ] + list(map(Animation, [self.x_axis, self.graph]))
        )
        self.wait(2)

    def point_out_approximation(self):
        rect = self.rects[10]
        rect.generate_target()
        rect.save_state()
        approximation = OldTexText("= Approximation")
        approximation.scale(0.8)
        group = VGroup(rect.target, approximation)
        group.arrange(RIGHT)
        group.to_edge(RIGHT)

        self.play(
            MoveToTarget(rect),
            Write(approximation),
        )
        self.wait(2)
        self.play(
            rect.restore,
            FadeOut(approximation)
        )
        self.wait()

    def let_dr_approah_zero(self):
        thinner_rects_list = [
            self.get_riemann_rectangles(
                self.graph,
                x_min = 0, 
                x_max = 3,
                dx = 1./(10*2**n),
                stroke_width = 1./(2**n),
                start_color = self.rects[0].get_fill_color(),
                end_color = self.rects[-1].get_fill_color(),
            )
            for n in range(1, 5)
        ]

        self.play(*list(map(FadeOut, [self.r_ticks, self.dr_group])))
        self.x_axis.remove(self.r_ticks, *self.r_ticks)
        for new_rects in thinner_rects_list:
            self.play(
                Transform(
                    self.rects, new_rects, 
                    lag_ratio = 0.5,
                    run_time = 2
                ),
                Animation(self.axes),
                Animation(self.graph),
            )
            self.wait()
        self.play(ApplyWave(
            self.rects,
            direction = RIGHT,
            run_time = 2,
            lag_ratio = 0.5,
        ))
        self.wait()

    def compute_area_under_graph(self):
        formula, formula_with_R = formulas = [
            self.get_area_formula(R)
            for R in ("3", "R")
        ]
        for mob in formulas:
            mob.to_corner(UP+RIGHT, buff = MED_SMALL_BUFF)

        brace = Brace(self.rects, RIGHT)
        height_label = brace.get_text("$2\\pi \\cdot 3$")
        height_label_with_R = brace.get_text("$2\\pi \\cdot R$")
        base_line = Line(
            self.coords_to_point(0, 0),
            self.coords_to_point(3, 0),
            color = YELLOW
        )

        fresh_rings = self.get_rings(dR = 0.025)
        fresh_rings.set_stroke(width = 0)
        self.radius_label.restore()
        VGroup(
            fresh_rings, self.radius_group
        ).to_corner(UP+LEFT, buff = SMALL_BUFF)

        self.play(Write(formula.top_line, run_time = 2))
        self.play(FocusOn(base_line))
        self.play(ShowCreation(base_line))
        self.wait()
        self.play(
            GrowFromCenter(brace),
            Write(height_label)
        )
        self.wait()
        self.play(FocusOn(formula))
        self.play(Write(formula.mid_line))
        self.wait()
        self.play(Write(formula.bottom_line))
        self.wait(2)

        self.play(*list(map(FadeOut, [
            self.ghost_rings,
            self.ring_sum.tex_mobs
        ])))
        self.play(*list(map(FadeIn, [fresh_rings, self.radius_group])))
        self.wait()
        self.play(
            Transform(formula, formula_with_R),
            Transform(height_label, height_label_with_R),
        )
        self.wait(2)

        self.fresh_rings = fresh_rings

    def show_circle_unwrapping(self):
        rings = self.fresh_rings
        rings.rotate(np.pi)
        rings.submobjects.reverse()
        ghost_rings = rings.copy()
        ghost_rings.set_fill(opacity = 0.25)
        self.add(ghost_rings, rings, self.radius_group)

        unwrapped = VGroup(*[
            self.get_unwrapped(ring, to_edge = None)
            for ring in rings
        ])
        unwrapped.stretch_to_fit_height(1)
        unwrapped.stretch_to_fit_width(2)
        unwrapped.move_to(ORIGIN, DOWN)
        unwrapped.apply_function(
            lambda p : np.dot(p, 
                np.array([[1, 0, 0], [-1, 1, 0], [0, 0, 1]])
            ),
            maintain_smoothness = False
        )
        unwrapped.rotate(np.pi/2)
        unwrapped.replace(self.rects, stretch = True)

        self.play(self.rects.fade, 0.8)
        self.play(
            Transform(
                rings, unwrapped,
                run_time = 5,
                lag_ratio = 0.5,
            ),
            Animation(self.radius_group)
        )
        self.wait()

    #####

    def get_ring_sum(self, rings):
        arranged_group = VGroup()
        tex_mobs = VGroup()
        for ring in rings:
            ring.generate_target()
            ring.target.set_stroke(width = 0)

        for ring in rings[:self.num_rings_in_ring_sum_start]:
            plus = OldTex("+")
            arranged_group.add(ring.target)
            arranged_group.add(plus)
            tex_mobs.add(plus)
        dots = OldTex("\\vdots")
        plus = OldTex("+")
        arranged_group.add(dots, plus)
        tex_mobs.add(dots, plus)
        last_ring = rings[-1]

        arranged_group.add(last_ring.target)
        arranged_group.arrange(DOWN, buff = SMALL_BUFF)
        arranged_group.set_height(FRAME_HEIGHT-1)
        arranged_group.to_corner(DOWN+LEFT, buff = MED_SMALL_BUFF)
        for mob in tex_mobs:
            mob.scale(0.7)

        middle_rings = rings[self.num_rings_in_ring_sum_start:-1]
        alphas = np.linspace(0, 1, len(middle_rings))
        for ring, alpha in zip(middle_rings, alphas):
            ring.target.set_fill(opacity = 0)
            ring.target.move_to(interpolate(
                dots.get_left(), last_ring.target.get_center(), alpha
            ))

        draw_ring_sum_anims = [Write(tex_mobs)]
        draw_ring_sum_anims += [
            MoveToTarget(
                ring,
                run_time = 3,
                path_arc = -np.pi/3,
                rate_func = squish_rate_func(smooth, alpha, alpha+0.8)
            )
            for ring, alpha in zip(rings, np.linspace(0, 0.2, len(rings)))
        ]
        draw_ring_sum_anims.append(FadeOut(self.radius_group))
        
        ring_sum = VGroup(rings, tex_mobs)
        ring_sum.rings = VGroup(*[r.target for r in rings])
        ring_sum.tex_mobs = tex_mobs
        
        return ring_sum, draw_ring_sum_anims

    def get_area_formula(self, R):
        formula = OldTex(
            "\\text{Area}", "&= \\frac{1}{2}", "b", "h",
            "\\\\ &=", "\\frac{1}{2}", "(%s)"%R, "(2\\pi \\cdot %s)"%R,
            "\\\\ &=", "\\pi ", "%s"%R, "^2"
            
        )
        formula.set_color_by_tex("b", GREEN, substring = False)
        formula.set_color_by_tex("h", RED, substring = False)
        formula.set_color_by_tex("%s"%R, GREEN)
        formula.set_color_by_tex("(2\\pi ", RED)
        formula.set_color_by_tex("(2\\pi ", RED)
        formula.scale(0.8)

        formula.top_line = VGroup(*formula[:4])
        formula.mid_line = VGroup(*formula[4:8])
        formula.bottom_line = VGroup(*formula[8:])
        return formula


class RecapCircleSolution(GraphRectangles, ReconfigurableScene):
    def setup(self):
        GraphRectangles.setup(self)
        ReconfigurableScene.setup(self)

    def construct(self):
        self.break_up_circle()
        self.show_sum()
        self.dr_indicates_spacing()
        self.smaller_dr()
        self.show_riemann_sum()
        self.limiting_riemann_sum()
        self.full_precision()

    def break_up_circle(self):
        self.remove(self.circle)
        rings = self.get_rings()
        rings.set_stroke(BLACK, 1)
        ring_sum, draw_ring_sum_anims = self.get_ring_sum(rings)

        hard_problem = OldTexText("Hard problem")
        down_arrow = OldTex("\\Downarrow")
        sum_words = OldTexText("Sum of many \\\\ small values")
        integral_condition = VGroup(hard_problem, down_arrow, sum_words)
        integral_condition.arrange(DOWN)
        integral_condition.scale(0.8)
        integral_condition.to_corner(UP+RIGHT)
        
        self.add(rings, self.radius_group)
        self.play(FadeIn(
            integral_condition, 
            lag_ratio = 0.5
        ))
        self.wait()
        self.play(*draw_ring_sum_anims)

        self.rings = rings
        self.integral_condition = integral_condition

    def show_sum(self):
        visible_rings = [ring for ring in self.rings if ring.get_fill_opacity() > 0]
        radii = self.dR*np.arange(len(visible_rings))
        radii[-1] = 3-self.dR

        radial_lines = VGroup()
        for ring in visible_rings:
            radius_line = Line(ORIGIN, ring.R*RIGHT, color = YELLOW)
            radius_line.rotate(np.pi/4)
            radius_line.shift(ring.get_center())
            radial_lines.add(radius_line)

        approximations = VGroup()
        for ring, radius in zip(visible_rings, radii):
            label = OldTex(
                "\\approx", "2\\pi", 
                "(%s)"%str(radius), "(%s)"%str(self.dR)
            )
            label[2].set_color(YELLOW)
            label[3].set_color(GREEN)
            label.scale(0.75)
            label.next_to(ring, RIGHT)
            approximations.add(label)
        approximations[-1].shift(UP+0.5*LEFT)
        area_label = OldTex("2\\pi", "r", "\\, dr")
        area_label.set_color_by_tex("r", YELLOW)
        area_label.set_color_by_tex("dr", GREEN)
        area_label.next_to(approximations, RIGHT, buff = 2*LARGE_BUFF)
        arrows = VGroup(*[
            Arrow(
                area_label.get_left(),
                approximation.get_right(),
                color = WHITE
            )
            for approximation in approximations
        ])

        self.play(Write(area_label))
        self.play(
            ShowCreation(arrows, lag_ratio = 0),
            FadeIn(radial_lines),
            *[
                ReplacementTransform(
                    area_label.copy(),
                    VGroup(*approximation[1:])
                )
                for approximation in approximations
            ]
        )
        self.wait()
        self.play(Write(VGroup(*[
            approximation[0]
            for approximation in approximations
        ])))
        self.wait()

        self.area_label = area_label
        self.area_arrows = arrows
        self.approximations = approximations

    def dr_indicates_spacing(self):
        r_ticks = VGroup(*[
            Line(
                self.coords_to_point(r, -self.tick_height),
                self.coords_to_point(r, self.tick_height),
                color = YELLOW
            )
            for r in np.arange(0, 3, self.dR)
        ])

        index = int(0.75*len(r_ticks))
        brace_ticks = VGroup(*r_ticks[index:index+2])
        dr_brace = Brace(brace_ticks, UP, buff = SMALL_BUFF)

        dr = self.area_label.get_part_by_tex("dr")
        dr_copy = dr.copy()
        circle = Circle().replace(dr)
        circle.scale(1.3)

        dr_num = self.approximations[0][-1]

        self.play(ShowCreation(circle))
        self.play(FadeOut(circle))
        self.play(ReplacementTransform(
            dr.copy(), dr_num,
            run_time = 2,
            path_arc = np.pi/2,
        ))
        self.wait()
        self.play(FadeIn(self.x_axis))
        self.play(Write(r_ticks, run_time = 1))
        self.wait()
        self.play(
            GrowFromCenter(dr_brace),
            dr_copy.next_to, dr_brace.copy(), UP
        )
        self.wait()

        self.r_ticks = r_ticks
        self.dr_brace_group = VGroup(dr_brace, dr_copy)

    def smaller_dr(self):
        self.transition_to_alt_config(dR = 0.05)

    def show_riemann_sum(self):
        graph = self.get_graph(lambda r : 2*np.pi*r)
        graph_label = self.get_graph_label(
            graph, "2\\pi r",
            x_val = 2.5,
            direction = UP+LEFT
        )
        rects = self.get_riemann_rectangles(
            graph,
            x_min = 0, 
            x_max = 3,
            dx = self.dR
        )

        self.play(
            Write(self.y_axis, run_time = 2),
            *list(map(FadeOut, [
                self.approximations,
                self.area_label,
                self.area_arrows,
                self.dr_brace_group,
                self.r_ticks,
            ]))
        )
        self.play(
            ReplacementTransform(
                self.rings.copy(), rects,
                run_time = 2,
                lag_ratio = 0.5
            ),
            Animation(self.x_axis),
        )
        self.play(ShowCreation(graph))
        self.play(Write(graph_label))
        self.wait()

        self.graph = graph
        self.graph_label = graph_label
        self.rects = rects

    def limiting_riemann_sum(self):
        thinner_rects_list = [
            self.get_riemann_rectangles(
                self.graph,
                x_min = 0, 
                x_max = 3,
                dx = 1./(10*2**n),
                stroke_width = 1./(2**n),
                start_color = self.rects[0].get_fill_color(),
                end_color = self.rects[-1].get_fill_color(),
            )
            for n in range(1, 4)
        ]

        for new_rects in thinner_rects_list:
            self.play(
                Transform(
                    self.rects, new_rects, 
                    lag_ratio = 0.5,
                    run_time = 2
                ),
                Animation(self.axes),
                Animation(self.graph),
            )
            self.wait()

    def full_precision(self):
        words = OldTexText("Area under \\\\ a graph")
        group = VGroup(OldTex("\\Downarrow"), words)
        group.arrange(DOWN)
        group.set_color(YELLOW)
        group.scale(0.8)
        group.next_to(self.integral_condition, DOWN)

        arc = Arc(start_angle = 2*np.pi/3, angle = 2*np.pi/3)
        arc.scale(2)
        arc.add_tip()
        # CHANGE: GL arc has no self-element in its submobject list: the tip is arc.submobjects[-1] (Cairo arc[1])
        arc.add(arc.submobjects[-1].copy().rotate(np.pi, RIGHT))
        arc_next_to_group = VGroup(
            self.integral_condition[0][0],
            words[0]
        )
        arc.set_height(
            arc_next_to_group.get_height()-MED_LARGE_BUFF
        )
        arc.next_to(arc_next_to_group, LEFT, SMALL_BUFF)

        self.play(Write(group))
        self.wait()
        self.play(ShowCreation(arc))
        self.wait()
