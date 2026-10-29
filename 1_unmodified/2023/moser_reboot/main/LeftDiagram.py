# ==============================================================================
# Scene:      LeftDiagram
# Source:     videos/_2023/moser_reboot/main.py (lines 308-384)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl LeftDiagram.py LeftDiagram -w -m --fps 15
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


class LeftDiagram(ExplainNChoose2):
    n = 6
    fudge_factor = 0.5

    def construct(self):
        # Initialize
        circle = Circle()
        circle.set_height(7.75)
        circle.set_stroke(RED, width=3)
        circle.move_to(2.6 * RIGHT)
        radians = np.arange(1, 7)
        dots = VGroup(*(
            Dot(circle.pfp(radians[i] / TAU))
            for i in [0, 2, 4, 1, 3, 5]
        ))

        # First four diagrams
        diagrams = VGroup()
        for n in range(2, 6):
            diagram = VGroup(
                circle.copy(),
                self.get_chords(dots[:n]),
                dots[:n].copy(),
            )
            diagram.set_stroke(background=True)
            diagram.preimage = diagram.copy()
            diagrams.add(diagram)

        diagrams.arrange(DOWN, buff=2.5)
        diagrams.set_height(FRAME_HEIGHT - 1)
        diagrams.to_edge(LEFT)

        numbers = VGroup(*(
            Integer(2**n, font_size=60).next_to(diagram, RIGHT)
            for n, diagram in zip(it.count(1), diagrams)
        ))

        for diagram, number in zip(diagrams, numbers):
            for dot in diagram[2]:
                dot.scale(2)
            self.play(
                TransformFromCopy(diagram.preimage, diagram),
                FadeInFromPoint(number, circle.get_center()),
            )
            self.wait()

    def get_chords(self, dots):
        return VGroup(*(
            Line(
                d1.get_center(), d2.get_center(),
                stroke_width=2,
                stroke_color=BLUE_B,
            )
            for d1, d2 in it.combinations(dots, 2)
        ))

    def get_samples(self, circle, n=1000, color=YELLOW):
        radius = circle.get_radius()
        center = circle.get_center()
        samples = DotCloud()
        samples.to_grid(n, n)
        samples.replace(circle)
        samples.set_radius(8 / n)
        samples.filter_out(lambda p: np.linalg.norm(p - center) > radius)
        samples.set_color(color)
        return samples

    def get_regions(self, samples, chords):
        regions = Group()
        for signs in it.product(*len(chords) * [[-1, 1]]):
            sub_samples = samples.copy()
            for chord, sign in zip(chords, signs):
                vect = sign * rotate_vector(chord.get_vector(), 90 * DEGREES)
                sub_samples.filter_out(lambda p: np.dot(p, vect) > 0)
            if sub_samples.get_num_points() > 0:
                regions.add(sub_samples)
        return regions
