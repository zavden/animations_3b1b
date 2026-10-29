# ==============================================================================
# Scene:      MeaningOfIndependence
# Source:     videos/_2018/eop/independence.py (lines 154-291)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl MeaningOfIndependence.py MeaningOfIndependence -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class MeaningOfIndependence(SampleSpaceScene):
    CONFIG = {
        "sample_space_config" : {
            "height" : 4,
            "width" : 4,
        }
    }
    def construct(self):
        self.add_labeled_space()
        self.align_conditionals()
        self.relabel()
        self.assume_independence()
        self.no_independence()    

    def add_labeled_space(self):
        self.add_sample_space(**self.sample_space_config)
        self.sample_space.shift(2*LEFT)
        self.sample_space.divide_horizontally(0.3)
        self.sample_space[0].divide_vertically(
            0.9, colors = [BLUE_D, GREEN_C]
        )
        self.sample_space[1].divide_vertically(
            0.5, colors = [BLUE_E, GREEN_E]
        )
        side_braces_and_labels = self.sample_space.get_side_braces_and_labels(
            ["P(A)", "P(\\overline A)"]
        )
        top_braces_and_labels, bottom_braces_and_labels = [
            part.get_subdivision_braces_and_labels(
                part.vertical_parts,
                labels = ["P(B | %s)"%s, "P(\\overline B | %s)"%s],
                direction = vect
            )
            for part, s, vect in zip(
                self.sample_space.horizontal_parts, 
                ["A", "\\overline A"], 
                [UP, DOWN],
            )
        ]
        braces_and_labels_groups = VGroup(
            side_braces_and_labels,
            top_braces_and_labels,
            bottom_braces_and_labels,
        )

        self.add(self.sample_space)
        self.play(Write(braces_and_labels_groups, run_time = 4))

    def align_conditionals(self):
        line = Line(*[
            interpolate(
                self.sample_space.get_corner(vect+LEFT),
                self.sample_space.get_corner(vect+RIGHT),
                0.7
            )
            for vect in (UP, DOWN)
        ])
        line.set_stroke(RED, 8)
        word = OldTexText("Independence")
        word.scale(1.5)
        word.next_to(self.sample_space, RIGHT, buff = LARGE_BUFF)
        word.set_color(RED)

        self.play(*it.chain(
            self.get_top_conditional_change_anims(0.7),
            self.get_bottom_conditional_change_anims(0.7)
        ))
        self.play(
            ShowCreation(line),
            Write(word, run_time = 1)
        )
        self.wait()

        self.independence_word = word
        self.independence_line = line

    def relabel(self):
        old_labels = self.sample_space[0].vertical_parts.labels
        ignored_braces, new_top_labels = self.sample_space[0].get_top_braces_and_labels(
            ["P(B)", "P(\\overline B)"]
        )
        equation = OldTex(
            "P(B | A) = P(B)"
        )
        equation.scale(1.5)
        equation.move_to(self.independence_word)

        self.play(
            Transform(old_labels, new_top_labels),
            FadeOut(self.sample_space[1].vertical_parts.labels),
            FadeOut(self.sample_space[1].vertical_parts.braces),
        )
        self.play(
            self.independence_word.next_to, equation, UP, MED_LARGE_BUFF,
            Write(equation)
        )
        self.wait()

        self.equation = equation

    def assume_independence(self):
        everything = VGroup(*self.get_top_level_mobjects())
        morty = Mortimer()
        morty.scale(0.7)
        morty.to_corner(DOWN+RIGHT)
        bubble = ThoughtBubble(direction = RIGHT)
        bubble.pin_to(morty)
        bubble.set_fill(opacity = 0)

        self.play(
            FadeIn(morty),
            everything.scale, 0.5,
            everything.move_to, bubble.get_bubble_center(),
        )
        self.play(
            morty.change, "hooray", everything,
            ShowCreation(bubble)
        )
        self.wait()
        self.play(Blink(morty))
        self.wait()

        self.morty = morty

    def no_independence(self):
        for part in self.sample_space.horizontal_parts:
            part.vertical_parts.labels = None
        self.play(*it.chain(
            self.get_top_conditional_change_anims(0.9),
            self.get_bottom_conditional_change_anims(0.5),
            [
                self.independence_word.fade, 0.7,
                self.equation.fade, 0.7,
                self.morty.change, "confused", self.sample_space,
                FadeOut(self.independence_line)
            ]
        ))
        self.wait()
