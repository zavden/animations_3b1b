# ==============================================================================
# Scene:      TopologyWordBreak
# Source:     videos/_2018/borsuk_addition.py (lines 322-371)
# Category:   2 · Renders with modifications
# Includes code copied from: _2018/uncertainty.py
#
# Run from this folder:
#     manimgl TopologyWordBreak.py TopologyWordBreak -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - genus computed from glyph subpaths (len(get_subpaths())-1): GL glyphs have no submobjects for their holes
# ==============================================================================

from manim_imports_ext import *
import warnings


# ----- From _2018/uncertainty.py -----

warnings.warn("""
    Warning: This file makes use of
    ContinualAnimation, which has since
    been deprecated
""")



# ----- From _2018/borsuk_addition.py -----

class TopologyWordBreak(Scene):
    def construct(self):
        word = OldTexText("Topology")
        word.scale(2)
        # CHANGE: a GL glyph has no submobjects for its holes, so the genus is computed as number of subpaths - 1 below
        colors = [BLUE, YELLOW, RED]
        classes = VGroup(*[VGroup() for x in range(3)])
        for letter in word:
            genus = len(letter.get_subpaths()) - 1
            letter.target_color = colors[genus]
            letter.generate_target()
            letter.target.set_color(colors[genus])
            classes[genus].add(letter.target)
        signs = VGroup()
        for group in classes:
            new_group = VGroup()
            for elem in group[:-1]:
                new_group.add(elem)
                sign = OldTex("\\simeq")
                new_group.add(sign)
                signs.add(sign)
            new_group.add(group[-1])
            group.submobjects = list(new_group.submobjects)
            group.arrange(RIGHT)

        word[2].target.shift(0.1 * DOWN)
        word[7].target.shift(0.1 * DOWN)

        classes.arrange(DOWN, buff=LARGE_BUFF, aligned_edge=LEFT)
        classes.shift(2 * RIGHT)

        genus_labels = VGroup(*[
            OldTexText("Genus %d:" % d).scale(1.5).next_to(
                classes[d], LEFT, MED_LARGE_BUFF
            )
            for d in range(3)
        ])
        genus_labels.shift(SMALL_BUFF * UP)

        self.play(Write(word))
        self.play(LaggedStartMap(
            ApplyMethod, word,
            lambda m: (m.set_color, m.target_color),
            run_time=1
        ))
        self.play(
            LaggedStartMap(MoveToTarget, word),
            LaggedStartMap(FadeIn, signs),
            LaggedStartMap(FadeInFromDown, genus_labels),
        )
        self.wait(3)
