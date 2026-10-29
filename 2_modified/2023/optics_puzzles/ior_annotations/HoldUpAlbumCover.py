# ==============================================================================
# Scene:      HoldUpAlbumCover
# Source:     videos/_2023/optics_puzzles/ior_annotations.py (lines 25-160)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl HoldUpAlbumCover.py HoldUpAlbumCover -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - The images Dark-side-of-the-moon and True-prism are missing (private): placeholder images; the code does not change
#
# Placeholder assets (not Grant's originals):
#   - _lib/assets/raster_images/Dark-side-of-the-moon.png (placeholder, make_optics_puzzles_assets.py)
#   - _lib/assets/raster_images/True-prism.png (placeholder, make_optics_puzzles_assets.py)
# ==============================================================================

from manim_imports_ext import *

class HoldUpAlbumCover(TeacherStudentsScene):
    background_color = interpolate_color(GREY_E, BLACK, 0.5)

    def construct(self):
        # Album
        album = ImageMobject("Dark-side-of-the-moon")
        album.set_height(3.5)
        album.move_to(self.hold_up_spot, DOWN)

        self.play(
            self.teacher.change("raise_right_hand", album),
            self.change_students("hooray", "coin_flip_2", "tease", look_at=album)
        )
        self.play(
            FadeIn(album),
        )
        self.wait(2)

        # Enlarge album
        full_rect = FullScreenRectangle()
        full_rect.set_fill(BLACK, 1)
        prism_image = ImageMobject("True-prism")
        true_prism = Group(
            SurroundingRectangle(prism_image, buff=0).set_stroke(WHITE, 10),
            prism_image
        )

        album.save_state()
        album.target = album.generate_target()
        album.target.set_height(5.5)
        album.target.next_to(ORIGIN, RIGHT, buff=0.5)
        true_prism.match_height(album.target).scale(0.98)
        true_prism.next_to(ORIGIN, LEFT, buff=0.5)

        titles = VGroup(
            Text("Genuine simulation"),
            Text("Pink Floyd"),
        )
        for title, mob in zip(titles, [true_prism, album.target]):
            title.move_to(mob)
            title.to_edge(UP, buff=0.5)


        self.add(full_rect, album, true_prism)

        self.play(
            FadeIn(full_rect),
            MoveToTarget(album),
            FadeInFromPoint(true_prism, album.get_center()),
            run_time=2,
        )
        self.remove(self.pi_creatures)
        self.play(FadeIn(titles))
        self.wait()

        # Why is this white
        white_point = np.array([3.25, 0.62, 0])
        red_arrow = Arrow(white_point + UL, white_point, buff=0.1, stroke_width=7)
        red_arrow.set_color(RED)
        why_white = Text("Why is this white?!")
        why_white.next_to(red_arrow, UP, SMALL_BUFF)
        why_white.match_x(album)
        why_white.set_color(RED)

        self.play(
            FadeIn(why_white, lag_ratio=0.1),
            GrowArrow(red_arrow),
        )
        self.wait()

        # Discrete
        roygbiv = Text("ROYGBV")
        roygbiv.rotate(-10 * DEGREES)
        roygbiv.move_to(white_point).shift(1.5 * RIGHT + 0.25 * UP)
        rainbow = VGroup(*(
            Arc(PI, -PI, radius=radius, stroke_width=10)
            for radius in np.linspace(1.5, 2.0, 6)
        ))
        rainbow.reverse_submobjects()
        rainbow.move_to(album, DOWN).shift(0.05 * UP)
        for mob in roygbiv, rainbow:
            mob.set_submobject_colors_by_gradient(
                RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE
            )

        self.play(
            FadeIn(roygbiv, lag_ratio=0.5),
            ShowCreation(rainbow, lag_ratio=0.5),
            run_time=4
        )
        self.wait()

        # Return
        self.play(LaggedStartMap(
            FadeOut, Group(
                why_white, red_arrow,
                roygbiv, rainbow,
                true_prism, *titles,
            ),
            shift=DOWN,
            scale=0.5,
            lag_ratio=0.1
        ))
        self.add(self.pi_creatures, full_rect, album)
        self.play(
            Restore(album),
            FadeOut(full_rect),
        )
        self.wait()

        # Ask question
        question = Text("Why exactly does\nthis work?")
        question.move_to(album, UP)
        arrow = Arrow(question.get_bottom(), 2 * RIGHT + UP)
        arrow.set_stroke(opacity=0)

        self.play(
            FadeOut(album, UP),
            FadeIn(question, UP),
            self.teacher.change("confused", arrow.get_end()),
            self.change_students("erm", "hesitant", "sassy", look_at=arrow.get_end())
        )
        self.play(GrowArrow(arrow))
        self.wait(5)

        # Standard explanation
        title = Text("Standard explanation:", font_size=60)
        title.to_edge(UP, buff=MED_SMALL_BUFF)

        self.play(
            FadeTransform(question, title),
            FadeOut(arrow, LEFT),
            self.teacher.change("raise_right_hand", look_at=3 * UP),
            self.change_students("pondering", "pondering", "pondering", look_at=3 * UP),
        )
        self.wait(5)
