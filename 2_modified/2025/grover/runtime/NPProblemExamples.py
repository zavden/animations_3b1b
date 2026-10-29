# ==============================================================================
# Scene:      NPProblemExamples
# Source:     videos/_2025/grover/runtime.py (lines 961-1015)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl NPProblemExamples.py NPProblemExamples -w -m --fps 15
#
# Placeholder assets (not Grant's originals):
#   - _lib/assets/svg_images/sudoku_example.svg  (generated: classic sudoku with cells, boxes and digits as outlines)
#
# Notes:
#   The grover SVGs (computer_chip, and/or/not_gate, 4-bit adder, BitCircuit, light_switch, QR, sudoku, magnifying_glass2, BinaryFunctionCircuit) are not in the public repo (Grant's Dropbox). Three were replaced with similar assets from the repo (computer_chip <- gpu.svg, magnifying_glass2 <- magnifying_glass.svg, which has the same 2nd lens subpath that get_magnifying_glass() indexes, and BinaryFunctionCircuit <- circuit.svg) and the rest were generated with _lib/assets/generated/2025/grover/make_grover_svgs.py, respecting the parts the code indexes (sudoku: 81 cells, 9 boxes, border and digits; QR: data modules and, at the end, 6 position-eye pieces; BitCircuit: the last 2 submobjects are the dots).
# ==============================================================================

from manim_imports_ext import *

class NPProblemExamples(InteractiveScene):
    def construct(self):
        # Examples
        example_images = Group(
            self.get_sudoku(),
            ImageMobject("US_color_graph"),
            Square().set_opacity(0),
        )
        for img in example_images:
            img.set_height(2)
        example_images.arrange_in_grid(2, 2, buff=1.5)
        example_images[2].match_x(example_images[:2])

        example_names = VGroup(
            Text("Sudoku"),
            Text("Graph Coloring"),
            Text("Reversing Cryptographic\nHash Functions"),
        )
        examples = Group()
        for name, img in zip(example_names, example_images):
            name.scale(0.65)
            name.next_to(img, DOWN)
            examples.add(Group(img, name))
        examples.move_to(2 * LEFT)

        self.play(LaggedStartMap(FadeIn, examples, lag_ratio=0.5))

        # Name them
        big_rect = SurroundingRectangle(examples, buff=0.35)
        big_rect.set_stroke(BLUE, 3)
        big_rect.round_corners(radius=0.5)
        name = Text("NP Problems", font_size=60)
        name.next_to(big_rect, buff=MED_LARGE_BUFF)

        self.play(LaggedStart(
            ShowCreation(big_rect),
            Write(name),
            # self.frame.animate.set_x(2),
            lag_ratio=0.2
        ))
        self.wait()

    def get_sudoku(self):
        sudoku = SVGMobject("sudoku_example")
        small_width = sudoku[0].get_width()
        for part in sudoku.submobjects:
            if len(part.get_anchors()) == 5:
                part.set_fill(opacity=0)
                part.set_stroke(WHITE, 1, 0.5)
                if part.get_width() > 2 * small_width:
                    part.set_stroke(WHITE, 2, 1)
            else:
                part.set_fill(WHITE, 1)

        return sudoku
