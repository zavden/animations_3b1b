# ==============================================================================
# Scene:      SideSumTruthiness
# Source:     videos/_2022/visual_proofs/lies.py (lines 2157-2205)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl SideSumTruthiness.py SideSumTruthiness -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class SideSumTruthiness(InteractiveScene):
    def construct(self):
        # Lines
        A, E, C = Dot().replicate(3)
        A.move_to(2 * UL)
        C.move_to(DR)
        VGroup(A, C).to_corner(DR, buff=1.5)

        alpha_tracker = ValueTracker(0.75)
        E.add_updater(lambda m: m.move_to(interpolate(
            A.get_center(), C.get_center(), alpha_tracker.get_value()
        )))

        AE = Line().set_stroke(RED, 3, opacity=0.75)
        EC = Line().set_stroke(BLUE, 3, opacity=0.75)
        AE.add_updater(lambda l: l.put_start_and_end_on(A.get_center(), E.get_center()))
        EC.add_updater(lambda l: l.put_start_and_end_on(E.get_center(), C.get_center()))

        labels = Text("AEC")
        labels[0].next_to(A, UP, SMALL_BUFF)
        labels[1].add_updater(lambda m: m.next_to(E, DL, SMALL_BUFF))
        labels[2].next_to(C, RIGHT, SMALL_BUFF)

        self.add(AE, EC, A, E, C, *labels)

        # Equation
        eq = OldTex("\\overline{AE} + \\overline{EC} = \\overline{AC}", font_size=60)
        eq.to_corner(UR)

        labels = VGroup(
            VGroup(Text("True"), Checkmark()),
            VGroup(Text("False"), Exmark()),
        )
        labels.scale(60 / 48)
        for label in labels:
            label[0].match_color(label[1])
            label.arrange(RIGHT, buff=MED_LARGE_BUFF)
            label.next_to(eq, DOWN, MED_LARGE_BUFF)

        labels[0].add_updater(lambda m: m.set_opacity(1 if 0 < alpha_tracker.get_value() < 1 else 0))
        labels[1].add_updater(lambda m: m.set_opacity(0 if 0 < alpha_tracker.get_value() < 1 else 1))

        self.add(eq)
        self.add(labels)

        # Move around
        for alpha in [0.3, 0.7, 0.5, 0.7, 0.3, -0.3, 0.7, 1.4, 1.2, 0.5]:
            self.play(alpha_tracker.animate.set_value(alpha), run_time=2)
        self.wait()
