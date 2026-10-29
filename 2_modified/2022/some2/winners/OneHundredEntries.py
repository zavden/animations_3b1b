# ==============================================================================
# Scene:      OneHundredEntries
# Source:     videos/_2022/some2/winners.py (lines 503-633)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl OneHundredEntries.py OneHundredEntries -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - The logo in _lib/custom/logo.py passes sheen=0.0 to Circle (an argument manimgl no longer has): add_pupil is redefined without sheen in a local subclass
# ==============================================================================

from manim_imports_ext import *


# CHANGE: Logo (_lib/custom/logo.py) passes sheen=0.0 to Circle and manimgl no longer has that argument; add_pupil is redefined without sheen
class Logo(Logo):
    def add_pupil(self):
        self.pupil = Circle(
            radius=self.pupil_radius,
            fill_color=BLACK,
            fill_opacity=1,
            stroke_width=0,
            stroke_color=BLACK,
        )
        self.pupil.rotate(90 * DEGREES)
        self.add(self.pupil)


class OneHundredEntries(InteractiveScene):
    def construct(self):
        # Logos
        logos = Group(ImageMobject("Leios"), Logo())
        for logo in logos:
            logo.set_height(0.75)
        logos.arrange(RIGHT, buff=MED_LARGE_BUFF)
        logos.to_corner(UL)
        logos[1].flip().flip()

        # Winners
        title = Text("Winners", font_size=72)
        title.add(Underline(title).scale(1.5).insert_n_curves(20).set_stroke(width=(0, 3, 3, 3, 0)))
        title.to_edge(UP, buff=MED_SMALL_BUFF)
        title.set_color(GREY_A)

        winners = VGroup(
            VideoIcon(),
            self.written_icon(),
            *(VideoIcon() for x in range(3))
        )
        winners.set_fill(BLUE_D)
        winners[1].set_fill(GREY_A)
        for winner in winners:
            winner.set_height(0.75)
        winners.arrange(DOWN, buff=MED_LARGE_BUFF)
        winners.next_to(title, DOWN, buff=MED_LARGE_BUFF)
        winners.shift(1.5 * LEFT)

        prizes = VGroup(*(
            VGroup(
                Text("$1,000 + ", color=GREEN),
                Randolph(mode="thinking", height=0.5, color=YELLOW)
            ).arrange(RIGHT, buff=MED_SMALL_BUFF).next_to(winner, RIGHT)
            for winner in winners
        ))

        self.add(title)
        self.play(LaggedStartMap(FadeIn, winners, shift=0.5 * DOWN, lag_ratio=0.1, run_time=1))
        self.play(LaggedStartMap(FadeIn, prizes, shift=0.25 * RIGHT, lag_ratio=0.1, run_time=1))
        self.wait()
        self.play(LaggedStartMap(GrowFromCenter, logos, lag_ratio=0.7, run_time=1))
        self.wait()

        # Large batches
        videos = VideoIcon().get_grid(10, 8, fill_rows_first=False)
        videos.set_height(6)
        videos.set_fill(BLUE_D)

        articles = self.written_icon().get_grid(10, 3, fill_rows_first=False)
        articles.remove(*articles[-5:])
        articles.match_height(videos)
        articles.next_to(videos, RIGHT, buff=2.0)

        VGroup(videos, articles).center().to_edge(DOWN, buff=MED_SMALL_BUFF)

        video_title = Text("80 top videos").next_to(videos, UP, buff=MED_LARGE_BUFF)
        article_title = Text("25 top non-video entries").next_to(articles, UP, buff=MED_LARGE_BUFF)

        self.play(
            LaggedStart(*(
                ReplacementTransform(vid, random.choice(videos))
                for vid in (winners[0], *winners[2:])
            )),
            ReplacementTransform(winners[1], random.choice(articles)),
            LaggedStartMap(FadeIn, videos),
            LaggedStartMap(FadeIn, articles),
            FadeOut(title, UP),
            LaggedStartMap(FadeOut, prizes, shift=UP),
        )
        self.add(videos, articles)
        self.play(
            Write(video_title),
            Write(article_title),
        )
        self.wait()

        # Mention added judges
        guest_words = Text("With guest judging help from:")
        guest_words.next_to(videos, LEFT, LARGE_BUFF).align_to(video_title, UP)
        guest_words.set_color(GREY_A)
        frame = self.camera.frame
        frame.save_state()

        judges = VGroup(
            Text("Alex Kontorovich"),
            Text("Henry Reich"),
            Text("Mithuna Yoganathan"),
            Text("Nicky Case"),
            Text("Tai-Danae Bradley"),
            Text("Deniz Ozbay"),
            Text("Jeffrey Wack"),
            Text("Fran Herr"),
        )
        judges.arrange(DOWN, aligned_edge=LEFT)
        judges.next_to(guest_words, DOWN, LARGE_BUFF)

        momath_brace = Brace(judges[-3:], RIGHT)
        momath_words = momath_brace.get_text("MoMath\nMuseum", buff=MED_SMALL_BUFF)
        momath = VGroup(momath_brace, momath_words)
        momath.set_color(YELLOW)

        self.play(
            frame.animate.scale(1.5, about_edge=RIGHT),
            FadeIn(guest_words),
            logos.animate.next_to(guest_words, UP),
            LaggedStartMap(FadeIn, judges, shift=0.5 * RIGHT, lag_ratio=0.5, run_time=6),
        )
        self.play(
            FadeIn(momath)
        )
        self.wait()

        # Return
        self.play(
            frame.animate.restore(),
            LaggedStart(*(
                FadeOut(mob, UL)
                for mob in [video_title, article_title, *logos, guest_words, *judges, momath]
            ), run_time=1)
        )
        self.wait()

    def written_icon(self):
        rect = Rectangle(height=0.1, width=1.5)
        rect.set_fill(WHITE, 1)
        rect.set_stroke(WHITE, 0)
        result = rect.get_grid(4, 1, buff=0.2)
        result[-1].stretch(0.5, 0, about_edge=LEFT)

        return result
