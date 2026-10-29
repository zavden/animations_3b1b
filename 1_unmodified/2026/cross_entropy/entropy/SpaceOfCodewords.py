# ==============================================================================
# Scene:      SpaceOfCodewords
# Source:     videos/_2026/cross_entropy/entropy.py (lines 245-467)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl SpaceOfCodewords.py SpaceOfCodewords -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

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
