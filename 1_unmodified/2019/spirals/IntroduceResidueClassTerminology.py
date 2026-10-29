# ==============================================================================
# Scene:      IntroduceResidueClassTerminology
# Source:     videos/_2019/spirals.py (lines 1760-1967)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl IntroduceResidueClassTerminology.py IntroduceResidueClassTerminology -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class IntroduceResidueClassTerminology(Scene):
    def construct(self):
        self.add_title()
        self.add_sequences()
        self.add_terms()
        self.highlight_example()
        self.simple_english()

    def add_title(self):
        title = OldTexText("Overly-fancy ", "terminology")
        title.scale(1.5)
        title.to_edge(UP, buff=MED_SMALL_BUFF)
        underline = Line().match_width(title)
        underline.next_to(title, DOWN, SMALL_BUFF)

        pre_title = OldTexText("Terminology")
        pre_title.replace(title, dim_to_match=1)

        self.play(FadeInFromDown(pre_title))
        self.wait()
        title[0].set_color(BLUE)
        underline.set_color(BLUE)
        self.play(
            ReplacementTransform(pre_title[0], title[1]),
            FadeIn(title[0], RIGHT),
            GrowFromCenter(underline)
        )
        self.play(
            title[0].set_color, WHITE,
            underline.set_color, WHITE,
        )
        self.wait()

        title.add(underline)
        self.add(title)

        self.title = title
        self.underline = underline

    def add_sequences(self):
        sequences = VGroup()
        n_terms = 7

        for r in range(6):
            sequence = VGroup(*[
                Integer(6 * k + r)
                for k in range(n_terms)
            ])
            sequence.arrange(RIGHT, buff=0.4)
            sequences.add(sequence)

        sequences.arrange(DOWN, buff=0.7, aligned_edge=LEFT)
        for sequence in sequences:
            for s1, s2 in zip(sequence[:n_terms], sequences[-1]):
                s1.align_to(s2, RIGHT)
            commas = VGroup()
            for num in sequence[:-1]:
                comma = OldTexText(",")
                comma.next_to(num.get_corner(DR), RIGHT, SMALL_BUFF)
                commas.add(comma)
            dots = OldTex("\\dots")
            dots.next_to(sequence.get_corner(DR), RIGHT, SMALL_BUFF)
            sequence.numbers = VGroup(*sequence)
            sequence.commas = commas
            sequence.dots = dots

            sequence.add(*commas)
            sequence.add(dots)
            sequence.sort(lambda p: p[0])

        labels = VGroup(*[
            OldTex("6k + {}:".format(r))
            for r in range(6)
        ])
        labels.set_color(YELLOW)
        for label, sequence in zip(labels, sequences):
            label.next_to(sequence, LEFT, MED_LARGE_BUFF)

        group = VGroup(sequences, labels)
        group.to_edge(LEFT).to_edge(DOWN, buff=MED_LARGE_BUFF)

        self.add(labels)
        self.play(LaggedStart(*[
            LaggedStartMap(
                FadeInFrom, sequence,
                lambda m: (m, LEFT),
            )
            for sequence in sequences
        ], lag_ratio=0.3))
        self.wait()

        self.sequences = sequences
        self.sequence_labels = labels

    def add_terms(self):
        sequences = self.sequences

        terms = OldTexText(
            "``", "Residue\\\\",
            "classes\\\\",
            "mod ", "6''"
        )
        terms.scale(1.5)
        terms.set_color(YELLOW)
        terms.to_edge(RIGHT)

        res_brace = Brace(terms.get_part_by_tex("Residue"), UP)
        remainder = OldTexText("Remainder")
        remainder.next_to(res_brace, UP, SMALL_BUFF)

        mod_brace = Brace(terms.get_part_by_tex("mod"), DOWN)
        mod_def = OldTexText(
            "``where the thing\\\\you divide by is''"
        )
        mod_def.next_to(mod_brace, DOWN, SMALL_BUFF)

        arrows = VGroup(*[
            Arrow(terms.get_left(), sequence.get_right())
            for sequence in sequences
        ])
        arrows.set_color(YELLOW)

        self.play(
            FadeIn(terms),
            LaggedStartMap(ShowCreation, arrows),
        )
        self.wait()
        self.play(
            GrowFromCenter(res_brace),
            FadeInFromDown(remainder),
        )
        self.wait()
        self.play(GrowFromCenter(mod_brace))
        self.play(Write(mod_def))
        self.wait()

        self.terminology = VGroup(
            terms,
            res_brace, remainder,
            mod_brace, mod_def,
            arrows
        )

    def highlight_example(self):
        sequences = self.sequences
        labels = self.sequence_labels

        r = 2
        k = 3
        sequence = sequences[r]
        label = labels[r]
        r_tex = label[0][3]
        n_rects = VGroup(*[
            SurroundingRectangle(num)
            for num in sequence.numbers
        ])
        r_rect = SurroundingRectangle(r_tex)
        n_rects.set_color(RED)
        r_rect.set_color(RED)

        n_rect = n_rects.submobjects.pop(k)

        self.play(ShowCreation(n_rect))
        self.wait()
        self.play(
            TransformFromCopy(n_rect, r_rect, path_arc=30 * DEGREES)
        )
        self.wait()
        self.play(ShowCreation(n_rects))
        self.wait()
        self.play(
            ShowCreationThenFadeOut(
                self.underline.copy().set_color(PINK),
            )
        )

    def simple_english(self):
        terminology = self.terminology
        sequences = self.sequences

        randy = Randolph()
        randy.set_height(2)
        randy.flip()
        randy.to_corner(DR)

        new_phrase = OldTexText("Everything 2 above\\\\a multiple of 6")
        new_phrase.scale(1.2)
        new_phrase.set_color(RED_B)
        new_phrase.next_to(sequences[2])

        self.play(
            FadeOut(terminology),
            FadeIn(new_phrase),
            VFadeIn(randy),
            randy.change, "sassy"
        )
        self.wait()
        self.play(randy.change, "angry")
        for x in range(2):
            self.play(Blink(randy))
            self.wait()
        self.play(
            FadeOut(new_phrase),
            FadeIn(terminology),
            FadeOut(randy, DOWN)
        )
        self.wait()
        self.wait(6)
