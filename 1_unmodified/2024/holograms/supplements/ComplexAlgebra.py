# ==============================================================================
# Scene:      ComplexAlgebra
# Source:     videos/_2024/holograms/supplements.py (lines 1557-1775)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ComplexAlgebra.py ComplexAlgebra -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ComplexAlgebra(InteractiveScene):
    def construct(self):
        # Add first lines
        lines = VGroup(
            Tex(R"R \cdot |R + O|^2"),
            Tex(R"R \cdot (R + O)(R^* + O^*)"),
            Tex(R"R \cdot R \cdot R^* + R \cdot R^* \cdot O  + R \cdot R \cdot O^*+ R \cdot O \cdot O^*"),
            Tex(R"\left(|R|^2 + |O|^2 \right) \cdot R + |R|^2 \cdot O + R^2 \cdot O^*"),
        )
        lines[2].scale(0.75)
        lines.arrange(DOWN, buff=LARGE_BUFF)
        lines.to_edge(UP)

        label = Text("Part of the wave\nbeyond the film", font_size=36)
        arrow = Vector(LEFT)
        arrow.next_to(lines[0], RIGHT)
        label.next_to(arrow, RIGHT)
        label.shift_onto_screen()

        self.add(lines[0])
        self.play(
            Write(label),
            GrowArrow(arrow)
        )
        self.wait()
        self.play(LaggedStart(
            TransformFromCopy(lines[0][:-1], lines[1][R"R \cdot (R + O)"][0]),
            TransformFromCopy(lines[0]["|R + O|"][0].copy(), lines[1]["(R^* + O^*)"][0]),
            lag_ratio=0.1,
            run_time=2
        ))
        self.wait()

        # FOIL expansion
        R0 = lines[1]["R"][0]
        R = lines[1]["R"][1]
        O = lines[1]["O"][0]
        Rc = lines[1]["R^*"][0]
        Oc = lines[1]["O^*"][0]
        l1_groups = [
            VGroup(R0, R, Rc),
            VGroup(R0, O, Rc),
            VGroup(R0, R, Oc),
            VGroup(R0, O, Oc),
        ]
        l2_groups = [
            lines[2][substr]
            for substr in [
                R"R \cdot R \cdot R^*",
                R"R \cdot R^* \cdot O",
                R"R \cdot R \cdot O^*",
                R"R \cdot O \cdot O^*",
            ]
        ]
        plusses = lines[2]["+"]
        plusses.add_to_back(VectorizedPoint())

        pre_rects = VGroup(map(self.get_term_rect, l1_groups[0]))
        post_rect = self.get_term_rect(l2_groups[0])
        VGroup(pre_rects, post_rect).set_stroke(width=0, opacity=0)
        self.add(pre_rects, post_rect)

        for l1_group, l2_group, plus in zip(l1_groups, l2_groups, plusses):
            self.play(
                Transform(pre_rects, VGroup(map(self.get_term_rect, l1_group))),
                Transform(post_rect, self.get_term_rect(l2_group)),
                FadeIn(l2_group),
                FadeIn(plus),
            )
            self.wait(0.5)

        self.add(lines[2])
        self.play(
            FadeOut(pre_rects),
            FadeOut(post_rect),
        )
        self.wait()

        # Highlight conjugate pairs
        pair_rects = VGroup(
            self.get_term_rect(lines[2][R"R \cdot R^*"][0]),
            self.get_term_rect(lines[2][R"R \cdot R^*"][1]),
            self.get_term_rect(lines[2][R"O \cdot O^*"]),
        )
        pair_rects.set_stroke(RED, 2)

        real_label = Text("Real numbers")
        real_label.next_to(lines[2], DOWN, buff=1.5)
        real_label.set_color(RED)
        arrows = VGroup(
            Arrow(real_label, rect.get_bottom())
            for rect in pair_rects
        )
        arrows.set_color(RED)

        self.play(ShowCreation(pair_rects, lag_ratio=0.1))
        self.play(
            FadeIn(real_label, lag_ratio=0.1),
            LaggedStartMap(GrowArrow, arrows)
        )
        self.wait()
        self.play(
            FadeOut(real_label),
            FadeOut(arrows),
            FadeOut(pair_rects),
        )
        self.wait()

        # Organize into the last line
        lines[3].next_to(lines[2], DOWN, buff=1.5)
        lines[3].set_opacity(1)
        l3_groups = [
            lines[3][R"\left(|R|^2 + |O|^2 \right) \cdot R"],
            lines[3][R"|R|^2 \cdot O"],
            lines[3][R"R^2 \cdot O^*"],
        ]
        l2_plusses = lines[2]["+"]
        l3_plusses = lines[3]["+"]

        l2_rects = VGroup(map(self.get_term_rect, l2_groups))
        l3_rects = VGroup(map(self.get_term_rect, l3_groups))
        l3_rects[2].match_height(l3_rects, stretch=True, about_edge=UP)

        box1_lines = VGroup(
            self.connecting_line(l2_rects[0], l3_rects[0]),
            self.connecting_line(l2_rects[3], l3_rects[0]),
        )
        box2_line = self.connecting_line(l2_rects[1], l3_rects[1])
        box3_line = self.connecting_line(l2_rects[2], l3_rects[2])

        real_brace1 = Brace(lines[3][R"\left(|R|^2 + |O|^2 \right)"], DOWN)
        real_brace2 = Brace(lines[3][R"|R|^2"][1], DOWN)
        real_label = real_brace1.get_text("Some real number", font_size=36)

        fade_opacity = 0.5

        self.play(
            ShowCreation(box1_lines, lag_ratio=0.5),
            FadeIn(l2_rects[0]),
            FadeIn(l2_rects[3]),
            FadeTransform(l2_groups[0].copy(), l3_groups[0], time_span=(0.5, 2)),
            FadeTransform(l2_groups[3].copy(), l3_groups[0], time_span=(1, 2)),
            FadeIn(l3_rects[0], time_span=(1, 2)),
            l2_groups[1].animate.set_opacity(fade_opacity),
            l2_groups[2].animate.set_opacity(fade_opacity),
            l2_plusses.animate.set_opacity(fade_opacity),
            run_time=2
        )
        self.wait()
        self.play(
            GrowFromCenter(real_brace1),
            FadeIn(real_label, shift=0.25 * DOWN)
        )
        self.wait()
        self.play(
            box1_lines.animate.set_stroke(WHITE, 1, 0.5),
            VGroup(l2_rects[0], l2_rects[3], l3_rects[0]).animate.set_stroke(GREY, 1, 0.5),
            l2_groups[1].animate.set_opacity(1),
            l2_groups[0].animate.set_opacity(fade_opacity),
            l2_groups[3].animate.set_opacity(fade_opacity),
            l3_groups[0].animate.set_opacity(fade_opacity),
            FadeOut(real_brace1),
            real_label.animate.set_opacity(fade_opacity),
        )
        self.play(
            FadeIn(l2_rects[1]),
            ShowCreation(box2_line),
            FadeIn(l3_rects[1], time_span=(0.5, 1.5)),
            TransformMatchingShapes(l2_groups[1].copy(), l3_groups[1], run_time=1),
            FadeIn(l3_plusses[1]),
        )
        self.wait()
        self.play(
            GrowFromCenter(real_brace2),
            real_label.animate.next_to(real_brace2, DOWN).set_opacity(1)
        )
        self.wait()
        self.play(
            box2_line.animate.set_stroke(WHITE, 1, 0.5),
            VGroup(l2_rects[1], l3_rects[1]).animate.set_stroke(GREY, 1, 0.5),
            l2_groups[2].animate.set_opacity(1),
            l2_groups[1].animate.set_opacity(fade_opacity),
            l3_groups[1].animate.set_opacity(fade_opacity),
            l3_plusses[1].animate.set_opacity(fade_opacity),
            FadeOut(real_brace2),
            FadeOut(real_label),
        )
        self.play(
            FadeTransform(l2_groups[2].copy(), l3_groups[2], run_time=1.5),
            ShowCreation(box3_line, run_time=1.5),
            FadeIn(l2_rects[1]),
            FadeIn(l3_rects[2], time_span=(0.5, 1.5)),
            FadeIn(l3_plusses[2])
        )
        self.wait()

        # Bring back
        self.play(
            FadeOut(VGroup(box1_lines, box2_line, box3_line)),
            FadeOut(l2_rects),
            l3_rects.animate.set_stroke(TEAL, 1, 1),
            lines[2].animate.set_opacity(0.5),
            lines[3].animate.set_opacity(1),
        )
        self.wait()

    def get_term_rect(self, term):
        rect = SurroundingRectangle(term)
        rect.round_corners()
        rect.set_stroke(TEAL, 2)
        return rect

    def connecting_line(self, high_box, low_box):
        return CubicBezier(
            high_box.get_bottom(),
            high_box.get_bottom() + 1.0 * DOWN,
            low_box.get_top() + 1.0 * UP,
            low_box.get_top(),
        ).set_stroke(WHITE, 2)
