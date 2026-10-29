# ==============================================================================
# Scene:      IntroduceTelepathyExample
# Source:     videos/_2018/eop/bayes_footnote.py (lines 1199-1339)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl IntroduceTelepathyExample.py IntroduceTelepathyExample -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - ask_about_chances: define randy, morty from self (undefined in the original)
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


class IntroduceTelepathyExample(StatisticsVsEmpathy):
    def construct(self):
        self.force_skipping()

        self.show_mind_reading_powers()
        self.claim_mind_reading_powers()
        self.generate_random_number()
        self.guess_number_correctly()
        self.ask_about_chances()
        self.revert_to_original_skipping_status()
        self.say_you_probably_got_lucky()

    def show_mind_reading_powers(self):
        randy, morty = self.randy, self.morty
        title = OldTexText("1 in 1{,}000 read minds")
        title.to_edge(UP)

        self.add(title)
        self.read_mind(randy, morty)

        self.title = title

    def claim_mind_reading_powers(self):
        randy, morty = self.randy, self.morty
        self.play(PiCreatureSays(
            randy, "I have the gift.",
            run_time = 1,
            look_at = morty.eyes,
        ))
        self.wait()
        self.play(RemovePiCreatureBubble(
            randy,
            target_mode = "happy",
            look_at = morty.eyes
        ))

    def generate_random_number(self):
        morty = self.morty
        bubble = morty.get_bubble("", direction = LEFT)
        numbers = [
            Integer(random.choice(list(range(100))))
            for x in range(30)
        ]
        numbers.append(Integer(67))
        for number in numbers:
            number.next_to(morty, UP, LARGE_BUFF, RIGHT)


        for number in numbers:
            self.add(number)
            Scene.wait(self, 0.1)
            self.remove(number)
        self.play(
            ShowCreation(bubble),
            number.move_to, bubble.get_bubble_center(), DOWN+LEFT,
            morty.change, "pondering", 
        )
        self.wait()

        morty.bubble = bubble
        self.number = number

    def guess_number_correctly(self):
        randy, morty = self.randy, self.morty
        number_copy = self.number.copy()

        self.read_mind(randy, morty)
        self.play(PiCreatureSays(
            randy, number_copy,
            target_mode = "hooray",
            look_at = morty.eyes
        ))
        self.wait()

    def ask_about_chances(self):
        # CHANGE: morty was used without being defined (bug of the original); take the scene attributes
        randy, morty = self.randy, self.morty
        probability = OldTex(
            "P(", "\\text{Telepath }", "|", "\\text{ Correct}", ")",
            "=", "???"
        )
        probability.set_color_by_tex("Telepath", BLUE)
        probability.set_color_by_tex("Correct", GREEN)
        probability.to_edge(UP)

        self.play(morty.change, "confused", randy.eyes)
        self.wait()
        self.play(ReplacementTransform(
            self.title, VGroup(*it.chain(*probability))
        ))
        self.wait()

    def say_you_probably_got_lucky(self):
        randy, morty = self.randy, self.morty

        self.play(
            PiCreatureSays(
                morty, "You probably \\\\ got lucky.",
                target_mode = "sassy",
                look_at = randy.eyes,
                bubble_config = {"height" : 3, "width" : 4}
            ),
            RemovePiCreatureBubble(
                randy, 
                target_mode = "plain",
                look_at = morty.eyes,
            )
        )
        self.wait(2)


    ###

    def read_mind(self, pi1, pi2):
        self.play(pi1.change, "telepath", pi2.eyes)
        self.send_mind_waves(pi1, pi2)
        self.send_mind_waves(pi2, pi1)
        self.wait()

    def send_mind_waves(self, pi1, pi2):
        angle = np.pi/3
        n_arcs = 5
        vect = pi2.eyes.get_center() - pi1.eyes.get_center()
        vect[1] = 0

        arc = Arc(angle = angle)
        arc.rotate(-angle/2 + angle_of_vector(vect), about_point = ORIGIN)
        arc.scale(3)
        arcs = VGroup(*[arc.copy() for x in range(n_arcs)])
        arcs.move_to(pi2.eyes.get_center(), vect)
        arcs.set_stroke(BLACK, 0)
        for arc in arcs:
            arc.save_state()
        arcs.scale(0.1)
        arcs.move_to(pi1.eyes, vect)
        arcs.set_stroke(WHITE, 4)

        self.play(LaggedStartMap(
            ApplyMethod, arcs,
            lambda m : (m.restore,),
            lag_ratio = 0.7,
        ))
        self.remove(arcs)
