# ==============================================================================
# Scene:      ImagesMod256
# Source:     videos/outside_videos/tweets/image_manipulation.py (lines 4-48)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl ImagesMod256.py ImagesMod256 -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - GL ImageMobject has no pixel_array and cannot be built from an array: read the PIL image from lion.image_path and save each altered frame to a temp PNG
#   - pixel_array -> PIL image of the file (RGB so the modulo does not hit an alpha channel)
#   - ImageMobject(array) is not supported by GL: save to a temp PNG and load it
# ==============================================================================

from manim_imports_ext import *

# Broken, but fixable
class ImagesMod256(Scene):
    CONFIG = {
    }

    def construct(self):
        # CHANGE: GL ImageMobject has no pixel_array and cannot be built from an array: read the PIL image from lion.image_path and save each altered frame to a temp PNG
        lion = ImageMobject("Lion")
        import os, tempfile
        tmp_dir = tempfile.mkdtemp()
        lion.set_height(6)
        lion.to_edge(DOWN)
        integer = Integer(1)
        expression = VGroup(
            OldTex("n \\rightarrow"),
            integer,
            OldTex("\\times n \\mod 256")
        )
        expression.arrange(RIGHT)
        expression[-2:].shift(MED_SMALL_BUFF * RIGHT)
        integer.next_to(expression[-1], LEFT, SMALL_BUFF)
        expression.to_edge(UP)
        self.add(lion)
        self.add(expression)
        self.wait(0.5)
        self.remove(lion)

        total_time = 10
        wait_time = 1.0 / 15
        alpha_range = np.linspace(0, 1, int(total_time / wait_time))
        for start, end in (1, 128), (128, 257):
            for alpha in ProgressDisplay(alpha_range):
                m = int(interpolate(start, end, smooth(alpha)))
                # CHANGE: pixel_array -> PIL image of the file (RGB so the modulo does not hit an alpha channel)
                im = Image.open(lion.image_path).convert("RGB")
                new_im = Image.eval(im, lambda n: (n * m) % 256)
                # CHANGE: ImageMobject(array) is not supported by GL: save to a temp PNG and load it
                alt_path = os.path.join(tmp_dir, f"mod_{m}.png")
                new_im.save(alt_path)
                alt_lion = ImageMobject(alt_path)
                alt_lion.replace(lion)
                self.add(alt_lion)

                new_int = Integer(m)
                new_int.next_to(expression[-1], LEFT, SMALL_BUFF)
                self.remove(integer)
                self.add(new_int)
                integer = new_int
                self.wait(1.0 / 15)
                self.remove(alt_lion)
        self.add(alt_lion)
        self.wait()
