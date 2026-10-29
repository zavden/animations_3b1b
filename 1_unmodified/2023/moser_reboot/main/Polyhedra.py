# ==============================================================================
# Scene:      Polyhedra
# Source:     videos/_2023/moser_reboot/main.py (lines 696-736)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl Polyhedra.py Polyhedra -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class Polyhedra(InteractiveScene):
    def construct(self):
        # Test
        frame = self.frame
        frame.reorient(30, 70)
        cube = VCube()
        cube.set_stroke(WHITE, 2, 0.5)
        cube.set_flat_stroke(False)
        cube.set_fill(BLUE_D, 0.8)
        cube.set_shading(1, 0.5, 0)
        cube.apply_depth_test()
        cube.move_to(2.0 * OUT)

        dodec = Dodecahedron()
        dodec.match_style(cube)
        dodec.move_to(2.0 * IN)
        dodec.set_fill(TEAL_E)

        camera_point = frame.get_implied_camera_location()
        cube.add_updater(lambda m: m.sort(lambda p: -get_norm(p - camera_point)))
        dodec.add_updater(lambda m: m.sort(lambda p: -get_norm(p - camera_point)))

        self.add(cube, dodec)
        self.play(LaggedStart(
            Rotating(
                cube,
                axis=np.array([1, 1, 1]),
                angle=PI,
                rate_func=smooth,
                about_point=cube.get_center()
            ),
            Rotating(
                dodec,
                axis=np.array([1, -1, 0]),
                angle=PI,
                rate_func=smooth,
                about_point=dodec.get_center()
            ),
            run_time=16,
            lag_ratio=0.2
        ))
