# ==============================================================================
# Scene:      AddingBitsObservationOverlay
# Source:     videos/_2022/wordle/scenes.py (lines 2201-2273)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl AddingBitsObservationOverlay.py AddingBitsObservationOverlay -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class AddingBitsObservationOverlay(Scene):
    def construct(self):
        mystery = Square(side_length=0.5).get_grid(1, 5, buff=SMALL_BUFF)
        mystery.set_stroke(WHITE, 1)
        for box in mystery:
            char = Text("?", font="Consolas")
            char.set_height(0.7 * box.get_height())
            char.move_to(box)
            box.add(char)

        # Delete...
        phase1_strs = [list("?????") for x in range(5)]
        phase2_strs = [list("s????") for x in range(4)]
        for i, s in enumerate(phase1_strs):
            s[i] = "t"
        for i, s in enumerate(phase2_strs):
            s[i + 1] = "t"
        kw = dict(
            font="Consolas",
            t2c={"t": RED, "s": YELLOW},
        )
        phase1 = VGroup(*(Text("".join(s), **kw) for s in phase1_strs))
        phase2 = VGroup(*(Text("".join(s), **kw) for s in phase2_strs))
        for phase in [phase1, phase2]:
            phase.arrange(DOWN, buff=SMALL_BUFF)

        phases = VGroup(mystery, phase1, phase2)
        phases.arrange(RIGHT, buff=2.0)
        phases.to_edge(UP)

        # Arrange observations
        mystery.set_x(-4).to_edge(UP, buff=LARGE_BUFF)
        arrows = Arrow(LEFT, RIGHT).set_width(3).replicate(2)
        arrows.arrange(RIGHT, buff=MED_LARGE_BUFF)
        arrows.next_to(mystery, RIGHT, buff=MED_LARGE_BUFF)

        obss = VGroup(
            OldTexText("Has a `t'"),
            OldTexText("Starts with `s'"),
        )
        obss.scale(0.85)
        bits_labels = VGroup(
            Text("2 bits"),
            Text("3 more bits"),
        )
        bits_labels.scale(0.75)
        for obs, bl, arrow in zip(obss, bits_labels, arrows):
            obs.next_to(arrow, UP)
            bl.next_to(arrow, DOWN)
            bl.set_color(YELLOW)

        self.add(mystery)
        for arrow, bl, obs in zip(arrows, bits_labels, obss):
            self.play(
                ShowCreation(arrow),
                Write(obs),
                run_time=1
            )
            self.play(FadeIn(bl, 0.25 * DOWN))
            self.wait()

        long_arrow = Arrow(arrows[0].get_start(), arrows[1].get_end(), buff=0)
        full_bits_label = Text("5 bits")
        full_bits_label.match_style(bits_labels[0])
        full_bits_label.next_to(long_arrow, DOWN)

        self.play(bits_labels.animate.to_edge(UP, buff=SMALL_BUFF))
        self.play(
            FadeTransform(arrows[0], long_arrow),
            FadeTransform(arrows[1], long_arrow),
            Write(full_bits_label, run_time=1),
        )
        self.wait()
