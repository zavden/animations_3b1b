# ==============================================================================
# Scene:      Thumbnail
# Source:     videos/_2018/eop/combinations.py (lines 3599-3614)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl Thumbnail.py Thumbnail -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

def get_stack(
    obj1, obj2, n, k,
    fixed_start = None,
    fixed_end = None,
    obj_to_obj_buff = SMALL_BUFF,
    vertical_buff = MED_SMALL_BUFF,
    ):
    stack = VGroup()
    for indices in it.combinations(list(range(n)), k):
        term = VGroup(*[
             obj1.copy() if i in indices else obj2.copy()
            for i in range(n)
        ])
        if fixed_start:
            term.add_to_back(fixed_start.copy())
        if fixed_end:
            term.add(fixed_end.copy())
        term.arrange(RIGHT, buff = obj_to_obj_buff)
        stack.add(term)
    stack.arrange(DOWN, buff = vertical_buff)
    return stack


def get_stacks(obj1, obj2, n, **kwargs):
    stacks = VGroup()
    for k in range(n+1):
        stacks.add(get_stack(obj1, obj2, n, k, **kwargs))
    stacks.arrange(
        RIGHT, 
        buff = MED_LARGE_BUFF,
        aligned_edge = DOWN
    )
    return stacks


class Thumbnail(Scene):
    def construct(self):
        n_choose_k = OldTex("n \\choose k")
        n_choose_k[1].set_color(YELLOW)
        n_choose_k[2].set_color(YELLOW)
        n_choose_k.scale(2)
        n_choose_k.to_edge(UP)
        stacks = get_stacks(
            OldTex("1").set_color(PINK),
            OldTex("0").set_color(BLUE),
            n = 5, vertical_buff = SMALL_BUFF,
        )
        stacks.to_edge(DOWN)
        stacks.shift(MED_SMALL_BUFF*LEFT)

        self.add(n_choose_k, stacks)
