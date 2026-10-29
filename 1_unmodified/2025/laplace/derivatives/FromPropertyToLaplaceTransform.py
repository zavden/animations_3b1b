# ==============================================================================
# Scene:      FromPropertyToLaplaceTransform
# Source:     videos/_2025/laplace/derivatives.py (lines 1827-1915)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl FromPropertyToLaplaceTransform.py FromPropertyToLaplaceTransform -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class FromPropertyToLaplaceTransform(InteractiveScene):
    def construct(self):
        # Add desired property
        t2c = {"{t}": BLUE, "{s}": YELLOW}
        prop = VGroup(
            Tex(R"d / d{t}", font_size=72, t2c=t2c),
            Vector(DOWN, thickness=5),
            Tex(R"\times {s}", font_size=72, t2c=t2c),
        )
        prop.arrange(DOWN)
        prop.to_edge(LEFT, buff=LARGE_BUFF)
        prop_rect = SurroundingRectangle(prop, buff=MED_LARGE_BUFF)
        prop_rect.set_stroke(GREEN, 2)
        goal_word = Text("Goal", font_size=72)
        goal_word.set_fill(GREEN)
        goal_word.next_to(prop_rect, UP)

        self.add(prop)
        self.play(
            ShowCreation(prop_rect),
            Write(goal_word)
        )

        # Show threads
        n_threads = 10
        threads = VGroup(
            self.get_thread(prop_rect.get_right() + shift)
            for shift in np.linspace(0.5 * UP, 0.5 * DOWN, n_threads)
        )
        kw = dict(
            lag_ratio=1.0 / n_threads,
            run_time=4
        )
        self.play(
            ShowCreation(threads, **kw),
            LaggedStartMap(VShowPassingFlash, threads.copy().set_stroke(WHITE, 2), time_width=2.0, **kw)
        )
        self.wait()

        # Transforms
        lt, inv_lt = transforms = VGroup(
            Tex(R"F({s}) = \int_0^\infty f({t}) e^{\minus {s}{t}} d{t}", t2c=t2c),
            Tex(R"f({t}) = \frac{1}{2\pi i} \int_{a - i\infty}^{a + i\infty} F({s}) e^{{s}{t}} d{s}", t2c=t2c),
        )

        transforms.arrange(DOWN, buff=2.5)
        transforms.to_edge(RIGHT)

        transform_rects = VGroup(SurroundingRectangle(term) for term in transforms)

        v_line = Line(*transform_rects, buff=0)
        h_line = Line(prop_rect.get_right(), v_line.get_center())
        VGroup(v_line, h_line, transform_rects).set_stroke(GREY, 1)

        self.play(
            Transform(threads, h_line.replicate(len(threads)), remover=True, lag_ratio=0.1, run_time=3)
        )
        self.add(h_line)
        self.play(GrowFromCenter(v_line, run_time=0.5))
        self.play(
            FadeIn(transform_rects),
            FadeIn(transforms),
        )
        self.wait()

        # Unify
        transforms.target = transforms.generate_target()
        transforms.target.space_out_submobjects(0.7)
        new_rect = SurroundingRectangle(transforms.target)
        new_rect.set_stroke(GREY, 2)

        self.play(
            MoveToTarget(transforms),
            ReplacementTransform(transform_rects[0], new_rect),
            ReplacementTransform(transform_rects[1], new_rect),
            v_line.animate.scale(0),
            h_line.animate.put_start_and_end_on(prop_rect.get_right(), new_rect.get_left()),
        )
        self.wait()

    def get_thread(self, start_point, step_size=0.15, angle_range=(-45 * DEG, 45 * DEG), n_steps=20):
        points = [start_point]
        for n in range(n_steps):
            step = rotate_vector(RIGHT, random.uniform(*angle_range))
            points.append(points[-1] + step)

        path = VMobject().set_points_smoothly(points, approx=False)
        path.set_stroke(GREY, 1)
        return path
