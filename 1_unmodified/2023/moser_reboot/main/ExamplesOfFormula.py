# ==============================================================================
# Scene:      ExamplesOfFormula
# Source:     videos/_2023/moser_reboot/main.py (lines 1154-1177)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ExamplesOfFormula.py ExamplesOfFormula -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ExamplesOfFormula(InteractiveScene):
    def construct(self):
        # Test
        examples = VGroup(*(
            self.get_example(n)
            for n in range(1, 7)
        ))
        examples.arrange(DOWN, buff=MED_LARGE_BUFF, aligned_edge=LEFT)
        examples.set_height(7)
        examples.to_edge(RIGHT)

        self.add(*(ex[0] for ex in examples))
        for ex in examples:
            self.play(FadeTransform(ex[0].copy(), ex[1]))
            self.wait(0.5)
        self.wait()

    def get_example(self, n):
        result = VGroup(
            Tex(fR"1 + {{{n} \choose 2 }} + {{{n} \choose 4 }}"),
            Tex(fR"= 1 + {choose(n, 2)} + {choose(n, 4)} = {1 + choose(n, 2) + choose(n, 4)}")
        )
        result.arrange(RIGHT)
        return result
