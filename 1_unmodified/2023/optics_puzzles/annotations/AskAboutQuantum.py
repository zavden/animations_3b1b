# ==============================================================================
# Scene:      AskAboutQuantum
# Source:     videos/_2023/optics_puzzles/annotations.py (lines 649-758)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl AskAboutQuantum.py AskAboutQuantum -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class AskAboutQuantum(TeacherStudentsScene):
    def construct(self):
        morty = self.teacher
        stds = self.students

        # Question
        self.play(
            stds[0].says("What about, like,\nphotons and quantum stuff?"),
            morty.change("well"),
            self.change_students(None, "sassy", "hesitant", look_at=stds[0].eyes),
        )
        self.wait(3)

        # Create T chart
        titles = VGroup(
            Text("Classical"),
            Text("Quantum"),
        )
        v_lines = Line(UP, DOWN).replicate(2).set_height(4.5)
        v_lines.arrange(RIGHT, buff=titles[0].get_width() + 0.75)
        v_lines.to_edge(UP, buff=0)
        v_lines.shift(1.5 * RIGHT)
        h_line = Line(LEFT, RIGHT)
        h_line.set_width(13.25)
        h_line.to_edge(UP, buff=titles.get_height() + 0.5)
        h_line.set_x(0)
        lines = VGroup(h_line, *v_lines)
        lines.set_stroke(WHITE, 2)

        titles[0].move_to(v_lines).to_edge(UP, buff=0.25)
        titles[1].next_to(v_lines, RIGHT, buff=0.5).match_y(titles[0])

        # Points
        points = VGroup(
            Text("Waves radiate away from changing charges"),
            Text("These waves have polarization"),
            Text("Energy scales continuously"),
        )
        points.scale(0.7)
        points.arrange(DOWN, buff=0.5, aligned_edge=LEFT)
        points.next_to(h_line, DOWN, buff=0.5, aligned_edge=LEFT)

        soft_h_lines = h_line.replicate(len(points))
        soft_h_lines.set_stroke(WHITE, 1, opacity=0.5)
        for point, soft_line in zip(points, soft_h_lines):
            soft_line.next_to(point, DOWN, buff=0.25)
            soft_line.align_to(h_line, LEFT)

        checks = VGroup(*(
            Checkmark().match_x(title).match_y(point)
            for point in points
            for title in titles
        ))
        cross = Exmark().move_to(checks[-1])

        last_q_point = Text(
            """
            Energy comes in
            discrete chunks
            (that is, in quanta)
            """,
            alignment="LEFT"
        )
        last_q_point.scale(0.7)
        last_q_point.next_to(cross, DOWN, buff=0.5)
        last_q_point.align_to(titles[1], LEFT)
        last_q_point.set_color(YELLOW)

        # Animate in the charge
        self.play(
            morty.change("raise_right_hand"),
            FadeTransform(stds[0].bubble.content["quantum"].copy(), titles[1]),
            FadeIn(titles[0], shift=0.25 * UP),
            ShowCreation(h_line),
            ShowCreation(v_lines),
            Write(soft_h_lines),
            stds[0].debubble(mode="pondering"),
            self.change_students(None, "pondering", "pondering", look_at=UP),
            run_time=2,
        )
        self.wait()

        # Points
        self.play(
            FadeIn(points[0], lag_ratio=0.1),
            Write(checks[:2], lag_ratio=0.7, stroke_color=GREEN),
            *(pi.animate.look_at(titles) for pi in self.pi_creatures)
        )
        self.wait()
        self.play(
            FadeIn(points[1], lag_ratio=0.1),
            Write(checks[2:4], lag_ratio=0.7, stroke_color=GREEN)
        )
        self.wait()

        self.play(
            FadeIn(points[2], lag_ratio=0.1),
            Write(checks[4], stroke_color=GREEN),
            FadeIn(cross, scale=0.5),
            morty.change("sassy", look_at=cross)
        )
        self.wait()

        self.play(
            FadeOut(self.pi_creatures, DOWN),
            FadeOut(soft_h_lines[-1]),
            # FadeIn(last_q_point, lag_ratio=0.1),
            v_lines.animate.set_height(7, about_edge=UP, stretch=True),
        )
        self.wait()
