# ==============================================================================
# Scene:      RefreshOnDerivativeDefinition
# Source:     videos/_2017/eoc/chapter7.py (lines 172-333)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl RefreshOnDerivativeDefinition.py RefreshOnDerivativeDefinition -w -m --fps 15
# ==============================================================================

# -*- coding: utf-8 -*-
from manim_imports_ext import *

class RefreshOnDerivativeDefinition(GraphScene):
    CONFIG = {
        "start_x" : 2,
        "start_dx" : 0.7,
        "df_color" : YELLOW,
        "dx_color" : GREEN,
        "secant_line_color" : MAROON_B,
    }
    def construct(self):
        self.setup_axes()
        def func(x):
            u = 0.3*x - 1.5
            return -u**3 + 5*u + 7
        graph = self.get_graph(func)
        graph_label = self.get_graph_label(graph)
        start_x_v_line, nudged_x_v_line = [
            self.get_vertical_line_to_graph(
                self.start_x + nudge, graph, 
                line_class = DashedLine,
                color = RED
            )
            for nudge in (0, self.start_dx)
        ]
        nudged_x_v_line.save_state()
        ss_group = self.get_secant_slope_group(
            self.start_x, graph,
            dx = self.start_dx,
            dx_label = "dx",
            df_label = "df",
            df_line_color = self.df_color,
            dx_line_color = self.dx_color,
            secant_line_color = self.secant_line_color,
        )
        derivative = OldTex(
            "{df", "\\over \\,", "dx}", "(", str(self.start_x), ")"
        )
        derivative.set_color_by_tex("df", self.df_color)
        derivative.set_color_by_tex("dx", self.dx_color)
        derivative.set_color_by_tex(str(self.start_x), RED)
        df = derivative.get_part_by_tex("df")
        dx = derivative.get_part_by_tex("dx")
        input_x = derivative.get_part_by_tex(str(self.start_x))
        derivative.move_to(self.coords_to_point(7, 4))
        derivative.save_state()
        deriv_brace = Brace(derivative)
        dx_to_0 = OldTex("dx", "\\to 0")
        dx_to_0.set_color_by_tex("dx", self.dx_color)
        dx_to_0.next_to(deriv_brace, DOWN)

        #Introduce graph
        self.play(ShowCreation(graph))
        self.play(Write(graph_label, run_time = 1))
        self.play(Write(derivative))
        self.wait()
        input_copy = input_x.copy()
        self.play(
            input_copy.next_to, 
            self.coords_to_point(self.start_x, 0),
            DOWN
        )
        self.play(ShowCreation(start_x_v_line))
        self.wait()

        #ss_group_development
        self.play(
            ShowCreation(ss_group.dx_line),
            ShowCreation(ss_group.dx_label),
        )
        self.wait()
        self.play(ShowCreation(ss_group.df_line))
        self.play(Write(ss_group.df_label))
        self.wait(2)
        self.play(
            ReplacementTransform(ss_group.dx_label.copy(), dx),
            ReplacementTransform(ss_group.df_label.copy(), df),
            run_time = 2
        )
        self.play(ShowCreation(ss_group.secant_line))
        self.wait()

        #Let dx approach 0
        self.play(
            GrowFromCenter(deriv_brace),
            Write(dx_to_0),
        )
        self.animate_secant_slope_group_change(
            ss_group,
            target_dx = 0.01,
            run_time = 5,
        )
        self.wait()

        #Write out fuller limit
        new_deriv = OldTex(
            "{f", "(", str(self.start_x), "+", "dx", ")", 
            "-", "f", "(", str(self.start_x), ")",
            "\\over \\,", "dx"
        )
        new_deriv.set_color_by_tex("dx", self.dx_color)
        new_deriv.set_color_by_tex("f", self.df_color)
        new_deriv.set_color_by_tex(str(self.start_x), RED)
        deriv_to_new_deriv = dict([
            (
                VGroup(derivative.get_part_by_tex(s)), 
                VGroup(*new_deriv.get_parts_by_tex(s))
            )
            for s in ["f", "over", "dx", "(", str(self.start_x), ")"]
        ])
        covered_new_deriv_parts = list(it.chain(*list(deriv_to_new_deriv.values())))
        uncovered_new_deriv_parts = [part for part in new_deriv if part not in covered_new_deriv_parts]
        new_deriv.move_to(derivative)
        new_brace = Brace(new_deriv, DOWN)

        self.animate_secant_slope_group_change(
            ss_group,
            target_dx = self.start_dx,
            run_time = 2
        )
        self.play(ShowCreation(nudged_x_v_line))
        self.wait()
        self.play(*[
            ReplacementTransform(*pair, run_time = 2)
            for pair in list(deriv_to_new_deriv.items())
        ]+[
            Transform(deriv_brace, new_brace),
            dx_to_0.next_to, new_brace, DOWN
        ])
        self.play(Write(VGroup(*uncovered_new_deriv_parts), run_time = 2))
        self.wait()

        #Introduce limit notation
        lim = OldTex("\\lim").scale(1.3)
        dx_to_0.generate_target()
        dx_to_0.target.scale(0.7)
        dx_to_0.target.next_to(lim, DOWN, buff = SMALL_BUFF)
        lim_group = VGroup(lim, dx_to_0.target)
        lim_group.move_to(new_deriv, LEFT)

        self.play(
            ReplacementTransform(deriv_brace, lim),
            MoveToTarget(dx_to_0),
            new_deriv.next_to, lim_group, RIGHT,
            run_time = 2
        )
        for sf, color in (1.2, YELLOW), (1/1.2, WHITE):
            self.play(
                lim.scale, sf,
                lim.set_color, color,
                lag_ratio = 0.5
            )
        self.wait(2)
        self.animate_secant_slope_group_change(
            ss_group, target_dx = 0.01,
            run_time = 5,
            added_anims = [
                Transform(nudged_x_v_line, start_x_v_line, run_time = 5)
            ]
        )
        self.wait(2)

        #Record attributes for DiscussLowercaseDs below
        digest_locals(self)
