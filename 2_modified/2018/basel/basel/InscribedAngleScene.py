# ==============================================================================
# Scene:      InscribedAngleScene
# Source:     videos/_2018/basel/basel.py (lines 2306-3022)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl InscribedAngleScene.py InscribedAngleScene -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - numpy 2: `array != None` is elementwise (ambiguous truth value); use `is not None`
#   - manimgl bug: with draw_together the render fails with "min_storage_buffer_offset_alignment" (unaligned GPU offsets); each mobject is drawn separately
# ==============================================================================

from manim_imports_ext import *
from once_useful_constructs.light import *
import warnings

warnings.warn("""
    Warning: This file makes use of
    ContinualAnimation, which has since
    been deprecated
""")


LIGHT_COLOR = YELLOW


INDICATOR_STROKE_WIDTH = 1


INDICATOR_STROKE_COLOR = WHITE


INDICATOR_TEXT_COLOR = WHITE


NUM_LEVELS = 15


AMBIENT_SCALE = 2.0


LIGHT_COLOR = YELLOW


inverse_power_law = lambda maxint,scale,cutoff,exponent: \
    (lambda r: maxint * (cutoff/(r/scale+cutoff))**exponent)


inverse_quadratic = lambda maxint,scale,cutoff: inverse_power_law(maxint,scale,cutoff,2)


class LightIndicator(VMobject):
    CONFIG = {
        "radius": 0.5,
        "intensity": 0,
        "opacity_for_unit_intensity": 1,
        "precision": 3,
        "show_reading": True,
        "measurement_point": ORIGIN,
        "light_source": None
    }

    def init_points(self):
        self.background = Circle(color=BLACK, radius = self.radius)
        self.background.set_fill(opacity=1.0)
        self.foreground = Circle(color=self.color, radius = self.radius)
        self.foreground.set_stroke(color=INDICATOR_STROKE_COLOR,width=INDICATOR_STROKE_WIDTH)

        self.add(self.background, self.foreground)
        self.reading = DecimalNumber(self.intensity,num_decimal_places = self.precision)
        self.reading.set_fill(color=INDICATOR_TEXT_COLOR)
        self.reading.move_to(self.get_center())
        if self.show_reading:
            self.add(self.reading)

    def set_intensity(self, new_int):
        self.intensity = new_int
        new_opacity = min(1, new_int * self.opacity_for_unit_intensity)
        self.foreground.set_fill(opacity=new_opacity)
        ChangeDecimalToValue(self.reading, new_int).update(1)
        return self

    def get_measurement_point(self):
        # CHANGE: numpy 2: `array != None` is elementwise (ambiguous truth value); use `is not None`
        if self.measurement_point is not None:
            return self.measurement_point
        else:
            return self.get_center()


    def measured_intensity(self):
        distance = get_norm(self.get_measurement_point() - 
            self.light_source.get_source_point())
        intensity = self.light_source.opacity_function(distance) / self.opacity_for_unit_intensity
        return intensity

    def update_mobjects(self):
        if self.light_source == None:
            print("Indicator cannot update, reason: no light source found")
        self.set_intensity(self.measured_intensity())


# CHANGE: manimgl bug: with draw_together the render fails with "min_storage_buffer_offset_alignment" (unaligned GPU offsets); each mobject is drawn separately
class InscribedAngleScene(ThreeDScene):
    default_camera_config = {"draw_together": False}




    def construct(self):

        BASELINE_YPOS = -2.5
        OBSERVER_POINT = [0,BASELINE_YPOS,0]
        LAKE0_RADIUS = 1.5
        INDICATOR_RADIUS = 0.6
        TICK_SIZE = 0.5
        LIGHTHOUSE_HEIGHT = 0.3
        LAKE_COLOR = BLUE
        LAKE_OPACITY = 0.15
        LAKE_STROKE_WIDTH = 5.0
        LAKE_STROKE_COLOR = BLUE
        TEX_SCALE = 0.8
        DOT_COLOR = BLUE

        LIGHT_MAX_INT = 1
        LIGHT_SCALE = 5
        LIGHT_CUTOFF = 1

        self.cumulated_zoom_factor = 1


        def zoom_out_scene(factor):


            phi0 = self.camera.get_phi() # default is 0 degs
            theta0 = self.camera.get_theta() # default is -90 degs
            distance0 = self.camera.get_distance()

            distance1 = 2 * distance0
            camera_target_point = self.camera.get_spherical_coords(phi0, theta0, distance1)

            self.play(
                ApplyMethod(self.camera.rotation_mobject.move_to, camera_target_point),
                self.zoomable_mobs.shift, self.obs_dot.get_center(),
                self.unzoomable_mobs.scale,2,{"about_point" : ORIGIN},
            )

            self.cumulated_zoom_factor *= factor


        def shift_scene(v):
            self.play(
                self.zoomable_mobs.shift,v,
                self.unzoomable_mobs.shift,v
            )

        self.force_skipping()

        self.zoomable_mobs = VMobject()
        self.unzoomable_mobs = VMobject()


        baseline = VMobject()
        baseline.set_points_as_corners([[-8,BASELINE_YPOS,0],[8,BASELINE_YPOS,0]])
        baseline.set_stroke(width = 0) # in case it gets accidentally added to the scene
        self.zoomable_mobs.add(baseline) # prob not necessary

        self.obs_dot = Dot(OBSERVER_POINT, fill_color = DOT_COLOR)
        self.ls0_dot = Dot(OBSERVER_POINT + 2 * LAKE0_RADIUS * UP, fill_color = WHITE)
        self.unzoomable_mobs.add(self.obs_dot) #, self.ls0_dot)

        # lake
        lake0 = Circle(radius = LAKE0_RADIUS,
            stroke_width = 0,
            fill_color = LAKE_COLOR,
            fill_opacity = LAKE_OPACITY
        )
        lake0.move_to(OBSERVER_POINT + LAKE0_RADIUS * UP)
        self.zoomable_mobs.add(lake0)

        # Morty and indicator
        morty = Mortimer().scale(0.3)
        morty.next_to(OBSERVER_POINT,DOWN)
        indicator = LightIndicator(precision = 2,
            radius = INDICATOR_RADIUS,
            show_reading  = False,
            color = LIGHT_COLOR
        )
        indicator.next_to(morty,LEFT)
        self.unzoomable_mobs.add(morty, indicator)

        # first lighthouse
        original_op_func = inverse_quadratic(LIGHT_MAX_INT,AMBIENT_SCALE,LIGHT_CUTOFF)
        ls0 = LightSource(opacity_function = original_op_func, num_levels = NUM_LEVELS)
        ls0.move_source_to(OBSERVER_POINT + LAKE0_RADIUS * 2 * UP)
        self.zoomable_mobs.add(ls0, ls0.lighthouse, ls0.ambient_light)

        self.add(lake0,morty,self.obs_dot,self.ls0_dot, ls0.lighthouse)

        self.wait()


        # shore arcs
        arc_left = Arc(-TAU/2,
            radius = LAKE0_RADIUS,
            start_angle = -TAU/4,
            stroke_width = LAKE_STROKE_WIDTH,
            stroke_color = LAKE_STROKE_COLOR
        )
        arc_left.move_arc_center_to(OBSERVER_POINT + LAKE0_RADIUS * UP)

        one_left = OldTex("1", color = LAKE_COLOR).scale(TEX_SCALE)
        one_left.next_to(arc_left,LEFT)
        

        arc_right = Arc(TAU/2,
            radius = LAKE0_RADIUS,
            start_angle = -TAU/4,
            stroke_width = LAKE_STROKE_WIDTH,
            stroke_color = LAKE_STROKE_COLOR
        )
        arc_right.move_arc_center_to(OBSERVER_POINT + LAKE0_RADIUS * UP)

        one_right = OldTex("1", color = LAKE_COLOR).scale(TEX_SCALE)
        one_right.next_to(arc_right,RIGHT)

        self.play(
            ShowCreation(arc_left),
            Write(one_left),
            ShowCreation(arc_right),
            Write(one_right),
        )


        self.play(
            SwitchOn(ls0.ambient_light),
            lake0.set_stroke,{"color": LAKE_STROKE_COLOR, "width" : LAKE_STROKE_WIDTH},
        )

        self.play(FadeIn(indicator))

        self.play(
            indicator.set_intensity,0.5
        )

        # diameter
        diameter = DoubleArrow(OBSERVER_POINT,
            ls0.get_source_point(),
            buff = 0,
            color = WHITE,
        )
        diameter_text = OldTex("d").scale(TEX_SCALE)
        diameter_text.next_to(diameter,RIGHT)

        self.play(
            ShowCreation(diameter),
            Write(diameter_text),
            #FadeOut(self.obs_dot),
            FadeOut(self.ls0_dot)
        )

        indicator_reading = OldTex("{1\over d^2}").scale(TEX_SCALE)
        indicator_reading.move_to(indicator)
        self.unzoomable_mobs.add(indicator_reading)

        self.play(
            FadeIn(indicator_reading)
        )

        # replace d with its value
        new_diameter_text = OldTex("{2\over \pi}").scale(TEX_SCALE)
        new_diameter_text.color = LAKE_COLOR
        new_diameter_text.move_to(diameter_text)
        self.play(
            Transform(diameter_text,new_diameter_text)
        )

        # insert into indicator reading
        new_reading = OldTex("{\pi^2 \over 4}").scale(TEX_SCALE)
        new_reading.move_to(indicator)

        self.play(
            Transform(indicator_reading,new_reading)
        )

        self.play(
            FadeOut(one_left),
            FadeOut(one_right),
            FadeOut(diameter_text),
            FadeOut(arc_left),
            FadeOut(arc_right)
        )




        def indicator_wiggle():
            INDICATOR_WIGGLE_FACTOR = 1.3

            self.play(
                ScaleInPlace(indicator, INDICATOR_WIGGLE_FACTOR, rate_func = wiggle),
                ScaleInPlace(indicator_reading, INDICATOR_WIGGLE_FACTOR, rate_func = wiggle)
            )


        def angle_for_index(i,step):
            return -TAU/4 + TAU/2**step * (i + 0.5)


        def position_for_index(i, step, scaled_down = False):

            theta = angle_for_index(i,step)
            radial_vector = np.array([np.cos(theta),np.sin(theta),0])
            position = self.lake_center + self.lake_radius * radial_vector

            if scaled_down:
                return position.scale_about_point(self.obs_dot.get_center(),0.5)
            else:
                return position


        def split_light_source(i, step, show_steps = True, run_time = 1):

            ls_new_loc1 = position_for_index(i,step + 1)
            ls_new_loc2 = position_for_index(i + 2**step,step + 1)

            hyp = VMobject()
            hyp1 = Line(self.lake_center,ls_new_loc1)
            hyp2 = Line(self.lake_center,ls_new_loc2)
            hyp.add(hyp2,hyp1)
            self.new_hypotenuses.append(hyp)

            if show_steps == True:
                self.play(
                    ShowCreation(hyp, run_time = run_time)
                )

            leg1 = Line(self.obs_dot.get_center(),ls_new_loc1)
            leg2 = Line(self.obs_dot.get_center(),ls_new_loc2)
            self.new_legs_1.append(leg1)
            self.new_legs_2.append(leg2)

            if show_steps == True:
                self.play(
                    ShowCreation(leg1, run_time = run_time),
                    ShowCreation(leg2, run_time = run_time),
                )

            ls1 = self.light_sources_array[i]


            ls2 = ls1.copy()
            self.add(ls2)
            self.additional_light_sources.append(ls2)

            # check if the light sources are on screen
            ls_old_loc = np.array(ls1.get_source_point())
            onscreen_old = np.all(np.abs(ls_old_loc[:2]) < 10 ** 2**step)
            onscreen_1 = np.all(np.abs(ls_new_loc1[:2][:2]) < 10 ** 2**step)
            onscreen_2 = np.all(np.abs(ls_new_loc2[:2]) < 10 ** 2**step)
            show_animation = (onscreen_old or onscreen_1 or onscreen_2)

            if show_animation:
                print("animating (", i, ",", step, ")")
                self.play(
                    ApplyMethod(ls1.move_source_to,ls_new_loc1, run_time = run_time),
                    ApplyMethod(ls2.move_source_to,ls_new_loc2, run_time = run_time),
                )
            else:
                ls1.move_source_to(ls_new_loc1)
                ls2.move_source_to(ls_new_loc1)





        def construction_step(n, show_steps = True, run_time = 1,
            simultaneous_splitting = False):

            # we assume that the scene contains:
            # an inner lake, self.inner_lake
            # an outer lake, self.outer_lake
            # light sources, self.light_sources
            # legs from the observer point to each light source
            # self.legs
            # altitudes from the observer point to the
            # locations of the light sources in the previous step
            # self.altitudes
            # hypotenuses connecting antipodal light sources
            # self.hypotenuses

            # these are mobjects!


            # first, fade out all of the hypotenuses and altitudes

            if show_steps == True:
                self.zoomable_mobs.remove(self.hypotenuses, self.altitudes, self.inner_lake)
                self.play(
                    FadeOut(self.hypotenuses),
                    FadeOut(self.altitudes),
                    FadeOut(self.inner_lake)
                )
            else:
                self.zoomable_mobs.remove(self.inner_lake)
                self.play(
                    FadeOut(self.inner_lake)
                )

            # create a new, outer lake
            self.lake_center = self.obs_dot.get_center() + self.lake_radius * UP

            new_outer_lake = Circle(radius = self.lake_radius,
                stroke_width = LAKE_STROKE_WIDTH,
                fill_color = LAKE_COLOR,
                fill_opacity = LAKE_OPACITY,
                stroke_color = LAKE_STROKE_COLOR
            )
            new_outer_lake.move_to(self.lake_center)

            if show_steps == True: 
                self.play(
                    FadeIn(new_outer_lake, run_time = run_time),
                    FadeIn(self.ls0_dot)
                )
            else:
                self.play(
                    FadeIn(new_outer_lake, run_time = run_time),
                )

            self.wait()

            self.inner_lake = self.outer_lake
            self.outer_lake = new_outer_lake
            self.altitudes = self.legs
            #self.lake_center = self.outer_lake.get_center()

            self.additional_light_sources = []
            self.new_legs_1 = []
            self.new_legs_2 = []
            self.new_hypotenuses = [] 

            for i in range(2**n):
                split_light_source(i,
                    step = n,
                    show_steps = show_steps,
                    run_time = run_time
                )



            # collect the newly created mobs (in arrays)
            # into the appropriate Mobject containers

            self.legs = VMobject()
            for leg in self.new_legs_1:
                self.legs.add(leg)
                self.zoomable_mobs.add(leg)
            for leg in self.new_legs_2:
                self.legs.add(leg)
                self.zoomable_mobs.add(leg)

            for hyp in self.hypotenuses.submobjects:
                self.zoomable_mobs.remove(hyp)

            self.hypotenuses = VMobject()
            for hyp in self.new_hypotenuses:
                self.hypotenuses.add(hyp)
                self.zoomable_mobs.add(hyp)

            for ls in self.additional_light_sources:
                self.light_sources.add(ls)
                self.light_sources_array.append(ls)
                self.zoomable_mobs.add(ls)

            # update scene
            self.add(
                self.light_sources,
                self.inner_lake,
                self.outer_lake,
            )
            self.zoomable_mobs.add(self.light_sources, self.inner_lake, self.outer_lake)

            if show_steps == True:
                self.add(
                    self.legs,
                    self.hypotenuses,
                    self.altitudes,
                )
                self.zoomable_mobs.add(self.legs, self.hypotenuses, self.altitudes)


            self.wait()

            if show_steps == True:
                self.play(FadeOut(self.ls0_dot))

            #self.lake_center = ls0_loc = self.obs_dot.get_center() + self.lake_radius * UP
            self.lake_radius *= 2








        self.lake_center = ls0_loc = ls0.get_source_point()

        self.inner_lake = VMobject()
        self.outer_lake = lake0
        self.legs = VMobject()
        self.legs.add(Line(OBSERVER_POINT,self.lake_center))
        self.altitudes = VMobject()
        self.hypotenuses = VMobject()
        self.light_sources_array = [ls0]
        self.light_sources = VMobject()
        self.light_sources.add(ls0)

        self.lake_radius = 2 * LAKE0_RADIUS # don't ask...

        self.zoomable_mobs.add(self.inner_lake, self.outer_lake, self.altitudes, self.light_sources)

        self.add(self.inner_lake,
            self.outer_lake,
            self.legs,
            self.altitudes,
            self.hypotenuses
        )

        self.play(FadeOut(diameter))
        
        self.additional_light_sources = []
        self.new_legs_1 = []
        self.new_legs_2 = []
        self.new_hypotenuses = []

        self.revert_to_original_skipping_status()

        construction_step(0)
        indicator_wiggle()
        self.play(FadeOut(self.ls0_dot))
        zoom_out_scene(2)

        return

        construction_step(1)
        indicator_wiggle()
        self.play(FadeOut(self.ls0_dot))
        zoom_out_scene(2)

        construction_step(2)
        indicator_wiggle()
        self.play(FadeOut(self.ls0_dot))



        self.revert_to_original_skipping_status()


        ANGLE_COLOR1 = BLUE_C
        ANGLE_COLOR2 = GREEN_D

        
        for mob in self.mobjects:
            mob.fade(1.0)

        for hyp in self.hypotenuses:
            hyp.set_stroke(width = 0)
        for alt in self.altitudes:
            alt.set_stroke(width = 0)
        for leg in self.legs:
            leg.set_stroke(width = 0)
        self.inner_lake.set_stroke(width = 0)
        self.outer_lake.set_stroke(width = 0)

        self.wait()

        inner_lake_center = self.inner_lake.get_center()
        inner_lake_radius = self.lake_radius * 0.25
        inner_ls = VGroup()
        for i in range(4):
            theta = -TAU/4 + (i+0.5) * TAU/4
            point = inner_lake_center + inner_lake_radius * np.array([np.cos(theta), np.sin(theta),0])
            dot = Dot(point, color = LAKE_STROKE_COLOR, radius = 0.3)
            inner_ls.add(dot)

        self.add(inner_ls)

        inner_ls1 = inner_ls.submobjects[0]
        inner_ls2 = inner_ls.submobjects[1]
        inner_ls1_center = inner_ls1.get_center()
        inner_ls2_center = inner_ls2.get_center()

        outer_lake_center = self.outer_lake.get_center()
        outer_lake_radius = self.lake_radius * 0.5
        outer_ls = VGroup()
        for i in range(8):
            theta = -TAU/4 + (i+0.5) * TAU/8
            point = outer_lake_center + outer_lake_radius * np.array([np.cos(theta), np.sin(theta),0])
            dot = Dot(point, color = LAKE_STROKE_COLOR, radius = 0.3)
            outer_ls.add(dot)

        self.add(outer_ls)

        outer_ls1 = outer_ls.submobjects[0]
        outer_ls2 = outer_ls.submobjects[1]
        outer_ls1_center = outer_ls1.get_center()
        outer_ls2_center = outer_ls2.get_center()

        self.wait()

        arc_radius = 2.0

        line1 = Line(inner_lake_center, inner_ls1_center, color = WHITE)
        line2 = Line(inner_lake_center, inner_ls2_center, color = WHITE)


        #arc_point1 = interpolate(inner_lake_center, inner_ls1_center, 0.2)
        #arc_point2 = interpolate(inner_lake_center, inner_ls2_center, 0.2)
        #inner_angle_arc = ArcBetweenPoints(arc_point1, arc_point2, angle = TAU/4)
        inner_angle_arc = Arc(angle = TAU/4, start_angle = -TAU/8, radius = arc_radius,
            stroke_color = ANGLE_COLOR1)
        inner_angle_arc.move_arc_center_to(inner_lake_center)

        inner_label = OldTex("\\theta", fill_color = ANGLE_COLOR1).scale(3).next_to(inner_angle_arc, LEFT, buff = -0.1)

        self.play(
            ShowCreation(line1),
            ShowCreation(line2),
        )
        self.play(
            ShowCreation(inner_angle_arc),
            FadeIn(inner_label)
        )




        self.wait()



        line3 = Line(outer_lake_center, inner_ls1_center, color = WHITE)
        line4 = Line(outer_lake_center, inner_ls2_center, color = WHITE)
        outer_angle_arc = Arc(angle = TAU/8, start_angle = -3*TAU/16, radius = arc_radius,
            stroke_color = ANGLE_COLOR2)
        outer_angle_arc.move_arc_center_to(outer_lake_center)

        outer_label = OldTex("{\\theta \over 2}", color = ANGLE_COLOR2).scale(2.5).move_to(outer_angle_arc)
        outer_label.shift([-2,-1,0])

        self.play(
            ShowCreation(line3),
            ShowCreation(line4),
        )
        self.play(
            ShowCreation(outer_angle_arc),
            FadeIn(outer_label)
        )



        self.wait()



        line5 = Line(outer_lake_center, outer_ls1_center, color = WHITE)
        line6 = Line(outer_lake_center, outer_ls2_center, color = WHITE)

        self.play(
            ShowCreation(line5),
            ShowCreation(line6)
        )


        self.wait()

        self.play(
            FadeOut(line1),
            FadeOut(line2),
            FadeOut(line3),
            FadeOut(line4),
            FadeOut(line5),
            FadeOut(line6),
            FadeOut(inner_angle_arc),
            FadeOut(outer_angle_arc),
            FadeOut(inner_label),
            FadeOut(outer_label),
        )


        self.wait()

        inner_lines = VGroup()
        inner_arcs = VGroup()

        for i in range(-2,2):

            theta = -TAU/4 + (i+0.5)*TAU/4
            ls_point = inner_lake_center + inner_lake_radius * np.array([
                np.cos(theta), np.sin(theta),0])
            line = Line(inner_lake_center, ls_point, color = WHITE)
            inner_lines.add(line)

            arc = Arc(angle = TAU/4, start_angle = theta, radius = arc_radius,
                stroke_color = ANGLE_COLOR1)
            arc.move_arc_center_to(inner_lake_center)
            inner_arcs.add(arc)

            if i == 1:
                arc.set_stroke(width = 0)

        for line in inner_lines.submobjects:
            self.play(
                ShowCreation(line),
            )
        self.add_foreground_mobject(inner_lines)
        for arc in inner_arcs.submobjects:
            self.play(
                ShowCreation(arc)
            )

        self.wait()

        outer_lines = VGroup()
        outer_arcs = VGroup()

        for i in range(-2,2):

            theta = -TAU/4 + (i+0.5)*TAU/4

            ls_point = inner_lake_center + inner_lake_radius * np.array([
                np.cos(theta), np.sin(theta),0])
            line = Line(outer_lake_center, ls_point, color = WHITE)
            outer_lines.add(line)

            theta = -TAU/4 + (i+0.5)*TAU/8
            arc = Arc(angle = TAU/8, start_angle = theta, radius = arc_radius,
                stroke_color = ANGLE_COLOR2)
            arc.move_arc_center_to(outer_lake_center)
            outer_arcs.add(arc)

            if i == 1:
                arc.set_stroke(width = 0)

        
        for line in outer_lines.submobjects:
            self.play(
                ShowCreation(line),
            )
        self.add_foreground_mobject(outer_lines)
        for arc in outer_arcs.submobjects:
            self.play(
                ShowCreation(arc)
            )

        self.wait()

        self.play(
            FadeOut(inner_lines),
            FadeOut(inner_arcs)
        )


        outer_lines2 = VGroup()

        for i in range(-2,2):

            theta = -TAU/4 + (i+0.5)*TAU/8
            ls_point = outer_lake_center + outer_lake_radius * np.array([
                np.cos(theta), np.sin(theta),0])
            line = Line(outer_lake_center, ls_point, color = WHITE)
            outer_lines2.add(line)

        self.play(
            ShowCreation(outer_lines2),
        )

        self.wait()

        outer_lines3 = outer_lines2.copy().rotate(TAU/2, about_point = outer_lake_center)
        outer_arcs3 = outer_arcs.copy().rotate(TAU/2, about_point = outer_lake_center)

        self.play(
            ShowCreation(outer_lines3),
        )
        self.add_foreground_mobject(outer_lines3)
        for arc in outer_arcs3.submobjects:
            self.play(
                ShowCreation(arc)
            )

        last_arc = outer_arcs3.submobjects[0].copy()
        last_arc.rotate(-TAU/8, about_point = outer_lake_center)
        last_arc2 = last_arc.copy()
        last_arc2.rotate(TAU/2, about_point = outer_lake_center)

        self.play(
            ShowCreation(last_arc),
            ShowCreation(last_arc2),
        )

        self.wait()

        self.play(
            FadeOut(outer_lines2),
            FadeOut(outer_lines3),
            FadeOut(outer_arcs),
            FadeOut(outer_arcs3),
            FadeOut(last_arc),
            FadeOut(last_arc2),
        )

        self.play(
            FadeOut(inner_ls),
            FadeOut(outer_ls),
        )


        self.wait()
