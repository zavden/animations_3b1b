# ==============================================================================
# Scene:      PreviewVisualizationWrapper
# Source:     videos/_2021/matrix_exp.py (lines 6434-6484)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl PreviewVisualizationWrapper.py PreviewVisualizationWrapper -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class PreviewVisualizationWrapper(Scene):
    def construct(self):
        background = FullScreenFadeRectangle(fill_color=GREY_E, fill_opacity=1)
        self.add(background)

        screen = ScreenRectangle(height=6)
        screen.set_fill(BLACK, 1)
        screen.set_stroke(GREY_A, 3)
        screen.to_edge(DOWN)
        self.add(screen)

        titles = VGroup(
            Text("How to think about matrix exponentiation"),
            Text(
                "How to visualize matrix exponentiation",
                t2s={"visualize": ITALIC},
            ),
            Text("What problems matrix exponentiation solves?"),
        )
        for title in titles:
            title.next_to(screen, UP)
            title.get_parts_by_text("matrix exponentiation").set_color(TEAL)

        self.play(FadeIn(titles[0], 0.5 * UP))
        self.wait(2)
        self.play(*(
            FadeTransform(
                titles[0].get_parts_by_text(w1),
                titles[1].get_parts_by_text(w2),
            )
            for w1, w2 in [
                ("How to", "How to"),
                ("think about", "visualize"),
                ("matrix exponentiation", "matrix exponentiation"),
            ]
        ))
        self.wait(2)
        self.play(
            *(
                FadeTransform(
                    titles[1].get_parts_by_text(w1),
                    titles[2].get_parts_by_text(w2),
                )
                for w1, w2 in [
                    ("How to visualize", "What problems"),
                    ("matrix exponentiation", "matrix exponentiation"),
                ]
            ),
            FadeIn(titles[2].get_parts_by_text("solves?"))
        )
        self.wait(2)
