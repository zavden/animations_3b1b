# ==============================================================================
# Scene:      OneOverX
# Source:     videos/_2017/eoc/chapter3.py (lines 1598-1995)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl OneOverX.py OneOverX -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class OneOverX(PiCreatureScene, GraphScene):
    CONFIG = {
        "unit_length" : 3.0,    
        "graph_origin" : (FRAME_X_RADIUS - LARGE_BUFF)*LEFT + 2*DOWN,
        "rectangle_color_kwargs" : {
            "fill_color" : BLUE,
            "fill_opacity" : 0.5,
            "stroke_width" : 1,
            "stroke_color" : WHITE,
        },

        "x_axis_label" : "",
        "y_axis_label" : "",
        "x_min" : 0,
        "y_min" : 0,
        "x_tick_frequency" : 0.5,
        "y_tick_frequency" : 0.5,
        "x_labeled_nums" : list(range(0, 4)),
        "y_labeled_nums" : [1],
        "y_axis_height" : 10,
        "morty_scale_val" : 0.8,
        "area_label_scale_factor" : 0.75,
        "dx" : 0.1,
        "start_x_value" : 1.3,
        "dx_color" : GREEN,
        "df_color" : RED,
    }
    def setup(self):
        for c in self.__class__.__bases__:
            c.setup(self)
        self.x_max = self.x_axis_width/self.unit_length
        self.y_max = self.y_axis_height/self.unit_length

    def construct(self):
        self.force_skipping()

        self.introduce_function()
        self.introduce_puddle()
        self.introduce_graph()
        self.perform_nudge()

    def introduce_function(self):
        func = OldTex("f(x) = ", "\\frac{1}{x}")
        func.to_edge(UP)
        recip_copy = func[1].copy()
        x_to_neg_one = OldTex("x^{-1}")
        x_to_neg_one.submobjects.reverse()
        neg_one = VGroup(*x_to_neg_one[:2])
        neg_two = OldTex("-2")

        self.play(
            Write(func),
            self.pi_creature.change_mode, "pondering"
        )
        self.wait()
        self.play(
            recip_copy.next_to, self.pi_creature, UP+LEFT,
            self.pi_creature.change_mode, "raise_right_hand"
        )
        x_to_neg_one.move_to(recip_copy)
        neg_two.replace(neg_one)
        self.play(ReplacementTransform(recip_copy, x_to_neg_one))
        self.wait()
        self.play(
            neg_one.scale, 1.5,
            neg_one.next_to, x_to_neg_one, LEFT, SMALL_BUFF, DOWN,
            rate_func = running_start,
            path_arc = np.pi
        )
        self.play(FadeIn(neg_two))
        self.wait()
        self.say(
            "More geometry!",
            target_mode = "hooray",
            added_anims = [
                FadeOut(x_to_neg_one),
                FadeOut(neg_two),
            ],
            run_time = 2
        )
        self.wait()
        self.play(RemovePiCreatureBubble(self.pi_creature))

    def introduce_puddle(self):
        rect_group = self.get_rectangle_group(self.start_x_value)

        self.play(
            DrawBorderThenFill(rect_group.rectangle),
            Write(rect_group.area_label),
            self.pi_creature.change_mode, "thinking"
        )
        self.play(
            GrowFromCenter(rect_group.x_brace),
            Write(rect_group.x_label),
        )
        self.wait()
        self.play(
            GrowFromCenter(rect_group.recip_brace),
            Write(rect_group.recip_label),
        )
        self.setup_axes(animate = True)
        self.wait()

        for d in 2, 3:
            self.change_rectangle_group(
                rect_group, d,
                target_group_kwargs = {
                    "x_label" : str(d),
                    "one_over_x_label" : "\\frac{1}{%d}"%d,
                },
                run_time = 2
            )
            self.wait()
        self.change_rectangle_group(rect_group, 3)
        self.wait()

        self.rect_group = rect_group

    def introduce_graph(self):
        rect_group = self.rect_group
        graph = self.get_graph(lambda x : 1./x)
        graph.set_points(list(reversed(graph.get_points())))

        self.change_rectangle_group(
            rect_group, 0.01,
            added_anims = [
                ShowCreation(graph)
            ],
            run_time = 5,
        )
        self.change_mode("happy")
        self.change_rectangle_group(rect_group, self.start_x_value)
        self.wait()

        self.graph = graph

    def perform_nudge(self):
        rect_group = self.rect_group
        graph = self.graph

        rect_copy = rect_group.rectangle.copy()
        rect_copy.set_fill(opacity = 0)
        new_rect = self.get_rectangle(
            self.start_x_value + self.dx
        )

        recip_brace = rect_group.recip_brace
        recip_brace.generate_target()
        recip_brace.target.next_to(
            new_rect, RIGHT, 
            buff = SMALL_BUFF,
            aligned_edge = DOWN,
        )
        recip_label = rect_group.recip_label
        recip_label.generate_target()
        recip_label.target.next_to(recip_brace.target, RIGHT)

        h_lines = VGroup(*[
            DashedLine(
                ORIGIN, (rect_copy.get_width()+LARGE_BUFF)*RIGHT, 
                color = self.df_color,
                stroke_width = 2
            ).move_to(rect.get_corner(UP+LEFT), LEFT)
            for rect in (rect_group.rectangle, new_rect)
        ])

        v_lines = VGroup(*[
            DashedLine(
                ORIGIN, (rect_copy.get_height()+MED_LARGE_BUFF)*UP,
                color = self.dx_color,
                stroke_width = 2
            ).move_to(rect.get_corner(DOWN+RIGHT), DOWN)
            for rect in (rect_group.rectangle, new_rect)
        ])

        dx_brace = Brace(v_lines, UP, buff = 0)
        dx_label = dx_brace.get_text("$dx$")
        dx_brace.add(dx_label)

        df_brace = Brace(h_lines, RIGHT, buff = 0)
        df_label = df_brace.get_text("$d\\left(\\frac{1}{x}\\right)$")
        df_brace.add(df_label)

        negative = OldTexText("Negative")
        negative.set_color(RED)
        negative.next_to(df_label, UP+RIGHT)
        negative.shift(RIGHT)
        negative_arrow = Arrow(
            negative.get_left(),
            df_label.get_corner(UP+RIGHT),
            color = RED
        )

        area_changes = VGroup()
        point_pairs = [
            (new_rect.get_corner(UP+RIGHT), rect_copy.get_corner(DOWN+RIGHT)),
            (new_rect.get_corner(UP+LEFT), rect_copy.get_corner(UP+RIGHT))
        ]
        for color, point_pair in zip([self.dx_color, self.df_color], point_pairs):
            area_change_rect = Rectangle(
                fill_opacity = 1,
                fill_color = color,
                stroke_width = 0
            )
            area_change_rect.replace(
                VGroup(*list(map(VectorizedPoint, point_pair))),
                stretch = True
            )
            area_changes.add(area_change_rect)
        area_gained, area_lost = area_changes

        area_gained_label = OldTexText("Area gained")
        area_gained_label.scale(0.75)
        area_gained_label.next_to(
            rect_copy.get_corner(DOWN+RIGHT), 
            UP+LEFT, buff = SMALL_BUFF
        )
        area_gained_arrow = Arrow(
            area_gained_label.get_top(),
            area_gained.get_center(),
            buff = 0,
            color = WHITE
        )
        
        area_lost_label = OldTexText("Area lost")
        area_lost_label.scale(0.75)
        area_lost_label.next_to(rect_copy.get_left(), RIGHT)
        area_lost_arrow = Arrow(
            area_lost_label.get_top(),
            area_lost.get_center(),
            buff = 0,
            color = WHITE
        )

        question = OldTex(
            "\\frac{d(1/x)}{dx} = ???"
        )
        question.next_to(
            self.pi_creature.get_corner(UP+LEFT), 
            UP, buff = MED_SMALL_BUFF,
        )

        self.play(
            FadeOut(rect_group.area_label),
            ReplacementTransform(rect_copy, new_rect),
            MoveToTarget(recip_brace),
            MoveToTarget(recip_label),
            self.pi_creature.change_mode, "pondering"
        )
        self.play(
            GrowFromCenter(dx_brace),
            *list(map(ShowCreation, v_lines))
        )
        self.wait()
        self.play(
            GrowFromCenter(df_brace),
            *list(map(ShowCreation, h_lines))
        )
        self.change_mode("confused")
        self.wait()

        self.play(
            FadeIn(area_gained),
            Write(area_gained_label, run_time = 2),
            ShowCreation(area_gained_arrow)
        )
        self.wait()
        self.play(
            FadeIn(area_lost),
            Write(area_lost_label, run_time = 2),
            ShowCreation(area_lost_arrow)
        )
        self.wait()
        self.revert_to_original_skipping_status()###
        self.play(
            Write(negative),
            ShowCreation(negative_arrow)
        )
        self.wait()
        self.play(
            Write(question),
            self.pi_creature.change_mode, "raise_right_hand"
        )
        self.wait(2)


    ########

    def create_pi_creature(self):
        morty = PiCreatureScene.create_pi_creature(self)
        morty.scale(
            self.morty_scale_val, 
            about_point = morty.get_corner(DOWN+RIGHT)
        )
        return morty

    def draw_graph(self):
        self.setup_axes()
        graph = self.get_graph(lambda x : 1./x)

        rect_group = self.get_rectangle_group(0.5)

        self.add(rect_group)
        self.wait()
        self.change_rectangle_group(
            rect_group, 2,
            target_group_kwargs = {
                "x_label" : "2",
                "one_over_x_label" : "\\frac{1}{2}",
            },
            added_anims = [ShowCreation(graph)]
        )
        self.wait()

    def get_rectangle_group(
        self, x, 
        x_label = "x", 
        one_over_x_label = "\\frac{1}{x}"
        ):
        result = VGroup()
        result.x_val = x
        result.rectangle = self.get_rectangle(x)

        result.x_brace, result.recip_brace = braces = [
            Brace(result.rectangle, vect)
            for vect in (UP, RIGHT)
        ]
        result.labels = VGroup()
        for brace, label in zip(braces, [x_label, one_over_x_label]):
            brace.get_text("$%s$"%label)
            result.labels.add(brace.get_text("$%s$"%label))
        result.x_label, result.recip_label = result.labels

        area_label = OldTexText("Area = 1")
        area_label.scale(self.area_label_scale_factor)
        max_width = max(result.rectangle.get_width()-2*SMALL_BUFF, 0)
        if area_label.get_width() > max_width:
            area_label.set_width(max_width)
        area_label.move_to(result.rectangle)
        result.area_label = area_label

        result.add(
            result.rectangle,
            result.x_brace,
            result.recip_brace,
            result.labels,
            result.area_label,
        )
        return result

    def get_rectangle(self, x):
        try:
            y = 1./x
        except ZeroDivisionError:
            y = 100

        rectangle = Rectangle(
            width = x*self.unit_length,
            height = y*self.unit_length,
            **self.rectangle_color_kwargs
        )
        rectangle.move_to(self.graph_origin, DOWN+LEFT)
        return rectangle

    def change_rectangle_group(
        self, 
        rect_group, target_x,
        target_group_kwargs = None,
        added_anims = [],
        **anim_kwargs
        ):
        target_group_kwargs = target_group_kwargs or {}
        if "run_time" not in anim_kwargs:
            anim_kwargs["run_time"] = 3

        target_group = self.get_rectangle_group(target_x, **target_group_kwargs)
        target_labels = target_group.labels
        labels_transform = Transform(
            rect_group.labels,
            target_group.labels
        )

        start_x = float(rect_group.x_val)
        def update_rect_group(group, alpha):
            x = interpolate(start_x, target_x, alpha)
            new_group = self.get_rectangle_group(x, **target_group_kwargs)
            Transform(group, new_group).update(1)
            labels_transform.update(alpha)
            for l1, l2 in zip(rect_group.labels, new_group.labels):
                l1.move_to(l2)
            return rect_group

        self.play(
            UpdateFromAlphaFunc(rect_group, update_rect_group),
            *added_anims,
            **anim_kwargs
        )
        rect_group.x_val = target_x
