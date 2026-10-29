# ==============================================================================
# Scene:      TrainingDataCHM
# Source:     videos/_2024/transformers/chm.py (lines 1938-2001)
# Category:   1 · Renders unmodified
# Includes code copied from: _2024/transformers/helpers.py
#
# Run from this folder:
#     manimgl TrainingDataCHM.py TrainingDataCHM -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *


# ----- From _2024/transformers/helpers.py -----

def get_paragraph(words, line_len=40, font_size=48):
    """
    Handle word wrapping
    """
    words = list(map(str.strip, words))
    word_lens = list(map(len, words))
    lines = []
    lh, rh = 0, 0
    while rh < len(words):
        rh += 1
        if sum(word_lens[lh:rh]) > line_len:
            rh -= 1
            lines.append(words[lh:rh])
            lh = rh
    lines.append(words[lh:])
    text = "\n".join([" ".join(line).strip() for line in lines])
    return Text(text, alignment="LEFT", font_size=font_size)



# ----- From _2024/transformers/chm.py -----

class TrainingDataCHM(InteractiveScene):
    def construct(self):
        # Test
        passages = [
            "The Computer History Museum (CHM) is a museum ... located in Mountain View...",
            "Computer History Museum ... 1401 N. Shoreline Blvd. Mountain View...",
            "Things to do in Mountain View ... the Computer History Museum ...",
            "While I was in Mountain View ... stopped by the Computer History Museum ...",
        ]
        items = VGroup(
            get_paragraph(passage.split(" "), line_len=35, font_size=30)
            for passage in passages
        )

        items.arrange(DOWN, buff=LARGE_BUFF, aligned_edge=LEFT)
        items.to_corner(DL)
        items.shift(0.5 * UP)
        dots = Tex(R"\vdots")
        dots.next_to(items, DOWN, MED_LARGE_BUFF)
        dots.shift_onto_screen(buff=MED_SMALL_BUFF)
        items.add(dots)

        title = Text("Training Data")
        title.next_to(items, UP, buff=LARGE_BUFF)
        title.shift_onto_screen(buff=MED_SMALL_BUFF)
        underline = Underline(title)

        chm_phrases = VGroup(item["Computer History Museum"] for item in items)
        mv_phrases = VGroup(item["Mountain View"] for item in items)

        self.play(
            FadeIn(title),
            ShowCreation(underline),
            LaggedStartMap(FadeIn, items, shift=DOWN, lag_ratio=0.15)
        )
        self.wait()
        self.play(chm_phrases.animate.set_color(RED).set_anim_args(lag_ratio=0.1))
        self.wait()
        self.play(mv_phrases.animate.set_color(PINK).set_anim_args(lag_ratio=0.1))
        self.wait()

        # Arrows to ffn
        ffn_point = 3 * RIGHT + DOWN
        arrows = VGroup(
            Arrow(
                item.get_right(),
                interpolate(item.get_right(), ffn_point, 0.6),
                path_arc=arc * DEGREES,
            )
            for item, arc in zip(items[:-1], range(-40, 40, 20))
        )
        arrows.set_fill(border_width=1)
        self.play(Write(arrows, lag_ratio=0.1), run_time=3)
        self.play(
            LaggedStart(
                *(
                    FadeOutToPoint(letter.copy(), ffn_point)
                    for letter in VGroup(chm_phrases, mv_phrases).family_members_with_points()
                ),
                lag_ratio=1e-2,
                run_time=3
            )
        )
        self.wait()
