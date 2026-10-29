# ==============================================================================
# Scene:      DefinitionFirstVsLastGP
# Source:     videos/_2021/matrix_exp.py (lines 1497-1498)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl DefinitionFirstVsLastGP.py DefinitionFirstVsLastGP -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class DefinitionFirstVsLast(Scene):
    show_love_and_quantum = True

    def construct(self):
        # Setup objects
        top_title = Text("Textbook progression")
        low_title = Text("Discovery progression")

        top_prog = VGroup(
            OldTexText("Definition", color=BLUE),
            OldTexText("Theorem"),
            OldTexText("Proof"),
            OldTexText("Examples"),
        )
        low_prog = VGroup(
            OldTexText("Specific\n\nproblem"),
            OldTexText("General\n\nproblems"),
            OldTexText("Helpful\n\nconstructs"),
            OldTexText("Definition", color=BLUE),
        )
        progs = VGroup(top_prog, low_prog)
        for progression in progs:
            progression.arrange(RIGHT, buff=1.2)
        progs.arrange(DOWN, buff=3)
        progs.set_width(FRAME_WIDTH - 2)

        for progression in progs:
            arrows = VGroup()
            for m1, m2 in zip(progression[:-1], progression[1:]):
                arrows.add(Arrow(m1, m2))
            progression.arrows = arrows

        top_dots = OldTex("\\dots", font_size=72)
        top_dots.next_to(top_prog.arrows[0], RIGHT)
        low_dots = top_dots.copy()
        low_dots.next_to(low_prog.arrows[-1], LEFT)

        top_rect = SurroundingRectangle(top_prog, buff=MED_SMALL_BUFF)
        top_rect.set_stroke(TEAL, 2)
        top_title.next_to(top_rect, UP)
        top_title.match_color(top_rect)
        low_rect = SurroundingRectangle(low_prog, buff=MED_SMALL_BUFF)
        low_rect.set_stroke(YELLOW, 2)
        low_title.next_to(low_rect, UP)
        low_title.match_color(low_rect)
        versus = Text("vs.")

        # Show progressions
        self.add(top_prog[0])
        self.play(
            GrowArrow(top_prog.arrows[0]),
            FadeIn(top_dots, 0.2 * RIGHT, lag_ratio=0.1),
        )
        self.wait()
        kw = {"path_arc": -90 * DEGREES}
        self.play(
            LaggedStart(
                TransformFromCopy(top_prog[0], low_prog[-1], **kw),
                TransformFromCopy(top_prog.arrows[0], low_prog.arrows[-1], **kw),
                TransformFromCopy(top_dots, low_dots, **kw),
            ),
            Write(versus)
        )
        self.wait()

        self.play(
            ShowCreation(top_rect),
            FadeIn(top_title, 0.25 * UP)
        )
        self.play(
            FadeOut(top_dots),
            FadeIn(top_prog[1]),
        )
        for arrow, term in zip(top_prog.arrows[1:], top_prog[2:]):
            self.play(
                GrowArrow(arrow),
                FadeIn(term, shift=0.25 * RIGHT),
            )
        self.wait()

        self.play(
            ShowCreation(low_rect),
            FadeIn(low_title, 0.25 * UP),
            versus.animate.move_to(midpoint(low_title.get_top(), top_rect.get_bottom())),
        )
        self.wait()
        self.play(FadeIn(low_prog[0]))
        self.play(
            GrowArrow(low_prog.arrows[0]),
            FadeIn(low_prog[1], shift=0.25 * RIGHT),
        )
        self.play(
            GrowArrow(low_prog.arrows[1]),
            FadeIn(low_prog[2], shift=0.25 * RIGHT),
            FadeOut(low_dots),
        )
        self.wait()

        # Highlight specific example
        full_rect = FullScreenRectangle()
        full_rect.set_fill(BLACK, opacity=0.75)
        sp, gp, hc = low_prog[:3].copy()
        self.add(full_rect, sp)
        self.play(FadeIn(full_rect))
        self.wait()

        # Go to general
        if not self.show_love_and_quantum:
            self.play(FadeIn(gp))
            self.play(FlashAround(gp, color=BLUE, run_time=2))
            self.wait()
            return

        # Love and quantum
        love = SVGMobject("hearts")
        love.set_height(1)
        love.set_fill(RED, 1)
        love.set_stroke(MAROON_B, 1)

        quantum = OldTex("|\\psi\\rangle")
        quantum.set_color(BLUE)
        quantum.match_height(love)
        group = VGroup(quantum, love)
        group.arrange(RIGHT, buff=MED_LARGE_BUFF)
        group.next_to(sp, UP, MED_LARGE_BUFF)

        love.save_state()
        love.match_x(sp)
        self.play(Write(love))
        self.wait()
        self.play(
            Restore(love),
            FadeIn(quantum, 0.5 * LEFT)
        )
        self.wait()
        self.play(
            love.animate.center().scale(1.5),
            FadeOut(quantum),
            FadeOut(sp),
            full_rect.animate.set_fill(opacity=1)
        )
        self.wait()


class DefinitionFirstVsLastGP(DefinitionFirstVsLast):
    show_love_and_quantum = False
