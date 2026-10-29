# ==============================================================================
# Scene:      TableOfContents
# Source:     videos/_2020/sir.py (lines 1651-1685)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl TableOfContents.py TableOfContents -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class TableOfContents(Scene):
    def construct(self):
        chapters = VGroup(
            OldTexText("Basic setup"),
            OldTexText("Identify and isolate"),
            OldTexText("Social distancing"),
            OldTexText("Travel restrictions"),
            OldTexText("$R$"),
            OldTexText("Central hubs"),
        )
        chapters.arrange(DOWN, buff=MED_LARGE_BUFF, aligned_edge=LEFT)
        chapters.set_height(FRAME_HEIGHT - 1)
        chapters.to_edge(LEFT, buff=LARGE_BUFF)

        for chapter in chapters:
            dot = Dot()
            dot.next_to(chapter, LEFT, SMALL_BUFF)
            chapter.add(dot)
            chapter.save_state()

        self.add(chapters)

        for chapter in chapters:
            non_chapter = [c for c in chapters if c is not chapter]
            chapter.target = chapter.saved_state.copy()
            chapter.target.scale(1.5, about_edge=LEFT)
            chapter.target.set_fill(YELLOW, 1)
            for nc in non_chapter:
                nc.target = nc.saved_state.copy()
                nc.target.scale(0.8, about_edge=LEFT)
                nc.target.set_fill(WHITE, 0.5)
            self.play(*map(MoveToTarget, chapters))
            self.wait()
        self.play(*map(Restore, chapters))
        self.wait()
