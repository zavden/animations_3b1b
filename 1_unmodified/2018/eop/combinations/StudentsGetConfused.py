# ==============================================================================
# Scene:      StudentsGetConfused
# Source:     videos/_2018/eop/combinations.py (lines 2620-2669)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl StudentsGetConfused.py StudentsGetConfused -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class Male(Tex):
    CONFIG = {
        "height" : 0.4,
        "tex" : "\\male",
        "color" : BLUE,
    }
    def __init__(self, **kwargs):
        digest_config(self, kwargs)
        Tex.__init__(self, self.tex, **kwargs)
        self.set_height(self.height)
        self.set_color(self.color)


class Female(Male):
    CONFIG = {
        "tex" : "\\female",
        "color" : MAROON_B,
    }


class StudentsGetConfused(PiCreatureScene):
    def construct(self):
        pi1, pi2 = self.pi_creatures
        line = VGroup(
            Male(), Female(), Female(), Male(), Female()
        )
        width = line.get_width()
        for i, mob in enumerate(line):
            mob.shift((i*width+SMALL_BUFF)*RIGHT)
        line.scale(1.5)
        line.arrange(RIGHT, SMALL_BUFF)
        line.move_to(self.pi_creatures, UP)

        self.add(line)
        self.play(
            self.get_shuffle_anim(line),
            PiCreatureSays(
                pi1, "Wait \\dots order matters now?",
                target_mode = "confused",
                look_at = line
            )
        )
        self.play(
            self.get_shuffle_anim(line),
            *[
                ApplyMethod(pi.change, "confused", line)
                for pi in self.pi_creatures
            ]
        )
        for x in range(4):
            self.play(self.get_shuffle_anim(line))
        self.wait()

    def create_pi_creatures(self):
        pis = VGroup(*[
            Randolph(color = color)
            for color in (BLUE_D, BLUE_B)
        ])
        pis[1].flip()
        pis.arrange(RIGHT, buff = 5)
        pis.to_edge(DOWN)
        return pis

    def get_shuffle_anim(self, line):
        indices = list(range(len(line)))
        random.shuffle(indices)
        line.generate_target()
        for i, m in zip(indices, line.target):
            m.move_to(line[i])
        return MoveToTarget(line, path_arc = np.pi)
