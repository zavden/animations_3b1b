# ==============================================================================
# Scene:      FalseEuclidFollowup
# Source:     videos/_2022/visual_proofs/lies.py (lines 2036-2124)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl FalseEuclidFollowup.py FalseEuclidFollowup -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class FalseEuclidFollowup(InteractiveScene):
    def construct(self):
        # All triangles are equilateral
        tri1 = Polygon(3 * UP, DL, RIGHT)
        tri2 = Polygon(3 * UP, LEFT, RIGHT)
        tri3 = tri2.copy().set_height(math.sqrt(3) * tri2.get_width() / 2, stretch=True, about_edge=DOWN)
        tris = VGroup(tri1, tri2, tri3)
        tris.set_fill(BLUE_D, 1)
        tris.set_stroke(WHITE, 2)
        tris.scale(1.5)
        tris.to_edge(DOWN, buff=1.0)
        tri = tri1

        def get_side(i, j, tri=tri):
            return Line(tri.get_vertices()[i], tri.get_vertices()[j]).set_stroke(YELLOW, 4)

        labels = Text("ABC")
        for letter, vert in zip(labels, tri.get_vertices()):
            letter.next_to(vert, normalize(vert - tri.get_center_of_mass()), SMALL_BUFF)

        equation = Tex("\\overline{AB} = \\overline{AC}")
        equation2 = Tex("\\overline{AB} = \\overline{AC} = \\overline{BC}")
        equation.next_to(labels, LEFT, aligned_edge=UP)
        equation2.move_to(equation).to_edge(LEFT)
        words = Text("All triangles are\nisosceles")
        words.next_to(equation, DOWN, LARGE_BUFF)
        VGroup(equation, words).to_edge(LEFT)
        iso = words.select_parts("isosceles")
        iso_cross = Cross(iso)
        equi = Text("equilateral")
        equi.move_to(iso, UP)
        equi.set_color(YELLOW)

        self.add(tri, labels)
        self.wait()
        self.play(
            FadeIn(equation), FadeIn(words),
            ShowCreationThenDestruction(get_side(0, 1), run_time=2),
            ShowCreationThenDestruction(get_side(0, 2), run_time=2),
        )
        self.play(Transform(tri, tri2), labels[1].animate.shift(1.5 * UP))
        self.wait()
        self.play(CyclicReplace(*labels))
        self.play(
            ShowCreationThenDestruction(get_side(1, 0), run_time=2),
            ShowCreationThenDestruction(get_side(1, 2), run_time=2),
            ShowCreation(iso_cross)
        )
        cross_group = VGroup(iso, iso_cross)
        self.play(
            cross_group.animate.shift(DOWN),
            FadeIn(equi, 0.5 * DOWN),
            Transform(tri, tri3),
            labels[2].animate.next_to(tri3, UP, SMALL_BUFF)
        )
        self.play(
            Transform(equation, equation2[:len(equation)]),
            FadeIn(equation2[len(equation):], RIGHT),
        )
        self.wait()

        words = VGroup(words.select_parts("All triangles are"), equi)

        # Three possibilities
        possibilities = VGroup(
            Text("1. This is true"),
            OldTexText("2. Euclid's axioms $\\Rightarrow$ falsehoods")[0],
            Text("3. This proof has a flaw"),
        )
        possibilities.arrange(DOWN, buff=1.0, aligned_edge=LEFT)
        possibilities.to_edge(RIGHT, buff=LARGE_BUFF)
        poss_title = Text("Possibilities", font_size=60)
        poss_title.next_to(possibilities, UP, buff=1.5, aligned_edge=LEFT)
        poss_title.add(Underline(poss_title))

        tri.add(labels)
        self.play(
            FadeOut(cross_group, DL),
            tri.animate.match_width(words).next_to(words, DOWN, LARGE_BUFF),
            LaggedStart(*(
                FadeIn(poss[:2], shift=LEFT)
                for poss in possibilities
            )),
            Write(poss_title)
        )
        self.wait()
        for poss in possibilities:
            self.play(Write(poss[2:], stroke_color=WHITE))
            self.wait()
