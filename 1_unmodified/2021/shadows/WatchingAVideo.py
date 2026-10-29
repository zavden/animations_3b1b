# ==============================================================================
# Scene:      WatchingAVideo
# Source:     videos/_2021/shadows.py (lines 6049-6071)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl WatchingAVideo.py WatchingAVideo -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class WatchingAVideo(Scene):
    def construct(self):
        self.add(FullScreenRectangle())
        randy = Randolph()
        randy.to_corner(DL)
        screen = ScreenRectangle(height=5)
        screen.set_fill(BLACK, 1)
        screen.to_corner(UR)

        def blink_wait(n=1):
            for x in range(n):
                self.wait()
                self.play(Blink(randy))
                self.wait()

        self.add(screen)
        self.add(randy)
        self.play(randy.change("pondering", screen))
        blink_wait()
        self.play(randy.change("thinking", screen))
        blink_wait()
        self.play(randy.change("hesitant", screen))
        blink_wait(2)
