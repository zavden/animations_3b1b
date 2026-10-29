# ==============================================================================
# Scene:      FlowNameAnimation
# Source:     videos/outside_videos/name_animation.py (lines 80-127)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl FlowNameAnimation.py FlowNameAnimation -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - GL curves are quadratic: get_anchors_and_handles() returns (anchors1, handles, anchors2), not the four cubic arrays of Cairo
#   - stale import of a module that does not exist (_2017.eoc.div_curl): define four_swirls_function inline (copied from _2018/div_curl.py), use CairoVectorField and the engine's move_submobjects_along_vector_field
#   - Scene.add_foreground_mobjects is a Cairo API that GL lacks: add the strokes normally (they stay in front of the field, which is added later with its own animation)
#   - ApplyMethod(m.restore) builds its target from a copy(), which drops saved_state in this ManimGL (documented fork bug #5): use the GL animation Restore, which restores each stroke from its saved state
# ==============================================================================

from manim_imports_ext import *

class FlowNameAnimation(Scene):
    CONFIG = {
        "patron_name": "Test Name"
    }

    def construct(self):
        name_mob = OldTexText(self.patron_name)
        name_mob.scale(2)
        max_width = FRAME_WIDTH - 2
        if name_mob.get_width() > max_width:
            name_mob.set_width(max_width)
        name_strokes = VGroup()
        for mob in name_mob.family_members_with_points():
            mob.insert_n_curves(20)
            # CHANGE: GL curves are quadratic: get_anchors_and_handles() returns (anchors1, handles, anchors2), not the four cubic arrays of Cairo
            anchors1, handles, anchors2 = mob.get_anchors_and_handles()
            for a1, h, a2 in zip(anchors1, handles, anchors2):
                stroke = VMobject()
                stroke.set_points([a1, h, a2])
                stroke.set_stroke(WHITE, width=2)
                name_strokes.add(stroke)
                stroke.save_state()

        # CHANGE: stale import of a module that does not exist (_2017.eoc.div_curl): define four_swirls_function inline (copied from _2018/div_curl.py), use CairoVectorField and the engine's move_submobjects_along_vector_field
        # the original imported these from a module (_2017/eoc/div_curl.py) that no longer exists in the repo; four_swirls_function is the one of 2018/div_curl.py,
        # VectorField is the Cairo-style grid of arrows (CairoVectorField) and move_submobjects_along_vector_field comes from the engine
        def four_swirls_function(point):
            x, y = point[:2]
            result = (y**3 - 4 * y) * RIGHT + (x**3 - 16 * x) * UP
            result *= 0.05
            return result
        VectorField = CairoVectorField
        func = four_swirls_function
        vector_field = VectorField(func)
        vector_field.submobjects.sort(
            key=lambda a: a.get_length()
        )
        flow = move_submobjects_along_vector_field(name_strokes, func)

        # CHANGE: Scene.add_foreground_mobjects is a Cairo API that GL lacks: add the strokes normally (they stay in front of the field, which is added later with its own animation)
        self.add(name_strokes)
        self.play(Write(name_strokes))
        self.play(LaggedStartMap(GrowArrow, vector_field))
        self.add(flow)
        self.wait(60)
        self.remove(flow)
        self.play(
            FadeOut(vector_field),
            # CHANGE: ApplyMethod(m.restore) builds its target from a copy(), which drops saved_state in this ManimGL (documented fork bug #5): use the GL animation Restore, which restores each stroke from its saved state
            LaggedStartMap(
                Restore, name_strokes,
                lag_ratio=0.2
            ),
            run_time=5,
        )
        self.wait()
