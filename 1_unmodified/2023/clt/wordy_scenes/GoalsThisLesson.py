# ==============================================================================
# Scene:      GoalsThisLesson
# Source:     videos/_2023/clt/wordy_scenes.py (lines 513-604)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl GoalsThisLesson.py GoalsThisLesson -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class GoalsThisLesson(TeacherStudentsScene):
    def construct(self):
        self.add(self.screen)
        self.screen.set_stroke(width=2)
        morty = self.teacher
        stds = self.students

        self.play(
            morty.change("tease"),
            self.change_students("confused", "thinking", "hesitant", look_at=self.screen)
        )
        self.wait(2)

        # Goals
        title = Text("Goals of this lesson", font_size=60)
        title.to_corner(UR)
        underline = Underline(title)
        underline.scale(1.2)
        underline.set_color(GREY_B)

        goals = BulletedList(
            "Make this quantitative",
            "Put formulas to it",
            "Use it to predict",
            buff=0.35,
            font_size=48
        )
        goals.next_to(underline, DOWN, MED_LARGE_BUFF)
        goals.align_to(title, LEFT)

        self.play(
            FadeIn(title),
            ShowCreation(underline),
            morty.change("raise_right_hand", title),
            self.change_students("erm", "thinking", "tease", look_at=title)
        )
        self.wait()

        for goal in goals:
            self.play(FadeIn(goal, UP))
            self.wait()

        # Three assumptions
        new_title = VGroup(
            Text("3 assumptions underlie the"),
            Text("Central Limit Theorem"),
        )
        for line in new_title:
            line.match_width(title)
        new_title.arrange(DOWN)
        new_title.move_to(title, UP)
        new_title.set_color(RED)

        numbers = VGroup(Tex("1."), Tex("2."), Tex("3."))
        numbers.arrange(DOWN, buff=0.5, aligned_edge=LEFT)
        numbers.next_to(new_title, DOWN, buff=0.75, aligned_edge=LEFT)
        numbers.set_color(RED)

        boxes = VGroup(*(
            Rectangle(height=1.2 * num.get_height(), width=4).next_to(num)
            for num in numbers
        ))
        boxes.set_stroke(width=0)
        boxes.set_fill(interpolate_color(RED_E, BLACK, 0.8), 1)
        for box in boxes:
            box.save_state()
            box.stretch(0, 0, about_edge=LEFT)

        self.play(
            FadeOut(title, 0.5 * DOWN),
            FadeIn(new_title, 0.5 * DOWN),
            underline.animate.next_to(new_title, DOWN, SMALL_BUFF).set_color(RED_E),
            LaggedStartMap(FadeOut, goals, shift=DOWN),
            morty.change("tease", new_title),
            self.change_students("hesitant", "pondering", "skeptical", new_title),
        )
        self.play(
            FadeIn(numbers, lag_ratio=0.25),
            morty.change("raise_left_hand")
        )
        self.wait(2)
        self.play(
            LaggedStartMap(Restore, boxes),
            LaggedStart(
                morty.change("tease"),
                stds[0].change("angry"),
                stds[1].change("hesitant"),
                stds[2].change("erm"),
                lag_ratio=0.2
            )
        )
        self.wait(4)
