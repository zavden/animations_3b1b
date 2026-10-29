# ==============================================================================
# Scene:      IntroduceGraph
# Source:     videos/_2017/mug.py (lines 510-599)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl IntroduceGraph.py IntroduceGraph -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class IntroduceGraph(PiCreatureScene):
    def construct(self):
        pi_creatures = self.pi_creatures
        dots = VGroup(*[
            Dot(color = pi.get_color()).scale(2).move_to(pi)
            for pi in pi_creatures
        ])
        lines = VGroup(*[
            Line(pi1.get_center(), pi2.get_center())
            for pi1, pi2 in it.combinations(pi_creatures, 2)
        ])

        graph_word = OldTexText("``", "", "Graph", "''", arg_separator = "")
        graph_word.to_edge(UP)
        planar_graph_word = OldTexText("``", "Planar", " graph", "''", arg_separator = "")
        planar_graph_word.move_to(graph_word)

        vertices_word = OldTexText("Vertices")
        vertices_word.to_edge(RIGHT, buff = LARGE_BUFF)
        vertices_word.set_color(YELLOW)

        vertex_arrows = VGroup(*[
            Arrow(vertices_word.get_left(), dot)
            for dot in dots[-2:]
        ])

        edge_word = OldTexText("Edge")
        edge_word.next_to(lines, LEFT, LARGE_BUFF)
        edge_arrow = Arrow(
            edge_word, lines, buff = SMALL_BUFF,
            color = WHITE
        )

        self.play(LaggedStartMap(GrowFromCenter, pi_creatures))
        self.play(
            LaggedStartMap(ShowCreation, lines),
            LaggedStartMap(
                ApplyMethod, pi_creatures,
                lambda pi : (pi.change, "pondering", lines)
            )
        )
        self.play(Write(graph_word))
        self.play(ReplacementTransform(
            pi_creatures, dots,
            run_time = 2,
            lag_ratio = 0.5
        ))
        self.add_foreground_mobjects(dots)
        self.play(
            FadeIn(vertex_arrows),
            FadeIn(vertices_word),
        )
        self.wait()
        self.play(LaggedStartMap(
            ApplyMethod, lines,
            lambda l : (l.rotate, np.pi/12),
            rate_func = wiggle
        ))
        self.play(
            FadeIn(edge_word),
            GrowArrow(edge_arrow),
        )
        self.wait(2)
        line = lines[2]
        self.play(
            line.set_points_smoothly, [
                line.get_start(),
                dots.get_left() + MED_SMALL_BUFF*LEFT,
                dots.get_corner(DOWN+LEFT) + MED_SMALL_BUFF*(DOWN+LEFT),
                dots.get_bottom() + MED_SMALL_BUFF*DOWN,
                line.get_end(),
            ],
            VGroup(edge_word, edge_arrow).shift, MED_LARGE_BUFF*LEFT,
        )
        self.wait()
        self.play(ReplacementTransform(graph_word, planar_graph_word))
        self.wait(2)

    ###

    def create_pi_creatures(self):
        pis = VGroup(
            PiCreature(color = BLUE_D),
            PiCreature(color = GREY_BROWN),
            PiCreature(color = BLUE_C).flip(),
            PiCreature(color = BLUE_E).flip(),
        )
        pis.scale(0.5)
        pis.arrange_in_grid(buff = 2)
        return pis
