# ==============================================================================
# Scene:      StartingCalc101
# Source:     videos/_2018/alt_calc.py (lines 474-786)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl StartingCalc101.py StartingCalc101 -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - typo in the original (add_udpater); it fails in Cairo too
#   - imports a 2017 scene (NudgeSideLengthOfCube) that is not part of this file, only to borrow a cube picture; replaced by an isometric cube drawn with Polygons
#   - a Cairo Scene ran setup() in __init__; in GL it runs in run(), so a scene created by hand needs it (get_graph reads default_graph_colors_cycle)
#   - a VMobject cannot hold an ImageMobject in GL (set_opacity/fade walk the family and fail with "no field fill_rgba"); the box and its image are grouped in a Group instead
#   - a GL scene keeps its camera frame in .mobjects once setup() has run; it must not end up in the group
#   - cv2 is not installed (and was never imported in this file); the 50x50 box blur is done with PIL (BoxBlur(25)), which is already available
#   - GL ImageMobject only takes a file name; CairoImageMobject (cairo_compat) accepts a pixel array like the Cairo one
# ==============================================================================

 # -*- coding: utf-8 -*-
from manim_imports_ext import *

class StartingCalc101(PiCreatureScene):
    CONFIG = {
        "camera_config": {"background_opacity": 1},
        "image_frame_width": 3.5,
        "image_frame_height": 2.5,
    }

    def construct(self):
        self.show_you()
        self.show_images()
        self.show_mystery_topic()

    def show_you(self):
        randy = self.pi_creature
        title = self.title = Title("Calculus 101")
        you = OldTexText("You")
        arrow = Vector(DL, color=WHITE)
        arrow.next_to(randy, UR)
        you.next_to(arrow.get_start(), UP)

        self.play(
            Write(you),
            GrowArrow(arrow),
            randy.change, "erm", title
        )
        self.wait()
        self.play(Write(title, run_time=1))
        self.play(FadeOut(VGroup(arrow, you)))

    def show_images(self):
        randy = self.pi_creature
        images = self.get_all_images()
        modes = [
            "pondering",  # hard_work_image
            "pondering",  # neat_example_image
            "hesitant",  # not_so_neat_example_image
            "hesitant",  # physics_image
            "horrified",  # piles_of_formulas_image
            "horrified",  # getting_stuck_image
            "thinking",  # aha_image
            "thinking",  # graphical_intuition_image
        ]

        for i, image, mode in zip(it.count(), images, modes):
            anims = []
            if hasattr(image, "fade_in_anim"):
                anims.append(image.fade_in_anim)
                anims.append(FadeIn(image.frame))
            else:
                anims.append(FadeIn(image))

            if i >= 3:
                image_to_fade_out = images[i - 3]
                if hasattr(image_to_fade_out, "fade_out_anim"):
                    anims.append(image_to_fade_out.fade_out_anim)
                else:
                    anims.append(FadeOut(image_to_fade_out))

            if hasattr(image, "continual_animations"):
                self.add(*image.continual_animations)

            anims.append(ApplyMethod(randy.change, mode))
            self.play(*anims)
            self.wait()
            if i >= 3:
                if hasattr(image_to_fade_out, "continual_animations"):
                    self.remove(*image_to_fade_out.continual_animations)
                self.remove(image_to_fade_out.frame)
        self.wait(3)

        self.remaining_images = images[-3:]

    def show_mystery_topic(self):
        images = self.remaining_images
        randy = self.pi_creature

        mystery_box = Rectangle(
            width=self.image_frame_width,
            height=self.image_frame_height,
            stroke_color=YELLOW,
            fill_color=GREY_D,
            fill_opacity=0.5,
        )
        mystery_box.scale(1.5)
        mystery_box.next_to(self.title, DOWN, MED_LARGE_BUFF)

        rects = images[-1].rects.copy()
        rects.center()
        rects.set_height(FRAME_HEIGHT - 1)
        # image = rects.get_image()
        # CHANGE: cv2 is not installed (and was never imported in this file); the 50x50 box blur is done with PIL (BoxBlur(25)), which is already available
        from PIL import Image, ImageFilter
        blurry_iamge = Image.open(get_full_raster_image_path("alt_calc_hidden_image")).convert("RGB").filter(ImageFilter.BoxBlur(25))
        array = np.array(blurry_iamge)
        # CHANGE: GL ImageMobject only takes a file name; CairoImageMobject (cairo_compat) accepts a pixel array like the Cairo one
        im_mob = CairoImageMobject(array)
        im_mob.replace(mystery_box, stretch=True)
        # CHANGE: a VMobject cannot hold an ImageMobject in GL (set_opacity/fade walk the family and fail with "no field fill_rgba"); the box and its image are grouped in a Group instead
        mystery_box = Group(mystery_box, im_mob)

        q_marks = OldTex("???").scale(3)
        q_marks.space_out_submobjects(1.5)
        q_marks.set_stroke(BLACK, 1)
        q_marks.move_to(mystery_box)
        mystery_box.add(q_marks)

        for image in images:
            if hasattr(image, "continual_animations"):
                self.remove(*image.continual_animations)
            self.play(
                image.shift, DOWN,
                image.fade, 1,
                randy.change, "erm",
                run_time=1.5
            )
            self.remove(image)
        self.wait()
        self.play(
            FadeInFromDown(mystery_box),
            randy.change, "confused"
        )
        self.wait(5)

    # Helpers

    def get_all_images(self):
        # Images matched to narration's introductory list
        images = VGroup(
            self.get_hard_work_image(),
            self.get_neat_example_image(),
            self.get_not_so_neat_example_image(),
            self.get_physics_image(),
            self.get_piles_of_formulas_image(),
            self.get_getting_stuck_image(),
            self.get_aha_image(),
            self.get_graphical_intuition_image(),
        )
        colors = color_gradient([BLUE, YELLOW], len(images))
        for i, image, color in zip(it.count(), images, colors):
            self.adjust_size(image)
            frame = Rectangle(
                width=self.image_frame_width,
                height=self.image_frame_height,
                color=color,
                stroke_width=2,
            )
            frame.move_to(image)
            image.frame = frame
            image.add(frame)
            image.next_to(self.title, DOWN)
            alt_i = (i % 3) - 1
            vect = (self.image_frame_width + LARGE_BUFF) * RIGHT
            image.shift(alt_i * vect)
        return images

    def adjust_size(self, group):
        group.set_width(min(
            group.get_width(),
            self.image_frame_width - 2 * MED_SMALL_BUFF
        ))
        group.set_height(min(
            group.get_height(),
            self.image_frame_height - 2 * MED_SMALL_BUFF
        ))
        return group

    def get_hard_work_image(self):
        new_randy = self.pi_creature.copy()
        new_randy.change_mode("telepath")
        bubble = new_randy.get_bubble(height=3.5, width=4)
        bubble.add_content(OldTex("\\frac{d}{dx}(\\sin(\\sqrt{x}))"))
        bubble.add(bubble.content)  # Remove?

        return VGroup(new_randy, bubble)

    def get_neat_example_image(self):
        filled_circle = Circle(
            stroke_width=0,
            fill_color=BLUE_E,
            fill_opacity=1
        )
        area = OldTex("\\pi r^2")
        area.move_to(filled_circle)
        unfilled_circle = Circle(
            stroke_width=3,
            stroke_color=YELLOW,
            fill_opacity=0,
        )
        unfilled_circle.next_to(filled_circle, RIGHT)
        circles = VGroup(filled_circle, unfilled_circle)
        circumference = OldTex("2\\pi r")
        circumference.move_to(unfilled_circle)
        equation = OldTex(
            "{d (\\pi r^2) \\over dr}  = 2\\pi r",
            tex_to_color_map={
                "\\pi r^2": BLUE_D,
                "2\\pi r": YELLOW,
            }
        )
        equation.next_to(circles, UP)

        return VGroup(
            filled_circle, area,
            unfilled_circle, circumference,
            equation
        )

    def get_not_so_neat_example_image(self):
        return OldTex("\\int x \\cos(x) \\, dx")

    def get_physics_image(self):
        t_max = 6.5
        r = 0.2
        spring = ParametricCurve(
            lambda t: op.add(
                r * (np.sin(TAU * t) * RIGHT + np.cos(TAU * t) * UP),
                t * DOWN,
            ),
            t_min=0, t_max=t_max,
            color=WHITE,
            stroke_width=2,
        )
        spring.color_using_background_image("grey_gradient")

        weight = Square()
        weight.set_stroke(width=0)
        weight.set_fill(opacity=1)
        weight.color_using_background_image("grey_gradient")
        weight.set_height(0.4)

        t_tracker = ValueTracker(0)
        group = VGroup(spring, weight)
        group.continual_animations = [
            # CHANGE: typo in the original (add_udpater); it fails in Cairo too
            t_tracker.add_updater(
                lambda tracker, dt: tracker.set_value(
                    tracker.get_value() + dt
                )
            ),
            spring.add_updater(
                lambda s: s.stretch_to_fit_height(
                    1.5 + 0.5 * np.cos(3 * t_tracker.get_value()),
                    about_edge=UP
                )
            ),
            weight.add_updater(
                lambda w: w.move_to(spring.get_points()[-1])
            )
        ]

        def update_group_style(alpha):
            spring.set_stroke(width=2 * alpha)
            weight.set_fill(opacity=alpha)

        group.fade_in_anim = UpdateFromAlphaFunc(
            group,
            lambda g, a: update_group_style(a)
        )
        group.fade_out_anim = UpdateFromAlphaFunc(
            group,
            lambda g, a: update_group_style(1 - a)
        )
        return group

    def get_piles_of_formulas_image(self):
        return OldTex("(f/g)' = \\frac{gf' - fg'}{g^2}")

    def get_getting_stuck_image(self):
        creature = self.pi_creature.copy()
        creature.change_mode("angry")
        equation = OldTex("\\frac{d}{dx}(x^x)")
        equation.set_height(creature.get_height() / 2)
        equation.next_to(creature, RIGHT, aligned_edge=UP)
        creature.look_at(equation)
        return VGroup(creature, equation)

    def get_aha_image(self):
        creature = self.pi_creature.copy()
        creature.change_mode("hooray")
        # CHANGE: the original ran the 2017 EOC scene NudgeSideLengthOfCube (end_at_animation_number=7) to borrow its cube, faces and bars;
        # that scene is not in this file, so a small isometric cube drawn here stands in for it
        corners = [np.array([np.cos(a), np.sin(a), 0]) for a in np.arange(30, 360, 60) * DEGREES]
        group = VGroup(*[
            Polygon(ORIGIN, *[corners[i] for i in idx], fill_color=color, fill_opacity=1, stroke_color=WHITE, stroke_width=1)
            for idx, color in [((2, 1, 0), BLUE_B), ((2, 3, 4), BLUE_D), ((4, 5, 0), BLUE_E)]
        ])
        group.set_height(0.75 * creature.get_height())
        group.next_to(creature, RIGHT)
        creature.look_at(group)
        return VGroup(creature, group)

    def get_graphical_intuition_image(self):
        # CHANGE: a Cairo Scene ran setup() in __init__; in GL it runs in run(), so a scene created by hand needs it (get_graph reads default_graph_colors_cycle)
        gs = GraphScene()
        gs.setup()
        gs.setup_axes()
        graph = gs.get_graph(
            lambda x: 0.2 * (x - 3) * (x - 5) * (x - 6) + 4,
            x_min=2, x_max=8,
        )
        rects = gs.get_riemann_rectangles(
            graph, x_min=2, x_max=8,
            stroke_width=0.5,
            dx=0.25
        )
        gs.add(graph, rects, gs.axes)
        # CHANGE: a GL scene keeps its camera frame in .mobjects once setup() has run; it must not end up in the group
        group = VGroup(*[m for m in gs.mobjects if m is not gs.frame])
        self.adjust_size(group)
        group.next_to(self.title, DOWN, MED_LARGE_BUFF)
        group.rects = rects
        group.continual_animations = [
            turn_animation_into_updater(Write(rects)),
            turn_animation_into_updater(ShowCreation(graph)),
            turn_animation_into_updater(FadeIn(gs.axes)),
        ]
        self.adjust_size(group)
        return group
