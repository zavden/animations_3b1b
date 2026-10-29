# ==============================================================================
# Scene:      IntroduceUnitCircleWithSine
# Source:     videos/_2017/eoc/chapter3.py (lines 2155-2332)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl IntroduceUnitCircleWithSine.py IntroduceUnitCircleWithSine -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class IntroduceUnitCircleWithSine(GraphScene):
    CONFIG = {
        "unit_length" : 2.5,
        "graph_origin" : ORIGIN,
        "x_axis_width" : 15,
        "y_axis_height" : 10,
        "x_min" : -3,
        "x_max" : 3,
        "y_min" : -2,
        "y_max" : 2,
        "x_labeled_nums" : [-2, -1, 1, 2],
        "y_labeled_nums" : [-1, 1],
        "x_tick_frequency" : 0.5,
        "y_tick_frequency" : 0.5,
        "circle_color" : BLUE,
        "example_radians" : 0.8,
        "rotations_per_second" : 0.25,
        "include_radial_line_dot" : True,
        "remove_angle_label" : True,
        "line_class" : DashedLine,
        "theta_label" : "= 0.8",
    }
    def construct(self):
        self.setup_axes()
        self.add_title()
        self.introduce_unit_circle()
        self.draw_example_radians()
        self.label_sine()
        self.walk_around_circle()

    def add_title(self):
        title = OldTex("f(\\theta) = \\sin(\\theta)")
        title.to_corner(UP+LEFT)
        self.add(title)
        self.title = title

    def introduce_unit_circle(self):
        circle = self.get_unit_circle()
        radial_line = Line(ORIGIN, self.unit_length*RIGHT)
        radial_line.set_color(RED)
        if self.include_radial_line_dot:
            dot = Dot()
            dot.move_to(radial_line.get_end())
            radial_line.add(dot)

        self.play(ShowCreation(radial_line))
        self.play(
            ShowCreation(circle),            
            Rotate(radial_line, 2*np.pi),
            run_time = 2,
        )
        self.wait()

        self.circle = circle
        self.radial_line = radial_line

    def draw_example_radians(self):
        circle = self.circle
        radial_line = self.radial_line

        line = Line(
            ORIGIN, self.example_radians*self.unit_length*UP,
            color = YELLOW,
        )
        line.shift(FRAME_X_RADIUS*RIGHT/3).to_edge(UP)
        line.insert_n_curves(10)
        line.make_smooth()

        arc = Arc(
            self.example_radians, radius = self.unit_length,
            color = line.get_color(),
        )
        arc_copy = arc.copy().set_color(WHITE)

        brace = Brace(line, RIGHT)
        brace_text = brace.get_text("$\\theta%s$"%self.theta_label)
        brace_text.set_color(line.get_color())
        theta_copy = brace_text[0].copy()

        self.play(
            GrowFromCenter(line),
            GrowFromCenter(brace),
        )
        self.play(Write(brace_text))
        self.wait()
        self.play(
            line.move_to, radial_line.get_end(), DOWN,
            FadeOut(brace)
        )
        self.play(ReplacementTransform(line, arc))
        self.wait()
        self.play(
            Rotate(radial_line, self.example_radians),
            ShowCreation(arc_copy)
        )
        self.wait()
        arc_copy.generate_target()
        arc_copy.target.scale(0.2)
        theta_copy.generate_target()
        theta_copy.target.next_to(
            arc_copy.target, RIGHT,
            aligned_edge = DOWN,
            buff = SMALL_BUFF
        )
        theta_copy.target.shift(SMALL_BUFF*UP)
        self.play(*list(map(MoveToTarget, [arc_copy, theta_copy])))
        self.wait()

        self.angle_label = VGroup(arc_copy, theta_copy)
        self.example_theta_equation = brace_text

    def label_sine(self):
        radial_line = self.radial_line

        drop_point = radial_line.get_end()[0]*RIGHT
        v_line = self.line_class(radial_line.get_end(), drop_point)
        brace = Brace(v_line, RIGHT)
        brace_text = brace.get_text("$\\sin(\\theta)$")
        brace_text[-2].set_color(YELLOW)

        self.play(ShowCreation(v_line))
        self.play(
            GrowFromCenter(brace),
            Write(brace_text)
        )
        self.wait()
        faders = [brace, brace_text, self.example_theta_equation]
        if self.remove_angle_label:
            faders += self.angle_label
        self.play(*list(map(FadeOut, faders)))

        self.v_line = v_line

    def walk_around_circle(self):
        radial_line = self.radial_line
        v_line = self.v_line

        def v_line_update(v_line):
            drop_point = radial_line.get_end()[0]*RIGHT
            v_line.put_start_and_end_on(
                radial_line.get_end(), drop_point
            )
            return v_line
        filler_arc = self.circle.copy()
        filler_arc.set_color(YELLOW)
        curr_arc_portion = self.example_radians/(2*np.pi)
        filler_portion = 1 - curr_arc_portion
        filler_arc.pointwise_become_partial(filler_arc, curr_arc_portion, 1)

        self.play(
            Rotate(radial_line, filler_portion*2*np.pi),
            ShowCreation(filler_arc),
            UpdateFromFunc(v_line, v_line_update),
            run_time = filler_portion/self.rotations_per_second,
            rate_func=linear,
        )
        for x in range(5):
            self.play(
                Rotate(radial_line, 2*np.pi),
                UpdateFromFunc(v_line, v_line_update),
                run_time = 1./self.rotations_per_second,
                rate_func=linear,
            )

    ##############

    def setup_axes(self):
        GraphScene.setup_axes(self)
        VGroup(*self.x_axis.numbers[:2]).shift(MED_SMALL_BUFF*LEFT)
        VGroup(*self.x_axis.numbers[2:]).shift(SMALL_BUFF*RIGHT)
        self.y_axis.numbers[0].shift(MED_SMALL_BUFF*DOWN)
        self.y_axis.numbers[1].shift(MED_SMALL_BUFF*UP)

    def get_unit_circle(self):
        return Circle(
            radius = self.unit_length,
            color = self.circle_color,
        )
