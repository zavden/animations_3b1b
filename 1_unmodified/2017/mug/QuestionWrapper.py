# ==============================================================================
# Scene:      QuestionWrapper
# Source:     videos/_2017/mug.py (lines 1939-1958)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl QuestionWrapper.py QuestionWrapper -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class QuestionWrapper(Scene):
    def construct(self):
        question = OldTexText(
            "Where", "\\emph{specifically}", "does\\\\", 
            "this proof break down?",
        )
        question.to_edge(UP)
        question.set_color_by_tex("specifically", YELLOW)
        screen_rect = ScreenRectangle(height = 5.5)
        screen_rect.next_to(question, DOWN)

        self.play(ShowCreation(screen_rect))
        self.wait()
        for word in question:
            self.play(LaggedStartMap(
                FadeIn, word,
                run_time = 0.05*len(word)
            ))
            self.wait(0.05)
        self.wait()
