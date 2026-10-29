# ==============================================================================
# Scene:      SARS2002
# Source:     videos/_2020/sir.py (lines 2392-2441)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl SARS2002.py SARS2002 -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class SARS2002(TeacherStudentsScene):
    def construct(self):
        image = ImageMobject("sars_icon")
        image.set_height(3.5)
        image.move_to(self.hold_up_spot, DR)
        image.shift(RIGHT)

        name = OldTexText("2002 SARS Outbreak")
        name.next_to(image, LEFT, MED_LARGE_BUFF, aligned_edge=UP)

        n_cases = VGroup(
            Integer(0, edge_to_fix=UR),
            OldTexText("total cases")
        )
        n_cases.arrange(RIGHT)
        n_cases.scale(1.25)
        n_cases.next_to(name, DOWN, buff=2)

        arrow = Arrow(name.get_bottom(), n_cases.get_top())

        n_cases.shift(MED_SMALL_BUFF * RIGHT)

        self.play(
            self.teacher.change, "raise_right_hand",
            FadeIn(image, DOWN, run_time=2),
            self.change_students(
                "pondering", "thinking", "pondering",
                look_at=image,
            )
        )
        self.play(
            FadeIn(name, RIGHT),
        )
        self.play(
            GrowArrow(arrow),
            UpdateFromAlphaFunc(
                n_cases,
                lambda m, a: m.set_opacity(a),
            ),
            ChangeDecimalToValue(n_cases[0], 8098),
            self.change_students(look_at=n_cases),
        )
        self.wait()
        self.play_all_student_changes(
            "thinking", look_at=n_cases,
        )
        self.play(self.teacher.change, "tease")
        self.wait(6)

        self.embed()
