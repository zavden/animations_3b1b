# ==============================================================================
# Scene:      ShowDotProductMeaning
# Source:     videos/_2019/clacks/solution2/simple_scenes.py (lines 104-261)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ShowDotProductMeaning.py ShowDotProductMeaning -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ShowDotProductMeaning(Scene):
    def construct(self):
        v_vect = Vector(2 * RIGHT, color=YELLOW)
        w_vect = Vector(3 * RIGHT, color=PINK)
        dot = Dot(color=RED)
        dot.shift(DOWN)

        v_vect.angle_tracker = ValueTracker()
        w_vect.angle_tracker = ValueTracker()

        def update_vect(vect):
            target = vect.angle_tracker.get_value()
            vect.rotate(target - vect.get_angle())
            vect.shift(dot.get_center() - vect.get_start())

        v_vect.add_updater(update_vect)
        w_vect.add_updater(update_vect)

        v_label = OldTex("\\vec{\\textbf{v}}")
        v_label.vect = v_vect
        w_label = OldTex("\\vec{\\textbf{w}}")
        w_label.vect = w_vect
        for label in v_label, w_label:
            label.match_color(label.vect)
            label.set_stroke(BLACK, 5, background=True)

        def update_label(label):
            target = np.array(label.vect.get_end())
            target += 0.25 * normalize(label.vect.get_vector())
            label.move_to(target)

        v_label.add_updater(update_label)
        w_label.add_updater(update_label)

        title = OldTex(
            "\\vec{\\textbf{w}}",
            "\\cdot",
            "\\vec{\\textbf{v}}",
            "=",
            "||", "\\vec{\\textbf{w}}", "||",
            "\\cdot",
            "||", "\\vec{\\textbf{v}}", "||",
            "\\cdot",
            "\\cos(\\theta)"
        )
        title.set_color_by_tex_to_color_map({
            "textbf{v}": v_vect.get_color(),
            "textbf{w}": w_vect.get_color(),
        })
        title.to_edge(UP)

        def get_w_line():
            center = dot.get_center()
            direction = w_vect.get_vector()
            return Line(
                center - 3 * direction,
                center + 3 * direction,
                stroke_color=GREY_B,
                stroke_width=1,
            )
        w_line = always_redraw(get_w_line)

        def get_proj_v():
            center = dot.get_center()
            v = v_vect.get_vector()
            w = w_vect.get_vector()
            w_unit = normalize(w)
            result = Vector(np.dot(v, w_unit) * w_unit)
            result.set_fill(v_vect.get_color(), 0.5)
            result.shift(center - result.get_start())
            return result
        proj_v = always_redraw(get_proj_v)

        def get_proj_line():
            return DashedLine(
                v_vect.get_end(),
                proj_v.get_end(),
                stroke_width=1,
                dash_length=0.025,
            )
        proj_line = always_redraw(get_proj_line)

        template_line = Line(LEFT, RIGHT)

        def get_vect_brace(vect):
            brace = Brace(template_line, UP, buff=SMALL_BUFF)
            brace.set_width(vect.get_length(), stretch=True)
            angle = vect.get_angle() % TAU
            if angle < PI:
                angle += PI
            brace.rotate(angle, about_point=ORIGIN)
            brace.shift(vect.get_center())
            return brace
        w_brace = always_redraw(
            lambda: get_vect_brace(w_vect)
        )
        proj_v_brace = always_redraw(
            lambda: get_vect_brace(proj_v)
        )

        def get_arc():
            center = dot.get_center()
            a1 = w_vect.get_angle()
            a2 = v_vect.get_angle()
            arc = Arc(
                start_angle=a1,
                angle=a2 - a1,
                radius=0.5,
                arc_center=center,
            )
            theta = OldTex("\\theta")
            p = arc.point_from_proportion(0.5)
            theta.move_to(
                center + 1.5 * (p - center)
            )
            return VGroup(arc, theta)
        arc = always_redraw(get_arc)

        self.add(
            title[:3],
            w_vect, v_vect, dot,
            w_label, v_label,
        )
        self.play(
            v_vect.angle_tracker.set_value, 170 * DEGREES,
            w_vect.angle_tracker.set_value, 45 * DEGREES,
            run_time=2,
        )
        self.wait()
        w_brace.update()
        self.play(
            GrowFromCenter(w_brace),
            Write(title[3:7])
        )

        self.add(w_line, w_vect, w_label, dot)
        self.play(ShowCreation(w_line))
        proj_v.update()
        self.play(
            ShowCreation(proj_line),
            TransformFromCopy(v_vect, proj_v),
        )
        self.add(proj_v, proj_line, dot)
        proj_v_brace.update()
        self.play(
            GrowFromCenter(proj_v_brace),
            FadeInFromDown(title[7:])
        )
        arc.update()
        self.play(Write(arc))
        self.wait()

        for angle in [135, 225, 270, 90, 150]:
            self.play(
                v_vect.angle_tracker.set_value, angle * DEGREES,
                run_time=2
            )
            self.wait()
