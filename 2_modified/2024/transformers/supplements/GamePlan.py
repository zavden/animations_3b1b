# ==============================================================================
# Scene:      GamePlan
# Source:     videos/_2024/transformers/supplements.py (lines 330-519)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl GamePlan.py GamePlan -w -m --fps 15
#
# Placeholder assets (not Grant's originals):
#   - raster_images/nn1_thumbnail.png ... nn4_thumbnail.png (placeholder)
#   - raster_images/Chapter5.png ... Chapter7.png (placeholder; Grant's Dropbox paths, which _lib resolves by name)
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class GamePlan(InteractiveScene):
    screen_opacity = 0.0

    def construct(self):
        # Setup up icons
        self.add(FullScreenRectangle())
        videos = VideoIcon().get_grid(7, 1, buff_ratio=0.3)
        videos.set_fill(BLUE_B)
        videos.set_height(6.5)
        videos.to_corner(UL)
        column_x = videos.get_x()

        nn_vids = videos[:4]
        tr_vids = videos[4:]
        tr_vids.save_state()
        tr_vids.scale(1.25)
        tr_vids.space_out_submobjects(1.25)
        tr_vids.set_y(0).to_edge(LEFT)

        def highlight_video(video, group=videos):
            for vid in group:
                vid.target = vid.generate_target()
                if vid is video:
                    vid.target.set_x(column_x + 0.5)
                    vid.target.set_opacity(1)
                else:
                    vid.target.set_x(column_x)
                    vid.target.set_opacity(0.5)
            return LaggedStartMap(MoveToTarget, group, lag_ratio=0.01, run_time=1)

        self.add(tr_vids)

        # Here now
        here_arrow = Vector(0.75 * LEFT, stroke_width=10)
        here_arrow.set_color(RED).next_to(tr_vids[0], RIGHT)
        here_words = Text("You are\nhere")
        here_words.next_to(here_arrow, RIGHT)
        here_words.set_color(RED)
        here_group = VGroup(here_arrow, here_words)

        self.play(
            highlight_video(tr_vids[0], tr_vids),
            MaintainPositionRelativeTo(here_group, tr_vids[0]),
            VFadeIn(here_group),
        )
        self.wait()

        # First chapter
        curly = self.get_curly_brace(tr_vids[0])

        topics = VGroup(
            Text("Beginning"),
            Text("Ending"),
            Text("Background material"),
            Text("Premise of deep learning"),
            Text("Word embeddings"),
            Text("Dot products"),
            Text("Softmax"),
        )
        topics.arrange(DOWN, buff=0.5, aligned_edge=LEFT)
        topics.next_to(curly.get_corner(UR), DR, buff=0.25)
        for topic in topics[-4:]:
            topic.scale(0.8, about_edge=LEFT)
            topic.shift(0.5 * RIGHT)
            dot = Dot(color=WHITE)
            dot.next_to(topic, LEFT)
            topic.add(dot)

        screen = ScreenRectangle()
        screen.set_fill(BLACK, 1)
        screen.set_stroke(WHITE, 2)
        screen.set_opacity(self.screen_opacity)
        screen.set_height(5)
        screen.next_to(topics[0], DOWN, aligned_edge=LEFT)

        self.play(
            FadeOut(here_group),
            ShowCreation(curly),
            FadeIn(screen, RIGHT),
            FadeInFromPoint(topics[0], here_group.get_center()),
        )
        self.wait()
        self.play(
            topics[0].animate.set_opacity(0.5),
            FadeIn(topics[1]),
            screen.animate.next_to(topics[1], DOWN, aligned_edge=LEFT)
        )
        self.wait()
        self.play(
            screen.animate.scale(0.5, about_edge=DR).to_edge(RIGHT),
            topics[1].animate.set_opacity(0.5),
            LaggedStartMap(FadeIn, topics[2:], shift=0.1 * DOWN, lag_ratio=0.5)
        )
        self.wait()

        # Second chapter
        new_curly = self.get_curly_brace(tr_vids[1].copy().shift(0.5 * RIGHT))
        screen.target = screen.generate_target()
        screen.target.set_height(5)
        screen.target.next_to(curly, RIGHT)
        att_title = Text("Attention")
        att_title.next_to(screen.target, UP, aligned_edge=LEFT)
        self.play(
            highlight_video(tr_vids[1], tr_vids),
            curly.animate.become(new_curly),
            FadeOut(topics),
            MoveToTarget(screen),
            FadeInFromPoint(att_title, tr_vids[1].get_center()),
        )
        self.wait()

        # Third chapter
        new_curly = self.get_curly_brace(tr_vids[2].copy().shift(0.5 * RIGHT))
        chapter3_topics = Text(
            "MLPs, Training, Positional encodings, ..."
        )
        chapter3_topics.next_to(screen, UP, aligned_edge=LEFT)

        self.play(
            highlight_video(tr_vids[2], tr_vids),
            curly.animate.become(new_curly),
            FadeOut(att_title),
            FadeIn(chapter3_topics, lag_ratio=0.1, time_span=(1, 3)),
        )
        self.wait()

        # Show earlier chapters
        prev_thumbnails = Group(
            ImageMobject(f"nn{k}_thumbnail.png")
            for k in range(1, 5)
        )
        prev_thumbnails.arrange(RIGHT, buff=1.0)
        prev_thumbnails.set_width(FRAME_WIDTH - 2)
        prev_thumbnails.move_to(2 * UP)

        tn_dir = "/Users/grant/3Blue1Brown Dropbox/3Blue1Brown/videos/2024/transformers/Thumbnails/"
        new_thumbnails = Group(
            ImageMobject(os.path.join(tn_dir, f"Chapter{n}"))
            for n in range(5, 8)
        )
        for tn1, tn2 in zip(prev_thumbnails, new_thumbnails):
            tn2.replace(tn1, stretch=True)
            tn2.next_to(tn1, DOWN, buff=1.0)
        chapter_titles = VGroup(
            Text(f"Chapter {k}", font_size=30)
            for k in range(1, 8)
        )
        for title, rect in zip(chapter_titles, (*prev_thumbnails, *new_thumbnails)):
            title.next_to(rect, UP, buff=0.2, aligned_edge=LEFT)

        tr_rect = SurroundingRectangle(
            Group(new_thumbnails, chapter_titles[4:]),
            buff=0.25
        )
        tr_rect.set_stroke(BLUE, 2)
        tr_label = Text("Transformers")
        tr_label.next_to(tr_rect, DOWN)

        self.play(
            FadeOut(curly),
            FadeOut(screen),
            FadeOut(chapter3_topics),
            LaggedStartMap(FadeIn, chapter_titles,),
            FadeIn(prev_thumbnails, shift=0.5 * UP, lag_ratio=0.25),
            *(
                FadeTransform(vid, tn)
                for vid, tn in zip(tr_vids, new_thumbnails)
            ),
        )
        self.play(
            ShowCreation(tr_rect),
            FadeIn(tr_label),
        )
        self.wait()

    def get_curly_brace(self, video, width=2.0, height=6.5, buff=0.1):
        start = video.get_right() + buff * RIGHT
        top_point = np.array([start[0] + width, 0.5 * height, 0])
        low_point = np.array([start[0] + width, -0.5 * height, 0])
        result = VGroup(
            CubicBezier(
                start,
                start + width * RIGHT,
                point + width * LEFT,
                point,
            )
            for point in [top_point, low_point]
        )
        result.set_stroke(GREY_A, 2)
        return result
