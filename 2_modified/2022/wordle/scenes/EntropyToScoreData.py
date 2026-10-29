# ==============================================================================
# Scene:      EntropyToScoreData
# Source:     videos/_2022/wordle/scenes.py (lines 3428-3524)
# Category:   2 · Renders with modifications
# Includes code copied from: _2022/wordle/simulations.py
#
# Run from this folder:
#     manimgl EntropyToScoreData.py EntropyToScoreData -w -m --fps 15
#
# Placeholder assets (not Grant's originals):
#   - _lib/assets/generated/2022/wordle/data/ent_score_pairs.json (regenerated with simulations.py; generator 2022/wordle/make_wordle_data.py)
# ==============================================================================

from manim_imports_ext import *


# ----- From _2022/wordle/simulations.py -----

DATA_DIR = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    "data",
)


ENT_SCORE_PAIRS_FILE = os.path.join(DATA_DIR, "ent_score_pairs.json")



# ----- From _2022/wordle/scenes.py -----

class EntropyToScoreData(Scene):
    def construct(self):
        # Axes
        axes = Axes(
            (0, 13), (0, 6),
            height=6,
            width=10,
        )
        axes.x_axis.add_numbers()
        axes.y_axis.add_numbers()
        x_label = Text("Entropy", font_size=24)
        x_label.next_to(axes.x_axis, UR, SMALL_BUFF)
        x_label.shift_onto_screen()
        y_label = Text("Score", font_size=24)
        y_label.next_to(axes.y_axis, UR)
        y_label.shift_onto_screen()
        axes.add(x_label, y_label)
        self.add(axes)
        self.wait()
        self.wait()

        # Data
        with open(ENT_SCORE_PAIRS_FILE) as fp:
            data = np.array(json.load(fp))

        dots = DotCloud([
            axes.c2p(*pair)
            for pair in data
        ])
        dots.set_radius(0.05)
        dots.set_color(BLUE)
        dots.set_opacity(0.02)

        dots.add_updater(lambda m: m)
        self.play(ShowCreation(dots, run_time=3))
        self.wait()

        # Window
        window = FullScreenRectangle().replicate(2)
        window.arrange(RIGHT, buff=3 * dots.radius)
        window.set_fill(BLACK, 0.7)

        window.set_x(axes.c2p(8.65, 0)[0])
        self.add(dots, window, axes)
        self.wait()
        for x in (0, 1, 2):
            self.play(
                window.animate.set_x(axes.c2p(x, 0)[0])
            )
            self.wait()

        self.play(FadeOut(window))
        self.wait()

        # Buckets
        bucket_size = 0.25
        buckets = dict()
        bucket_xs = np.arange(0, axes.x_range[1], bucket_size)
        bars = VGroup()
        for x in bucket_xs:
            indices = (x < data[:, 0]) & (data[:, 0] <= x + bucket_size)
            buckets[x] = data[indices, 1]
            y = data[indices, 1].mean()
            if not indices.any():
                continue
            bar = Rectangle(
                width=axes.x_axis.unit_size * bucket_size,
                height=axes.y_axis.unit_size * y
            )
            bar.set_stroke(WHITE, 1)
            bar.move_to(axes.c2p(x, 0), DL)
            bar.set_fill(TEAL, 0.5)
            bars.add(bar)

        self.play(FadeIn(bars, lag_ratio=0.1, run_time=2))
        self.wait()
        bars.save_state()
        self.play(
            bars[:4].animate.fade(0.7),
            bars[5:].animate.fade(0.7),
        )
        self.wait()
        self.play(Restore(bars))
        self.play(
            bars[:16].animate.fade(0.7),
            bars[17:].animate.fade(0.7),
        )
        self.wait()
        self.play(Restore(bars))

        # Model
        curve = axes.get_graph(
            lambda x: 1 + 0.56 * math.log(x + 1) + 0.08 * x,
        )
        curve.set_stroke(YELLOW, 2)
        self.play(ShowCreation(curve, run_time=2))
        self.wait()
