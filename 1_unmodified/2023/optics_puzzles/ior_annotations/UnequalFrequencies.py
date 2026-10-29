# ==============================================================================
# Scene:      UnequalFrequencies
# Source:     videos/_2023/optics_puzzles/ior_annotations.py (lines 899-929)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl UnequalFrequencies.py UnequalFrequencies -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class UnequalFrequencies(InteractiveScene):
    def construct(self):
        # Test
        # self.add(ImageMobject("WaveEqStill").set_height(FRAME_HEIGHT))

        word_eq = TexText(R"Freq. of light $\ne$ Resonant freq.")
        eq = Tex(R"\omega_l \ne \omega_r")
        word_lhs = word_eq["Freq. of light"]
        word_rhs = word_eq["Resonant freq."]
        word_lhs.set_color(TEAL)
        word_rhs.set_color(PINK)
        eq[R"\omega_l"].set_color(TEAL)
        eq[R"\omega_r"].set_color(PINK)
        equations = VGroup(word_eq, eq)
        equations.arrange(DOWN)
        equations.to_corner(UR)

        oml_point = np.array([-1.2, 2.7, 0])
        arrow = Arrow(word_eq.get_left(), oml_point, path_arc=90 * DEGREES)
        arrow.set_color(TEAL)
        oml = eq[R"\omega_l"]
        oml_copy = oml.copy().move_to(oml_point)

        self.play(
            FadeIn(word_eq),
            ShowCreation(arrow),
        )
        self.wait()
        self.play(ReplacementTransform(oml_copy, oml))
        self.play(Write(eq[R"\ne \omega_r"]))
        self.wait()
