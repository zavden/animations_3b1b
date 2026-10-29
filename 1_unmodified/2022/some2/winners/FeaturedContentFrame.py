# ==============================================================================
# Scene:      FeaturedContentFrame
# Source:     videos/_2022/some2/winners.py (lines 636-672)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl FeaturedContentFrame.py FeaturedContentFrame -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class FeaturedContentFrame(InteractiveScene):
    title = "Example Title"
    thumbnail = "Lion"
    author = "author"
    frame_scale_factor = 0.75

    def construct(self):
        # Frames
        self.add(FullScreenRectangle())

        frame = ScreenRectangle()
        frame.set_fill(BLACK, 1)
        frame.set_stroke(WHITE, 2)
        frame.set_height(self.frame_scale_factor * FRAME_HEIGHT)
        frame.to_edge(DOWN, buff=MED_SMALL_BUFF)
        self.add(frame)

        # Title
        title = Text(self.title, font_size=66)
        title.set_max_width(FRAME_WIDTH - 1)
        title.to_edge(UP, buff=MED_SMALL_BUFF)
        author = Text("by " + self.author, font_size=48, color=GREY_A)
        author.move_to(midpoint(title.get_bottom(), frame.get_top()))

        if self.thumbnail:
            thumbnail = ImageMobject(self.thumbnail)
            thumbnail.replace(frame, dim_to_match=1)
        else:
            thumbnail = Mobject()

        self.play(
            Write(title, run_time=1),
            DrawBorderThenFill(frame),
            FadeIn(thumbnail),
        )
        self.play(FadeIn(author, shift=0.5 * DOWN))
        self.wait()
