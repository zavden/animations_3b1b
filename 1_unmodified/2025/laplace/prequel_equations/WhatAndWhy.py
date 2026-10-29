# ==============================================================================
# Scene:      WhatAndWhy
# Source:     videos/_2025/laplace/prequel_equations.py (lines 201-218)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl WhatAndWhy.py WhatAndWhy -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class WhatAndWhy(InteractiveScene):
    def construct(self):
        words = VGroup(
            Tex(R"\text{1) Understanding } e^{i {t}} \\ \text{ intuitively}", t2c={R"{t}": GREY_B}),
            TexText(R"2) How they \\ \quad \quad naturally arise"),
        )
        words[0][R"intuitively"].align_to(words[0]["Understanding"], LEFT)
        words[1][R"naturally arise"].align_to(words[1]["How"], LEFT)
        words.refresh_bounding_box()
        words.scale(1.25)
        self.add(words)
        words.arrange(DOWN, aligned_edge=LEFT, buff=2.5)
        words.next_to(ORIGIN, RIGHT)
        words.set_opacity(0)
        for word, u in zip(words, [1, -1]):
            word.set_opacity(1)
            self.play(Write(word))
            self.wait()
