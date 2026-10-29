# ==============================================================================
# Scene:      TableOfContents
# Source:     videos/_2019/hyperdarts.py (lines 413-449)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl TableOfContents.py TableOfContents -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class TableOfContents(Scene):
    def construct(self):
        rect = FullScreenFadeRectangle(opacity=0.75)
        self.add(rect)

        parts = VGroup(
            OldTexText("The game"),
            OldTexText("The puzzle"),
            OldTexText("The micropuzzles"),
            OldTexText("The answer"),
        )

        parts.scale(1.5)
        parts.arrange(DOWN, buff=LARGE_BUFF, aligned_edge=LEFT)
        parts.to_edge(LEFT, buff=2)

        parts.set_opacity(0.5)
        self.add(parts)

        for part in parts:
            dot = Dot()
            dot.next_to(part, LEFT, SMALL_BUFF)
            dot.match_style(part)
            self.add(dot)

        last_part = VMobject()
        last_part.save_state()

        for part in parts:
            part.save_state()
            self.play(
                part.scale, 1.5, {"about_edge": LEFT},
                part.set_opacity, 1,
                Restore(last_part)
            )
            self.wait()
            last_part = part
