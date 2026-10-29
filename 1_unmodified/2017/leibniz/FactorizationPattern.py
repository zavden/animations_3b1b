# ==============================================================================
# Scene:      FactorizationPattern
# Source:     videos/_2017/leibniz.py (lines 2175-2368)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl FactorizationPattern.py FactorizationPattern -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class FactorizationPattern(Scene):
    def construct(self):
        self.force_skipping()

        self.add_number_line()
        self.show_one_mod_four_primes()
        self.show_three_mod_four_primes()
        self.ask_why_this_is_true()
        self.show_two()

    def add_number_line(self):
        line = NumberLine(
            x_min = 0,
            x_max = 36,
            unit_size = 0.4,
            numbers_to_show = list(range(0, 33, 4)),
            big_tick_numbers = list(range(0, 33, 4)),
        )
        line.shift(2*DOWN)
        line.to_edge(LEFT)
        line.add_numbers()

        self.add(line)
        self.number_line = line

    def show_one_mod_four_primes(self):
        primes = [5, 13, 17, 29]
        dots = VGroup(*[
            Dot(self.number_line.number_to_point(prime))
            for prime in primes
        ])
        dots.set_color(GREEN)
        prime_mobs = VGroup(*list(map(Tex, list(map(str, primes)))))
        arrows = VGroup()
        for prime_mob, dot in zip(prime_mobs, dots):
            prime_mob.next_to(dot, UP, LARGE_BUFF)
            prime_mob.set_color(dot.get_color())
            arrow = Arrow(prime_mob, dot, buff = SMALL_BUFF)
            arrow.set_color(dot.get_color())
            arrows.add(arrow)

        factorizations = VGroup(*[
            OldTex("=(%d+%si)(%d-%si)"%(x, y_str, x, y_str))
            for x, y in [(2, 1), (3, 2), (4, 1), (5, 2)]
            for y_str in [str(y) if y is not 1 else ""]
        ])
        factorizations.arrange(DOWN, aligned_edge = LEFT)
        factorizations.to_corner(UP+LEFT)
        factorizations.shift(RIGHT)
        movers = VGroup()
        for p_mob, factorization in zip(prime_mobs, factorizations):
            mover = p_mob.copy()
            mover.generate_target()
            mover.target.next_to(factorization, LEFT)
            movers.add(mover)
        v_dots = OldTex("\\vdots")
        v_dots.next_to(factorizations[-1][0], DOWN)
        factorization.add(v_dots)

        self.play(*it.chain(
            list(map(Write, prime_mobs)),
            list(map(ShowCreation, arrows)),
            list(map(DrawBorderThenFill, dots)),
        ))
        self.wait()
        self.play(*[
            MoveToTarget(
                mover,
                run_time = 2,
                path_arc = np.pi/2,
            )
            for mover in movers
        ])
        self.play(FadeIn(
            factorizations, 
            run_time = 2,
            lag_ratio = 0.5
        ))
        self.wait(4)
        self.play(*list(map(FadeOut, [movers, factorizations])))

    def show_three_mod_four_primes(self):
        primes = [3, 7, 11, 19, 23, 31]
        dots = VGroup(*[
            Dot(self.number_line.number_to_point(prime))
            for prime in primes
        ])
        dots.set_color(RED)
        prime_mobs = VGroup(*list(map(Tex, list(map(str, primes)))))
        arrows = VGroup()
        for prime_mob, dot in zip(prime_mobs, dots):
            prime_mob.next_to(dot, UP, LARGE_BUFF)
            prime_mob.set_color(dot.get_color())
            arrow = Arrow(prime_mob, dot, buff = SMALL_BUFF)
            arrow.set_color(dot.get_color())
            arrows.add(arrow)

        words = OldTexText("Already Gaussian primes")
        words.to_corner(UP+LEFT)
        word_arrows = VGroup(*[
            Line(
                words.get_bottom(), p_mob.get_top(),
                color = p_mob.get_color(),
                buff = MED_SMALL_BUFF
            )
            for p_mob in prime_mobs
        ])

        self.play(*it.chain(
            list(map(Write, prime_mobs)),
            list(map(ShowCreation, arrows)),
            list(map(DrawBorderThenFill, dots)),
        ))
        self.wait()
        self.play(
            Write(words),
            *list(map(ShowCreation, word_arrows))
        )
        self.wait(4)
        self.play(*list(map(FadeOut, [words, word_arrows])))

    def ask_why_this_is_true(self):
        randy = Randolph(color = BLUE_C)
        randy.scale(0.7)
        randy.to_edge(LEFT)
        randy.shift(0.8*UP)

        links_text = OldTexText("(See links in description)")
        links_text.scale(0.7)
        links_text.to_corner(UP+RIGHT)
        links_text.shift(DOWN)

        self.play(FadeIn(randy))
        self.play(PiCreatureBubbleIntroduction(
            randy, "Wait...why?",
            bubble_type = ThoughtBubble,
            bubble_config = {"height" : 2, "width" : 3},
            target_mode = "confused",
            look_at = self.number_line,
        ))
        self.play(Blink(randy))
        self.wait()
        self.play(FadeIn(links_text))
        self.wait(2)
        self.play(*list(map(FadeOut, [
            randy, randy.bubble, randy.bubble.content,
            links_text
        ])))

    def show_two(self):
        two_dot = Dot(self.number_line.number_to_point(2))
        two = OldTex("2")
        two.next_to(two_dot, UP, LARGE_BUFF)
        arrow = Arrow(two, two_dot, buff = SMALL_BUFF)
        VGroup(two_dot, two, arrow).set_color(YELLOW)

        mover = two.copy()
        mover.generate_target()
        mover.target.to_corner(UP+LEFT)
        factorization = OldTex("=", "(1+i)", "(1-i)")
        factorization.next_to(mover.target, RIGHT)
        factors = VGroup(*factorization[1:])

        time_i_arrow = Arrow(
            factors[1].get_bottom(),
            factors[0].get_bottom(),
            path_arc = -np.pi
        )
        times_i = OldTex("\\times i")
        # times_i.scale(1.5)
        times_i.next_to(time_i_arrow, DOWN)
        times_i.set_color(time_i_arrow.get_color())
        words = OldTexText("You'll see why this matters...")
        words.next_to(times_i, DOWN)
        words.shift_onto_screen()

        self.play(
            Write(two),
            ShowCreation(arrow),
            DrawBorderThenFill(two_dot)
        )
        self.wait()
        self.play(
            MoveToTarget(mover),
            Write(factorization)
        )

        self.revert_to_original_skipping_status()
        self.wait(2)
        self.play(ShowCreation(time_i_arrow))
        self.play(Write(times_i))
        self.wait(2)
        self.play(FadeIn(words))
        self.wait(2)
