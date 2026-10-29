# ==============================================================================
# Scene:      Thumbnail
# Source:     videos/_2022/puzzles/subsets.py (lines 5434-5484)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl Thumbnail.py Thumbnail -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class Thumbnail(InteractiveScene):
    def construct(self):
        # Add plane
        plane = ComplexPlane(
            (-3, 3), (-3, 3),
            background_line_style=dict(stroke_color=BLUE_D, stroke_width=3),
            faded_line_ratio=1,
            axis_config=dict(stroke_color=GREY_B),
        )
        plane.set_width(FRAME_WIDTH)
        plane.scale(1.2)
        # plane.move_to(0.75 * DOWN)
        # plane.add_coordinate_labels(font_size=24)

        circle = Circle(radius=get_norm(plane.n2p(1) - plane.n2p(0)))
        circle.move_to(plane.n2p(0))
        circle.set_stroke(WHITE, 2)

        points = [plane.n2p(np.exp(complex(0, angle))) for angle in np.arange(0, TAU, TAU / 5)]
        glow_dots = GlowDots(points, radius=0.5)
        dots = DotCloud(points, radius=0.05, color=YELLOW)
        lines = VGroup(*(Line(plane.n2p(0), point) for point in points))
        lines.set_stroke(YELLOW, 4)

        self.add(plane)
        self.add(circle)
        self.add(lines)
        self.add(dots)
        self.add(glow_dots)

        # Question
        st = "$\\big\\{1,\\dots, 2000\\big\\}$"
        question = OldTexText(
            f"How many subsets of {st}\\\\", "have a sum divisible by 5?",
            tex_to_color_map={st: TEAL}
        )
        question.set_backstroke(BLACK, width=20)
        # question.set_width(FRAME_WIDTH - 0.5)
        question.set_width(FRAME_WIDTH - 3.5)
        question.to_edge(UP, buff=0.25)
        br = VGroup(BackgroundRectangle(question[:2], buff=SMALL_BUFF), BackgroundRectangle(question[2], buff=SMALL_BUFF))
        br.set_fill(BLACK, 2)
        # self.add(br, question)

        # Complex

        words = Text("Use complex numbers of course...", color=YELLOW)
        words.set_backstroke(width=20)
        # words.add_background_rectangle(opacity=0.95, buff=MED_SMALL_BUFF)
        words.set_width(FRAME_WIDTH / 2 - 0.1)
        words.to_corner(DL, buff=SMALL_BUFF)
