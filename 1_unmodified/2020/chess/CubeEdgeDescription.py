# ==============================================================================
# Scene:      CubeEdgeDescription
# Source:     videos/_2020/chess.py (lines 2833-2886)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl CubeEdgeDescription.py CubeEdgeDescription -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

def string_to_bools(message):
    # For easter eggs on the board
    as_int = int.from_bytes(message.encode(), 'big')
    bits = "{0:b}".format(as_int)
    bits = (len(message) * 8 - len(bits)) * '0' + bits
    return [bool(int(b)) for b in bits]


class CubeEdgeDescription(Scene):
    CONFIG = {
        "camera_config": {"background_color": GREY_E}
    }

    def construct(self):
        bits = VGroup(*[
            VGroup(*[
                Integer(int(b))
                for b in string_to_bools(char)
            ]).arrange(RIGHT, buff=SMALL_BUFF)
            for char in "hi"
        ])
        bits.arrange(DOWN, buff=LARGE_BUFF)
        arrow = Arrow(
            bits[0][7].get_bottom(),
            bits[1][7].get_top(),
            buff=SMALL_BUFF,
            tip_config={"length": 0.15, "width": 0.15}
        )
        arrow.set_color(BLUE)
        words = OldTexText("Bit flip")
        words.set_color(BLUE)
        words.next_to(arrow, LEFT)
        bf_group = VGroup(bits, arrow, words)
        parens = OldTex("()")[0]
        parens.scale(2)
        parens.match_height(bf_group, stretch=True)
        parens[0].next_to(bf_group, LEFT, SMALL_BUFF)
        parens[1].next_to(bf_group, RIGHT, SMALL_BUFF)
        bf_group.add(parens)
        bf_group.to_edge(UP)

        cube_words = OldTexText("Edge of an\\\\n-dimensional cube")
        top_group = VGroup(
            bf_group,
            Vector(RIGHT),
            cube_words
        )
        top_group.arrange(RIGHT)
        top_group.to_edge(UP)

        self.add(bf_group)
        self.play(
            TransformFromCopy(*bits),
            GrowArrow(arrow),
            FadeIn(words, 0.25 * UP)
        )
        self.wait()
        self.play(
            GrowArrow(top_group[1]),
            FadeIn(cube_words, LEFT)
        )
        self.wait()
