# ==============================================================================
# Scene:      DefineIndexOfRefraction
# Source:     videos/_2023/optics_puzzles/ior_annotations.py (lines 163-200)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl DefineIndexOfRefraction.py DefineIndexOfRefraction -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class DefineIndexOfRefraction(InteractiveScene):
    def construct(self):
        # Speeds
        ior = "1.52"
        speed1 = Tex(R"\text{Speed} = c \approx 3\times 10^8 \, {\text{m} / \text{s}}")
        speed2 = Tex(R"\text{Speed} \approx c / " + ior)
        speed2[ior].set_color(PINK)
        for speed, x in zip([speed1, speed2], [-1, 1]):
            speed.set_x(x * FRAME_WIDTH / 4)
            speed.set_y(-2)
            self.play(FadeIn(speed, lag_ratio=0.1))
            self.wait()

        # Index of refraction
        num_words = R"\text{Speed in a vacuum}"
        den_words = R"\text{Speed in a glass}"
        equation = Tex(
            fR"{{{num_words} \over {den_words}}} \approx {ior}",
            font_size=36
        )
        equation[den_words].set_color(BLUE)
        equation[ior].set_color(PINK).scale(1.5, about_edge=LEFT)
        equation.to_corner(UL)

        name = TexText("``Index of refraction''")
        name.next_to(equation, DOWN, buff=LARGE_BUFF)
        arrow = Arrow(name, equation[ior], buff=0.2)

        self.play(
            TransformMatchingShapes(speed1["Speed"].copy(), equation[num_words]),
            TransformMatchingShapes(speed2["Speed"].copy(), equation[den_words]),
            Write(equation[R"\over"]),
            Write(equation[R"\approx"]),
            TransformFromCopy(speed2[ior], equation[ior]),
        )
        self.wait()
        self.play(Write(name), GrowArrow(arrow))
        self.wait()
