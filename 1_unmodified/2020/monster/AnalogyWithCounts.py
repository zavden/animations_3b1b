# ==============================================================================
# Scene:      AnalogyWithCounts
# Source:     videos/_2020/monster.py (lines 2381-2455)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl AnalogyWithCounts.py AnalogyWithCounts -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

def get_snowflake(height=2):
    snowflake = SVGMobject("snowflake")
    snowflake.set_fill(GREY_C, 1)
    snowflake.set_gloss(1)
    snowflake.set_shadow(0.2)
    snowflake.set_stroke(WHITE, 1)
    snowflake.set_height(height)
    return snowflake


class AnalogyWithCounts(Scene):
    def construct(self):
        # Setup
        line = Line(LEFT, RIGHT)
        words = OldTexText("Abstraction of")
        words.match_width(line)
        words.scale(0.9)
        words.next_to(line, UP, SMALL_BUFF)
        line.add(words)
        line.rotate(-90 * DEGREES)
        line.scale(0.5)

        diagrams = VGroup(*[
            VGroup(mob1, line.copy(), mob2)
            for mob1, mob2 in [
                (OldTexText("Groups"), OldTexText("Symmetry actions")),
                (OldTex("D_6"), get_snowflake(height=1)),
                (OldTexText("Numbers"), OldTexText("Counts")),
                (OldTex("9").scale(1.5), VGroup(*[Dot() for x in range(9)]).arrange_in_grid(buff=SMALL_BUFF)),
            ]
        ])
        for diagram, vect in zip(diagrams, [LEFT, LEFT, RIGHT, RIGHT]):
            diagram[0].set_color(YELLOW)
            diagram[2].set_fill(BLUE)
            diagram.arrange(DOWN)
            diagram.scale(1.5)
            diagram.shift(3.5 * vect - diagram[1].get_center())

        # Show diagrams
        self.add(diagrams[0][0])
        self.play(
            Write(diagrams[0][1]),
            FadeIn(diagrams[0][2], 2 * UP),
        )
        self.wait()
        self.play(*[
            AnimationGroup(
                ReplacementTransform(
                    m2.copy().replace(m1, stretch=True).set_opacity(0),
                    m2,
                ),
                Transform(
                    m1.copy(),
                    m1.copy().replace(m2, stretch=True).set_opacity(0),
                    remover=True
                )
            )
            for m1, m2 in zip(diagrams[0], diagrams[2])
        ])
        self.wait()

        self.play(
            FadeOut(diagrams[0]),
            FadeIn(diagrams[1]),
        )
        flake = diagrams[1][2]
        self.add(flake)
        self.play(
            FadeOut(diagrams[2]),
            FadeIn(diagrams[3]),
            Rotate(flake, 60 * DEGREES),
        )
        self.play(Rotate(flake, PI, UP))
        self.play(Rotate(flake, -120 * DEGREES))
        self.play(Rotate(flake, PI, RIGHT))
        self.play(Rotate(flake, 120 * DEGREES))
        self.play(Rotate(flake, PI, UP))
        self.play(
            VFadeOut(diagrams[1]),
            Rotate(flake, 180 * DEGREES),
            FadeIn(diagrams[0]),
            FadeOut(diagrams[3]),
            FadeIn(diagrams[2]),
        )
        self.wait(2)
