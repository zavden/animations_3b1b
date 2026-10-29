# ==============================================================================
# Scene:      AnnotateIntro
# Source:     videos/_2025/laplace/derivative_supplements.py (lines 16-65)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl AnnotateIntro.py AnnotateIntro -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class AnnotateIntro(InteractiveScene):
    def construct(self):
        # Test
        randy = Randolph(height=1.0)
        left_section = Rectangle(5.25, 1.5).to_edge(LEFT)
        right_section = Rectangle(5, 1.3).next_to(left_section, RIGHT, buff=0)
        left_brace = Brace(left_section, UP)
        right_brace = Brace(right_section, RIGHT)

        q_marks = Tex(R"???", font_size=36)
        length_question = VGroup(Vector(LEFT), q_marks, Vector(RIGHT))
        length_question.arrange(RIGHT)
        length_question.match_width(left_section)
        length_question.move_to(left_brace, DOWN)

        randy.next_to(left_brace, UP, buff=0.25)

        self.play(
            randy.change("maybe", look_at=left_section),
            GrowFromCenter(left_brace)
        )
        self.play(Blink(randy))
        self.wait()
        self.play(
            randy.change("hesitant", look_at=left_section),
            FadeTransform(left_brace, length_question)
        )
        self.play(Blink(randy))
        self.wait()

        # Move to right section
        arrows = length_question[0::2]
        right_brace.save_state()
        right_brace.rotate(90 * DEG)
        right_brace.replace(arrows, stretch=True)
        right_brace.set_opacity(0)

        kw = dict(path_arc=-30 * DEG, run_time=2)
        self.play(
            Restore(right_brace, **kw),
            arrows.animate.rotate(90 * DEG).set_opacity(0).replace(right_brace.saved_state, stretch=True).set_anim_args(**kw),
            q_marks.animate.next_to(right_brace.saved_state, RIGHT).set_anim_args(**kw),
            randy.change("pondering", right_section),
        )

        h_lines = DashedLine(ORIGIN, 5 * LEFT).replicate(2)
        h_lines.set_stroke(WHITE, 1)
        h_lines[0].next_to(right_brace.get_corner(UL), LEFT, buff=0)
        h_lines[1].next_to(right_brace.get_corner(DL), LEFT, buff=0)
        self.play(*map(ShowCreation, h_lines))
