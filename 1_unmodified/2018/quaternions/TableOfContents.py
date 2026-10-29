# ==============================================================================
# Scene:      TableOfContents
# Source:     videos/_2018/quaternions.py (lines 1165-1199)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl TableOfContents.py TableOfContents -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class TableOfContents(Scene):
    def construct(self):
        chapters = VGroup(
            OldTexText(
                "\\underline{Chapter 1}\\\\", "Linus the Linelander"
            ),
            OldTexText(
                "\\underline{Chapter 2}\\\\", "Felix the Flatlander"
            ),
            OldTexText(
                "\\underline{Chapter 3}\\\\", " You, the 3d-lander"
            ),
        )
        for chapter in chapters:
            chapter.space_out_submobjects(1.5)
        chapters.arrange(
            DOWN, buff=1.5, aligned_edge=LEFT
        )
        chapters.to_edge(LEFT)

        for chapter in chapters:
            self.play(FadeInFromDown(chapter))
            self.wait(2)
        for chapter in chapters:
            chapters.save_state()
            other_chapters = VGroup(*[
                c for c in chapters if c is not chapter
            ])
            self.play(
                chapter.set_width, 0.5 * FRAME_WIDTH,
                chapter.center,
                other_chapters.fade, 1
            )
            self.wait(3)
            self.play(chapters.restore)
