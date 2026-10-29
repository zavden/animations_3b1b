# ==============================================================================
# Scene:      ShowSeveralConvexShapes
# Source:     videos/_2021/shadows.py (lines 5437-5493)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ShowSeveralConvexShapes.py ShowSeveralConvexShapes -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

def sort_to_camera(mobject, camera_frame):
    cl = camera_frame.get_implied_camera_location()
    mobject.sort(lambda p: -get_norm(p - cl))
    return mobject


class ShowSeveralConvexShapes(Scene):
    def construct(self):
        frame = self.camera.frame
        frame.reorient(0, 70)

        dodec = Dodecahedron()
        dodec.set_fill(BLUE_D)

        spike = VGroup()
        hexagon = RegularPolygon(6)
        spike.add(hexagon)
        for v1, v2 in adjacent_pairs(hexagon.get_vertices()):
            spike.add(Polygon(v1, v2, 2 * OUT))
        spike.set_fill(BLUE_E)

        blob = Group(Sphere())
        blob.stretch(0.5, 0)
        blob.stretch(0.5, 1)
        blob.set_color(BLUE_E)
        blob.apply_function(
            lambda p: [*(2 - p[2]) * p[:2], p[2]]
        )
        blob.set_color(BLUE_E)

        cylinder = Group(Cylinder())
        cylinder.set_color(GREY_BROWN)
        cylinder.rotate(PI / 4, UP)

        examples = Group(*(
            Group(*mob)
            for mob in (dodec, spike, blob, cylinder)
        ))

        for ex in examples:
            ex.set_depth(2)
            ex.deactivate_depth_test()
            ex.set_gloss(0.5)
            ex.set_shadow(0.5)
            ex.set_reflectiveness(0.2)
            ex.rotate(20 * DEGREES, OUT)
            sort_to_camera(ex, self.camera.frame)
            for sm in ex:
                if isinstance(sm, VMobject):
                    sm.set_stroke(WHITE, 1)
                    sm.set_fill(opacity=0.9)
                else:
                    sm.always_sort_to_camera(self.camera)

        examples.arrange(RIGHT, buff=LARGE_BUFF)

        self.play(LaggedStart(*(
            LaggedStartMap(Write, ex, run_time=1)
            if isinstance(ex[0], VMobject)
            else ShowCreation(ex[0])
            for ex in examples
        ), lag_ratio=0.5, run_time=8))
        self.wait()
