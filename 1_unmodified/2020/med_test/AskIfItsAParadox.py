# ==============================================================================
# Scene:      AskIfItsAParadox
# Source:     videos/_2020/med_test.py (lines 1871-1963)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl AskIfItsAParadox.py AskIfItsAParadox -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class AskIfItsAParadox(TeacherStudentsScene):
    def construct(self):
        # Add fact
        stats = VGroup(
            OldTexText("Sensitivity: ", "90\\%"),
            OldTexText("Specificity: ", "91\\%"),
            OldTexText("Prevalence: ", "1\\%"),
        )
        stats.arrange(DOWN, buff=0.25, aligned_edge=LEFT)
        for stat, color in zip(stats, [GREEN_B, GREY_B, YELLOW]):
            stat[0].set_color(color)
            stat[1].align_to(stats[0][1], LEFT)

        brace = Brace(stats, UP)
        prob = OldTex(
            "P(\\text{Cancer} \\,|\\, +) \\approx \\frac{1}{11}",
            tex_to_color_map={
                "\\text{Cancer}": YELLOW,
                "+": GREEN,
            }
        )
        prob.next_to(brace, UP, buff=SMALL_BUFF)

        fact = VGroup(stats, brace, prob)
        fact.to_corner(UL)

        box = SurroundingRectangle(fact, buff=MED_SMALL_BUFF)
        box.set_fill(BLACK, 0.5)
        box.set_stroke(WHITE, 2)
        fact.add_to_back(box)
        fact.to_edge(UP, buff=SMALL_BUFF)

        self.add(fact)

        # Commentary
        self.student_says(
            "I'm sorry, is that\\\\a paradox?",
            target_mode="sassy",
            index=1
        )
        self.play_student_changes(
            "angry", "sassy", "angry",
            added_anims=[self.teacher.change, "guilty"]
        )
        self.wait(2)

        p_triangle = SVGMobject("PenroseTriangle")
        p_triangle.remove(p_triangle[0])
        p_triangle.set_fill(opacity=0)
        p_triangle.set_stroke(GREY_B, 3)
        p_triangle.set_gloss(1)
        p_triangle.set_height(3)
        p_triangle.next_to(self.students[2].get_corner(UR), UP)
        p_triangle = CurvesAsSubmobjects(p_triangle[0])

        self.play(
            self.students[0].change, "thinking", p_triangle,
            RemovePiCreatureBubble(
                self.students[1], target_mode="tease", look_at=p_triangle,
            ),
            self.students[2].change, "raise_right_hand", p_triangle,
            self.teacher.change, "tease", p_triangle,
            ShowCreation(p_triangle, run_time=2, lag_ratio=0.01),
        )
        self.wait(3)

        # Veridical paradox
        v_paradox = OldTexText("``Veridical paradox''", font_size=72)
        v_paradox.move_to(self.hold_up_spot, DOWN)
        v_paradox.to_edge(UP)
        v_paradox.shift(0.5 * LEFT)
        vp_line = Underline(v_paradox)

        self.play(
            FadeIn(v_paradox, shift=UP),
            self.change_students(*3 * ["pondering"], look_at=v_paradox),
            FadeOut(p_triangle, shift=UP),
            self.teacher.change, "raise_right_hand", v_paradox
        )
        self.play(ShowCreation(vp_line))
        self.wait()

        definition = OldTexText(
            "- Provably true\\\\",
            "- Seems false",
            alignment="",
        )
        definition.next_to(v_paradox, DOWN, MED_LARGE_BUFF, aligned_edge=LEFT)

        for part in definition:
            self.play(FadeIn(part, shift=0.25 * RIGHT))
            self.wait()
        self.wait(5)
