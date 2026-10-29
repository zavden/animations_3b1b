# ==============================================================================
# Scene:      AngleToProbabilityChart
# Source:     videos/_2017/bell.py (lines 535-587)
# Category:   1 · Renders unmodified
# Includes code copied from: _2017/waves.py
#
# Run from this folder:
#     manimgl AngleToProbabilityChart.py AngleToProbabilityChart -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *
import warnings


# ----- From _2017/waves.py -----

warnings.warn("""
    Warning: This file makes use of
    ContinualAnimation, which has since
    been deprecated
""")



# ----- From _2017/bell.py -----

class AngleToProbabilityChart(Scene):
    def construct(self):
        left_title = OldTexText("Angle between \\\\ filters")
        left_title.to_corner(UP+LEFT)
        right_title = OldTexText(
            "Probability that photons passing \\\\",
            "through the first pass through the second"
        )
        right_title.next_to(left_title, RIGHT, LARGE_BUFF)

        h_line = Line(LEFT, RIGHT).scale(FRAME_X_RADIUS)
        h_line.to_edge(UP, buff = 2)
        v_line = Line(UP, DOWN).scale(FRAME_Y_RADIUS)
        v_line.next_to(left_title, RIGHT, MED_LARGE_BUFF)
        v_line.to_edge(UP, buff = 0)
        VGroup(h_line, v_line).set_color(BLUE)
        self.add(left_title, right_title, h_line, v_line)

        angles = [0, 22.5, 45, 67.5, 90]
        angle_mobs = VGroup(*[
            OldTex(str(angle) + "^\\circ")
            for angle in angles
        ])
        angle_mobs.arrange(DOWN, buff = MED_LARGE_BUFF)
        angle_mobs.next_to(left_title, DOWN, LARGE_BUFF)

        probs = [
            np.cos(angle*np.pi/180.0)**2
            for angle in angles
        ]
        prob_mobs = VGroup(*[
            OldTex("%.1f"%(100*prob) + "\\%")
            for prob in probs
        ])
        prob_mobs.set_color(YELLOW)

        angle_prob_pairs = list(zip(angle_mobs, prob_mobs))
        for angle_mob, prob_mob in angle_prob_pairs:
            prob_mob.next_to(angle_mob, RIGHT, buff = 3)
        for prob_mob in prob_mobs[1:]:
            prob_mob.align_to(prob_mobs[0], LEFT)


        for i in [0, 4, 2, 1, 3]:
            self.play(FadeIn(angle_mobs[i]))
            self.play(ReplacementTransform(
                angle_mobs[i].copy(), prob_mobs[i]
            ))

        explanation = OldTexText("Based on $\\cos(\\theta)^2$")
        explanation.next_to(prob_mobs, RIGHT, LARGE_BUFF)
        self.play(Write(explanation, run_time = 2))
        self.wait()
