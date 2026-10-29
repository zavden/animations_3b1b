# ==============================================================================
# Scene:      AlicesFaceAverage
# Source:     videos/_2021/shadows.py (lines 2510-2720)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl AlicesFaceAverage.py AlicesFaceAverage -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class AlicesFaceAverage(Scene):
    def construct(self):
        # Background
        background = FullScreenRectangle()
        self.add(background)

        panels = Rectangle(2, 2.5).replicate(5)
        panels.set_stroke(WHITE, 1)
        panels.set_fill(BLACK, 1)
        dots = OldTex("\\dots")
        panels.replace_submobject(3, dots)
        panels.arrange(RIGHT, buff=0.25)
        panels.set_width(FRAME_WIDTH - 1)
        panels.move_to(2 * DOWN, DOWN)
        self.add(panels)
        panels = VGroup(*panels[:-2], panels[-1])

        # Label the rotations
        indices = ["1", "2", "3", "n"]
        rot_labels = VGroup(*(
            OldTex(f"R_{i}") for i in indices
        ))
        for label, panel in zip(rot_labels, panels):
            label.set_height(0.3)
            label.next_to(panel, DOWN)

        rot_words = Text("Sequence of random rotations")
        rot_words.next_to(rot_labels, DOWN, MED_LARGE_BUFF)

        self.play(Write(rot_words, run_time=2))
        self.wait(2)
        self.play(LaggedStartMap(
            FadeIn, rot_labels,
            shift=0.25 * DOWN,
            lag_ratio=0.5
        ))
        self.wait()

        # Show the shadow areas
        font_size = 30
        fra_labels = VGroup(*(
            OldTex(
                f"f(R_{i})", "\\cdot ", "A",
                tex_to_color_map={"A": BLUE},
                font_size=font_size
            )
            for i in indices
        ))

        DARK_BLUE = interpolate_color(BLUE_D, BLUE_E, 0.5)
        area_shadow_labels = VGroup(*(
            OldTex(
                "\\text{Area}(", "\\text{Shadow}_" + i, ")",
                tex_to_color_map={"\\text{Shadow}_" + i: DARK_BLUE},
                font_size=font_size
            )
            for i in indices
        ))
        s_labels = VGroup(*(
            OldTex(
                f"S_{i}", "=",
                tex_to_color_map={f"S_{i}": DARK_BLUE},
                font_size=font_size
            )
            for i in indices
        ))
        label_arrows = VGroup()

        for fra, area, s_label, panel in zip(fra_labels, area_shadow_labels, s_labels, panels):
            fra.next_to(panel, UP, SMALL_BUFF)
            area.next_to(fra, UP)
            area.to_edge(UP, buff=LARGE_BUFF)
            label_arrows.add(Arrow(area, fra, buff=0.2, stroke_width=3))

            fra.generate_target()
            eq = VGroup(s_label, fra.target)
            eq.arrange(RIGHT, buff=SMALL_BUFF)
            eq.move_to(fra, DOWN)

        self.add(area_shadow_labels)
        self.add(fra_labels)
        self.add(label_arrows)

        lr = 0.2
        self.play(
            LaggedStartMap(FadeIn, area_shadow_labels, lag_ratio=lr),
            LaggedStartMap(ShowCreation, label_arrows, lag_ratio=lr),
            LaggedStartMap(FadeIn, fra_labels, shift=DOWN, lag_ratio=lr),
        )
        self.wait()
        self.play(
            LaggedStart(*(
                FadeTransform(area, area_s)
                for area, area_s in zip(area_shadow_labels, s_labels)
            ), lag_ratio=lr),
            LaggedStartMap(MoveToTarget, fra_labels, lag_ratio=lr),
            LaggedStartMap(Uncreate, label_arrows, lag_ratio=lr),
        )

        # Show average
        sample_average = OldTex(
            "\\text{Sample average}", "=",
            "\\frac{1}{n}", "\\left(",
            "f(R_1)", "\\cdot ", "A", "+",
            "f(R_2)", "\\cdot ", "A", "+",
            "f(R_3)", "\\cdot ", "A", "+",
            "\\cdots ",
            "f(R_n)", "\\cdot ", "A",
            "\\right)",
            font_size=font_size
        )
        sample_average.set_color_by_tex("A", BLUE)
        sample_average.to_edge(UP, buff=MED_SMALL_BUFF)
        for tex in ["\\left", "\\right"]:
            part = sample_average.get_part_by_tex(tex)
            part.scale(1.5)
            part.stretch(1.5, 1)

        self.play(FadeIn(sample_average[:2]))
        self.play(
            TransformMatchingShapes(
                fra_labels.copy(),
                sample_average[4:-1]
            )
        )
        self.wait()
        self.play(
            Write(VGroup(*sample_average[2:4], sample_average[-1]))
        )
        self.wait()

        # Factor out A
        sample_average.generate_target()
        cdots = sample_average.target.get_parts_by_tex("\\cdot", substring=False)
        As = sample_average.target.get_parts_by_tex("A", substring=False)
        new_pieces = VGroup(*(
            sm for sm in sample_average.target
            if sm.get_tex() not in ["A", "\\cdot"]
        ))
        new_A = As[0].copy()
        new_cdot = cdots[0].copy()
        new_pieces.insert_submobject(2, new_cdot)
        new_pieces.insert_submobject(2, new_A)
        new_pieces.arrange(RIGHT, buff=SMALL_BUFF)
        new_pieces.move_to(sample_average)
        for group, target in (As, new_A), (cdots, new_cdot):
            for sm in group:
                sm.replace(target)
            group[1:].set_opacity(0)

        self.play(LaggedStart(
            *(
                FlashAround(mob, time_width=3)
                for mob in sample_average.get_parts_by_tex("A")
            ),
            lag_ratio=0.1,
            run_time=2
        ))
        self.play(MoveToTarget(sample_average, path_arc=-PI / 5))
        self.wait()

        # True average
        brace = Brace(new_pieces[4:], DOWN, buff=SMALL_BUFF, font_size=30)
        lim = OldTex("n \\to \\infty", font_size=30)
        lim.next_to(brace, DOWN)
        VGroup(brace, lim).set_color(YELLOW)
        sample = sample_average[0][:len("Sample")]
        cross = Cross(sample)
        cross.insert_n_curves(20)
        cross.scale(1.5)

        self.play(
            FlashAround(sample_average[2:], run_time=3, time_width=1.5)
        )
        self.play(
            FlashUnder(sample_average[:2], color=RED),
            run_time=2
        )
        self.play(
            GrowFromCenter(brace),
            FadeIn(lim, 0.25 * DOWN),
            ShowCreation(cross)
        )
        self.play(
            LaggedStart(*map(FadeOut, [
                *fra_labels, *s_labels, *panels, dots, *rot_labels, rot_words
            ]))
        )
        self.wait()

        # Some constant
        rect = SurroundingRectangle(
            VGroup(new_pieces[4:], brace, lim),
            buff=SMALL_BUFF,
        )
        rect.set_stroke(YELLOW, 1)
        rect.stretch(0.98, 0)
        words = Text("Some constant")
        words.next_to(rect, DOWN)
        subwords = Text("Independent of the size and shape of the 2d piece")
        subwords.scale(0.5)
        subwords.next_to(words, DOWN)
        subwords.set_fill(GREY_A)

        self.play(
            ShowCreation(rect),
            FadeIn(words, 0.25 * DOWN)
        )
        self.wait()
        self.play(Write(subwords))
        self.wait()
