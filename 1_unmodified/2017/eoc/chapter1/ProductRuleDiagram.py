# ==============================================================================
# Scene:      ProductRuleDiagram
# Source:     videos/_2017/eoc/chapter1.py (lines 466-592)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ProductRuleDiagram.py ProductRuleDiagram -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ProductRuleDiagram(Scene):
    def construct(self):
        df = 0.4
        dg = 0.2
        rect_kwargs = {
            "stroke_width" : 0,
            "fill_color" : BLUE,
            "fill_opacity" : 0.6,
        }

        rect = Rectangle(width = 4, height = 3, **rect_kwargs)
        rect.shift(DOWN)
        df_rect = Rectangle(
            height = rect.get_height(),
            width = df,
            **rect_kwargs
        )
        dg_rect = Rectangle(
            height = dg,
            width = rect.get_width(),
            **rect_kwargs
        )
        corner_rect = Rectangle(
            height = dg, 
            width = df,
            **rect_kwargs
        )
        d_rects = VGroup(df_rect, dg_rect, corner_rect)
        for d_rect, direction in zip(d_rects, [RIGHT, DOWN, RIGHT+DOWN]):
            d_rect.next_to(rect, direction, buff = 0)
            d_rect.set_fill(YELLOW, 0.75)

        corner_pairs = [
            (DOWN+RIGHT, UP+RIGHT),
            (DOWN+RIGHT, DOWN+LEFT),
            (DOWN+RIGHT, DOWN+RIGHT),
        ]
        for d_rect, corner_pair in zip(d_rects, corner_pairs):
            line = Line(*[
                rect.get_corner(corner)
                for corner in corner_pair
            ])
            d_rect.line = d_rect.copy().replace(line, stretch = True)
            d_rect.line.set_color(d_rect.get_color())

        f_brace = Brace(rect, UP)
        g_brace = Brace(rect, LEFT)
        df_brace = Brace(df_rect, UP)
        dg_brace = Brace(dg_rect, LEFT)

        f_label = f_brace.get_text("$f$")
        g_label = g_brace.get_text("$g$")
        df_label = df_brace.get_text("$df$")
        dg_label = dg_brace.get_text("$dg$")

        VGroup(f_label, df_label).set_color(GREEN)
        VGroup(g_label, dg_label).set_color(RED)

        f_label.generate_target()
        g_label.generate_target()
        fg_group = VGroup(f_label.target, g_label.target)
        fg_group.generate_target()
        fg_group.target.arrange(RIGHT, buff = SMALL_BUFF)
        fg_group.target.move_to(rect.get_center())

        for mob in df_brace, df_label, dg_brace, dg_label:
            mob.save_state()
            mob.scale(0.01, about_point = rect.get_corner(
                mob.get_center() - rect.get_center()
            ))

        self.add(rect)
        self.play(
            GrowFromCenter(f_brace),
            GrowFromCenter(g_brace),
            Write(f_label),
            Write(g_label),
        )
        self.play(MoveToTarget(fg_group))
        self.play(*[
            mob.restore
            for mob in (df_brace, df_label, dg_brace, dg_label)
        ] + [
            ReplacementTransform(d_rect.line, d_rect)
            for d_rect in d_rects
        ])
        self.wait()
        self.play(
            d_rects.space_out_submobjects, 1.2,
            MaintainPositionRelativeTo(
                VGroup(df_brace, df_label),
                df_rect
            ),
            MaintainPositionRelativeTo(
                VGroup(dg_brace, dg_label),
                dg_rect
            ),
        )
        self.wait()

        deriv = OldTex(
            "d(", "fg", ")", "=", 
            "f", "\\cdot", "dg", "+", "g", "\\cdot", "df"
        )
        deriv.to_edge(UP)
        alpha_iter = iter(np.linspace(0, 0.5, 5))
        self.play(*[
            ApplyMethod(
                mob.copy().move_to,
                deriv.get_part_by_tex(tex, substring = False),
                rate_func = squish_rate_func(smooth, alpha, alpha+0.5)
            )
            for mob, tex in [
                (fg_group, "fg"),
                (f_label, "f"),
                (dg_label, "dg"),
                (g_label, "g"),
                (df_label, "df"),
            ]
            for alpha in [next(alpha_iter)]
        ]+[
            Write(VGroup(*it.chain(*[
                deriv.get_parts_by_tex(tex, substring = False)
                for tex in ("d(", ")", "=", "\\cdot", "+")
            ])))
        ], run_time = 3)
        self.wait()
