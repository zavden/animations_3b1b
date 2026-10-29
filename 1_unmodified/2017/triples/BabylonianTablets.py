# ==============================================================================
# Scene:      BabylonianTablets
# Source:     videos/_2017/triples.py (lines 268-305)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl BabylonianTablets.py BabylonianTablets -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class BabylonianTablets(Scene):
    def construct(self):
        title = OldTexText("Plimpton 322 Tablets \\\\ (1800 BC)")
        title.to_corner(UP+LEFT)
        ac_pairs = [
            (119, 169),
            (3367, 4825),
            (4601, 6649),
            (12709, 18541),
            (65, 97),
            (319, 481),
            (2291, 3541),
            (799, 1249),
            (481, 769),
            (4961, 8161),
            (45, 75),
            (1679, 2929),
            (161, 289),
            (1771, 3229),
            (56, 106),
        ]
        triples = VGroup()
        for a, c in ac_pairs:
            b = int(np.sqrt(c**2 - a**2))
            tex = "%s^2 + %s^2 = %s^2"%tuple(
                map("{:,}".format, [a, b, c])
            )
            tex = tex.replace(",", "{,}")
            triple = OldTex(tex)
            triples.add(triple)
        triples.arrange(DOWN, aligned_edge = LEFT)
        triples.set_height(FRAME_HEIGHT - LARGE_BUFF)
        triples.to_edge(RIGHT)

        self.add(title)
        self.wait()
        self.play(LaggedStartMap(FadeIn, triples, run_time = 5))
        self.wait()
