# ==============================================================================
# Scene:      WhatAHologramReconstructs
# Source:     videos/_2024/holograms/supplements.py (lines 920-956)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl WhatAHologramReconstructs.py WhatAHologramReconstructs -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class WhatAHologramReconstructs(InteractiveScene):
    def construct(self):
        # Test
        self.add(FullScreenRectangle())
        title = Text("What a Hologram reproduces", font_size=60)
        title.to_edge(UP, buff=MED_SMALL_BUFF)
        underline = Underline(title, buff=-0.05)

        items = VGroup(
            Text("1) Copy of the reference wave"),
            Text("2) Copy of the object wave"),
            TexText(R"3) Reflection$^*$ of the object wave"),
        )
        items.scale(0.8)
        items.arrange(DOWN, buff=1.75, aligned_edge=LEFT)
        items.next_to(underline, DOWN, LARGE_BUFF)
        items.to_edge(LEFT)

        self.play(
            FadeIn(title),
            ShowCreation(underline)
        )

        self.play(
            LaggedStart(
                (FadeIn(item[:2])
                for item in items),
                lag_ratio=0.05,
            )
        )
        self.wait()
        for n, item in enumerate(items):
            self.play(
                items[:n].animate.set_opacity(0.25),
                FadeIn(item[2:], lag_ratio=0.1)
            )
            self.wait()
