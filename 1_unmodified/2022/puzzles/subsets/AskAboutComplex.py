# ==============================================================================
# Scene:      AskAboutComplex
# Source:     videos/_2022/puzzles/subsets.py (lines 4080-4171)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl AskAboutComplex.py AskAboutComplex -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class AskAboutComplex(TeacherStudentsScene):
    def construct(self):
        # Ask
        morty = self.teacher
        ss = self.students
        self.student_says("Why complex\nnumbers?")
        self.play(
            ss[0].change("pondering"),
            ss[1].change("erm"),
            morty.change("tease"),
        )
        self.wait(2)
        self.play(
            RemovePiCreatureBubble(ss[2], target_mode="erm", look_at=morty.eyes),
            morty.change("hesitant"),
        )
        self.wait(2)

        # Hidden information
        kw = dict(tex_to_color_map={
            "x": BLUE,
            "{0}": BLUE,
            "{1}": BLUE,
            "{-1}": BLUE,
        })
        fx, f0, f1, fm1 = lines = VGroup(
            Tex("f(x) = \\sum_{n = 0}^N c_n x^n", **kw),
            Tex("f({0}) = c_0", **kw),
            Tex("f({1}) = c_0 + c_1 + c_2 + \\cdots + c_n", **kw),
            Tex("f({-1}) = c_0 - c_1 + c_2 - \\cdots + c_n", **kw),
        )
        lines.arrange(DOWN, buff=MED_LARGE_BUFF, aligned_edge=LEFT)
        lines.set_height(4)
        lines[0].next_to(lines[1], LEFT, LARGE_BUFF)
        lines.next_to(morty, UL).to_edge(UP)

        self.play(
            morty.change("raise_right_hand"),
            FadeInFromPoint(fx, morty.get_center(), run_time=2),
            ss[1].change("hesitant", lines)
        )
        for line in lines[1:]:
            self.play(FadeIn(line, 0.5 * DOWN))
        self.wait()
        self.play(morty.change("tease"))
        self.wait()

        # Blank check
        new_line = Tex(
            "f(\\dots) = \\text{(more information)}",
            tex_to_color_map={"\\dots": BLUE}
        )
        new_line.match_height(lines[-1])
        new_line.next_to(lines[-1], DOWN, MED_LARGE_BUFF, aligned_edge=LEFT)

        dots_in_set = Tex(
            "x \\in \\mathds{R}",
            isolate=["\\mathds{R}", "\\dots"],
            tex_to_color_map={"x": BLUE},
            font_size=60
        )
        dots_in_set.next_to(morty, UR, MED_LARGE_BUFF).shift_onto_screen()
        set_part = dots_in_set.select_part("\\mathds{R}")
        C_set = Tex("\\mathds{C}", color=TEAL, font_size=60)
        C_set.move_to(set_part)

        self.play(
            Write(new_line),
            self.change_students(
                "thinking", "hesitant", "pondering",
                look_at=new_line,
            ),
        )
        self.wait()
        self.play(
            TransformFromCopy(
                new_line.select_part("\\dots"),
                dots_in_set.select_part("x"),
                path_arc=-45 * DEGREES,
            ),
            morty.change("raise_left_hand", dots_in_set),
        )
        self.play(Write(dots_in_set[1:]))
        self.wait()
        self.play(
            morty.change("shruggie"),
            ss[0].change("pondering"),
            ss[2].change("hesitant"),
            FadeOut(dots_in_set.select_part("\\mathds{R}"), UP),
            FadeIn(C_set, UP),
        )
        self.wait(5)
