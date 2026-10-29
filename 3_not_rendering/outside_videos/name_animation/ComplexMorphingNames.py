# ==============================================================================
# Scene:      ComplexMorphingNames
# Source:     videos/outside_videos/name_animation.py (lines 8-77)
# Category:   3 · Does not render
#
# Run from this folder:
#     manimgl ComplexMorphingNames.py ComplexMorphingNames -w -m --fps 15
#
# Why it does not render:
#   Not rendered (set aside by the user, 2026-10-28): broken in the original. Its base class is commented out (# class ComplexMorphingNames(ComplexTransformationScene)) with the note "I'm guessing most of this needs to be fixed", so construct() calls add_transformable_plane() on a plain Scene (AttributeError). Restoring the base class would also make get_post_transform_rotation run Transform(...).update(1) inside an updater every frame, the fork leak (bug #4) that coincided with the GPU hangs.
#
# Notes:
#   Pending user decision (2026-10-28). The original comments out its base class (# class ComplexMorphingNames(ComplexTransformationScene)) and says "I'm guessing most of this needs to be fixed": as written it calls add_transformable_plane(), which plain Scene lacks. Restoring the base class would make get_post_transform_rotation run Transform(...).update(1) inside an updater every frame, which is fork bug #4 (leak) that coincided with the GPU hangs.
# ==============================================================================

from manim_imports_ext import *

# I'm guessing most of this needs to be fixed...
# class ComplexMorphingNames(ComplexTransformationScene):
class ComplexMorphingNames(Scene):
    CONFIG = {
        "patron_name": "Janel",
        "function": lambda z: 0.2 * (z**3),
        "default_apply_complex_function_kwargs": {
            "run_time": 5,
        },
        "output_directory": os.path.join(get_output_dir(), "EightDollarPatrons"),
        "include_coordinate_labels": False,
        "vert_start_color": YELLOW,  # TODO
        "vert_end_color": PINK,
        "horiz_start_color": GREEN,
        "horiz_end_color": BLUE,
        "use_multicolored_plane": True,
        # "plane_config" : {
        #     "unit_size" : 1.5,
        # },
    }

    def construct(self):
        name = self.patron_name
        self.clear()
        self.frames = []
        self.setup()
        self.add_transformable_plane()
        self.plane.fade()

        name_mob = OldTexText(name)
        name_mob.set_width(4)
        name_mob.next_to(ORIGIN, UP, LARGE_BUFF)
        self.start_vect = name_mob.get_center()
        for submob in name_mob.family_members_with_points():
            submob.insert_n_curves(100)
        name_mob_copy = name_mob.copy()

        self.play(Write(name_mob))
        self.play(
            self.get_rotation(name_mob),
            run_time=5,
        )
        self.wait()
        self.add_transformable_mobjects(name_mob)
        self.apply_complex_function(self.function)
        self.wait()
        self.play(
            self.get_post_transform_rotation(name_mob, name_mob_copy),
            run_time=10
        )
        self.wait(3)

    def get_rotation(self, name_mob):
        return UpdateFromAlphaFunc(
            name_mob,
            lambda mob, alpha: mob.move_to(rotate_vector(
                self.start_vect, 2 * np.pi * alpha
            ))
        )

    def get_post_transform_rotation(self, name_mob, name_mob_copy):
        simple_rotation = self.get_rotation(name_mob_copy)

        def update(name_mob, alpha):
            simple_rotation.update(alpha)
            new_name = simple_rotation.mobject.copy()
            new_name.apply_complex_function(self.function)
            Transform(name_mob, new_name).update(1)
            return name_mob
        return UpdateFromAlphaFunc(name_mob, update)
