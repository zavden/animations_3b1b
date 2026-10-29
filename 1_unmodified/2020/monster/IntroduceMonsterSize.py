# ==============================================================================
# Scene:      IntroduceMonsterSize
# Source:     videos/_2020/monster.py (lines 321-445)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl IntroduceMonsterSize.py IntroduceMonsterSize -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

MONSTER_SIZE = 808017424794512875886459904961710757005754368000000000


def get_monster(height=3):
    monster = SVGMobject("monster")
    monster.set_fill(GREY_BROWN)
    monster.set_stroke(BLACK, 0.1)
    monster.set_height(height)
    return monster


def get_size_bars(mob, stroke_width=3, buff=SMALL_BUFF):
    bars = VGroup(*[Line(UP, DOWN) for x in range(2)])
    bars.match_height(mob)
    bars[0].next_to(mob, LEFT, buff=buff)
    bars[1].next_to(mob, RIGHT, buff=buff)
    bars.set_stroke(WHITE, stroke_width)
    return bars


class IntroduceMonsterSize(Scene):
    def construct(self):
        # Show number
        max_width = FRAME_WIDTH - 1
        size_label = OldTexText("{:,}".format(MONSTER_SIZE))[0]
        size_label.set_width(max_width)

        n_syms = len(size_label)
        partials = VGroup()
        for n in range(len(size_label) + 1):
            partial = size_label[:n].copy()
            partial.set_height(1.5)
            if partial.get_width() > max_width:
                partial.set_width(max_width)
            partial.center()
            partial.set_color(interpolate_color(BLUE, YELLOW, n / n_syms))
            partials.add(partial)

        self.play(
            UpdateFromAlphaFunc(
                size_label,
                lambda m, a: m.set_submobjects(
                    partials[int(a * n_syms)].submobjects
                ),
                run_time=6,
                rate_func=bezier([0, 0, 1, 1])
            )
        )
        self.wait()

        # Show factorization
        factors = OldTex(
            r"= 2^{46} \cdot 3^{20} \cdot 5^{9} \cdot 7^{6} \cdot 11^{2} \cdot 13^{3} \cdot 17 \cdot 19 \cdot 23 \cdot 29 \cdot 31 \cdot 41 \cdot 47 \cdot 59 \cdot 71"
        )
        factors.set_width(max_width)
        approx = OldTex("\\approx 8\\times 10^{53}")
        approx.set_height(0.8)
        approx.move_to(DOWN)
        factors.next_to(approx, UP, buff=MED_LARGE_BUFF)

        self.play(
            size_label.next_to, factors, UP, MED_LARGE_BUFF,
            FadeIn(factors, 0.5 * DOWN),
            Write(approx),
        )
        self.wait()

        value_group = VGroup(size_label, factors, approx)

        # Jupiter
        jupiter = TexturedSurface(Sphere(), "JupiterTexture")
        jupiter.rotate(90 * DEGREES, RIGHT)
        jupiter.set_height(3.5)
        jupiter.to_edge(DOWN)
        jupiter.add_updater(lambda m, dt: m.rotate(-0.1 * dt, UP))
        jupiter.set_shadow(0.9)

        self.play(
            UpdateFromAlphaFunc(jupiter, lambda m, a: m.set_opacity(a)),
            ApplyMethod(value_group.to_edge, UP, run_time=2)
        )
        self.wait(4)

        # Alternate intelligences
        alien = SVGMobject("alien")
        alien.set_height(3)
        alien.to_corner(DL)
        alien.set_stroke(GREEN, width=0)
        alien.set_fill(GREEN_E, 1)

        server = SVGMobject("server_stack")
        server.set_height(3)
        server.to_corner(DR)
        server.set_stroke(BLACK, 2)
        server.set_fill(GREY, 1)
        server.set_gloss(0.5)

        alien_words = OldTexText("Interesting!")
        alien_words.set_color(GREEN)
        alien_words.next_to(alien, UR, buff=-MED_SMALL_BUFF)
        server_words = OldTexText("Very interesting\\\\indeed!")
        server_words.next_to(server, LEFT)

        self.play(
            FadeOut(jupiter, DOWN),
            DrawBorderThenFill(alien),
        )
        self.play(Write(server))
        self.wait()
        for words in alien_words, server_words:
            self.play(Write(words, run_time=1))
            self.wait()

        # What is it?
        question = OldTexText("What is it?")
        question.scale(2)
        question.move_to(UP)

        self.play(
            LaggedStartMap(
                FadeOut,
                VGroup(factors, approx, alien_words, alien, server_words, server),
                lambda m: (m, DOWN),
            ),
            ApplyMethod(size_label.move_to, 0.5 * DOWN, run_time=2),
            FadeIn(question, UP, run_time=2, rate_func=squish_rate_func(smooth, 0.5, 1)),
        )
        self.wait()

        monster = get_monster()
        monster.next_to(size_label, UP)
        monster.to_edge(RIGHT, buff=2)
        m_size_bars = get_size_bars(monster, buff=MED_SMALL_BUFF, stroke_width=5)

        self.play(
            question.shift, 2 * LEFT,
            DrawBorderThenFill(monster),
            run_time=2,
        )
        self.play(ShowCreation(m_size_bars, lag_ratio=0.4))
        self.wait(2)
        self.play(LaggedStart(*[
            FadeOut(mob, DOWN)
            for mob in self.mobjects
        ]))
