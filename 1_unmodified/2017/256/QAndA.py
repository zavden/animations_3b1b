# ==============================================================================
# Scene:      QAndA
# Source:     videos/_2017/256.py (lines 768-851)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl QAndA.py QAndA -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class QAndA(PiCreatureScene):
    def construct(self):
        self.pi_creature.center().to_edge(DOWN)
        self.show_powers_of_two()

        num_subscriber_words = OldTex(
            "> 2^{18} = 262{,}144", "\\text{ subscribers}"
        )
        num_subscriber_words.to_edge(UP)
        num_subscriber_words.shift(RIGHT)
        num_subscriber_words.set_color_by_tex("subscribers", RED)

        q_and_a = OldTexText("Q\\&A")
        q_and_a.next_to(self.pi_creature.get_corner(UP+LEFT), UP)
        q_and_a.save_state()
        q_and_a.shift(DOWN)
        q_and_a.set_fill(opacity = 0)

        reddit = OldTexText("reddit.com/r/3blue1brown")
        reddit.next_to(num_subscriber_words, DOWN, LARGE_BUFF)
        twitter = OldTexText("@3blue1brown")
        twitter.set_color(BLUE_C)
        twitter.next_to(reddit, DOWN)

        self.play(Write(num_subscriber_words))
        self.play(self.pi_creature.change, "gracious", num_subscriber_words)
        self.wait()
        self.play(
            q_and_a.restore,
            self.pi_creature.change, "raise_right_hand",
        )
        self.wait()
        self.play(Write(reddit))
        self.wait()
        self.play(
            FadeIn(twitter),
            self.pi_creature.change_mode, "shruggie"
        )
        self.wait(2)

    def show_powers_of_two(self):
        rows = 16
        cols = 64
        dots = VGroup(*[
            VGroup(*[
                Dot() for x in range(rows)
            ]).arrange(DOWN, buff = SMALL_BUFF)
            for y in range(cols)
        ]).arrange(RIGHT, buff = SMALL_BUFF)
        dots.set_width(FRAME_WIDTH - 2*LARGE_BUFF)
        dots.next_to(self.pi_creature, UP)
        dots = VGroup(*it.chain(*dots))
        top = dots.get_top()
        dots.sort(
            lambda p : get_norm(p-top)
        )

        powers_of_two = VGroup(*[
            Integer(2**i)
            for i in range(int(np.log2(rows*cols))+1)
        ])

        curr_power = powers_of_two[0]
        curr_power.to_edge(UP)
        self.play(
            Write(curr_power),
            FadeIn(dots[0])
        )
        for i, power_of_two in enumerate(powers_of_two):
            if i == 0:
                continue
            power_of_two.to_edge(UP)
            self.play(
                FadeIn(VGroup(*dots[2**(i-1) : 2**i])),
                Transform(
                    curr_power, power_of_two,
                    rate_func = squish_rate_func(smooth, 0, 0.5)
                )
            )
        self.wait()
        self.play(
            FadeOut(dots),
            FadeOut(powers_of_two)
        )
