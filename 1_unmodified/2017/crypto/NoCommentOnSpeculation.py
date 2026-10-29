# ==============================================================================
# Scene:      NoCommentOnSpeculation
# Source:     videos/_2017/crypto.py (lines 327-397)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl NoCommentOnSpeculation.py NoCommentOnSpeculation -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class NoCommentOnSpeculation(TeacherStudentsScene):
    def construct(self):
        axes = VGroup(
            Line(0.25*LEFT, 4*RIGHT),
            Line(0.25*DOWN, 3*UP),
        )
        times = np.arange(0, 4.25, 0.25)
        prices = [
            0.1, 0.5, 1.75, 1.5,
            2.75, 2.2, 1.3, 0.8,
            1.1, 1.3, 1.2, 1.4,
            1.5, 1.7, 1.2, 1.3,
        ]
        graph = VMobject()
        graph.set_points_as_corners([
            time*RIGHT + price*UP
            for time, price in zip(times, prices)
        ])
        graph.set_stroke(BLUE)
        group = VGroup(axes, graph)
        group.next_to(self.teacher, UP+LEFT)

        cross = Cross(group)

        mining_graphic = ImageMobject("bitcoin_mining_graphic")
        mining_graphic.set_height(2)
        mining_graphic.next_to(self.teacher, UP+LEFT)
        mining_cross = Cross(mining_graphic)
        mining_cross.set_stroke(RED, 8)

        axes.save_state()
        axes.shift(DOWN)
        axes.fade(1)
        self.play(
            self.teacher.change, "sassy",
            axes.restore,
        )
        self.play(ShowCreation(
            graph, run_time = 2,
            rate_func=linear
        ))
        self.wait()
        self.play(ShowCreation(cross))
        group.add(cross)
        self.play(
            group.shift, FRAME_WIDTH*RIGHT,
            self.teacher.change, "happy"
        )
        self.wait()

        self.student_says(
            "But...what are they?",
            index = 0,
            target_mode = "confused"
        )
        self.wait(2)
        self.play(
            FadeIn(mining_graphic),
            RemovePiCreatureBubble(self.students[0]),
            self.teacher.change, "sassy",
        )
        self.play(ShowCreation(mining_cross))
        self.wait()
        self.play(
            VGroup(mining_graphic, mining_cross).shift,
            FRAME_WIDTH*RIGHT
        )
        black_words = OldTexText("Random words\\\\Blah blah")
        black_words.set_color(BLACK)
        self.teacher_thinks(black_words)
        self.zoom_in_on_thought_bubble()
