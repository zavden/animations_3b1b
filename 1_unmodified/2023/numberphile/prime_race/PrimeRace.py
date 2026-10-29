# ==============================================================================
# Scene:      PrimeRace
# Source:     videos/_2023/numberphile/prime_race.py (lines 5-98)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl PrimeRace.py PrimeRace -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *
import sympy

class PrimeRace(InteractiveScene):
    race_length = 26863

    def construct(self):
        ONE_COLOR = BLUE
        THREE_COLOR = RED
        colors = [ONE_COLOR, THREE_COLOR]

        # Labels
        labels = VGroup(
            Tex(R"p \equiv 1 \mod 4", t2c={"1": ONE_COLOR}),
            Tex(R"p \equiv 3 \mod 4", t2c={"3": THREE_COLOR}),
        )
        labels.arrange(DOWN, buff=0.75)
        labels.to_edge(LEFT)

        h_line = Line(LEFT, RIGHT)
        h_line.set_width(100)
        h_line.to_edge(LEFT)

        v_line = Line(UP, DOWN)
        v_line.set_height(1.5 * labels.get_height())
        v_line.next_to(labels, RIGHT)
        v_line.set_y(0)
        VGroup(h_line, v_line).set_stroke(width=2)

        self.add(h_line, v_line)
        self.add(labels)

        # Start the race
        primes: list[int] = list(sympy.primerange(3, self.race_length))
        team1 = VGroup()
        team3 = VGroup()
        teams = [team1, team3]
        blocks = []
        for prime in primes:
            index = int((prime % 4) == 3)
            square = Square(side_length=1)
            square.set_fill(colors[index], 0.5)
            square.set_stroke(colors[index], 1.0)
            p_mob = Integer(prime)
            p_mob.set_max_width(0.8 * square.get_width())
            block = VGroup(square, p_mob)

            teams[index].add(block)
            blocks.append(block)

        for team, label in zip(teams, labels):
            team.arrange(RIGHT, buff=0)
            team.next_to(v_line, RIGHT, buff=SMALL_BUFF)
            team.match_y(label)

        h_line.set_width(teams[1].get_width() + 10, about_edge=LEFT)

        for block in blocks[:10]:
            self.play(FadeIn(block[0]), Write(block[1]))

        # Next sets
        frame = self.frame
        frame.target = frame.generate_target()
        frame.target.scale(1.75, about_edge=LEFT)
        self.play(
            LaggedStartMap(
                FadeIn, VGroup(*blocks[10:30]),
                lag_ratio=0.9,
            ),
            MoveToTarget(frame, rate_func=rush_into),
            run_time=12,
        )

        # Last set
        curr = 30
        tups = [
            (200, 10, linear, 1.25),
            (len(blocks) - 100, 60, linear, 1.25),
            (len(blocks) - 1, 5, smooth, 0.8)
        ]

        for index, rt, func, sf in tups:
            frame.target = frame.generate_target()
            frame.target.scale(sf)
            frame.target.set_x(blocks[index].get_right()[0] + 1)
            self.play(
                ShowIncreasingSubsets(VGroup(*blocks[curr:index])),
                MoveToTarget(frame),
                run_time=rt,
                rate_func=func,
            )
            curr = index

        blocks = VGroup(*blocks)
        self.add(blocks)
        self.play(frame.animate.set_height(8, about_point=blocks.get_right() + 2 * LEFT), run_time=3)
        self.wait()
