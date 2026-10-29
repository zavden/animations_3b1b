# ==============================================================================
# Scene:      PreviewStrategy
# Source:     videos/_2025/laplace/derivatives.py (lines 722-804)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl PreviewStrategy.py PreviewStrategy -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class PreviewStrategy(InteractiveScene):
    def construct(self):
        # Set up terms
        rect = Rectangle(6, 4)
        ode, lt_ode, lt_ans, ans = terms = VGroup(
            Text("Differential\nEquation"),
            Text("Transformed\nEquation"),
            Text("Transformed\nSolution"),
            Text("Solution"),
        )
        VGroup(lt_ode, lt_ans).set_color(YELLOW)
        for term, corner in zip(terms, [UL, DL, DR, UR]):
            term.move_to(rect.get_corner(corner))

        # Set up arrows
        lt_arrow = self.get_lt_arrow(ode, lt_ode, buff=MED_SMALL_BUFF)
        solve_arrow = self.get_lt_arrow(lt_ode, lt_ans, label_tex=R"\substack{\text{Solve} \\ \text{(Algebraically)}}")
        solve_arrow[1][:5].scale(1.5, about_edge=DOWN).shift(0.1 * UP)
        inv_lt_arrow = self.get_lt_arrow(lt_ans, ans, label_tex=R"\mathcal{L}^{-1}", buff=MED_SMALL_BUFF)

        arrows = VGroup(lt_arrow, solve_arrow, inv_lt_arrow)

        # Show creation of terms
        self.add(ode)
        self.wait()
        self.play(
            self.grow_lt_arrow(lt_arrow),
            TransformMatchingStrings(ode.copy(), lt_ode, key_map={"Differential": "Transformed"}),
            run_time=1.5
        )
        self.wait()
        self.play(
            self.grow_lt_arrow(solve_arrow),
            FadeTransform(lt_ode.copy(), lt_ans),
            run_time=1.5
        )
        self.wait()
        self.play(
            self.grow_lt_arrow(inv_lt_arrow),
            FadeTransform(lt_ans["Solution"][0].copy(), ans),
            run_time=1.5
        )
        self.wait()

        # Add domain backgrounds
        time_domain = FullScreenRectangle()
        time_domain.stretch(0.55, 1, about_edge=UP)
        time_domain.set_stroke(BLUE, 3)
        time_domain.set_fill(opacity=0)
        s_domain = FullScreenRectangle()
        s_domain.stretch(0.45, 1, about_edge=DOWN)
        s_domain.set_stroke(YELLOW, 3)
        s_domain.set_fill(opacity=0)

        time_label = Text("Time domain")
        s_label = Text("s domain")
        s_label.set_fill(YELLOW)

        for label, domain in [(time_label, time_domain), (s_label, s_domain)]:
            label.next_to(domain.get_corner(UL), DR)

        self.play(LaggedStart(
            FadeIn(time_domain),
            FadeIn(time_label),
            FadeIn(s_domain),
            FadeIn(s_label),
        ))
        self.wait()

    def get_lt_arrow(self, m1, m2, thickness=4, label_font_size=36, buff=0.15, label_tex=R"\mathcal{L}"):
        arrow = Arrow(m1, m2, buff=buff, thickness=thickness)
        arrow.set_fill(border_width=2)
        label = Tex(label_tex, font_size=label_font_size)
        label.move_to(arrow.get_center())
        shift_dir = rotate_vector(normalize(arrow.get_vector()), 90 * DEG)
        label.shift(1.25 * label.get_height() * shift_dir)
        return VGroup(arrow, label)

    def grow_lt_arrow(self, lt_arrow):
        return AnimationGroup(
            GrowArrow(lt_arrow[0]),
            FadeIn(lt_arrow[1], shift=0.25 * lt_arrow[0].get_vector())
        )
