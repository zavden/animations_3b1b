# ==============================================================================
# Scene:      RotatingNameLetters
# Source:     videos/outside_videos/name_animation.py (lines 168-250)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl RotatingNameLetters.py RotatingNameLetters -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Camera.frame_rate is read-only in this ManimGL (the frame rate comes from the render options, 15/30 fps set by the pipeline): drop the assignment
#   - NameAnimationScene.run re-created the scene per name with Cairo-only calls (self.__init__(), file_writer.file_name/begin, camera.frame_rate) and wrote the video as <name><Class>.mp4: render the first name once through the normal Scene.run so the output is <Class>.mp4 (the list has a single name)
#
# Notes:
#   Renders, but the video shows Latin letters (the 'Test name' pattern) instead of the Chinese name 范英睿: the pipeline's default LaTeX template has no CJK support (plain `latex` reports 'Unicode character ... not set up'). CJKutf8/ctex are installed, so a CJK template could be used (pending user decision).
# ==============================================================================

from manim_imports_ext import *

class NameAnimationScene(Scene):
    CONFIG = {
        "animated_name": "Test name",
        "all_names": [
            "范英睿",
        ],
        "animate_all_names": True,
        "linger_after_completion": False,
    }

    def run(self):
        # CHANGE: NameAnimationScene.run re-created the scene per name with Cairo-only calls (self.__init__(), file_writer.file_name/begin, camera.frame_rate) and wrote the video as <name><Class>.mp4: render the first name once through the normal Scene.run so the output is <Class>.mp4 (the list has a single name)
        if self.animate_all_names:
            self.animated_name = self.edit_name_text(self.all_names[0])
        super().run()

    def edit_name_text(self, name):
        return name


class RotatingNameLetters(NameAnimationScene):
    def edit_name_text(self, name):
        if len(name) < 8:
            name += " Is Delightful"
        return name

    def construct(self):
        diameter = 3.0
        radius = diameter / 2
        letter_scale = 1

        name = self.animated_name.replace(" ", "$\\cdot$")
        name += "$\\cdot$"
        text_mob = OldTexText(name)
        text_mob.set_stroke(BLACK, 2, background=True)
        # for part in text_mob.get_parts_by_tex("$\\cdot$"):
        #     part.set_opacity(0)
        letter_mobs = text_mob[0]
        nb_letters = len(letter_mobs)
        randy = PiCreature()
        randy.move_to(ORIGIN).set_height(0.5 * diameter)
        randy.set_color(BLUE_E)
        randy.look_at(UP + RIGHT)
        self.add(randy)
        dtheta = TAU / nb_letters
        angles = np.arange(TAU / 4, -3 * TAU / 4, -dtheta)
        name_mob = VGroup()
        for (letter_mob, angle) in zip(letter_mobs, angles):
            letter_mob.scale(letter_scale)
            pos = radius * np.cos(angle) * RIGHT + radius * np.sin(angle) * UP
            letter_mob.move_to(pos)
            name_mob.add(letter_mob)

        pos2 = radius * np.cos(angles[2]) * RIGHT + \
            radius * np.sin(angles[2]) * UP

        times_n_label = VGroup(
            OldTex("\\times"),
            Integer(1)
        )
        times_n_label.arrange(RIGHT)
        times_n_label.shift(FRAME_WIDTH * RIGHT / 4)
        times_n_label.to_edge(UP)

        self.play(
            LaggedStartMap(FadeIn, name_mob, run_time=3),
            ApplyMethod(randy.change, "pondering", pos2, run_time=1),
            FadeIn(times_n_label)
        )

        for n in range(2, nb_letters + 2):

            group = []

            for (j, letter_mob) in enumerate(name_mob.submobjects):

                new_angle = TAU / 4 - n * j * dtheta
                new_pos = radius * np.cos(new_angle) * \
                    RIGHT + radius * np.sin(new_angle) * UP
                letter_mob.target = letter_mob.copy().move_to(new_pos)
                anim = MoveToTarget(letter_mob, path_arc=- j * dtheta)
                group.append(anim)
            new_n = Integer(n)
            new_n.move_to(times_n_label[1])
            self.play(
                AnimationGroup(*group, run_time=3),
                UpdateFromFunc(randy, lambda r: r.look_at(name_mob.submobjects[2])),
                FadeOut(times_n_label[1]),
                FadeIn(new_n)
            )
            times_n_label.submobjects[1] = new_n
            self.wait(0.5)

        thank_you = OldTexText("Thank You!").next_to(randy, DOWN)
        new_randy = randy.copy()
        new_randy.change("hooray")
        new_randy.set_color(BLUE_E)
        new_randy.look_at(ORIGIN)
        self.play(
            ReplacementTransform(name_mob, VGroup(*thank_you)),
            Transform(randy, new_randy)
        )
        self.play(Blink(randy))
