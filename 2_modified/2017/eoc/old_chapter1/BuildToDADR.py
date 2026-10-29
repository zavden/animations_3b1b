# ==============================================================================
# Scene:      BuildToDADR
# Source:     videos/_2017/eoc/old_chapter1.py (lines 787-1154)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl BuildToDADR.py BuildToDADR -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Python 2 integer division: np.linspace needs an int
#   - GL get_bubble(content, bubble_type=...) builds the bubble around its content (Cairo: get_bubble(SpeechBubble), .write, .resize_to_content, .pin_to)
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


class BuildToDADR(CircleScene):
    CONFIG = {
        "include_pi_creature" : True,
    }
    def construct(self):
        self.outer_ring = self.increase_radius()
        self.write_initial_terms()
        self.show_fractions()
        self.transition_to_dR()
        self.elaborate_on_d()
        self.not_infinitely_small()

    def create_pi_creature(self):
        morty = Mortimer()
        morty.flip()
        morty.to_corner(DOWN+LEFT)
        return morty

    def write_initial_terms(self):
        change = OldTexText("Change in area")
        change.set_color(GREEN_B)
        equals, two_pi_R, dR, plus, pi, dR2, squared = rhs = OldTex(
            "=", "2 \\pi R", "(0.1)", "+", "\\pi", "(0.1)", "^2"
        )
        VGroup(dR, dR2).set_color(self.dR_color)
        change.next_to(self.circle, buff = LARGE_BUFF)
        rhs.next_to(change)

        circum_brace = Brace(two_pi_R, UP)
        circum_text = circum_brace.get_text("Circumference")
        error_brace = Brace(VGroup(pi, squared), UP)
        error_text = error_brace.get_text("Error")
        error_text.set_color(RED)

        self.play(
            Write(change, run_time = 1),
            self.pi_creature.change_mode, "pondering",
        )
        self.wait()
        self.play(*it.chain(
            list(map(Write, [equals, two_pi_R, dR])),
            list(map(FadeIn, [circum_text, circum_brace]))
        ))
        self.wait()
        self.play(*it.chain(
            list(map(Write, [plus, pi, dR2, squared])),
            list(map(FadeIn, [error_brace, error_text]))
        ))
        self.wait(2)
        self.change = change
        self.circum_term = VGroup(two_pi_R, dR)
        self.circum_term.label = VGroup(circum_brace, circum_text)
        self.error_term = VGroup(pi, dR2, squared)
        self.error_term.label = VGroup(error_brace, error_text)        
        self.equals = equals
        self.plus = plus

    def show_fractions(self):
        terms = [self.change, self.circum_term, self.error_term]
        for term in terms:
            term.frac_line = OldTex("\\frac{\\quad}{\\quad}")
            term.frac_line.stretch_to_fit_width(term.get_width())
            term.frac_line.next_to(term, DOWN, buff = SMALL_BUFF)
            term.denom = OldTex("(0.1)")
            term.denom.next_to(term.frac_line, DOWN, buff = SMALL_BUFF)
            term.denom.set_color(self.dR_color)
            term.denom.save_state()
            term.denom.replace(self.nudge_label)

        self.equals.generate_target()
        self.equals.target.next_to(self.change.frac_line, RIGHT)
        self.plus.generate_target()
        self.plus.target.next_to(self.circum_term.frac_line, RIGHT)

        self.play(*it.chain(
            [Write(term.frac_line) for term in terms],
            list(map(MoveToTarget, [self.equals, self.plus]))
        ))
        self.play(*[term.denom.restore for term in terms])
        self.wait(2)
        self.play(
            self.outer_ring.set_color, YELLOW,
            rate_func = there_and_back
        )
        self.play(
            self.nudge_label.scale, 2,
            rate_func = there_and_back
        )
        self.wait(2)
        canceleres = VGroup(self.circum_term[1], self.circum_term.denom)
        self.play(canceleres.set_color, RED)
        self.play(FadeOut(canceleres))
        self.remove(self.circum_term)
        self.play(
            self.circum_term[0].move_to, self.circum_term.frac_line, LEFT,
            self.circum_term[0].shift, 0.1*UP,
            FadeOut(self.circum_term.frac_line),
            MaintainPositionRelativeTo(
                self.circum_term.label,
                self.circum_term[0]
            )
        )
        self.circum_term = self.circum_term[0]
        self.wait(2)
        self.play(
            FadeOut(self.error_term[-1]),
            FadeOut(self.error_term.denom)
        )
        self.error_term.remove(self.error_term[-1])
        self.play(
            self.error_term.move_to, self.error_term.frac_line,
            self.error_term.shift, 0.3*LEFT + 0.15*UP,
            FadeOut(self.error_term.frac_line),
            self.plus.shift, 0.7*LEFT + 0.1*UP,
            MaintainPositionRelativeTo(
                self.error_term.label,
                self.error_term
            )
        )
        self.wait()

    def transition_to_dR(self):
        dRs = VGroup(
            self.nudge_label, 
            self.change.denom,
            self.error_term[1],
        )
        error_brace, error_text = self.error_term.label
        for s, width in ("(0.01)", 0.05), ("(0.001)", 0.03), ("dR", 0.03):
            new_dRs = VGroup(*[
                OldTex(s).move_to(mob, LEFT)
                for mob in dRs
            ])
            new_dRs.set_color(self.dR_color)
            new_outer_ring = self.get_ring(self.radius, width)
            new_nudge_line = self.nudge_line.copy()
            new_nudge_line.set_width(width)
            new_nudge_line.move_to(self.nudge_line, LEFT)
            error_brace.target = error_brace.copy()
            error_brace.target.stretch_to_fit_width(
                VGroup(self.error_term[0], new_dRs[-1]).get_width()
            )
            error_brace.target.move_to(error_brace, LEFT)
            self.play(
                MoveToTarget(error_brace),
                Transform(self.outer_ring, new_outer_ring),
                Transform(self.nudge_line, new_nudge_line),
                *[
                    Transform(*pair)
                    for pair in zip(dRs, new_dRs)
                ]
            )
            self.wait()
            if s == "(0.001)":
                self.plus.generate_target()
                self.plus.target.next_to(self.circum_term)
                self.error_term.generate_target()
                self.error_term.target.next_to(self.plus.target)
                error_brace.target = Brace(self.error_term.target)
                error_text.target = error_brace.target.get_text("Truly tiny")
                error_text.target.set_color(error_text.get_color())
                self.play(*list(map(MoveToTarget, [
                    error_brace, error_text, self.plus, self.error_term
                ])))
                self.wait()

        difference_text = OldTexText(
            "``Tiny " , "d", "ifference in ", "$R$", "''",
            arg_separator = ""

        )
        difference_text.set_color_by_tex("d", self.dR_color)
        difference_text.next_to(self.pi_creature, UP+RIGHT)
        difference_arrow = Arrow(difference_text, self.change.denom)
        self.play(
            Write(difference_text, run_time = 2),
            ShowCreation(difference_arrow),
            self.pi_creature.change_mode, "speaking"
        )
        self.wait()

        dA = OldTex("dA")
        dA.set_color(self.change.get_color())
        frac_line = self.change.frac_line
        frac_line.generate_target()
        frac_line.target.stretch_to_fit_width(dA.get_width())
        frac_line.target.next_to(self.equals, LEFT)
        dA.next_to(frac_line.target, UP, 2*SMALL_BUFF)
        self.change.denom.generate_target()
        self.change.denom.target.next_to(frac_line.target, DOWN, 2*SMALL_BUFF)
        A = OldTex("A").replace(difference_text[3])
        difference_arrow.target = Arrow(difference_text, dA.get_left())
        self.play(
            Transform(self.change, dA),
            MoveToTarget(frac_line),
            MoveToTarget(self.change.denom),
            Transform(difference_text[3], A),
            difference_text[1].set_color, dA.get_color(),
            MoveToTarget(difference_arrow),
        )
        self.wait(2)
        self.play(*list(map(FadeOut, [difference_text, difference_arrow])))

    def elaborate_on_d(self):
        arc = Arc(-np.pi, start_angle = -np.pi/2)
        arc.set_height(
            self.change.get_center()[1]-self.change.denom.get_center()[1]
        )
        arc.next_to(self.change.frac_line, LEFT)
        arc.add_tip()

        self.play(
            ShowCreation(arc),
            self.pi_creature.change_mode, "sassy"
        )
        self.wait()
        self.play(self.pi_creature.shrug)
        self.play(FadeOut(arc))
        self.wait()

        d = OldTexText("``$d$''")
        arrow = OldTex("\\Rightarrow")
        arrow.next_to(d)
        ignore_error = OldTexText("Ignore error")
        d_group = VGroup(d, arrow, ignore_error)
        d_group.arrange()
        d_group.next_to(
            self.pi_creature.get_corner(UP+RIGHT), 
            buff = LARGE_BUFF
        )
        error_group = VGroup(
            self.plus, self.error_term, self.error_term.label
        )

        self.play(
            Write(d),
            self.pi_creature.change_mode, "speaking"
        )
        self.play(*list(map(Write, [arrow, ignore_error])))
        self.play(error_group.fade, 0.8)
        self.wait(2)
        equality_brace = Brace(VGroup(self.change.denom, self.circum_term))
        equal_word = equality_brace.get_text("Equality")
        VGroup(equality_brace, equal_word).set_color(BLUE)
        self.play(
            GrowFromCenter(equality_brace),
            Write(equal_word, run_time = 1)
        )
        self.wait(2)
        self.play(*list(map(FadeOut, [equality_brace, equal_word])))

        less_wrong_philosophy = OldTexText("``Less wrong'' philosophy")
        less_wrong_philosophy.move_to(ignore_error, LEFT)
        self.play(Transform(ignore_error, less_wrong_philosophy))
        self.wait()

        big_dR = 0.3
        big_outer_ring = self.get_ring(self.radius, big_dR)
        big_nudge_line = self.nudge_line.copy()
        big_nudge_line.stretch_to_fit_width(big_dR)
        big_nudge_line.move_to(self.nudge_line, LEFT)
        new_nudge_arrow = Arrow(self.nudge_label, big_nudge_line, buff = SMALL_BUFF)
        self.outer_ring.save_state()
        self.nudge_line.save_state()
        self.nudge_arrow.save_state()
        self.play(
            Transform(self.outer_ring, big_outer_ring),
            Transform(self.nudge_line, big_nudge_line),
            Transform(self.nudge_arrow, new_nudge_arrow),
        )
        self.play(
            *[
                mob.restore 
                for mob in [
                    self.outer_ring,
                    self.nudge_line,
                    self.nudge_arrow,
                ]
            ],
            rate_func=linear,
            run_time = 7
        )
        self.play(self.pi_creature.change_mode, "hooray")
        self.less_wrong_philosophy = VGroup(
            d, arrow, ignore_error
        )

    def not_infinitely_small(self):
        randy = Randolph().flip()
        randy.scale(0.7)
        randy.to_corner(DOWN+RIGHT)
        bubble = SpeechBubble()
        bubble.write("$dR$ is infinitely small")
        bubble.resize_to_content()
        bubble.stretch(0.7, 1)
        bubble.pin_to(randy)
        bubble.set_fill(BLACK, opacity = 1)
        bubble.add_content(bubble.content)
        self.play(FadeIn(randy))
        self.play(
            randy.change_mode, "speaking",
            ShowCreation(bubble),
            Write(bubble.content),
            self.pi_creature.change_mode, "confused"
        )
        self.wait()

        to_infs = [self.change, self.change.denom, self.nudge_label]
        for mob in to_infs:
            mob.save_state()
            mob.inf = OldTex("1/\\infty")
            mob.inf.set_color(mob.get_color())
            mob.inf.move_to(mob)
        self.play(*[
            Transform(mob, mob.inf)
            for mob in to_infs
        ])
        self.wait()
        self.play(self.pi_creature.change_mode, "pleading")
        self.wait()
        self.play(*it.chain(
            [mob.restore for mob in to_infs],
            list(map(FadeOut, [bubble, bubble.content])),
            [randy.change_mode, "erm"],
            [self.pi_creature.change_mode, "happy"],
        ))
        for n in range(7):
            target = OldTex("0.%s1"%("0"*n))
            target.set_color(self.nudge_label.get_color())
            target.move_to(self.nudge_label, LEFT)
            self.outer_ring.target = self.get_ring(self.radius, 0.1/(n+1))
            self.nudge_line.get_center = self.nudge_line.get_left
            self.play(
                Transform(self.nudge_label, target),
                MoveToTarget(self.outer_ring),
                self.nudge_line.stretch_to_fit_width, 0.1/(n+1)
            )
        self.wait()
        bubble.write("Wrong!")
        bubble.resize_to_content()
        bubble.stretch(0.7, 1)
        bubble.pin_to(randy)
        bubble.add_content(bubble.content)
        self.play(
            FadeIn(bubble),
            Write(bubble.content, run_time = 1),
            randy.change_mode, "angry",
        )
        self.play(randy.set_color, RED)
        self.play(self.pi_creature.change_mode, "guilty")
        self.wait()

        # CHANGE: GL get_bubble(content, bubble_type=...) builds the bubble around its content (Cairo: get_bubble(SpeechBubble), .write, .resize_to_content, .pin_to)
        new_bubble = self.pi_creature.get_bubble("But it gets \\\\ less wrong!", bubble_type = SpeechBubble)
        new_bubble.set_fill(BLACK, opacity = 0.8)

        self.play(
            FadeOut(bubble),
            FadeOut(bubble.content),
            ShowCreation(new_bubble),
            Write(new_bubble.content),
            randy.change_mode, "erm",
            randy.set_color, BLUE_E,
            self.pi_creature.change_mode, "shruggie"
        )
        self.wait(2)
