# ==============================================================================
# Scene:      FakeDiagram
# Source:     videos/_2017/eoc/chapter5.py (lines 594-692)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl FakeDiagram.py FakeDiagram -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - in Cairo Scene.__init__ ran construct(); GL needs cairo_nested_scene(Class, **kw) to build a scene inside another
# ==============================================================================

from manim_imports_ext import *

class FakeDiagram(TeacherStudentsScene):
    def construct(self):
        # CHANGE: in Cairo Scene.__init__ ran construct(); GL needs cairo_nested_scene(Class, **kw) to build a scene inside another
        gs = cairo_nested_scene(GraphScene,skip_animations = True)
        gs.setup_axes()
        background_graph, foreground_graph = graphs = VGroup(*[
            gs.get_graph(
                lambda t : np.log(2)*2**t,
                x_min = -8,
                x_max = 2 + dx
            )
            for dx in (0.25, 0)
        ])
        for graph in graphs:
            end_point = graph.get_points()[-1]
            axis_point = end_point[0]*RIGHT + gs.graph_origin[1]*UP
            for alpha in np.linspace(0, 1, 20):
                point = interpolate(axis_point, graph.get_points()[0], alpha)
                graph.add_line_to(point)
            graph.set_stroke(width = 1)
            graph.set_fill(opacity = 1)
            graph.set_color(BLUE_D)
        background_graph.set_color(YELLOW)
        background_graph.set_stroke(width = 0.5)

        graphs.next_to(self.teacher, UP+LEFT, LARGE_BUFF)
        two_to_t = OldTex("2^t")
        two_to_t.next_to(
            foreground_graph.get_corner(DOWN+RIGHT), UP+LEFT
        )
        corner_line = Line(*[
            graph.get_corner(DOWN+RIGHT)
            for graph in graphs
        ])
        dt_brace = Brace(corner_line, DOWN, buff = SMALL_BUFF)
        dt = dt_brace.get_text("$dt$")

        side_brace = Brace(graphs, RIGHT, buff = SMALL_BUFF)
        deriv = side_brace.get_text("$\\frac{d(2^t)}{dt}$")

        circle = Circle(color = RED)
        circle.replace(deriv, stretch = True)
        circle.scale(1.5)

        words = OldTexText("Not a real explanation")
        words.to_edge(UP)
        arrow = Arrow(words.get_bottom(), two_to_t.get_corner(UP+LEFT))
        arrow.set_color(WHITE)

        diagram = VGroup(
            graphs, two_to_t, dt_brace, dt, 
            side_brace, deriv, circle,
            words, arrow
        )

        self.play(self.teacher.change_mode, "raise_right_hand")
        self.play(
            Animation(VectorizedPoint(graphs.get_right())),
            DrawBorderThenFill(foreground_graph),
            Write(two_to_t)
        )
        self.wait()
        self.play(
            ReplacementTransform(
                foreground_graph.copy(),
                background_graph,
            ),
            Animation(foreground_graph),
            Animation(two_to_t),
            GrowFromCenter(dt_brace),
            Write(dt)
        )
        self.play(GrowFromCenter(side_brace))
        self.play(Write(deriv, run_time = 2))
        self.wait()

        self.play(
            ShowCreation(circle),
            self.teacher.change_mode, "hooray"
        )
        self.play_student_changes(*["confused"]*3)
        self.play(
            Write(words),
            ShowCreation(arrow),
            self.teacher.change_mode, "shruggie"
        )
        self.wait(3)
        self.play(
            FadeOut(diagram),
            *[
                ApplyMethod(pi.change_mode, "plain")
                for pi in self.get_pi_creatures()
            ]
        )
        self.teacher_says(
            "More numerical \\\\ than visual..."
        )
        self.wait(2)

        self.diagram = diagram
