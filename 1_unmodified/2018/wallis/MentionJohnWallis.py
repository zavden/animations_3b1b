# ==============================================================================
# Scene:      MentionJohnWallis
# Source:     videos/_2018/wallis.py (lines 4043-4070)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl MentionJohnWallis.py MentionJohnWallis -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class WallisNumeratorDenominatorGenerator(object):
    def __init__(self):
        self.n = 0

    def __iter__(self):
        return self

    def __next__(self):
        return next(self)

    def __next__(self):
        n = self.n
        self.n += 1
        if n % 2 == 0:
            return (n + 2, n + 1)
        else:
            return (n + 1, n + 2)


def get_wallis_product(n_terms=6, show_result=True):
    tex_mob_args = []
    nd_generator = WallisNumeratorDenominatorGenerator()
    for x in range(n_terms):
        numerator, denominator = next(nd_generator)
        tex_mob_args += [
            "{%d" % numerator, "\\over", "%d}" % denominator, "\\cdot"
        ]
    tex_mob_args[-1] = "\\cdots"
    if show_result:
        tex_mob_args += ["=", "{\\pi", "\\over", "2}"]

    result = OldTex(*tex_mob_args)
    return result


class MentionJohnWallis(Scene):
    def construct(self):
        product = get_wallis_product(10)
        product.to_edge(UP)

        name = OldTexText("``Wallis product''")
        name.scale(1.5)
        name.set_color(BLUE)
        name.next_to(product, DOWN, MED_LARGE_BUFF)

        image = ImageMobject("John_Wallis")
        image.set_height(3)
        image.next_to(name, DOWN)
        image_name = OldTexText("John Wallis")
        image_name.next_to(image, DOWN)

        infinity = OldTex("\\infty")
        infinity.set_height(1.5)
        infinity.next_to(image, RIGHT, MED_LARGE_BUFF)

        self.add(product)
        self.wait()
        self.play(Write(name))
        self.play(GrowFromEdge(image, UP))
        self.play(Write(image_name))
        self.wait(2)
        self.play(Write(infinity, run_time=3))
        self.wait(2)
