# ==============================================================================
# Scene:      Quiz
# Source:     videos/_2025/grover/runtime.py (lines 6-170)
# Category:   2 · Renders with modifications
# Includes code copied from: _2025/grover/qc_supplements.py
#
# Run from this folder:
#     manimgl Quiz.py Quiz -w -m --fps 15
#
# Placeholder assets (not Grant's originals):
#   - _lib/assets/svg_images/computer_chip.svg  (substitute: copy of the repo's gpu.svg, a chip with pins)
#
# Notes:
#   The grover SVGs (computer_chip, and/or/not_gate, 4-bit adder, BitCircuit, light_switch, QR, sudoku, magnifying_glass2, BinaryFunctionCircuit) are not in the public repo (Grant's Dropbox). Three were replaced with similar assets from the repo (computer_chip <- gpu.svg, magnifying_glass2 <- magnifying_glass.svg, which has the same 2nd lens subpath that get_magnifying_glass() indexes, and BinaryFunctionCircuit <- circuit.svg) and the rest were generated with _lib/assets/generated/2025/grover/make_grover_svgs.py, respecting the parts the code indexes (sudoku: 81 cells, 9 boxes, border and digits; QR: data modules and, at the end, 6 position-eye pieces; BitCircuit: the last 2 submobjects are the dots).
# ==============================================================================

from manim_imports_ext import *


# ----- From _2025/grover/qc_supplements.py -----

def get_quantum_computer_symbol(height=2, color=GREY_B, symbol_tex=R"|Q\rangle", symbol_color=TEAL):
    chip = SVGMobject("computer_chip")
    chip.set_height(height)
    chip.to_edge(RIGHT)
    chip.set_fill(GREY_C)
    chip.set_shading(0.7, 0, 0)
    symbol = Tex(symbol_tex)
    symbol.set_fill(symbol_color)
    symbol.set_stroke(symbol_color, 1)
    symbol.set_height(0.4 * chip.get_height())
    symbol.move_to(chip)

    result = VGroup(chip, symbol)
    return result



# ----- From _2025/grover/runtime.py -----

class Quiz(InteractiveScene):
    def construct(self):
        # Set up terms
        choices = VGroup(
            TexText(R"A) $\mathcal{O}\big(\sqrt{N}\big)$"),
            TexText(R"B) $\mathcal{O}\big(\log(N)\big)$"),
            TexText(R"C) $\mathcal{O}\big(\log(\log(N))\big)$"),
            TexText(R"D) $\mathcal{O}(1)$"),
        )
        choices.arrange(DOWN, buff=0.5, aligned_edge=LEFT)
        choices.to_edge(LEFT, buff=1.0)

        covers = VGroup(
            SurroundingRectangle(choice[2:], buff=SMALL_BUFF)
            for choice in choices
        )
        covers.set_fill(GREY_D, 1)
        covers.set_stroke(WHITE, 1)
        for cover, choice in zip(covers, choices):
            choice[2:].set_fill(opacity=0)
            cover.set_width(choices.get_width(), about_edge=LEFT, stretch=True)
            cover.align_to(covers, LEFT)
            cover.save_state()
            cover.stretch(0, 0, about_edge=LEFT)

        self.play(
            LaggedStartMap(Restore, covers, lag_ratio=0.25),
            LaggedStartMap(FadeIn, choices, lag_ratio=0.25),
        )
        self.wait()

        # Reference mostly wrong answers
        pis = Randolph().get_grid(6, 6, buff=2.0)
        pis.set_height(7)
        pis.to_edge(RIGHT)
        pis.sort(lambda p: np.dot(p, DR))

        symbol_height = 0.35
        symbols = [
            Exmark().set_color(RED).set_height(symbol_height),
            Checkmark().set_color(GREEN).set_height(symbol_height),
        ]
        all_symbols = VGroup()
        for pi in pis:
            pi.body.set_color(interpolate_color(BLUE_E, BLUE_C, random.random()))
            pi.change_mode("pondering")
            correct = random.random() < 0.2
            symbol = symbols[correct].copy()
            symbol.next_to(pi, UR, buff=0)
            all_symbols.add(symbol)
            pi.generate_target()
            pi.target.change_mode(["sad", "hooray"][correct])

        self.play(LaggedStartMap(FadeIn, pis, run_time=2))
        self.play(
            LaggedStartMap(MoveToTarget, pis, lag_ratio=0.01),
            LaggedStartMap(Write, all_symbols, lag_ratio=0.01),
        )
        pis.shuffle()
        self.play(LaggedStartMap(Blink, pis[::4]))
        self.wait()
        self.play(
            FadeOut(pis, lag_ratio=1e-3),
            FadeOut(all_symbols, lag_ratio=1e-3),
        )

        # Show question
        frame = self.frame

        question = VGroup(
            get_quantum_computer_symbol(),
            Clock(),
            Tex(R"?"),
        )
        for mob in question:
            mob.set_height(1.5)
        question.arrange(RIGHT, buff=0.5)
        question.set_width(4)
        question[2].scale(0.7)
        question.next_to(choices, UP, aligned_edge=LEFT)

        clock = question[1]
        cycle_animation(ClockPassesTime(clock, hours_passed=12, run_time=24))
        self.play(
            VFadeIn(question, suspend_mobject_updating=True, lag_ratio=0.01),
            VGroup(choices, covers).animate.shift(DOWN).set_anim_args(run_time=2),
            frame.animate.match_x(choices).set_anim_args(run_time=2),
        )
        self.add(choices, Point(), covers)
        choices.set_opacity(1)
        self.play(
            LaggedStart(
                (cover.animate.stretch(0, 0, about_edge=RIGHT).set_opacity(0)
                for cover in covers),
                lag_ratio=0.25,
            ),
        )
        self.wait(16)

        # Show distribution
        question.clear_updaters()
        dists = [
            np.array([18, 20, 8, 54], dtype=float),
            np.array([51, 55, 37, 65], dtype=float),  # Stanford
            np.array([17, 25, 5, 39], dtype=float),   # IMO, IIRC
        ]
        for dist in dists:
            dist[:] = dist / dist.sum()

        max_bar_width = 5.0
        prob_bar_group = VGroup()
        for dist in dists:
            prob_bars = VGroup()
            for choice, prob in zip(choices, dist):
                bar = Rectangle(width=prob * max_bar_width, height=0.35)
                bar.next_to(choice, LEFT)
                bar.set_fill(interpolate_color(BLUE_D, GREEN, prob * 1.5), 1)
                bar.set_stroke(WHITE, 1)
                prob_bars.add(bar)
            prob_bar_group.add(prob_bars)

        prob_bars = prob_bar_group[0].copy()

        prob_labels = VGroup()
        for bar in prob_bars:
            label = Integer(100, font_size=36, unit=R"\%")
            label.bar = bar
            label.add_updater(lambda m: m.set_value(np.round(100 * m.bar.get_width() / max_bar_width)))
            label.add_updater(lambda m: m.next_to(m.bar, LEFT))
            prob_labels.add(label)

        self.play(
            LaggedStart(
                (GrowFromPoint(bar, bar.get_right())
                for bar in prob_bars),
                lag_ratio=0.2,
            ),
            VFadeIn(prob_labels)
        )
        self.wait()
        for index in [1, 2, 0]:
            self.play(Transform(prob_bars, prob_bar_group[index]))
            self.wait()

        # Go through each answer
        covers = VGroup(
            SurroundingRectangle(VGroup(bar, label, choice))
            for bar, label, choice in zip(prob_bars, prob_labels, choices)
        )
        covers.set_stroke(width=0)
        covers.set_fill(BLACK, 0.8)

        self.add(Point())
        self.play(FadeIn(covers[:3]))
        self.wait()
        self.play(
            FadeOut(covers[1]),
            FadeIn(covers[3])
        )
        self.wait()
        self.play(
            FadeOut(covers[0]),
            FadeIn(covers[1])
        )
        self.wait()
