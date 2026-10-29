# ==============================================================================
# Scene:      MusicalIntervalsAsPairs
# Source:     videos/_2024/inscribed_rect/loops.py (lines 3035-3154)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl MusicalIntervalsAsPairs.py MusicalIntervalsAsPairs -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class MusicalIntervalsAsPairs(InteractiveScene):
    def construct(self):
        # Add piano
        piano = Piano()[:39]
        piano.center()
        piano.set_width(FRAME_WIDTH)
        piano.set_shading(0.2, 0.1, 0)

        keys = piano[15:27]
        key_labels = VGroup(map(Tex, [
            R"C",
            R"C^{\#}",
            R"D",
            R"D^{\#}",
            R"E",
            R"F",
            R"F^{\#}",
            R"G",
            R"G^{\#}",
            R"A",
            R"A^{\#}",
            R"B",
        ]))
        key_labels.scale(0.6)
        key_labels.set_stroke(WHITE, 1)
        for key, label in zip(keys, key_labels):
            label.next_to(key.get_bottom(), UP, buff=0.1)

        self.add(piano)

        # Highlight random key pairs
        random.seed(0)
        indices = list(range(12))
        keys.save_state()
        for _ in range(24):
            i, j = random.sample(indices, 2)
            keys[i].set_color(TEAL)
            keys[j].set_color(TEAL)
            self.add(key_labels[i])
            self.add(key_labels[j])
            self.wait(0.5)
            # self.play_notes(i, j, 0.5)  # Only used for screen recording
            self.remove(key_labels)
            keys.restore()

        # Show the circle
        circle = Circle(radius=3)
        circle.set_stroke(WHITE, 3)
        circle.flip(axis=UR)

        key_labels.target = key_labels.generate_target()
        dots = Group()
        for label, alpha in zip(key_labels.target, np.arange(0, 1, 1 / 12)):
            point = circle.pfp(alpha)
            label.move_to(1.1 * point)
            dots.add(GlowDot(point, color=TEAL, radius=0.3))

        self.play(
            FadeOut(piano[:15]),
            keys.animate.set_opacity(0.5),
            FadeOut(piano[27:]),
            VFadeIn(key_labels),
        )
        self.remove(key_labels)
        self.play(
            ShowCreation(circle),
            LaggedStart(
                (FadeTransform(Group(key), dot)
                for key, dot in zip(keys, dots)),
                lag_ratio=0.1,
                group_type=Group,
            ),
            MoveToTarget(key_labels, lag_ratio=0.01),
            run_time=2
        )

        # Show the random connections again
        random.seed(0)
        line = Line().set_stroke(TEAL, 3)
        self.add(line)

        for _ in range(24):
            i, j = random.sample(indices, 2)
            line.put_start_and_end_on(
                dots[i].get_center(),
                dots[j].get_center(),
            )
            self.wait(1 / 3)

    def play_notes(self, i, j, duration=0.5, sample_rate=44100):
        """
        Play two notes simultaneously, specified as half steps above middle C.

        Parameters:
        i (int): Half steps above middle C for first note
        j (int): Half steps above middle C for second note
        duration (float): Length of time to play in seconds
        sample_rate (int): Number of samples per second
        """
        import sounddevice as sd
        # Middle C is 261.63 Hz
        base_freq = 261.63

        # Calculate frequencies using equal temperament formula
        freq1 = base_freq * (2 ** (i / 12))
        freq2 = base_freq * (2 ** (j / 12))

        # Generate time array
        t = np.linspace(0, duration, int(sample_rate * duration), False)

        # Generate sine waves for each note
        note1 = np.sin(2 * np.pi * freq1 * t)
        note2 = np.sin(2 * np.pi * freq2 * t)

        # Combine notes and normalize
        combined = (note1 + note2) / 2

        # Play the sound
        sd.play(combined, sample_rate)
        sd.wait()  # Wait until the sound has finished playing
