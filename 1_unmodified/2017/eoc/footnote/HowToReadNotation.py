# ==============================================================================
# Scene:      HowToReadNotation
# Source:     videos/_2017/eoc/footnote.py (lines 399-648)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl HowToReadNotation.py HowToReadNotation -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class HowToReadNotation(GraphScene, ReconfigurableScene):
    CONFIG = {
        "x_max" : 5,
        "dx" : 0.4,
        "x" : 2,
        "graph_origin" : 2.5*DOWN + 5*LEFT,
    }
    def setup(self):
        for base in self.__class__.__bases__:
            base.setup(self)

    def construct(self):
        self.force_skipping()

        self.add_graph()
        self.take_two_steps()
        self.change_step_size()
        self.show_dfs()
        self.show_ddf()

        self.revert_to_original_skipping_status()
        self.show_proportionality_to_dx_squared()
        return

        self.write_second_derivative()

    def add_graph(self):
        self.setup_axes()
        graph = self.get_graph(lambda x : x**2)
        graph_label = self.get_graph_label(
            graph, "f(x)", 
            direction = LEFT,
            x_val = 3.3
        )
        self.add(graph, graph_label)

        self.graph = graph

    def take_two_steps(self):
        v_lines = [
            self.get_vertical_line_to_graph(
                self.x + i*self.dx, self.graph,
                line_class = DashedLine,
                color = WHITE
            )
            for i in range(3)
        ]
        braces = [
            Brace(VGroup(*v_lines[i:i+2]), buff = 0)
            for i in range(2)
        ]
        for brace in braces:
            brace.dx = OldTex("dx")
            max_width = 0.7*brace.get_width()
            if brace.dx.get_width() > max_width:
                brace.dx.set_width(max_width)
            brace.dx.next_to(brace, DOWN, SMALL_BUFF)

        self.play(ShowCreation(v_lines[0]))
        self.wait()
        for brace, line in zip(braces, v_lines[1:]):
            self.play(
                ReplacementTransform(
                    VectorizedPoint(brace.get_corner(UP+LEFT)),
                    brace,
                ),
                Write(brace.dx, run_time = 1),
            )
            self.play(ShowCreation(line))
        self.wait()

        self.v_lines = v_lines
        self.braces = braces

    def change_step_size(self):
        self.transition_to_alt_config(dx = 0.6)
        self.transition_to_alt_config(dx = 0.01, run_time = 3)

    def show_dfs(self):
        dx_lines = VGroup()
        df_lines = VGroup()
        df_dx_groups = VGroup()
        df_labels = VGroup()
        for i, v_line1, v_line2 in zip(it.count(1), self.v_lines, self.v_lines[1:]):
            dx_line = Line(
                v_line1.get_bottom(),
                v_line2.get_bottom(),
                color = GREEN
            )
            dx_line.move_to(v_line1.get_top(), LEFT)
            dx_lines.add(dx_line)

            df_line = Line(
                dx_line.get_right(),
                v_line2.get_top(),
                color = YELLOW
            )
            df_lines.add(df_line)
            df_label = OldTex("df_%d"%i)
            df_label.set_color(YELLOW)
            df_label.scale(0.8)
            df_label.next_to(df_line.get_center(), UP+LEFT, MED_LARGE_BUFF)
            df_arrow = Arrow(
                df_label.get_bottom(),
                df_line.get_center(),
                buff = SMALL_BUFF,
            )
            df_line.label = df_label
            df_line.arrow = df_arrow
            df_labels.add(df_label)

            df_dx_groups.add(VGroup(df_line, dx_line))

        for brace, dx_line, df_line in zip(self.braces, dx_lines, df_lines):
            self.play(
                VGroup(brace, brace.dx).next_to,
                dx_line, DOWN, SMALL_BUFF,
                FadeIn(dx_line),
            )
            self.play(ShowCreation(df_line))
            self.play(
                ShowCreation(df_line.arrow),
                Write(df_line.label)
            )
            self.wait(2)

        self.df_dx_groups = df_dx_groups
        self.df_labels = df_labels

    def show_ddf(self):
        df_dx_groups = self.df_dx_groups.copy()
        df_dx_groups.generate_target()
        df_dx_groups.target.arrange(
            RIGHT, 
            buff = MED_LARGE_BUFF,
            aligned_edge = DOWN
        )
        df_dx_groups.target.next_to(
            self.df_dx_groups, RIGHT, 
            buff = 3,
            aligned_edge = DOWN
        )

        df_labels = self.df_labels.copy()
        df_labels.generate_target()
        h_lines = VGroup()
        for group, label in zip(df_dx_groups.target, df_labels.target):
            label.next_to(group.get_right(), LEFT, SMALL_BUFF)
            width = df_dx_groups.target.get_width() + MED_SMALL_BUFF
            h_line = DashedLine(ORIGIN, width*RIGHT)
            h_line.move_to(
                group.get_corner(UP+RIGHT)[1]*UP + \
                df_dx_groups.target.get_right()[0]*RIGHT,
                RIGHT
            )
            h_lines.add(h_line)
            max_height = 0.8*group.get_height()
            if label.get_height() > max_height:
                label.set_height(max_height)


        ddf_brace = Brace(h_lines, LEFT, buff = SMALL_BUFF)
        ddf = ddf_brace.get_tex("d(df)", buff = SMALL_BUFF)
        ddf.scale(
            df_labels[0].get_height()/ddf.get_height(), 
            about_point = ddf.get_right()
        )
        ddf.set_color(MAROON_B)

        self.play(
            *list(map(MoveToTarget, [df_dx_groups, df_labels])),
            run_time = 2
        )
        self.play(ShowCreation(h_lines, run_time = 2))
        self.play(GrowFromCenter(ddf_brace))
        self.play(Write(ddf))
        self.wait(2)

        self.ddf = ddf

    def show_proportionality_to_dx_squared(self):
        ddf = self.ddf.copy()
        ddf.generate_target()
        ddf.target.next_to(self.ddf, UP, LARGE_BUFF)
        rhs = OldTex(
            "\\approx", "(\\text{Some constant})", "(dx)^2"
        )
        rhs.scale(0.8)
        rhs.next_to(ddf.target, RIGHT)

        example_dx = OldTex(
            "dx = 0.01 \\Rightarrow (dx)^2 = 0.0001"
        )
        example_dx.scale(0.8)
        example_dx.to_corner(UP+RIGHT)

        self.play(MoveToTarget(ddf))
        self.play(Write(rhs))
        self.wait()
        self.play(Write(example_dx))
        self.wait(2)
        self.play(FadeOut(example_dx))

        self.ddf = ddf
        self.dx_squared = rhs.get_part_by_tex("dx")

    def write_second_derivative(self):
        ddf_over_dx_squared = OldTex(
            "{d(df)", "\\over", "(dx)^2}"
        )
        ddf_over_dx_squared.scale(0.8)
        ddf_over_dx_squared.move_to(self.ddf, RIGHT)
        ddf_over_dx_squared.set_color_by_tex("df", self.ddf.get_color())
        parens = VGroup(
            ddf_over_dx_squared[0][1],
            ddf_over_dx_squared[0][4],
            ddf_over_dx_squared[2][0],
            ddf_over_dx_squared[2][3],
        )

        right_shifter = ddf_over_dx_squared[0][0]
        left_shifter = ddf_over_dx_squared[2][4]

        exp_two = OldTex("2")
        exp_two.set_color(self.ddf.get_color())
        exp_two.scale(0.5)
        exp_two.move_to(right_shifter.get_corner(UP+RIGHT), LEFT)
        exp_two.shift(MED_SMALL_BUFF*RIGHT)
        pre_exp_two = VGroup(ddf_over_dx_squared[0][2])

        self.play(
            Write(ddf_over_dx_squared.get_part_by_tex("over")),
            *[
                ReplacementTransform(
                    mob, 
                    ddf_over_dx_squared.get_part_by_tex(tex),
                    path_arc = -np.pi/2,                    
                )
                for mob, tex in [(self.ddf, "df"), (self.dx_squared, "dx")]
            ]
        )
        self.wait(2)
        self.play(FadeOut(parens))
        self.play(
            left_shifter.shift, 0.2*LEFT,
            right_shifter.shift, 0.2*RIGHT,
            ReplacementTransform(pre_exp_two, exp_two),
            ddf_over_dx_squared.get_part_by_tex("over").scale, 0.8
        )
        self.wait(2)
