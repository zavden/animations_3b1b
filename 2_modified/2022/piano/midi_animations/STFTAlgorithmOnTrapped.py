# ==============================================================================
# Scene:      STFTAlgorithmOnTrapped
# Source:     videos/_2022/piano/midi_animations.py (lines 150-151)
# Category:   2 · Renders with modifications
# Includes code copied from: _2022/piano/wav_to_midi.py
#
# Run from this folder:
#     manimgl STFTAlgorithmOnTrapped.py STFTAlgorithmOnTrapped -w -m --fps 15
#
# Placeholder assets (not Grant's originals):
#   - _lib/assets/generated/2022/piano/data/3-16-attempts/*.mid (synthetic MIDI transcriptions of Ode to Joy; generator make_piano_assets.py)
#
# Extra packages installed in the venv: mido
# ==============================================================================

from manim_imports_ext import *
import mido


# ----- From _2022/piano/wav_to_midi.py -----

DATA_DIR = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    "data",
)


piano_midi_range = list(range(21, 109))


# CHANGE: timidity is not installed; the audio is synthesized with numpy (sines with harmonics and exponential decay)
def midi_to_wav(mid_file):
    from scipy.io import wavfile
    wav_file = mid_file.replace(".mid", ".wav")
    sample_rate = 48000
    mid = mido.MidiFile(mid_file, clip=True)
    tempo = 500000
    t = 0.0
    pending = dict()
    notes = []
    for msg in mido.merge_tracks(mid.tracks):
        t += mido.tick2second(msg.time, mid.ticks_per_beat, tempo)
        if msg.type == "set_tempo":
            tempo = msg.tempo
        elif msg.type == "note_on" and msg.velocity > 0:
            pending[msg.note] = (t, msg.velocity)
        elif msg.type in ("note_off", "note_on") and msg.note in pending:
            start, vel = pending.pop(msg.note)
            notes.append((msg.note, start, t, vel))
    total = max([n[2] for n in notes] + [1.0]) + 1.5
    audio = np.zeros(int(total * sample_rate))
    for note, start, end, vel in notes:
        freq = 440 * 2**((note - 69) / 12)
        dur = (end - start) + 0.6
        ts = np.arange(int(dur * sample_rate)) / sample_rate
        wave = sum(
            amp * np.sin(TAU * freq * k * ts)
            for k, amp in enumerate([1.0, 0.5, 0.25, 0.12, 0.06], start=1)
            if freq * k < sample_rate / 2
        )
        env = np.exp(-ts * 3.0) * np.minimum(1, ts / 0.005)
        env *= np.where(ts > end - start, np.exp(-(ts - (end - start)) * 25), 1)
        i0 = int(start * sample_rate)
        chunk = wave * env * (vel / 127) * 0.2
        audio[i0:i0 + len(chunk)] += chunk[:len(audio) - i0]
    audio /= max(1.0, np.abs(audio).max() / 0.9)
    wavfile.write(wav_file, sample_rate, (audio * 32767).astype(np.int16))
    return wav_file



# ----- From _2022/piano/midi_animations.py -----

class AnimatedMidi(Scene):
    midi_file = "3-16-attempts/Help_Long_as_piano_5ms.mid"
    dist_per_sec = 4.0
    bpm = 240
    CONFIG = {
        "camera_config": {
            "anti_alias_width": 0,
            "samples": 4,
        }
    }
    hit_depth = 0.025
    note_color = BLUE
    hit_color = TEAL
    note_to_key_width_ratio = 0.5
    sound_file_time_offset = 0.3

    def construct(self):
        self.add_piano()
        self.add_note_rects()
        self.add_piano_sound()
        self.scroll()

    def add_piano(self):
        piano = Piano3D()
        piano.set_width(9)
        piano.move_to(5 * DOWN)

        frame = self.camera.frame
        frame.set_phi(70 * DEGREES)

        self.piano = piano
        self.add(piano)

    def add_note_rects(self):
        mid_file = self.mid_file = os.path.join(DATA_DIR, self.midi_file)

        # Pull out track
        mid = mido.MidiFile(mid_file, clip=True)
        track = mido.midifiles.MidiTrack()
        track.extend([
            msg
            for msg in mido.merge_tracks(mid.tracks)
            if msg.type not in ['pitchwheel', 'time_signature']
        ])

        # Relevant constants
        offset = piano_midi_range[0]
        tempo = 250000  # microseconds per quarter note
        # (ms / beat) * (s / ms) * (beats / tick)
        sec_per_tick = tempo * 1e-6 / mid.ticks_per_beat
        dist_per_tick = self.dist_per_sec * sec_per_tick

        pending_notes = {key: None for key in piano_midi_range}
        notes_to_time_spans = {key: [] for key in piano_midi_range}

        note_rects = VGroup()
        time_in_ticks = 0
        for msg in track:
            time_in_ticks += msg.time
            if msg.type == 'set_tempo':
                sec_per_tick *= msg.tempo / tempo
                dist_per_tick *= msg.tempo / tempo
                tempo = msg.tempo
            if msg.type == 'note_on' and msg.velocity > 0:
                pending_notes[msg.note] = (time_in_ticks, msg.velocity)
            elif msg.type == 'note_off':
                if msg.note not in pending_notes or pending_notes[msg.note] is None:
                    continue
                if msg.note not in piano_midi_range:
                    continue
                print(pending_notes[msg.note])
                start_time_in_ticks, velocity = pending_notes.pop(msg.note)
                key = self.piano[msg.note - offset]
                rect = Rectangle(
                    width=self.note_to_key_width_ratio * key.get_width(),
                    height=(time_in_ticks - start_time_in_ticks) * dist_per_tick
                )
                rect.next_to(key, UP, buff=start_time_in_ticks * dist_per_tick)
                rect.set_stroke(width=0)
                rect.set_fill(self.note_color, opacity=clip(0.25 + velocity / 100, 0, 1))
                note_rects.add(rect)
                notes_to_time_spans[msg.note].append((
                    start_time_in_ticks * sec_per_tick,
                    time_in_ticks * sec_per_tick
                ))

        self.note_rects = note_rects
        self.notes_to_time_spans = notes_to_time_spans
        self.add(note_rects)

    def add_piano_sound(self):
        self.add_sound(
            midi_to_wav(self.mid_file),
            self.sound_file_time_offset
        )

    def scroll(self):
        piano = self.piano
        note_rects = self.note_rects
        notes_to_time_spans = self.notes_to_time_spans

        for key in piano:
            key.original_z = key.get_z()
            key.original_color = key[0].get_fill_color()

        piano.time = 0

        def update_piano(piano, dt):
            piano.time += dt
            for note, key in zip(piano_midi_range, piano):
                hit = False
                for start, end in notes_to_time_spans[note]:
                    if start - 1 / 60 < piano.time < end + 1 / 60:
                        hit = True
                if hit:
                    key.set_z(key.original_z - self.hit_depth)
                    key.set_fill(interpolate_color(
                        key[0].get_fill_color(), self.hit_color, 0.5
                    ))
                else:
                    key.set_z(key.original_z)
                    key.set_fill(key.original_color)

        piano.add_updater(update_piano)
        note_rects_start = note_rects.get_center().copy()
        note_rects.add_updater(lambda m: m.move_to(
            note_rects_start + self.dist_per_sec * self.time * DOWN
        ))
        black_rect = Rectangle(width=piano.get_width(), height=5)
        black_rect.set_fill(BLACK, 1)
        black_rect.set_stroke(width=0)
        black_rect.move_to(piano, UP)
        self.add(note_rects, black_rect, piano)

        self.wait(note_rects.get_height() / self.dist_per_sec + 3.0)


class STFTAlgorithmOnTrapped(AnimatedMidi):
    midi_file = "3-16-attempts/Help_Long_STFT.mid"
