# ==============================================================================
# Scene:      FillIn100PointDiagram
# Source:     videos/_2023/moser_reboot/main.py (lines 634-649)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl FillIn100PointDiagram.py FillIn100PointDiagram -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ExplainNChoose2(InteractiveScene):
    n = 7
    fudge_factor = 0.1

    def construct(self):
        # Setup circle
        circle, chords, dots, numbers = diagram = self.get_circle_diagram()
        self.add(*diagram)

        # Ask question
        question = Text("How many pairs of points?")
        question.to_edge(RIGHT, MED_LARGE_BUFF)
        question.to_edge(UP, MED_SMALL_BUFF)
        question.add(Underline(question))
        self.add(question)

        # Show all pairs
        indices = list(range(self.n))
        pair_labels = VGroup()
        pair_label_template = Tex("(0, 0)")
        last_label = VectorizedPoint()
        last_label.next_to(question, DOWN)
        last_label.shift(1.5 * LEFT)

        for i, j in it.combinations(indices, 2):
            label = pair_label_template.copy()
            values = label.make_number_changeable("0", replace_all=True)
            values[0].set_value(i + 1)
            values[1].set_value(j + 1)
            label.next_to(last_label, DOWN)
            if label.get_y() < -3:
                label.next_to(pair_labels, RIGHT, MED_LARGE_BUFF)
                label.align_to(pair_labels, UP)
            pair_labels.add(label)

            chords.set_opacity(0.25)
            dots.set_opacity(0.25)
            numbers.set_opacity(0.25)
            temp_line = Line(dots[i].get_center(), dots[j].get_center())
            temp_line.set_stroke(BLUE_B, 3)
            for mob in [dots[i], dots[j], numbers[i], numbers[j]]:
                mob.set_opacity(1)

            self.add(pair_labels)
            self.add(temp_line)
            self.wait(0.25)
            self.remove(temp_line)

            last_label = label

        self.play(
            chords.animate.set_opacity(1),
            numbers.animate.set_opacity(1),
            dots.animate.set_opacity(1),
        )
        self.wait()

        # Show n choose 2
        nc2 = Tex(R"{n \choose 2}")
        nc2.set_color(YELLOW)
        nc2_label = TexText("``n choose 2''")

        group = VGroup(nc2, nc2_label)
        group.arrange(RIGHT, buff=MED_LARGE_BUFF)
        group.next_to(question, DOWN)

        self.play(
            FadeIn(nc2, DOWN),
            pair_labels.animate.set_height(4).to_edge(DOWN)
        )
        self.play(Write(nc2_label))
        self.wait()

        # Show counts
        n_value = Integer(1)
        n_value.move_to(nc2[1])
        n_value.set_color(YELLOW)

        number_rects = VGroup(*(SurroundingRectangle(number) for number in numbers))
        pair_rects = VGroup(*(
            SurroundingRectangle(pair, buff=SMALL_BUFF).set_stroke(YELLOW, 1)
            for pair in pair_labels
        ))
        rhs = Tex("= 0")
        rhs_num = rhs.make_number_changeable("0")
        rhs.next_to(nc2, RIGHT)

        nc2[1].set_opacity(0)
        self.play(
            Write(number_rects, lag_ratio=0.5),
            ChangeDecimalToValue(n_value, self.n),
        )
        self.play(FadeOut(number_rects, lag_ratio=0.1))
        self.wait()
        self.play(
            VFadeIn(rhs),
            nc2_label.animate.next_to(nc2, DOWN),
            ChangeDecimalToValue(rhs_num, choose(self.n, 2), run_time=3),
            ShowIncreasingSubsets(pair_rects, run_time=3),
        )
        self.wait()
        self.play(FadeOut(pair_rects, lag_ratio=0.04))

        # Show how to calculate it
        new_rhs = Tex(R"= {7 \cdot (7 - 1) \over 2}")
        new_rhs.next_to(nc2, RIGHT)

        self.play(
            rhs.animate.next_to(new_rhs, RIGHT),
            Write(new_rhs[:2]),
            Write(new_rhs[R"\over"]),
        )
        self.wait()
        self.play(Write(new_rhs[R"\cdot (7 - 1)"]))
        self.wait()
        self.play(Write(new_rhs[R"2"]))
        self.wait()

    def get_circle_diagram(self):
        circle = Circle()
        circle.set_stroke(Color("red"), width=2)
        circle.set_height(6)
        circle.to_edge(LEFT)
        points = [
            circle.pfp(a + self.fudge_factor * np.random.uniform(-0., 0.5))
            for a in np.arange(0, 1, 1 / self.n)
        ]
        dots = VGroup(*(
            Dot(point, radius=0.04).set_fill(WHITE)
            for point in points
        ))

        chords = VGroup(*(
            Line(p1, p2).set_stroke(BLUE_B, 1)
            for p1, p2 in it.combinations(points, 2)
        ))

        numbers = VGroup()
        for n, point in zip(it.count(1), points):
            number = Integer(n, font_size=36)
            vect = normalize(point - circle.get_center())
            number.next_to(point, vect, buff=MED_SMALL_BUFF)
            numbers.add(number)

        return VGroup(circle, chords, dots, numbers)


class FillIn100PointDiagram(ExplainNChoose2):
    n = 100

    def construct(self):
        # Show all points
        circle, chords, dots, numbers = diagram = self.get_circle_diagram()
        diagram.center()
        chords.set_stroke(width=1, opacity=0.1)
        for dot in dots:
            dot.scale(0.75)

        self.add(circle, chords, dots)
        self.play(
            ShowCreation(chords),
            run_time=9,
        )
