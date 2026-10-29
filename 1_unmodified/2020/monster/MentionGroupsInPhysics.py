# ==============================================================================
# Scene:      MentionGroupsInPhysics
# Source:     videos/_2020/monster.py (lines 1662-1732)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl MentionGroupsInPhysics.py MentionGroupsInPhysics -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class MentionGroupsInPhysics(TeacherStudentsScene):
    def construct(self):
        # Intro
        self.teacher_says("Groups are ubiquitous\\\\in physics.")
        self.play_student_changes("thinking", "happy", "hesitant")
        self.wait(4)

        noether = ImageMobject("EmmyNoether")
        noether.set_height(3)
        noether.to_corner(UL)

        nt_label = OldTexText("Noether's theorem")
        nt_label.set_height(0.5)
        nt_label.move_to(self.hold_up_spot, DOWN)

        self.play(
            FadeIn(nt_label, DOWN),
            FadeIn(noether, DOWN),
            FadeOut(VGroup(self.teacher.bubble, self.teacher.bubble.content)),
            self.teacher.change, "raise_right_hand",
        )
        self.play_student_changes("pondering", "pondering", "thinking", look_at=nt_label)

        # Theorem
        nt_label.generate_target()
        nt_label.target.center().to_edge(UP)
        rule = VGroup(
            OldTexText("Conservation law", color=BLUE),
            OldTex("\\Leftrightarrow"),
            OldTexText("Symmetry", color=YELLOW),
        )
        rule.set_height(0.5)
        rule.arrange(RIGHT)
        rule.next_to(nt_label.target, DOWN, MED_LARGE_BUFF)

        self.look_at(
            nt_label.target,
            added_anims=[MoveToTarget(nt_label)]
        )
        self.play(
            self.teacher.change, "happy", rule,
            *[
                FadeIn(part, rule.get_center() - part.get_center())
                for part in rule
            ],
        )
        self.wait(2)

        # Examples
        examples = VGroup(
            OldTexText("Momentum", " $\\Leftrightarrow$ ", "Translation in space"),
            OldTexText("Energy", " $\\Leftrightarrow$ ", "Translation in time"),
        )
        examples.arrange(DOWN, buff=MED_LARGE_BUFF)
        examples.next_to(rule, DOWN, buff=MED_LARGE_BUFF)
        for example in examples:
            example[0].set_color(BLUE)
            example[2].set_color(YELLOW)
            example.shift((rule[1].get_x() - example[1].get_x()) * RIGHT)

        self.play(
            self.teacher.change, "raise_right_hand",
            FadeIn(examples[0], UP),
            self.change_students("confused", "erm", "pondering")
        )
        self.look_at(rule)
        self.wait()
        self.play(FadeIn(examples[1], UP))
        self.wait(4)
        self.play_student_changes("thinking", "maybe", "thinking")
        self.wait(4)
