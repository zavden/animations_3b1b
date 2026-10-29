# ==============================================================================
# Scene:      ArrayOfValidMessages
# Source:     videos/_2020/hamming.py (lines 2465-2574)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ArrayOfValidMessages.py ArrayOfValidMessages -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

def zap_anim(bit, bolt_height=0.75):
    bolt = SVGMobject("lightning_bolt")
    bolt[0].add_line_to(bolt[0].get_start())
    bolt.set_fill(RED_B, 1)
    bolt.set_stroke(width=0)
    bolt.set_height(bolt_height)

    bolt.move_to(bit.get_center(), DL)

    outline = bolt.deepcopy()
    outline.set_stroke(RED_D, 2)
    outline.set_fill(opacity=0)

    return AnimationGroup(
        Succession(
            GrowFromPoint(bolt, bolt.get_corner(UR), rate_func=rush_into),
            FadeOut(bolt, run_time=0.5),
        ),
        Succession(
            ShowCreation(outline),
            FadeOut(outline),
        ),
        run_time=1,
    )


class ArrayOfValidMessages(Scene):
    def construct(self):
        # Messages
        title = OldTexText("All possible messages")
        title.to_edge(UP)
        nr = 22
        nc = 46
        dots = VGroup(*[Dot() for x in range(nr * nc)])
        dots.arrange_in_grid(nr, nc)
        dots.set_color(GREY_C)
        dots.set_height(6)
        dots.to_edge(DOWN)
        shuffled_dots = dots.copy()
        shuffled_dots.shuffle()

        self.add(title)
        self.play(Write(shuffled_dots, remover=True, run_time=6, lag_ratio=5 / len(dots)))
        self.add(dots)
        self.wait()

        # Valid messages
        subset = OldTex("\\subset")
        subset.set_height(0.4)
        subset.to_edge(UP)
        valid_label = OldTexText("Valid messages")
        valid_label.set_color(YELLOW)
        valid_label.next_to(subset, LEFT)

        valid_dots = VGroup()
        for row in range(0, nr, 3):
            for col in range(0, nc, 3):
                valid_dot = dots[row * nc + col]
                valid_dot.generate_target()
                valid_dot.target.scale(2)
                valid_dot.target.set_color(YELLOW)
                valid_dots.add(valid_dot)

        self.play(
            LaggedStartMap(MoveToTarget, valid_dots, run_time=3),
            Write(subset),
            FadeIn(valid_label, LEFT),
            title.next_to, subset, RIGHT,
        )
        self.wait()

        # Words analogy
        example_words = VGroup(
            OldTexText("Hello world", color=YELLOW),
            OldTexText("Helho world", color=GREY_B),
        )
        example_words.scale(1.25)
        index = 12 * nc + 21
        example_dots = VGroup(dots[index], dots[index + 1]).copy()

        example_groups = VGroup()
        for word, dot in zip(example_words, example_dots):
            arrow = Vector(0.7 * DOWN)
            arrow.next_to(dot, UP, SMALL_BUFF)
            word.next_to(arrow, UP, SMALL_BUFF)
            example_group = VGroup(word, arrow, dot)
            example_groups.add(example_group)

        fade_rect = SurroundingRectangle(dots)
        fade_rect.set_stroke(BLACK, 0)
        fade_rect.set_fill(BLACK, 0.7)

        self.play(
            FadeIn(fade_rect),
            FadeIn(example_groups[0])
        )
        self.wait()
        self.play(
            zap_anim(example_words[0][0][3:5]),
            Transform(*example_groups),
        )
        self.wait()
        self.play(FadeOut(example_groups[0]), FadeOut(fade_rect))

        # Corrections
        valid_centers = [vd.get_center() for vd in valid_dots]
        lines = VGroup()
        for dot in dots:
            dc = dot.get_center()
            norms = [get_norm(dc - vc) for vc in valid_centers]
            line = Line(dc, valid_centers[np.argmin(norms)])
            line.set_stroke(WHITE, 1)
            lines.add(line)

        shuffled_lines = VGroup(*lines)
        shuffled_lines.shuffle()

        self.play(ShowCreation(shuffled_lines, lag_ratio=10 / len(lines), run_time=5))
        self.wait()

        # Mandering path between valid messages
        self.add(fade_rect, valid_dots)
        self.play(FadeIn(fade_rect))

        path = [RIGHT, UP, UP, RIGHT, RIGHT, RIGHT, UP, UP, RIGHT, RIGHT, DOWN]
        dist = get_norm(dots[1].get_center() - dots[0].get_center())
        curr = dots[index].get_center()
        arrows = VGroup()
        for vect in path:
            new = curr + dist * vect
            arrows.add(Arrow(curr, new, buff=0, fill_color=RED))
            curr = new

        for arrow in arrows:
            self.play(GrowArrow(arrow), run_time=0.5)
        self.wait()
