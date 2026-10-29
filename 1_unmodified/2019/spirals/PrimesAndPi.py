# ==============================================================================
# Scene:      PrimesAndPi
# Source:     videos/_2019/spirals.py (lines 258-323)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl PrimesAndPi.py PrimesAndPi -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

def is_prime(n):
    if n < 2:
        return False
    for k in range(2, int(np.sqrt(n)) + 1):
        if n % k == 0:
            return False
    return True


class PrimesAndPi(Scene):
    def construct(self):
        self.show_primes()
        self.show_rational_approximations()

    def show_primes(self):
        n_rows = 10
        n_cols = 10
        matrix = IntegerMatrix([
            [n_cols * x + y for y in range(n_cols)]
            for x in range(n_rows)
        ])
        numbers = matrix.get_entries()
        primes = VGroup(*filter(
            lambda m: is_prime(m.get_value()),
            numbers,
        ))
        non_primes = VGroup(*filter(
            lambda m: not is_prime(m.get_value()),
            numbers
        ))

        self.add(numbers)

        self.play(
            LaggedStart(*[
                ApplyFunction(
                    lambda m: m.set_color(TEAL).scale(1.2),
                    prime
                )
                for prime in primes
            ]),
            non_primes.set_opacity, 0.25,
            run_time=2,
        )
        self.wait()

        self.numbers = numbers

    def show_rational_approximations(self):
        numbers = self.numbers

        approxs = OldTex(
            "{22 \\over 7} &=", "{:.12}\\dots\\\\".format(22 / 7),
            "{355 \\over 113} &=", "{:.12}\\dots\\\\".format(355 / 113),
            "\\pi &=", "{:.12}\\dots\\\\".format(PI),
        )
        approxs[:2].shift(MED_LARGE_BUFF * UP)
        approxs[-2:].shift(MED_LARGE_BUFF * DOWN)
        approxs[-2:].set_color(YELLOW)
        approxs[1][:4].set_color(YELLOW)
        approxs[3][:8].set_color(YELLOW)
        approxs.scale(1.5)

        randy = Randolph(color=YELLOW, height=1)
        randy.move_to(approxs[-2][0], RIGHT)
        approxs[-2][0].set_opacity(0)

        self.play(
            LaggedStartMap(FadeOutAndShiftDown, numbers),
            LaggedStartMap(FadeIn, approxs),
            FadeIn(randy)
        )
        self.play(Blink(randy))
        self.play(randy.change, "pondering", UR)
        self.wait()
