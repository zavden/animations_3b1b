# ==============================================================================
# Scene:      ExplainTracing
# Source:     videos/_2020/ctracing.py (lines 43-197)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ExplainTracing.py ExplainTracing -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ExplainTracing(Scene):
    def construct(self):
        # Words
        words = VGroup(
            OldTexText("Testing, ", "Testing, ", "Testing!"),
            OldTexText("Contact Tracing"),
        )
        words[0].set_color(GREEN)
        words[1].set_color(BLUE_B)
        words.set_width(FRAME_WIDTH - 2)
        words.arrange(DOWN, buff=1)

        self.play(ShowIncreasingSubsets(words[0], rate_func=linear))
        self.wait()
        self.play(Write(words[1], run_time=1))
        self.wait()

        self.play(
            words[1].to_edge, UP,
            FadeOut(words[0], 6 * UP)
        )

        ct_word = words[1][0]

        # Groups
        clusters = VGroup()
        for x in range(4):
            cluster = VGroup()
            for y in range(4):
                cluster.add(Randolph())
            cluster.arrange_in_grid(buff=LARGE_BUFF)
            clusters.add(cluster)
        clusters.scale(0.5)
        clusters.arrange_in_grid(buff=2)
        clusters.set_height(4)

        self.play(FadeIn(clusters))

        pis = VGroup()
        boxes = VGroup()
        for cluster in clusters:
            for pi in cluster:
                pis.add(pi)
                box = SurroundingRectangle(pi, buff=0.05)
                boxes.add(box)
                pi.box = box

        boxes.set_stroke(WHITE, 1)

        sicky = clusters[0][2]
        covid_words = OldTexText("COVID-19\\\\Positive!")
        covid_words.set_color(RED)
        arrow = Vector(RIGHT, color=RED)
        arrow.next_to(sicky, LEFT)
        covid_words.next_to(arrow, LEFT, SMALL_BUFF)

        self.play(
            sicky.change, "sick",
            sicky.set_color, "#9BBD37",
            FadeIn(covid_words, RIGHT),
            GrowArrow(arrow),
        )
        self.play(ShowCreation(sicky.box))
        self.wait(2)
        anims = []
        for pi in clusters[0]:
            if pi is not sicky:
                anims.append(ApplyMethod(pi.change, "tired"))
                anims.append(ShowCreation(pi.box))
        self.play(*anims)
        self.wait()

        self.play(VFadeIn(
            boxes[4:],
            run_time=2,
            rate_func=there_and_back_with_pause,
        ))
        self.wait()

        self.play(FadeOut(
            VGroup(
                covid_words,
                arrow,
                *boxes[:4],
                *pis,
            ),
            lag_ratio=0.1,
            run_time=3,
        ))
        self.play(ct_word.move_to, 2 * UP)

        # Underlines
        implies = OldTex("\\Downarrow")
        implies.scale(2)
        implies.next_to(ct_word, DOWN, MED_LARGE_BUFF)
        loc_tracking = OldTexText("Location Tracking")
        loc_tracking.set_color(GREY_BROWN)
        loc_tracking.match_height(ct_word)
        loc_tracking.next_to(implies, DOWN, MED_LARGE_BUFF)

        q_marks = OldTex("???")
        q_marks.scale(2)
        q_marks.next_to(implies, RIGHT)

        cross = Cross(implies)
        cross.set_stroke(RED, 7)

        self.play(
            Write(implies),
            FadeIn(loc_tracking, UP)
        )
        self.play(FadeIn(q_marks, lag_ratio=0.1))
        self.wait()

        parts = VGroup(ct_word[:7], ct_word[7:])
        lines = VGroup()
        for part in parts:
            line = Line(part.get_left(), part.get_right())
            line.align_to(part[0], DOWN)
            line.shift(0.1 * DOWN)
            lines.add(line)
        
        ct_word.set_stroke(BLACK, 2, background=True)
        self.add(lines[1], ct_word)
        self.play(ShowCreation(lines[1]))
        self.wait()
        self.play(ShowCreation(lines[0]))
        self.wait()

        self.play(
            ShowCreation(cross),
            FadeOut(q_marks, RIGHT),
            FadeOut(lines),
        )
        self.wait()

        dp_3t = OldTexText("DP-3T")
        dp_3t.match_height(ct_word)
        dp_3t.move_to(loc_tracking)
        dp_3t_long = OldTexText("Decentralized Privacy-Preserving Proximity Tracing")
        dp_3t_long.next_to(dp_3t, DOWN, LARGE_BUFF)

        arrow = Vector(UP)
        arrow.set_stroke(width=8)
        arrow.move_to(implies)

        self.play(
            FadeInFromDown(dp_3t),
            FadeOut(loc_tracking),
            FadeOut(implies),
            FadeOut(cross),
            ShowCreation(arrow)
        )
        self.play(Write(dp_3t_long))
        self.wait()
