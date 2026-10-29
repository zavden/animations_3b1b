# ==============================================================================
# Scene:      StartSimple
# Source:     videos/_2021/shadows.py (lines 967-1030)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl StartSimple.py StartSimple -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class StartSimple(Scene):
    def construct(self):
        # Words
        title = Text("Universal problem-solving advice")
        title.set_width(FRAME_WIDTH - 4)
        title.to_edge(UP)
        title.set_color(BLUE)
        title.set_backstroke()
        line = Underline(title, buff=-0.035)
        line.set_width(FRAME_WIDTH - 1)
        line.set_color(BLUE_B)
        line.set_stroke(width=[0, 3, 3, 3, 0])
        line.insert_n_curves(101)

        words = Text(
            "Start with the simplest non-trivial\n"
            "variant of the problem you can."
        )
        words.next_to(line, DOWN, MED_SMALL_BUFF)
        rect = BackgroundRectangle(words, fill_opacity=1, buff=SMALL_BUFF)
        words.set_backstroke(width=5)

        # Shapes
        cube = VCube()
        cube.deactivate_depth_test()
        cube.set_color(BLUE_E)
        cube.set_opacity(0.75)
        cube.set_stroke(WHITE, 0.5, 0.5)
        cube.set_height(2)
        cube.rotate(PI / 4, [1, 2, 0])
        cube.sort(lambda p: p[2])
        cube = Group(*cube)
        cube.set_gloss(1)

        arrow = Arrow(LEFT, RIGHT)
        face = cube[np.argmax([f.get_z() for f in cube])].copy()
        group = Group(cube, arrow, face)
        group.arrange(RIGHT, buff=MED_LARGE_BUFF)
        group.next_to(words, DOWN, LARGE_BUFF)
        group.set_width(2)
        group.to_edge(RIGHT)
        group.set_y(0)

        self.camera.light_source.set_x(-4)

        self.play(
            ShowCreation(line),
            Write(title, run_time=1),
        )
        self.wait()
        self.play(
            FadeIn(rect),
            FadeIn(words, lag_ratio=0.1),
            run_time=2
        )
        self.wait()
        self.play(FlashAround(words.get_part_by_text("non-trivial"), run_time=2))
        self.wait()
        self.play(
            LaggedStart(*map(DrawBorderThenFill, cube)),
            ShowCreation(arrow),
            TransformFromCopy(cube[-1], face)
        )
        self.wait(3)
