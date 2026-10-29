# ==============================================================================
# Scene:      Pendulum
# Source:     videos/_2017/eoc/chapter10.py (lines 163-462)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl Pendulum.py Pendulum -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class Pendulum(ReconfigurableScene):
    CONFIG = {
        "anchor_point" : 3*UP + 4*LEFT,
        "radius" : 4,
        "weight_radius" : 0.2,
        "angle" : np.pi/6,
        "approx_tex" : [
            "\\approx 1 - ", "{\\theta", "^2", "\\over", "2}"
        ],
        "leave_original_cosine" : False,
        "perform_substitution" : True,
    }
    def construct(self):
        self.draw_pendulum()
        self.show_oscillation()
        self.show_height()
        self.get_angry_at_cosine()
        self.substitute_approximation()
        self.show_confusion()

    def draw_pendulum(self):
        pendulum = self.get_pendulum()
        ceiling = self.get_ceiling()

        self.add(ceiling)
        self.play(ShowCreation(pendulum.line))
        self.play(DrawBorderThenFill(pendulum.weight, run_time = 1))

        self.pendulum = pendulum

    def show_oscillation(self):
        trajectory_dots = self.get_trajectory_dots()
        kwargs = self.get_swing_kwargs()

        self.play(
            ShowCreation(
                trajectory_dots,
                rate_func=linear,
                run_time = kwargs["run_time"]
            ),
            Rotate(self.pendulum, -2*self.angle, **kwargs),
        )
        for m in 2, -2, 2:
            self.play(Rotate(self.pendulum, m*self.angle, **kwargs))
        self.wait()

    def show_height(self):
        v_line = self.get_v_line()
        h_line = self.get_h_line()
        radius_brace = self.get_radius_brace()
        height_brace = self.get_height_brace()
        height_tex = self.get_height_brace_tex(height_brace)
        arc, theta = self.get_arc_and_theta()

        height_tex_R = height_tex.get_part_by_tex("R")
        height_tex_theta = height_tex.get_part_by_tex("\\theta")
        to_write = VGroup(*[
            part
            for part in height_tex
            if part not in [height_tex_R, height_tex_theta]
        ])

        self.play(
            ShowCreation(h_line),
            GrowFromCenter(height_brace)
        )
        self.play(
            ShowCreation(v_line),
            ShowCreation(arc),
            Write(theta),
        )
        self.play(
            GrowFromCenter(radius_brace)
        )
        self.wait(2)
        self.play(
            Write(to_write),
            ReplacementTransform(
                radius_brace[-1].copy(),
                height_tex_R
            ),
            ReplacementTransform(
                theta.copy(),
                height_tex_theta
            ),
            run_time = 2
        )
        self.wait(2)

        self.arc = arc
        self.theta = theta
        self.height_tex_R = height_tex_R
        self.cosine = VGroup(*[
            height_tex.get_part_by_tex(tex)
            for tex in ("cos", "theta", ")")
        ])
        self.one_minus = VGroup(*[
            height_tex.get_part_by_tex(tex)
            for tex in ("\\big(1-", "\\big)")
        ])

    def get_angry_at_cosine(self):
        cosine = self.cosine
        morty = Mortimer()
        morty.to_corner(DOWN+RIGHT)
        cosine.generate_target()
        cosine.save_state()
        cosine.target.next_to(morty, UP)
        if self.leave_original_cosine:
            cosine_copy = cosine.copy()
            self.add(cosine_copy)
            self.one_minus.add(cosine_copy)

        self.play(FadeIn(morty))
        self.play(
            MoveToTarget(cosine),
            morty.change, "angry", cosine.target,
        )
        self.wait()
        self.play(Blink(morty))
        self.wait()

        self.morty = morty

    def substitute_approximation(self):
        morty = self.morty
        cosine = self.cosine
        cosine.generate_target()
        cosine_approx = self.get_cosine_approx()
        cosine_approx.next_to(cosine, UP+RIGHT)
        cosine_approx.to_edge(RIGHT)
        cosine.target.next_to(
            cosine_approx, LEFT,
            align_using_submobjects = True
        )
        kwargs = self.get_swing_kwargs()

        self.play(
            FadeIn(
                cosine_approx,
                run_time = 2,
                lag_ratio = 0.5
            ),
            MoveToTarget(cosine),
            morty.change, "pondering", cosine_approx
        )
        self.wait()
        if not self.perform_substitution:
            return
        self.play(
            ApplyMethod(
                cosine_approx.theta_squared_over_two.copy().next_to,
                self.height_tex_R,
                run_time = 2,
            ),
            FadeOut(self.one_minus),
            morty.look_at, self.height_tex_R,
        )
        self.play(morty.change, "thinking", self.height_tex_R)
        self.transition_to_alt_config(
            angle = np.pi/12,
            transformation_kwargs = {"run_time" : 2},
        )

    def show_confusion(self):
        randy = Randolph(color = BLUE_C)
        randy.scale(0.8)
        randy.next_to(self.cosine, DOWN+LEFT)
        randy.to_edge(DOWN)

        self.play(FadeIn(randy))
        self.play(
            randy.change, "confused", self.cosine
        )
        self.play(randy.look_at, self.height_tex_R)
        self.wait()
        self.play(randy.look_at, self.cosine)
        self.play(Blink(randy))
        self.wait()

    #######

    def get_pendulum(self):
        line = Line(
            self.anchor_point,
            self.anchor_point + self.radius*DOWN,
            color = WHITE
        )
        weight = Circle(
            radius = self.weight_radius,
            fill_color = GREY,
            fill_opacity = 1,
            stroke_width = 0,
        )
        weight.move_to(line.get_end())
        result = VGroup(line, weight)
        result.rotate(
            self.angle, 
            about_point = self.anchor_point
        )
        result.line = line
        result.weight = weight

        return result

    def get_ceiling(self):
        line = Line(LEFT, RIGHT, color = GREY)
        line.scale(FRAME_X_RADIUS)
        line.move_to(self.anchor_point[1]*UP)
        return line

    def get_trajectory_dots(self, n_dots = 40, color = YELLOW):
        arc_angle = np.pi/6
        proportions = self.swing_rate_func(
            np.linspace(0, 1, n_dots)
        )
        angles = -2*arc_angle*proportions
        angle_to_point = lambda a : np.cos(a)*RIGHT + np.sin(a)*UP
        dots = VGroup(*[
            # Line(*map(angle_to_point, pair))
            Dot(angle_to_point(angle), radius = 0.005)
            for angle in angles
        ])
            
        dots.set_color(color)
        dots.scale(self.radius)
        dots.rotate(-np.pi/2 + arc_angle)
        dots.shift(self.anchor_point)
        return dots

    def get_v_line(self):
        return DashedLine(
            self.anchor_point, 
            self.anchor_point + self.radius*DOWN,
            color = WHITE
        )

    def get_h_line(self, color = BLUE):
        start = self.anchor_point + self.radius*DOWN
        end = start + self.radius*np.sin(self.angle)*RIGHT

        return Line(start, end, color = color)

    def get_radius_brace(self):
        v_line = self.get_v_line()
        brace = Brace(v_line, RIGHT)
        brace.rotate(self.angle, about_point = self.anchor_point)
        brace.add(brace.get_text("$R$", buff = SMALL_BUFF))
        return brace

    def get_height_brace(self):
        h_line = self.get_h_line()
        height = (1 - np.cos(self.angle))*self.radius
        line = Line(
            h_line.get_end(),
            h_line.get_end() + height*UP,
        )
        brace = Brace(line, RIGHT)
        return brace

    def get_height_brace_tex(self, brace):
        tex_mob = OldTex(
            "R", "\\big(1-", "\\cos(", "\\theta", ")", "\\big)"
        )
        tex_mob.set_color_by_tex("theta", YELLOW)
        tex_mob.next_to(brace, RIGHT)
        return tex_mob

    def get_arc_and_theta(self):
        arc = Arc(
            start_angle = -np.pi/2,
            angle = self.angle,
            color = YELLOW
        )
        theta = OldTex("\\theta")
        theta.set_color(YELLOW)
        theta.next_to(
            arc.point_from_proportion(0.5), 
            DOWN, SMALL_BUFF
        )
        for mob in arc, theta:
            mob.shift(self.anchor_point)
        return arc, theta

    def get_cosine_approx(self):
        approx = OldTex(*self.approx_tex)
        approx.set_color_by_tex("theta", YELLOW)
        approx.theta_squared_over_two = VGroup(*approx[1:5])

        return approx

    def get_swing_kwargs(self):
        return {
            "about_point" : self.anchor_point,
            "run_time" : 1.7,
            "rate_func" : self.swing_rate_func,
        }

    def swing_rate_func(self, t):
        return (1-np.cos(np.pi*t))/2.0
