# ==============================================================================
# Scene:      Rewrite3DRandomProcedure
# Source:     videos/_2017/putnam.py (lines 1215-1249)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl Rewrite3DRandomProcedure.py Rewrite3DRandomProcedure -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Grant's repo renamed TexMobject->Tex here (new GL class); the 2017 code needs the Cairo-style OldTexText
# ==============================================================================

from manim_imports_ext import *

class Rewrite3DRandomProcedure(Scene):
    def construct(self):
        random_procedure = OldTexText("Random procedure")
        underline = Line(LEFT, RIGHT)
        underline.stretch_to_fit_width(random_procedure.get_width())
        underline.scale(1.1)
        underline.next_to(random_procedure, DOWN)
        group = VGroup(random_procedure, underline)
        group.to_corner(UP+LEFT)
        
        # CHANGE: Grant's repo renamed TexMobject->Tex here (new GL class); the 2017 code needs the Cairo-style OldTexText
        words = VGroup(*list(map(OldTexText, [
            "Choose 4 random points",
            "Choose 3 random lines",
            "Choose $P_4$ at random",
            "Flip coin for each line \\\\ to get $P_1$, $P_2$, $P_3$",
        ])))
        words.scale(0.8)
        words.arrange(DOWN, buff = MED_LARGE_BUFF)
        words.next_to(underline, DOWN)
        words[1].set_color(YELLOW)
        cross = Cross(words[0])
        cross.set_stroke(RED, 6)

        self.play(
            Write(random_procedure),
            ShowCreation(underline)
        )
        self.play(FadeIn(words[0]))
        self.play(ShowCreation(cross))
        self.wait()
        self.play(LaggedStartMap(FadeIn, words[1]))
        self.play(LaggedStartMap(FadeIn, words[2]))
        self.wait(2)
        self.play(Write(words[3]))
        self.wait(3)
