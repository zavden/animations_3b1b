# ==============================================================================
# Scene:      StateOfBitcoin
# Source:     videos/_2017/256.py (lines 660-766)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl StateOfBitcoin.py StateOfBitcoin -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

def get_google_logo():
    result = SVGMobject(
        file_name = "google_logo",
        height = 0.75
    )
    blue, red, yellow, green = [
        "#4885ed", "#db3236", "#f4c20d", "#3cba54"
    ]
    colors = [red, yellow, blue, green, red, blue]
    result.set_color_by_gradient(*colors)
    return result


class StateOfBitcoin(TeacherStudentsScene):
    def construct(self):
        title = OldTexText("Total", "B", "mining")
        title.to_edge(UP)
        bitcoin_logo = BitcoinLogo()
        bitcoin_logo.set_height(0.5)
        bitcoin_logo.move_to(title[1])
        title.remove(title[1])

        rate = OldTexText(
            "5 Billion Billion", 
            "$\\frac{\\text{Hashes}}{\\text{Second}}$"
        )
        rate.next_to(title, DOWN, MED_LARGE_BUFF)

        google = get_google_logo()
        kilo = OldTexText("Kilo")
        kilo.scale(1.5)
        kilo.next_to(google[-1], LEFT, SMALL_BUFF, DOWN)
        third = OldTex("1 \\over 3")
        third.next_to(kilo, LEFT)
        kilogoogle = VGroup(*it.chain(third, kilo, google))
        kilogoogle.sort()
        kilogoogle.next_to(rate, DOWN, MED_LARGE_BUFF)

        rate.save_state()
        rate.shift(DOWN)
        rate.set_fill(opacity = 0)

        all_text = VGroup(title, bitcoin_logo, rate, kilogoogle)

        gpu = SVGMobject(
            file_name = "gpu",
            height = 1,
            fill_color = GREY_B,
        )
        gpu.shift(0.5*FRAME_X_RADIUS*RIGHT)
        gpu_name = OldTexText("GPU")
        gpu_name.set_color(BLUE)
        gpu_name.next_to(gpu, UP)
        gpu_group = VGroup(gpu, gpu_name)
        gpu_group.to_edge(UP)
        cross = Cross(gpu_group)
        gpu_group.add(cross)

        asic = OldTexText(
            "Application", "Specific\\\\", "Integrated", "Circuit"
        )
        for word in asic:
            word[0].set_color(YELLOW)
        asic.move_to(gpu)
        asic.to_edge(UP)
        asic.shift(LEFT)
        circuit = SVGMobject(
            file_name = "circuit",
            height = asic.get_height(),
            fill_color = WHITE,
        )
        random.shuffle(circuit.submobjects)
        circuit.set_color_by_gradient(WHITE, GREY)
        circuit.next_to(asic, RIGHT)
        asic_rate = OldTexText("Trillion hashes/sec")
        asic_rate.next_to(asic, DOWN, MED_LARGE_BUFF)
        asic_rate.set_color(GREEN)

        self.play(
            Write(title),
            DrawBorderThenFill(bitcoin_logo)
        )
        self.play(
            self.teacher.change, "raise_right_hand",
            rate.restore,
        )
        self.play_student_changes(*["pondering"]*3)
        self.play(LaggedStartMap(FadeIn, kilogoogle))
        self.play_student_changes(*["surprised"]*3)
        self.wait()
        self.play_student_changes(
            *["plain"]*3,
            added_anims = [
                all_text.to_edge, LEFT,
                self.teacher.change_mode, "happy"
            ],
            look_at = gpu
        )
        self.play(
            Write(gpu_name),
            DrawBorderThenFill(gpu)
        )
        self.play(ShowCreation(cross))
        self.wait()
        self.play(
            Write(asic),
            gpu_group.to_edge, DOWN,
            self.teacher.change, "raise_right_hand",
        )

        self.play_student_changes(
            *["pondering"]*3,
            added_anims = [Write(asic_rate)]
        )
        self.play(LaggedStartMap(
            FadeIn, circuit,
            run_time = 3,
            lag_ratio = 0.2,
        ))
        self.wait()
