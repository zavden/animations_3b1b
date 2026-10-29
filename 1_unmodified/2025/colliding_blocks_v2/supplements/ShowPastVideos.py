# ==============================================================================
# Scene:      ShowPastVideos
# Source:     videos/_2025/colliding_blocks_v2/supplements.py (lines 4-69)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ShowPastVideos.py ShowPastVideos -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ShowPastVideos(InteractiveScene):
    def construct(self):
        # Show the video
        title = Text("2019 Video:", font_size=72)
        title[-1].set_opacity(0)
        title.to_edge(UP)
        background = FullScreenFadeRectangle()
        background.set_fill(GREY_E, 1)
        screen = ScreenRectangle().set_height(6)
        screen.next_to(title, DOWN)
        screen.set_fill(BLACK, 1).set_stroke(WHITE, 2)

        vertical_frame = screen.copy().set_shape(7 * 9 / 16, 7)
        vertical_frame.to_corner(UR)
        vertical_frame.match_style(screen)

        self.add(background, screen)
        self.play(
            Write(title),
            VShowPassingFlash(screen.copy().set_fill(opacity=0).set_stroke(BLUE, 4).insert_n_curves(20), time_width=1.5, run_time=3),
        )
        self.wait()

        # Three versions
        versions = VGroup(
            Text("2019 video: "),
            Text("Adapted as a short:\n(separate channel) ", alignment="LEFT"),
            Text("Re-posted to this channel: "),
        )
        versions[1]["(separate channel)"].set_fill(GREY_B)
        versions.arrange(DOWN, buff=1.0, aligned_edge=LEFT)
        versions.to_corner(UL)

        counts = VGroup(
            Text("13.8M Views").set_color(YELLOW),
            Text("42.6M Views").set_color(ORANGE),
            Text("62.0M Views").set_color(RED),
        )
        for version, count in zip(versions, counts):
            count.next_to(version, RIGHT, aligned_edge=UP)

        explanation = VGroup(
            Text("My only reason for making shorts at all"),
            Text("is to pique the curiosity of people in the shorts feed and"),
            Text("encourage them to pop out for a full explanation. Originally I didn't"),
            Text("want to trash up this channel with shorts, but then the only way to link to"),
            Text("link to a long-form videos was if the short lived on the same channel.  ¯\\_(ツ)_/¯"),
        )
        for part in explanation:
            part.match_width(versions[2])
        explanation.arrange(DOWN, buff=0.15)
        explanation.set_fill(GREY_B)
        explanation.next_to(versions[2], DOWN, buff=0.5)

        self.play(
            Transform(title, versions[0]),
            FadeIn(counts[0]),
            Transform(screen, vertical_frame)
        )
        for i in [1, 2]:
            self.play(
                FadeIn(versions[i]),
                FadeIn(counts[i], lag_ratio=0.1,)
            )
        self.play(FadeIn(explanation, lag_ratio=0.01, run_time=1))
        self.wait()
