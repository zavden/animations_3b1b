# ==============================================================================
# Scene:      TableOfContents
# Source:     videos/_2024/puzzles/supplements.py (lines 4-72)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl TableOfContents.py TableOfContents -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class TableOfContents(InteractiveScene):
    def construct(self):
        # Test
        p_titles = VGroup(Text(f"Puzzle #{n}") for n in range(1, 6))
        subtitles = VGroup(map(Text, [
            "Twirling Tiles",
            "Tarski Plank Problem",
            "Monge's theorem",
            "Determining Det(M)",
            "The Hypercube Stack",
        ]))
        subtitles.set_color(GREY_B)
        titles = VGroup(VGroup(*pair) for pair in zip(p_titles, subtitles))
        for title in titles:
            title.arrange(DOWN, aligned_edge=LEFT)

        titles.arrange(DOWN, buff=LARGE_BUFF, aligned_edge=LEFT)
        titles.set_height(FRAME_HEIGHT - 1)
        titles.to_edge(LEFT)

        self.play(LaggedStartMap(FadeIn, titles, shift=LEFT, lag_ratio=0.25, run_time=2))
        self.wait()
        og_state = titles.copy()

        for i in range(5):
            target = og_state.copy()
            for j, title in enumerate(target):
                if i == j:
                    sf = 1.5
                    op = 1.0
                else:
                    sf = 0.75
                    op = 0.5
                title.scale(sf, about_edge=LEFT)
                title.set_opacity(op)
            target.arrange(DOWN, buff=1.0, aligned_edge=LEFT)
            target.set_height(FRAME_HEIGHT - 1)
            target.to_edge(LEFT)
            self.play(Transform(titles, target))
            self.wait()

        self.play(Transform(titles, og_state))

        # Morty referencing
        rect = SurroundingRectangle(titles[:3])
        rect.set_stroke(YELLOW, 3)
        randy = Randolph(height=4).flip()
        randy.body.insert_n_curves(10)
        randy.next_to(titles, RIGHT, buff=1.5)
        randy.to_edge(DOWN)

        self.play(
            randy.change("tease"),
            VFadeIn(randy),
            ShowCreation(rect),
            titles[3:].animate.set_opacity(0.5)
        )
        self.play(Blink(randy))
        self.play(randy.change("hooray"))
        self.play(Blink(randy))
        self.wait()

        # Gather them up
        self.play(
            FadeOut(rect),
            FadeOut(randy),
            titles[3:].animate.set_opacity(1)
        )
        self.wait()
