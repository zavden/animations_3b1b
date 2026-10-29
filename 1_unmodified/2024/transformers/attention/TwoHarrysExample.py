# ==============================================================================
# Scene:      TwoHarrysExample
# Source:     videos/_2024/transformers/attention.py (lines 3329-3358)
# Category:   1 · Renders unmodified
# Includes code copied from: _2024/transformers/embedding.py, _2024/transformers/helpers.py
#
# Run from this folder:
#     manimgl TwoHarrysExample.py TwoHarrysExample -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *


# ----- From _2024/transformers/helpers.py -----

class ContextAnimation(LaggedStart):
    def __init__(
        self,
        target,
        sources,
        direction=UP,
        hue_range=(0.1, 0.3),
        time_width=2,
        min_stroke_width=0,
        max_stroke_width=5,
        lag_ratio=None,
        strengths=None,
        run_time=3,
        fix_in_frame=False,
        path_arc=PI / 2,
        **kwargs,
    ):
        arcs = VGroup()
        if strengths is None:
            strengths = np.random.random(len(sources))**2
        for source, strength in zip(sources, strengths):
            sign = direction[1] * (-1)**int(source.get_x() < target.get_x())
            arcs.add(Line(
                source.get_edge_center(direction),
                target.get_edge_center(direction),
                path_arc=sign * path_arc,
                stroke_color=random_bright_color(hue_range=hue_range),
                stroke_width=interpolate(
                    min_stroke_width,
                    max_stroke_width,
                    strength,
                )
            ))
        if fix_in_frame:
            arcs.fix_in_frame()
        arcs.shuffle()
        lag_ratio = 0.5 / len(arcs) if lag_ratio is None else lag_ratio

        super().__init__(
            *(
                VShowPassingFlash(arc, time_width=time_width)
                for arc in arcs
            ),
            lag_ratio=lag_ratio,
            run_time=run_time,
            **kwargs,
        )



# ----- From _2024/transformers/embedding.py -----

def break_into_pieces(phrase_mob: Text, offsets: list[int]):
    phrase = phrase_mob.get_string()
    lhs = offsets
    rhs = [*offsets[1:], len(phrase)]
    result = []
    for lh, rh in zip(lhs, rhs):
        substr = phrase[lh:rh]
        start = phrase_mob.substr_to_path_count(phrase[:lh])
        end = start + phrase_mob.substr_to_path_count(substr)
        result.append(phrase_mob[start:end])
    return VGroup(*result)


def break_into_words(phrase_mob):
    offsets = [m.start() for m in re.finditer(" ", phrase_mob.get_string())]
    return break_into_pieces(phrase_mob, [0, *offsets])



# ----- From _2024/transformers/attention.py -----

class TwoHarrysExample(InteractiveScene):
    def construct(self):
        # Test
        s1, s2 = sentences = VGroup(
            break_into_words(Text("... " + " ... ".join(words)))
            for words in [
                ("wizard", "Hogwarts", "Hermione", "Harry"),
                ("Queen", "Sussex", "William", "Harry"),
            ]
        )
        sentences.arrange(DOWN, buff=2.0, aligned_edge=RIGHT)
        sentences.to_edge(LEFT)

        def context_anim(group):
            self.play(
                ContextAnimation(
                    group[-1],
                    VGroup(*it.chain(*group[1:-1:2])),
                    direction=DOWN,
                    path_arc=PI / 4,
                    run_time=5,
                    lag_ratio=0.025,
                )
            )

        self.add(s1)
        context_anim(s1)
        self.wait()
        self.play(FadeTransformPieces(s1.copy(), s2))
        context_anim(s2)
