# ==============================================================================
# Scene:      BillionsOfInputs
# Source:     videos/_2026/cross_entropy/part2_supplements.py (lines 154-208)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl BillionsOfInputs.py BillionsOfInputs -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class BillionsOfInputs(InteractiveScene):
    def construct(self):
        # Simple function
        func = Tex(R"L(x, y)", font_size=90, t2c={"L": RED})
        self.play(Write(func))
        self.wait()

        # Many labels
        lp = func["L("][0]
        rp = func[")"][0]
        xy = func["x, y"][0]

        lp.target = lp.generate_target()
        rp.target = rp.generate_target()
        lp.target.shift(2 * LEFT)
        rp.target.shift(2 * RIGHT)
        min_x = lp.target.get_x(RIGHT)
        max_x = rp.target.get_x(LEFT)

        w_i_template = Tex(R"w_{0}", font_size=48)
        subscr = w_i_template.make_number_changeable("0", edge_to_fix=LEFT)
        all_ws = VGroup()
        n_terms = 200
        for n in range(n_terms):
            subscr.set_value(n)
            all_ws.add(w_i_template.copy())
        all_ws[-1].remove(all_ws[-1][-1])
        all_ws.arrange(RIGHT)
        for mob in all_ws:
            mob.add(Text(",").next_to(mob, RIGHT, buff=0.05).match_y(mob.get_corner(DL)))

        def update_opacities(xs):
            for mob in xs:
                x = mob.get_x()
                alpha = min(
                    clip(inverse_interpolate(min_x, min_x + LARGE_BUFF, x), 0, 1),
                    clip(inverse_interpolate(max_x, max_x - LARGE_BUFF, x), 0, 1),
                )
                mob.set_fill(opacity=alpha)

        all_ws.add_updater(update_opacities)
        all_ws.next_to(lp.target, RIGHT, SMALL_BUFF)

        self.play(
            MoveToTarget(lp),
            MoveToTarget(rp),
            FadeOut(xy),
            VFadeIn(all_ws, suspend_mobject_updating=True),
        )
        self.play(
            all_ws.animate.next_to(rp, LEFT),
            run_time=20,
            rate_func=lambda t: t**3,
        )
        self.wait()
