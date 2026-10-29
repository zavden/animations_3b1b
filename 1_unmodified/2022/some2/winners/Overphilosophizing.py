# ==============================================================================
# Scene:      Overphilosophizing
# Source:     videos/_2022/some2/winners.py (lines 1081-1146)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl Overphilosophizing.py Overphilosophizing -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class Overphilosophizing(TeacherStudentsScene):
    def construct(self):
        # Start
        morty = self.teacher

        rects = VGroup(*(
            Rectangle(width=w)
            for w in [2, 9, 2]
        ))
        rects.set_height(1.0, stretch=True)
        rects.arrange(RIGHT, buff=0)
        rects.set_stroke(WHITE, 1)
        rects.set_fill(opacity=0.5)
        rects.set_submobject_colors_by_gradient(YELLOW_E, BLUE, GREY_BROWN)
        rects.set_y(2)

        words = VGroup(*map(Text, ["Motivation", "Core lesson", "Broader\nconnections"]))
        words.scale(0.7)
        for word, rect in zip(words, rects):
            word.rect = rect
            word.start_width = word.get_width()
            word.add_updater(lambda m: m.set_max_width(min(m.rect.get_width() * 0.8, m.start_width)))
            word.add_updater(lambda m: m.move_to(m.rect))

        self.add(*rects, *words)

        # Shift sizes
        def left_shift(x, rects=rects, **kw):
            return (
                rects[0].animate.set_width(rects[0].get_width() + x, about_edge=LEFT, stretch=True).set_anim_args(**kw),
                rects[1].animate.set_width(rects[1].get_width() - x, about_edge=RIGHT, stretch=True).set_anim_args(**kw),
            )

        def right_shift(x, rects=rects, **kw):
            return (
                rects[1].animate.set_width(rects[1].get_width() + x, about_edge=LEFT, stretch=True).set_anim_args(**kw),
                rects[2].animate.set_width(rects[2].get_width() - x, about_edge=RIGHT, stretch=True).set_anim_args(**kw),
            )

        self.play(
            morty.change("guilty"),
            self.change_students("erm", "erm", "erm", look_at=rects),
        )
        self.wait()
        self.play(*left_shift(2, run_time=3))
        self.play(self.change_students("tired", "dejected", "tired", look_at=rects))
        self.wait()
        self.play(
            morty.change("raise_right_hand"),
            self.change_students("thinking", "thinking", "thinking", look_at=rects),
            *left_shift(-3),
        )
        self.wait()
        self.play(*right_shift(-1))

        # Examples beat philosophy
        exs = OldTexText("Examples", " > Sweeping statements", font_size=36)
        exs.to_edge(UP)
        exs.align_to(rects, LEFT)
        arrow = Arrow(exs[0].get_bottom(), rects[0].get_top(), buff=0.1)

        self.play(
            Write(exs),
            ShowCreation(arrow),
        )
        self.wait(4)
