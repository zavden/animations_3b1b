# ==============================================================================
# Scene:      DelicacyInIntermixingSeries
# Source:     videos/_2018/wallis.py (lines 4393-4541)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl DelicacyInIntermixingSeries.py DelicacyInIntermixingSeries -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class DelicacyInIntermixingSeries(Scene):
    def construct(self):
        n_terms = 6

        top_product, bottom_product = products = VGroup(*[
            OldTex(*it.chain(*[
                ["{%d" % (2 * x), "\\over", "%d}" % (2 * x + u), "\\cdot"]
                for x in range(1, n_terms + 1)
            ]))
            for u in (-1, 1)
        ])
        top_product.set_color(GREEN)
        bottom_product.set_color(BLUE)
        top_product.to_edge(UP)
        bottom_product.next_to(top_product, DOWN, LARGE_BUFF)

        infinity = OldTex("\\infty")
        top_product.limit = infinity
        zero = OldTex("0")
        bottom_product.limit = zero

        for product in products:
            cdots = OldTex("\\cdots")
            cdots.move_to(product[-1], LEFT)
            cdots.match_color(product)
            product.submobjects[-1] = cdots
            product.parts = VGroup(*[
                product[i:i + 4]
                for i in range(0, len(product), 4)
            ])
            arrow = Vector(0.75 * RIGHT)
            arrow.set_color(WHITE)
            arrow.next_to(product, RIGHT)
            product.arrow = arrow
            product.limit.next_to(arrow, RIGHT)
            product.limit.match_color(product)

        group = VGroup(products, infinity)
        h_line = Line(LEFT, RIGHT)
        h_line.stretch_to_fit_width(group.get_width() + LARGE_BUFF)
        h_line.next_to(group, DOWN, aligned_edge=RIGHT)
        times = OldTex("\\times")
        times.next_to(h_line, UP, aligned_edge=LEFT)
        q_marks = OldTex("?????")
        q_marks.set_color_by_gradient(BLUE, YELLOW)
        q_marks.scale(2)
        q_marks.next_to(h_line, DOWN)

        # Show initial products
        self.play(
            LaggedStartMap(FadeIn, top_product),
            LaggedStartMap(FadeIn, bottom_product),
        )
        self.wait()
        for product in products:
            self.play(
                GrowArrow(product.arrow),
                FadeIn(product.limit, direction=LEFT)
            )
            self.wait()
        self.play(
            Write(times),
            ShowCreation(h_line)
        )
        self.play(Write(q_marks, run_time=3))
        self.wait(2)

        # Show alternate interweaving
        top_parts_iter = iter(top_product.parts)
        bottom_parts_iter = iter(bottom_product.parts)
        movers1 = VGroup()
        while True:
            try:
                new_terms = [
                    next(bottom_parts_iter),
                    next(top_parts_iter),
                    next(top_parts_iter),
                ]
                movers1.add(*new_terms)
            except StopIteration:
                break
        new_product = VGroup()
        movers1.save_state()
        for mover in movers1:
            mover.generate_target()
            new_product.add(mover.target)
        new_product.arrange(RIGHT, buff=SMALL_BUFF)
        new_product.next_to(h_line, DOWN, LARGE_BUFF, aligned_edge=LEFT)

        new_arrow = top_product.arrow.copy()
        new_arrow.next_to(new_product, RIGHT)

        ghost_top = top_product.copy().fade()
        ghost_bottom = bottom_product.copy().fade()
        self.add(ghost_top, top_product)
        self.add(ghost_bottom, bottom_product)

        new_limit = OldTex("\\frac{\\pi}{2}", "\\sqrt{2}")
        new_limit.next_to(new_arrow, RIGHT)

        randy = Randolph(height=1.5)
        randy.flip()
        randy.to_corner(DR)

        movers2 = VGroup(*it.chain(*list(zip(
            top_product.parts, bottom_product.parts
        ))))
        final_product = VGroup()
        for mover in movers2:
            mover.final_position = mover.copy()
            if mover is movers2[-2]:
                # Excessive ellipses
                final_dot = mover.final_position[-1][0]
                mover.final_position.submobjects[-1] = final_dot
            final_product.add(mover.final_position)
        final_product.arrange(RIGHT, buff=SMALL_BUFF)
        final_product.move_to(new_product, RIGHT)

        self.play(
            FadeOut(q_marks),
            LaggedStartMap(
                MoveToTarget, movers1,
                run_time=5,
                lag_ratio=0.2,
            )
        )
        self.play(
            GrowArrow(new_arrow),
            FadeIn(new_limit, LEFT),
            bottom_product.parts[3:].fade, 1,
        )
        self.play(FadeIn(randy))
        self.play(randy.change, "confused", new_limit)
        self.wait()
        self.play(Blink(randy))
        self.wait()
        self.play(LaggedStartMap(
            Transform, movers2,
            lambda m: (m, m.final_position),
            run_time=3,
            path_arc=TAU / 4,
        ))
        self.play(
            FadeOut(new_limit[1]),
            randy.change, "pondering", new_limit
        )
        self.wait(2)
        self.play(Blink(randy))
        self.wait(2)
