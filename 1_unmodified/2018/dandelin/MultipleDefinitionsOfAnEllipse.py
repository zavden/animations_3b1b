# ==============================================================================
# Scene:      MultipleDefinitionsOfAnEllipse
# Source:     videos/_2018/dandelin.py (lines 203-237)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl MultipleDefinitionsOfAnEllipse.py MultipleDefinitionsOfAnEllipse -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class MultipleDefinitionsOfAnEllipse(Scene):
    def construct(self):
        title = Title("Multiple definitions of ``ellipse''")
        self.add(title)

        definitions = VGroup(
            OldTexText("1. Stretch a circle"),
            OldTexText("2. Thumbtack \\\\ \\quad\\, construction"),
            OldTexText("3. Slice a cone"),
        )
        definitions.arrange(
            DOWN, buff=LARGE_BUFF,
            aligned_edge=LEFT
        )
        definitions.next_to(title, DOWN, LARGE_BUFF)
        definitions.to_edge(LEFT)

        for definition in definitions:
            definition.saved_state = definition.copy()
            definition.saved_state.set_fill(GREY_B, 0.5)

        self.play(LaggedStartMap(
            FadeInFrom, definitions,
            lambda m: (m, RIGHT),
            run_time=4
        ))
        self.wait()
        for definition in definitions:
            others = [d for d in definitions if d is not definition]
            self.play(
                definition.set_fill, WHITE, 1,
                definition.scale, 1.2, {"about_edge": LEFT},
                *list(map(Restore, others))
            )
            self.wait(2)
