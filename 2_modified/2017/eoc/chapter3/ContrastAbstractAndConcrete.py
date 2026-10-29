# ==============================================================================
# Scene:      ContrastAbstractAndConcrete
# Source:     videos/_2017/eoc/chapter3.py (lines 41-169)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl ContrastAbstractAndConcrete.py ContrastAbstractAndConcrete -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Grant's repo renamed TexMobject->Tex here (new GL class); the 2017 code needs the Cairo-style OldTex
#   - Mobject.parents is an internal list in GL: renamed the pi creature attribute
# ==============================================================================

from manim_imports_ext import *

class ContrastAbstractAndConcrete(Scene):
    def construct(self):
        v_line = Line(UP, DOWN).scale(FRAME_Y_RADIUS)
        l_title = OldTexText("Abstract functions")
        l_title.shift(FRAME_X_RADIUS*LEFT/2)
        l_title.to_edge(UP)
        r_title = OldTexText("Applications")
        r_title.shift(FRAME_X_RADIUS*RIGHT/2)
        r_title.to_edge(UP)
        h_line = Line(LEFT, RIGHT).scale(FRAME_X_RADIUS)
        h_line.shift((r_title.get_bottom()[1]-MED_SMALL_BUFF)*UP)

        # CHANGE: Grant's repo renamed TexMobject->Tex here (new GL class); the 2017 code needs the Cairo-style OldTex
        functions = VGroup(*list(map(OldTex, [
            "f(x) = 2x^2 - x^3",
            "f(x) = \\sin(x)",
            "f(x) = e^x",
            "\\v_dots"
        ])))
        functions.arrange(
            DOWN, 
            aligned_edge = LEFT,
            buff = LARGE_BUFF
        )
        functions.shift(FRAME_X_RADIUS*LEFT/2)
        functions[-1].shift(MED_LARGE_BUFF*RIGHT)

        self.add(l_title, r_title)
        self.play(*list(map(ShowCreation, [h_line, v_line])))
        self.play(Write(functions))
        self.wait()
        anims = [
            method(func_mob)
            for func_mob, method in zip(functions, [
                self.get_car_anim,
                self.get_spring_anim,
                self.get_population_anim,
            ])
        ]
        for anim in anims:
            self.play(FadeIn(anim.mobject))
            self.play(anim)
            self.play(FadeOut(anim.mobject))


    def get_car_anim(self, alignement_mob):
        car = Car()
        point = 2*RIGHT + alignement_mob.get_bottom()[1]*UP
        target_point = point + 5*RIGHT
        car.move_to(point)
        return MoveCar(
            car, target_point, 
            run_time = 5,
        )

    def get_spring_anim(self, alignement_mob):
        compact_spring, extended_spring = [
            ParametricCurve(
                lambda t : (t/denom)*RIGHT+np.sin(t)*UP+np.cos(t)*OUT,
                t_max = 12*np.pi,
            )
            for denom in (12.0, 4.0)
        ]
        for spring in compact_spring, extended_spring:
            spring.scale(0.5)
            spring.rotate(np.pi/6, UP)
            spring.set_color(GREY)
            spring.next_to(ORIGIN, RIGHT)
            spring.shift(
                alignement_mob.get_center()[1]*UP + SMALL_BUFF*RIGHT \
                -spring.get_points()[0]
            )
            weight = Square(
                side_length = 0.5,
                stroke_width = 0, 
                fill_color = GREY_B,
                fill_opacity = 1,
            )
            weight.move_to(spring.get_points()[-1])
            spring.add(weight)

        return Transform(
            compact_spring, extended_spring, 
            rate_func = lambda t : 1+np.sin(6*np.pi*t),
            run_time = 5
        )

    def get_population_anim(self, alignement_mob):
        colors = color_gradient([BLUE_B, BLUE_E], 12)
        pis = VGroup(*[
            Randolph(
                mode = "happy",
                color = random.choice(colors)
            ).shift(
                4*x*RIGHT + 4*y*UP + \
                2*random.random()*RIGHT + \
                2*random.random()*UP
            )
            for x in range(20)
            for y in range(10)
        ])
        pis.set_height(3)
        pis.center()
        pis.to_edge(DOWN, buff = SMALL_BUFF)
        pis.shift(FRAME_X_RADIUS*RIGHT/2.)

        anims = []
        for index, pi in enumerate(pis):
            if index < 2:
                anims.append(FadeIn(pi))
                continue
            mom_index, dad_index = random.choice(
                list(it.combinations(list(range(index)), 2))
            )
            # CHANGE: Mobject.parents is an internal list in GL: renamed the pi creature attribute
            pi.bn_parents = VGroup(pis[mom_index], pis[dad_index]).copy()
            # CHANGE: Mobject.parents is an internal list in GL: renamed the pi creature attribute
            pi.bn_parents.set_fill(opacity = 0)
        exp = 1
        while 2**exp < len(pis):
            low_index = 2**exp
            high_index = min(2**(exp+1), len(pis))
            these_pis = pis[low_index:high_index]
            anims.append(Transform(
                # CHANGE: Mobject.parents is an internal list in GL: renamed the pi creature attribute
                VGroup(*[pi.bn_parents for pi in these_pis]),
                VGroup(*[VGroup(pi, pi.copy()) for pi in these_pis]),
                lag_ratio = 0.5,
                run_time = 2,
            ))
            exp += 1

        return Succession(*anims, rate_func=linear)
