# ==============================================================================
# Scene:      LookOverTweet
# Source:     videos/_2020/med_test.py (lines 5789-5927)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl LookOverTweet.py LookOverTweet -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class LookOverTweet(Scene):
    def construct(self):
        # Tweet
        bg_rect = FullScreenFadeRectangle()
        bg_rect.set_fill(GREY_E, 1)
        self.add(bg_rect)

        tweet = ImageMobject("twitter_covid_test_poll")
        tweet.set_height(6)
        tweet.to_edge(LEFT)
        self.play(FadeIn(tweet, shift=UP, scale=1.2))
        self.wait()

        # Tweet highlights
        lines = VGroup(
            Line((-3.9, 1.7), (0.3, 1.7)),
            Line((-3.4, 0.1), (-0.7, 0.1)),
            VGroup(
                Line((0.2, 0.1), (0.8, 0.1)),
                Line((-6.4, -0.3), (-4, -0.3)),
            ),
        )
        lines.set_color(RED)

        rects = VGroup(*(Rectangle(3.2, 0.37) for x in range(4)))
        rects.arrange(DOWN, buff=0.08)
        rects.set_stroke(BLUE, 3)
        rects.set_fill(BLUE, 0.25)
        rects.move_to((-4.8, -1.66, 0.))

        # Population
        icon = SVGMobject("person")
        icon.set_stroke(width=0)
        globals()['icon'] = icon
        population = VGroup(*(icon.copy() for x in range(1000)))

        population.scale(1 / population[0].get_height())
        population.arrange_in_grid(
            30, 33,
            buff=MED_LARGE_BUFF,
        )
        population.set_width(4)
        population.to_edge(RIGHT)
        population.set_fill(GREY_B)
        population[random.randint(0, 1000)].set_fill(YELLOW)

        pop_title = OldTexText("1", " in ", "1,000")
        pop_title[0].set_color(YELLOW)
        pop_title.next_to(population, UP)

        self.play(
            FadeIn(pop_title, shift=0.25 * UP),
            ShowIncreasingSubsets(population),
            ShowCreation(lines[0])
        )
        self.wait()

        pop_group = VGroup(population, pop_title)

        # Positive result
        clipboard = SVGMobject("clipboard")
        clipboard.set_stroke(width=0)
        clipboard.set_fill(interpolate_color(GREY_BROWN, WHITE, 0.5), 1)
        clipboard.set_width(2.5)
        clipboard.move_to(population)
        clipboard.to_edge(UP)

        result = OldTexText(
            "+\\\\",
            "SARS\\\\CoV-2\\\\",
            "Detected"
        )
        result[0].scale(1.5, about_edge=DOWN)
        result[0].set_fill(GREEN)
        result[0].set_stroke(GREEN, 2)
        result[-1].set_fill(GREEN)
        result.set_width(clipboard.get_width() * 0.7)
        result.move_to(clipboard)
        result.shift(0.2 * DOWN)
        clipboard.add(result)

        self.play(
            pop_group.scale, 0.4,
            pop_group.to_edge, DOWN,
            FadeIn(clipboard, DOWN),
        )
        self.wait()

        # FPR, FRN
        self.play(ShowCreation(lines[1]))
        self.wait()
        self.play(ShowCreation(lines[2]))
        self.wait()

        # Answer choices
        rect = rects[0].copy()
        self.play(DrawBorderThenFill(rect))
        self.wait()
        for r2 in rects[1:]:
            self.play(Transform(rect, r2))
            self.wait()
        self.play(FadeOut(rect))

        # Focus on FPR
        rect = Rectangle()
        rect.match_width(lines[1])
        rect.scale(1.02)
        rect.set_height(0.4, stretch=True)
        rect.match_style(lines[1])
        rect.move_to(lines[1], DOWN)
        rect.set_fill(RED, 0.2)

        self.play(
            FadeOut(lines[0]),
            FadeOut(lines[2]),
            DrawBorderThenFill(rect)
        )

        # Randy
        randy = Randolph(height=2)
        randy.flip()
        randy.next_to(tweet, RIGHT, LARGE_BUFF, DOWN)

        bubble = randy.get_bubble(height=3, width=3, direction=RIGHT)
        bubble.flip()
        bubble.write("99\\%\\\\right?")

        self.play(
            FadeIn(randy),
            FadeOut(clipboard, RIGHT),
            FadeOut(pop_group, 0.5 * RIGHT),
        )
        self.play(
            randy.change, "maybe",
            DrawBorderThenFill(bubble),
            Write(bubble.content),
        )
        self.play(Blink(randy))
        self.wait()
