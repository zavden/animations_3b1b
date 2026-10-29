# ==============================================================================
# Scene:      StatisticsVsEmpathy
# Source:     videos/_2018/eop/bayes_footnote.py (lines 1084-1156)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl StatisticsVsEmpathy.py StatisticsVsEmpathy -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

SICKLY_GREEN = "#9BBD37"


class StatisticsVsEmpathy(PiCreatureScene):
    def construct(self):
        randy, morty = self.randy, self.morty
        sick_one = PiCreature()
        sick_one.scale(0.5)
        sick_group = VGroup(
            sick_one, VectorizedPoint(sick_one.get_bottom())
        )
        priors = VGroup(*[
            OldTex("%.1f"%p+ "\\%").move_to(ORIGIN, RIGHT)
            for p in np.arange(0.1, 2.0, 0.1)
        ])
        priors.next_to(randy, UP+LEFT, LARGE_BUFF)
        prior = priors[0]
        prior.save_state()

        self.play(PiCreatureSays(
            morty, 
            "1 in 1{,}000 people \\\\ have this disease.",
            look_at = randy.eyes
        ))
        self.play(randy.change, "pondering", morty.eyes)
        self.wait()
        self.play(Write(prior))
        self.wait()
        self.play(
            prior.scale, 0.1,
            prior.set_fill, None, 0,
            prior.move_to, randy.eyes
        )
        self.wait()
        self.play(
            PiCreatureBubbleIntroduction(
                randy, sick_group,
                target_mode = "guilty",
                bubble_type = ThoughtBubble,
                content_introduction_class = FadeIn,
                look_at = sick_one,
            ),
            RemovePiCreatureBubble(morty)
        )
        self.play(
            sick_one.change_mode, "sick",
            sick_one.set_color, SICKLY_GREEN
        )
        self.wait()

        probably_me = OldTexText("That's probably \\\\ me")
        probably_me.next_to(sick_one, DOWN)
        target_sick_group = VGroup(
            sick_one.copy(),
            probably_me
        )
        target_sick_group.scale(0.8)
        self.pi_creature_thinks(
            target_sick_group,
            target_mode = "pleading",
        )
        self.wait(2)

        self.play(prior.restore)
        for new_prior in priors[1:]:
            self.play(Transform(prior, new_prior, run_time = 0.5))
        self.wait()

    ######

    def create_pi_creatures(self):
        randy = self.randy = Randolph()
        morty = self.morty = Mortimer()
        randy.to_edge(DOWN).shift(3*LEFT)
        morty.to_edge(DOWN).shift(3*RIGHT)
        return VGroup(randy, morty)
