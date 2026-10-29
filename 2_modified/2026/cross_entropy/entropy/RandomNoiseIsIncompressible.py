# ==============================================================================
# Scene:      RandomNoiseIsIncompressible
# Source:     videos/_2026/cross_entropy/entropy.py (lines 677-1146)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl RandomNoiseIsIncompressible.py RandomNoiseIsIncompressible -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - The robot is looked up in 'Lunar Rover Assets/' next to the file (before: Grant's output folder, with Path(...) which gave 'PosixPath + str'); the path is passed to ImageMobject as a str.
#   - The example images that were missing (ShrewMole, US_color_graph, TerryTaoPaulErdos, PixarCampus, IMG-9874, PiCreatureDalle3_13, EiffelTower1, Dalle3_blue_1) are replaced with placeholder images in _lib/assets/raster_images/ (the code looks them up by name).
#
# Placeholder assets (not Grant's originals):
#   - _lib/assets/raster_images/{ShrewMole,US_color_graph,TerryTaoPaulErdos,PixarCampus,IMG-9874,PiCreatureDalle3_13,EiffelTower1,Dalle3_blue_1}.png (labeled placeholder images, made with placeholder.py; the originals are not in the repo)
#
# Notes:
#   Lunar Rover Assets/Stationary.png is the faithful conversion of images/lunar_rover_assets/Stationary.tif; arrow.svg is the faithful conversion of images/arrow.ai.
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *
import numpy as np

def bit_string_mobject(
    bit_string: str,
    font: str = "Consolas",
    font_size: int = 48,
    colors: List[Colors] = [GREY_C, GREY_B]
):
    result = Text(bit_string, font=font, font_size=font_size)
    result["0"].set_color(colors[0])
    result["1"].set_color(colors[1])
    return result


def int_to_bit_string(n_bits, value=None, **kwargs):
    if value is None:
        value = np.random.randint(0, 2**n_bits)
    return bit_string_mobject(f"{value:0{n_bits}b}", **kwargs)


class InstructionArrow(SVGMobject):
    def __init__(self, direction=RIGHT, width=0.5, *args, **kwargs):
        super().__init__("arrow.svg", *args, **kwargs)
        self.set_width(width)
        self.rotate(angle_of_vector(direction))
        self.direction = direction


class ArrowGroup(VGroup):
    def __init__(self):
        super().__init__(InstructionArrow(v) for v in [UP, DOWN, LEFT, RIGHT])


class SpaceOfCodewords(InteractiveScene):
    layer_colors = (BLUE_E, TEAL_E)

    def construct(self):
        # Introduce diagram
        diagram = self.get_core_diagram(n_layers=8)
        ellipsis = Tex(R"\vdots", font_size=72)
        ellipsis.next_to(diagram, UP)

        self.add(diagram[0])
        for l1, l2 in zip(diagram, diagram[1:]):
            layer_copy = l1.copy()
            for box in layer_copy:
                point = VectorizedPoint()
                point.next_to(box[0], RIGHT, SMALL_BUFF)
                box[0].add(point)
            self.play(LaggedStart(
                TransformFromCopy(layer_copy, l2[0::2]),
                TransformFromCopy(layer_copy, l2[1::2]),
                lag_ratio=0.5,
                run_time=1.5
            ))
            self.wait(0.5)
        self.play(Write(ellipsis))
        self.add(diagram)
        self.wait()

        # Just stare at it
        frame = self.frame
        randy, morty = pis = VGroup(Randolph(), Mortimer())
        pis.arrange(RIGHT, buff=2.0)
        pis.next_to(diagram, DOWN, LARGE_BUFF)

        self.play(
            frame.animate.set_height(11, about_edge=UP),
            VFadeIn(pis),
            randy.change("pondering", diagram),
            morty.change("raise_right_hand", diagram),
        )
        self.play(Blink(randy))
        self.wait()
        self.play(randy.change("thinking", diagram))
        self.play(Blink(randy))
        self.wait()

        # Highlight layers
        bit_labels = VGroup(
            TexText(Rf"{n + 1} bit{"s" if n > 0 else ""} $\rightarrow$").next_to(layer, LEFT)
            for n, layer in enumerate(diagram)
        )

        last_bit_label = Mobject()
        for n, layer in enumerate(diagram):
            bit_label = bit_labels[n]
            self.highlight_layer(diagram, n, added_anims=[
                frame.animate.move_to(LEFT).set_height(1.05 * FRAME_HEIGHT),
                FadeIn(bit_label),
                FadeOut(last_bit_label),
                pis.animate.set_opacity(0)
            ])
            last_bit_label = bit_label
        self.wait()
        self.play(
            FadeOut(pis),
            FadeOut(last_bit_label),
            frame.animate.to_default_state(),
            diagram.animate.set_fill(opacity=1),
        )

        # Recursive parts
        to_fade = VGroup()
        for bit_string in ["0", "1", "00", "01", "10", "11", "100"]:
            prefixes = VGroup(
                rect[0][:len(bit_string)]
                for rect in self.get_blocks_with_prefix(diagram, bit_string)
            ).copy()
            prefixes.set_fill(RED, 1)
            prefix_rect = SurroundingRectangle(prefixes[0], buff=SMALL_BUFF)
            prefix_rect.set_stroke(RED, 2)

            self.highlight_bit_string(
                diagram,
                bit_string,
                prefix=True,
                added_anims=[ShowCreation(prefix_rect), FadeOut(to_fade)]
            )
            self.play(FadeIn(prefixes, lag_ratio=0.5 / len(prefixes)))
            to_fade = VGroup(prefixes, prefix_rect)
            self.wait()
            self.add(diagram)
        self.play(diagram.animate.set_fill(opacity=1), FadeOut(to_fade))

        # Allocate four particular strings
        symbols = VGroup(Vector(0.5 * v, thickness=8) for v in [UP, DOWN, LEFT, RIGHT])
        symbols.set_fill(YELLOW)
        prefixes = ["0", "10", "110", "111"]

        key_blocks = VGroup()
        equation_labels = VGroup()
        blocked_groups = VGroup()
        for symbol, prefix in zip(symbols, prefixes):
            all_blocks = self.get_blocks_with_prefix(diagram, prefix)
            block = all_blocks[0]
            blocks_above = all_blocks[1:]
            blocks_below = VGroup(
                self.get_block_by_bit_string(diagram, prefix[:n])
                for n in range(1, len(prefix))
            )

            label = block[0]
            label.target = label.generate_target()
            new_label = VGroup(label.target, Tex(R"="), symbol)
            new_label.arrange(RIGHT, buff=0.2)
            new_label.set_max_width(0.8 * block.get_width())
            new_label.move_to(label)

            blocks_below.target = blocks_below.generate_target()
            for block_below in blocks_below.target:
                block_below.set_fill(opacity=0.25).set_stroke(opacity=0.5)
                block_below[0].set_fill(opacity=0).set_stroke(width=0)

            self.play(
                blocks_above.animate.set_fill(opacity=0.25).set_stroke(opacity=0.5),
                MoveToTarget(blocks_below),
                MoveToTarget(label),
                Write(new_label[1:])
            )
            self.wait()
            key_blocks.add(block)
            block.equation = VGroup(label, *new_label[1:])
            equation_labels.add(block.equation)
            blocked_groups.add(blocks_above)

        self.add(diagram, equation_labels)

        # Explicity show blocking
        braces = VGroup(Brace(block, DOWN, SMALL_BUFF) for block in key_blocks)
        for brace in braces[1:]:
            brace.stretch(0.5, 1, about_edge=UP)
        prop_labels = VGroup(
            VGroup(brace, brace.get_tex(f"1 / {n}", font_size=36))
            for brace, n in zip(braces, [2, 4, 8, 8])
        )

        for block, prop_label, eq_label, blocked_group in zip(key_blocks, prop_labels, equation_labels, blocked_groups):
            underline = Underline(eq_label, buff=0.05)
            underline.set_max_height(0.7, stretch=True)
            underline.set_stroke(YELLOW, (0, 3, 3, 3, 0))
            self.play(
                ShowCreation(underline),
                blocked_group.animate.set_fill(RED, 0.2),
            )
            self.play(
                FadeIn(prop_label, scale=2)
            )
            self.wait()

    def get_core_diagram(self, n_layers=8, layer_height=0.75, width=12):
        diagram = VGroup(
            self.get_layer(n, layer_height, width)
            for n in range(1, n_layers - 1)
        )
        diagram.arrange(UP, buff=0)
        return diagram

    def get_layer(self, n, height=0.75, total_width=12):
        rects = Rectangle(total_width / 2**n, height).replicate(2**n)
        rects.arrange(RIGHT, buff=0)
        rects.set_fill(BLUE, 1)
        rects.set_submobject_colors_by_gradient(*self.layer_colors)
        rects.set_stroke(WHITE, 1)

        labels = VGroup()
        for rect, bits in zip(rects, it.product(*["01"] * n)):
            bit_string = "".join(bits)
            label = Text(bit_string)
            if n > 4:
                label.arrange(DOWN, buff=SMALL_BUFF)
            label.move_to(rect)
            label.set_max_height(0.8 * rect.get_height())
            label.set_max_width(0.8 * rect.get_width())
            rect.add(label)
            rect.bit_string = bit_string

        return rects

    def highlight_layer(self, diagram, layer_num, alt_opacity=0.1, added_anims=[]):
        diagram.target = diagram.generate_target()
        for n, layer in enumerate(diagram.target):
            if n == layer_num:
                opacity = 1
            else:
                opacity = alt_opacity
            layer.set_fill(opacity=opacity)
        self.play(MoveToTarget(diagram), *added_anims)

    def highlight_bit_string(self, diagram, bit_string, prefix=False, alt_opacity=0.1, added_anims=[]):
        diagram.target = diagram.generate_target()
        for layer in diagram.target:
            for rect in layer:
                if rect.bit_string == bit_string:
                    opacity = 1
                elif prefix and rect.bit_string.startswith(bit_string):
                    opacity = 1
                else:
                    opacity = alt_opacity
                rect.set_fill(opacity=opacity)
        self.play(MoveToTarget(diagram), *added_anims)

    def get_blocks_with_prefix(self, diagram, prefix):
        return VGroup(
            rect
            for layer in diagram
            for rect in layer
            if rect.bit_string.startswith(prefix)
        )

    def get_block_by_bit_string(self, diagram, bit_string):
        for layer in diagram:
            for rect in layer:
                if rect.bit_string == bit_string:
                    return rect
        return None


class RandomNoiseIsIncompressible(SpaceOfCodewords):
    def construct(self):
        # Receive n bits
        frame = self.frame
        frame.reorient(0, 0, 0, (-2.75, 0, 0.0), 5)
        # CHANGE: the robot lived in a "Lunar Rover Assets" folder next to Grant's video output; now it is next to this file
        # (Stationary.png is the conversion of Stationary.tif). Also ImageMobject requires str (not Path) in this version of manimgl.
        robot_path = str(Path(__file__).parent / 'Lunar Rover Assets' / 'Stationary.png')
        robot = ImageMobject(robot_path)
        robot.set_height(2)
        robot.to_edge(LEFT, buff=SMALL_BUFF)

        n_bits = 16
        bit_string = self.get_bit_string(n_bits)
        bit_string.next_to(robot, RIGHT)

        self.add(robot)
        self.play(
            FadeIn(bit_string, shift=3 * LEFT, lag_ratio=0.1, run_time=3)
        )
        self.wait()

        # Instruction-by-instruction
        syms = ArrowGroup()
        colors = color_gradient([YELLOW, BLUE], 4, interp_by_hsl=True)
        cw_lengths = [1, 1, 1, 1, 2, 2, 2, 2, 3, 1]
        cw_partial_sums = np.cumsum(cw_lengths)
        buff = 0.5 * get_norm(bit_string[0].get_right() - bit_string[1].get_left())
        rects = VGroup(
            SurroundingRectangle(bit_string[n1:n2], buff=buff)
            for n1, n2 in zip([0, *cw_partial_sums], cw_partial_sums)
        )
        intruction_indices = [0, 0, 0, 0, 1, 1, 1, 1, 2, 0]
        instructions = VGroup()
        for idx, rect in zip(intruction_indices, rects):
            rect.set_stroke(colors[idx], 2)
            arrow = syms[idx].copy()
            arrow.set_fill(colors[idx])
            arrow.match_x(rect)
            arrow.set_y(rects.get_y() + 0.5)
            instructions.add(arrow)

        self.play(
            ShowIncreasingSubsets(instructions),
            ShowIncreasingSubsets(rects),
            rate_func=linear,
            run_time=1
        )
        self.wait()

        # Full message
        brace = Brace(bit_string, UP, SMALL_BUFF)
        message_word = brace.get_text("message")
        instructions.target = instructions.generate_target()
        instructions.target.arrange(RIGHT, buff=SMALL_BUFF).scale(0.5)
        instructions.target.next_to(message_word, UP)

        full_rect = SurroundingRectangle(bit_string).set_stroke(YELLOW, 2)

        self.play(LaggedStart(
            ReplacementTransform(rects, VGroup(full_rect), path_arc=10 * DEG, lag_ratio=0.1),
            MoveToTarget(instructions),
            GrowFromCenter(brace),
            FadeIn(message_word, 0.5 * UP),
        ))
        self.wait()

        # n bits
        mid_message = Tex(R"\rightarrow m_i")
        mid_message.next_to(bit_string[-1:], RIGHT, MED_SMALL_BUFF, index_of_submobject_to_align=0)
        mid_message[-1].set_opacity(0)

        low_brace = Brace(bit_string, DOWN, SMALL_BUFF)
        n_bit_label = low_brace.get_tex(R"n \text{ bits}")

        self.play(LaggedStart(
            frame.animate.set_height(6, about_edge=LEFT),
            FadeTransform(message_word[0].copy(), mid_message[1:]),
            Write(mid_message[0]),
            FadeOut(message_word),
            instructions.animate.set_width(1).next_to(mid_message[1], DOWN, SMALL_BUFF),
            ReplacementTransform(brace, low_brace, path_arc=-20 * DEG),
            FadeIn(n_bit_label, shift=DOWN),
            run_time=2
        ))
        self.wait()

        # Show all 2^n possible strings
        top_bit_strings, low_bit_strings = [
            VGroup(
                self.get_bit_string(n_bits, n)
                for n in n_range
            ).arrange(DOWN)
            for n_range in [range(4), range(2**n_bits - 4, 2**n_bits)]
        ]
        ellipses = VGroup(
            Tex(R"\vdots").next_to(bit_string, vect)
            for vect in [UP, DOWN]
        )
        top_bit_strings.next_to(ellipses, UP)
        low_bit_strings.next_to(ellipses, DOWN)

        top_messages = VGroup(
            Tex(fR"\rightarrow m_{n}").next_to(bs[-1:], RIGHT, MED_SMALL_BUFF, index_of_submobject_to_align=0)
            for n, bs in enumerate(top_bit_strings)
        )
        low_messages = VGroup(
            Tex(fR"\rightarrow m_{{2^n - {4 - n}}}").next_to(bs[-1:], RIGHT, MED_SMALL_BUFF, index_of_submobject_to_align=0)
            for n, bs in enumerate(low_bit_strings)
        )
        for message in [*top_messages, mid_message, *low_messages]:
            message[2:].scale(0.5, about_edge=LEFT)

        all_bit_strings = VGroup(*top_bit_strings, bit_string, *low_bit_strings)
        all_messages = VGroup(*top_messages, mid_message, *low_messages)

        brace = Brace(VGroup(top_messages, low_messages), RIGHT)
        count = brace.get_tex("2^n", font_size=72, buff=0.2)

        kw = dict(lag_ratio=0.5, run_time=4)
        self.play(
            frame.animate.to_default_state().shift(0.25 * DOWN),
            VGroup(low_brace, n_bit_label).animate.next_to(low_bit_strings, DOWN, SMALL_BUFF),
            GrowFromCenter(brace),
            LaggedStartMap(FadeIn, VGroup(*top_bit_strings, *low_bit_strings), **kw),
            LaggedStartMap(FadeIn, VGroup(*top_messages, *low_messages), **kw),
            Write(ellipses),
            Write(count),
            FadeOut(full_rect),
            mid_message.animate.set_fill(opacity=1),
        )
        self.wait()

        # Flash through
        for n in range(10):
            yellow_bit_strings = all_bit_strings.copy().set_color(YELLOW)
            yellow_bit_strings.shuffle()
            self.play(ShowSubmobjectsOneByOne(yellow_bit_strings, rate_func=linear))
            self.remove(yellow_bit_strings)

        # Reference equally likely
        prob_eq = Tex(R"P(m_i) = {1 \over 2^n}")
        prob_eq.move_to(bit_string).to_edge(RIGHT)
        arrows = VGroup(
            Arrow(
                prob_eq.get_left() + 0.25 * f * UP,
                mess.get_right(),
                path_arc=f * 20 * DEG,
                thickness=3,
                fill_color=TEAL,
                buff=0.2
            )
            for mess, f in zip(all_messages, np.linspace(1, -1, len(all_messages)))
        )
        self.play(
            FadeOut(brace),
            FadeTransform(count, prob_eq["2^n"]),
            Write(prob_eq[:-2]),
            LaggedStartMap(GrowArrow, arrows)
        )
        self.add(prob_eq)

        # Fade robot
        self.play(instructions.animate.set_width(2).next_to(robot, DOWN, buff=-0.2))
        self.wait()
        self.play(Group(robot, instructions).animate.fade(0.5).scale(0.75, about_edge=LEFT))
        self.wait()

        # Alternate data types
        prob_pointer = VGroup(arrows, prob_eq)
        text_rhss = VGroup(
            Text(f"= “{text}”", font_size=30).set_fill(random_bright_color(
                hue_range=(0.53, 0.53),
                saturation_range=(0.8, 0.8),
                luminance_range=(0.7, 0.4),
            ))
            for text in self.get_example_strings()
        )
        image_rhss = Group(
            Group(Tex("="), ImageMobject(filename, height=3)).arrange(RIGHT, SMALL_BUFF)
            for filename in self.get_example_image_names()
        )
        for pair in zip(image_rhss, text_rhss):
            for mob in pair:
                mob.next_to(mid_message, RIGHT).align_to(mid_message[1])
        alt_strings = VGroup(
            self.get_bit_string(n_bits).replace(bit_string)
            for n in range(len(text_rhss))
        )
        alt_strings[0].become(bit_string.copy())

        index_tracker = ValueTracker(0)

        def get_submob(group):
            n = len(group)
            index, _ = integer_interpolate(0, n, index_tracker.get_value())
            return group[index]

        shown_text = VGroup(text_rhss[0])
        shown_image = Group(image_rhss[-1])

        self.play(
            FadeOut(prob_pointer, RIGHT),
            FadeIn(shown_text, RIGHT, suspend_mobject_updating=True),
        )
        self.play(
            index_tracker.animate.set_value(1),
            UpdateFromFunc(bit_string, lambda m: m.set_submobjects(list(get_submob(alt_strings)))),
            UpdateFromFunc(shown_text, lambda m: m.set_submobjects([get_submob(text_rhss)])),
            run_time=2,
            rate_func=linear
        )
        self.wait()
        self.play(
            FadeOut(shown_text, RIGHT),
            FadeIn(shown_image, RIGHT),
        )
        self.play(
            index_tracker.animate.set_value(0),
            UpdateFromFunc(bit_string, lambda m: m.set_submobjects(list(get_submob(alt_strings)))),
            UpdateFromFunc(shown_image, lambda m: m.set_submobjects([get_submob(image_rhss)])),
            run_time=2,
            rate_func=linear
        )
        self.wait()
        self.play(
            Transform(bit_string, alt_strings[0]),
            FadeOut(shown_image, RIGHT),
            FadeIn(text_rhss[7], RIGHT),
        )
        self.wait()
        self.play(
            Transform(bit_string, alt_strings[1]),
            FadeOut(text_rhss[7], RIGHT),
            FadeIn(text_rhss[6], RIGHT),
        )
        self.wait()
        self.play(
            FadeOut(text_rhss[6]),
            FadeIn(prob_pointer, lag_ratio=0.1, run_time=2),
        )
        self.wait()

        # Emphasize random noise
        rect = SurroundingRectangle(bit_string)
        rects = VGroup(SurroundingRectangle(mob) for mob in all_bit_strings)
        rect.set_stroke(YELLOW, 2)
        rects.set_stroke(YELLOW, 2)

        self.play(ShowCreation(rect))
        self.play(
            UpdateFromFunc(bit_string, lambda m: m.become(self.get_bit_string(n_bits).replace(bit_string)))
        )
        self.wait()
        self.play(TransformFromCopy(VGroup(rect), rects))
        self.wait()
        self.play(
            FadeOut(rects),
            rect.animate.surround(prob_eq[R"{1 \over 2^n}"])
        )
        self.wait()
        self.play(FadeOut(rect))

        # Put into the diagram
        frame = self.frame

        to_fade = Group(
            robot, instructions, all_bit_strings, ellipses, all_messages, prob_pointer,
            low_brace, n_bit_label
        )
        diagram = self.get_core_diagram(n_layers=7)
        diagram.next_to(to_fade, RIGHT, buff=2.0)
        top_layer = diagram[-1]
        diagram.remove(top_layer)

        m_terms = VGroup(Tex(Rf"m_{{{n}}}", font_size=36) for n in range(16))
        for m_term, message in zip(m_terms, it.cycle([*top_messages, *low_messages])):
            m_term.move_to(message[1], LEFT)
            m_term[1:].scale(0.5, about_edge=LEFT)

        m_terms.target = m_terms.generate_target()
        for term, box in zip(m_terms.target, diagram[3]):
            term.next_to(box, UP, SMALL_BUFF)
            term.set_fill(box.get_fill_color())

        self.play(
            frame.animate.set_height(2 * FRAME_HEIGHT, about_edge=LEFT),
            FadeIn(diagram),
            FadeIn(top_layer),
            run_time=2,
        )
        self.wait()
        self.highlight_layer(diagram, 3, alt_opacity=0.2, added_anims=[
            frame.animate.set_height(FRAME_HEIGHT).move_to(diagram).set_anim_args(run_time=3),
            MoveToTarget(m_terms, run_time=2, lag_ratio=0.01),
            FadeOut(to_fade),
            FadeOut(top_layer)
        ])
        self.wait()

        # Circle all the bits
        rects = VGroup(SurroundingRectangle(block[0], buff=0.05) for block in diagram[3])
        rects.set_stroke(YELLOW, 4)
        rects.insert_n_curves(100)

        self.play(LaggedStartMap(VShowPassingFlash, rects, time_width=2, lag_ratio=0.08, run_time=5))

        # Push and pop
        m_terms.save_state()
        diagram.save_state()
        residue7 = self.push_down_message(m_terms, diagram, top_layer, index=7)
        self.wait()
        residue13 = self.push_down_message(m_terms, diagram, top_layer, index=13)
        self.wait()
        self.play(
            Restore(m_terms),
            Restore(diagram),
            FadeOut(VGroup(residue7, residue13)),
        )
        self.wait()

    def get_bit_string(self, n_bits, value=None, **kwargs):
        return int_to_bit_string(n_bits, value, **kwargs)

    def push_down_message(self, m_terms, diagram, top_layer, index):
        # Move one message down
        moved_m_term = m_terms[index]
        rect = SurroundingRectangle(moved_m_term).set_stroke(YELLOW, 2)
        old_box = diagram[3][index]
        new_box = diagram[2][index // 2]
        brace = Brace(new_box, DOWN, SMALL_BUFF)
        brace.stretch(0.5, 1, about_edge=UP)

        self.play(ShowCreation(rect))
        self.play(
            VGroup(moved_m_term, rect).animate.next_to(brace, DOWN, SMALL_BUFF),
            GrowFromCenter(brace),
            new_box.animate.set_fill(opacity=1),
            diagram[1][index // 4][0].animate.set_opacity(0),
            old_box.animate.set_fill(opacity=0.2),
            rate_func=rush_into,
        )

        # Show overlapping
        blocked_box = diagram[3][index - 1]
        blocked_box.target = blocked_box.generate_target()
        blocked_box.target.set_fill(RED)
        blocked_box.target[0].set_fill(WHITE)
        blocked_m_term = m_terms[index - 1]
        bang = Tex(R"!", font_size=30)
        bang.set_fill(RED)
        bang.next_to(blocked_m_term, RIGHT, buff=0.05, aligned_edge=DOWN)

        self.play(
            MoveToTarget(blocked_box),
            blocked_m_term.animate.set_color(RED),
            FadeIn(bang, shift=0.1 * UP, scale=0.5),
            rate_func=rush_from,
        )
        self.wait()

        # Wander
        wanderer = VGroup(m_terms[index - 1], bang)

        self.play(
            wanderer.animate.next_to(m_terms[0], UP).set_anim_args(path_arc=10 * DEG),
            blocked_box.animate.set_fill(opacity=0.1),
            run_time=2,
        )
        self.play(wanderer.animate.next_to(m_terms[-1], UP), run_time=2)
        self.play(wanderer.animate.next_to(m_terms[index - 2], UP), run_time=2)

        # Pop up
        top_layer_index = 2 * (index - 1)
        top_boxes = top_layer[top_layer_index - 2:top_layer_index]
        moved_m_terms = m_terms[index - 2:index]
        moved_m_terms.target = moved_m_terms.generate_target()
        for term, box in zip(moved_m_terms.target, top_boxes):
            term.next_to(box, UP, buff=0.15)
            term.set_fill(box.get_fill_color())
        moved_m_terms.target.space_out_submobjects(1.5)

        self.play(
            FadeIn(top_boxes),
            MoveToTarget(moved_m_terms),
            FadeOut(bang),
            diagram[3][index - 2].animate.set_fill(opacity=0.1),
            rate_func=rush_into,
        )
        self.wait()

        return VGroup(rect, brace, top_boxes)

    def get_example_strings(self):
        return [
            "Text to compress...",
            "Claude Shannon",
            "3Blue1Brown",
            "Randy the pi creature",
            "(hey, psst, subscribe)",
            "happy birthday to you",
            "Q7m4!",
            "1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11",
            "2, 3, 5, 7, 11,",
            "Random examples of text",
            "are very hard to think of",
            "but I refuse to use an LLM",
            "when there‘s joy in",
            "easter eggs for the",
            "attentive viewer‘ like you",
            "It was the best of times...",
            "Wouldn't it be cool if",
            "these texts could really be",
            "compressed to just 16 bits",
            "blah, blah, blah, yada, yada",
        ]

    def get_example_image_names(self):
        return [
            "Andrey_Kolmogorov",
            "Richard_Hamming",
            "ShrewMole",
            "ss_central_america",
            "Fork",
            "Turing",
            "Cow",
            "Puppy",
            "Principia_equal_area",
            "US_color_graph",
            "TerryTaoPaulErdos",
            "ZoeyInGrass",
            "sars_icon",
            "PixarCampus",
            "IMG-9874",
            "PiCreatureDalle3_13",
            "Tom_In_Bowtie",
            "EiffelTower1",
            "Dalle3_blue_1",
            "Claude_Shannon",
        ]

    def old_material(self):
        # Show 3-bit examples for robot
        bit_string_diagram = VGroup(all_bit_strings, ellipses, all_messages, arrows, prob_eq)
        bit_string_diagram.save_state()

        three_bit_messages = VGroup(
            self.get_bit_string(3, n)
            for n in range(8)
        )
        three_bit_messages.arrange(DOWN)
        three_bit_messages.next_to(robot, RIGHT)

        syms = [Vector(0.5 * v) for v in [UP, DOWN, LEFT, RIGHT]]
        examples = VGroup(three_bit_messages[i] for i in [0, 7, 4])

        self.play(
            bit_string_diagram.animate.set_height(1.5).to_corner(UR),
            *(
                TransformFromCopy(bs1[-3:], bs2)
                for bs1, bs2 in zip(top_bit_strings, three_bit_messages[:4])
            ),
            *(
                TransformFromCopy(bs1[-3:], bs2)
                for bs1, bs2 in zip(low_bit_strings, three_bit_messages[4:])
            ),
        )
        self.wait()
