#!/usr/bin/env python3
"""Remove reviewed time ranges from a mono or stereo 16-bit PCM WAV."""

import argparse
from array import array
import json
import math
from pathlib import Path
import shutil
from tempfile import TemporaryFile
import wave


def retained_spans(cuts, rate, total_frames):
    if not isinstance(cuts, list) or not cuts:
        raise ValueError("Expected a nonempty JSON array of [start, end] ranges in seconds")

    spans = []
    cursor = 0
    for index, cut in enumerate(cuts, 1):
        if not isinstance(cut, list) or len(cut) != 2 or not all(
            type(value) in (int, float) and math.isfinite(value) and value >= 0 for value in cut
        ):
            raise ValueError(f"Cut {index} must contain two finite, nonnegative times")
        start, end = (round(value * rate) for value in cut)
        if not cursor <= start < end <= total_frames:
            raise ValueError(f"Cut {index} is out of bounds, empty, out of order, or overlaps a previous cut")
        if cursor < start:
            spans.append((cursor, start))
        cursor = end

    if cursor < total_frames:
        spans.append((cursor, total_frames))
    if not spans:
        raise ValueError("The cuts remove the entire recording")
    return spans


def read_frames(source, count):
    data = source.readframes(count)
    if len(data) != count * source.getnchannels() * source.getsampwidth():
        raise ValueError("The WAV ended before its declared frame count")
    return data


def fade(data, channels, fade_in):
    samples = array("h")
    samples.frombytes(data)
    frames = len(samples) // channels
    denominator = max(1, frames - 1)
    for frame in range(frames):
        numerator = frame if fade_in else frames - 1 - frame
        gain = numerator / denominator
        for channel in range(channels):
            index = frame * channels + channel
            samples[index] = round(samples[index] * gain)
    return samples.tobytes()


def render(source, destination, spans, fade_frames):
    channels = source.getnchannels()
    destination.setnchannels(channels)
    destination.setsampwidth(source.getsampwidth())
    destination.setframerate(source.getframerate())

    for index, (start, end) in enumerate(spans):
        source.setpos(start)
        length = end - start
        has_left_join = index > 0
        has_right_join = index + 1 < len(spans)
        # Share short spans between the two fades so the windows cannot overlap.
        window = min(fade_frames, length // max(1, has_left_join + has_right_join))
        fade_in = window if has_left_join else 0
        fade_out = window if has_right_join else 0

        if fade_in:
            destination.writeframesraw(fade(read_frames(source, fade_in), channels, fade_in=True))
        remaining = length - fade_in - fade_out
        while remaining:
            count = min(remaining, 65_536)
            destination.writeframesraw(read_frames(source, count))
            remaining -= count
        if fade_out:
            destination.writeframesraw(fade(read_frames(source, fade_out), channels, fade_in=False))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="Input PCM WAV")
    parser.add_argument("cuts", type=Path, help="JSON array of [start, end] pairs in source seconds")
    parser.add_argument("output", type=Path, help="Path for a new WAV file")
    parser.add_argument("--fade-ms", type=float, default=6, help="Fade per side of each join (default: 6 ms)")
    args = parser.parse_args()

    try:
        if not math.isfinite(args.fade_ms) or args.fade_ms < 0:
            raise ValueError("Fade duration must be finite and nonnegative")
        if args.output.suffix.lower() != ".wav":
            raise ValueError("Output path must end in .wav")
        if args.output.exists() or args.output.is_symlink():
            raise FileExistsError(f"Output already exists: {args.output}")
        cuts = json.loads(args.cuts.read_text(encoding="utf-8"))

        with wave.open(str(args.input), "rb") as source, TemporaryFile() as staged:
            if source.getsampwidth() != 2 or source.getnchannels() not in (1, 2):
                raise ValueError("Input must be a mono or stereo 16-bit PCM WAV")
            rate = source.getframerate()
            total_frames = source.getnframes()
            spans = retained_spans(cuts, rate, total_frames)
            fade_frames = round(args.fade_ms * rate / 1000)
            with wave.open(staged, "wb") as destination:
                render(source, destination, spans, fade_frames)
            staged.seek(0)

            output = args.output.open("xb")
            try:
                with output:
                    shutil.copyfileobj(staged, output)
            except BaseException:
                args.output.unlink(missing_ok=True)
                raise
    except (EOFError, OSError, OverflowError, ValueError, wave.Error) as error:
        parser.exit(1, f"{parser.prog}: {error}\n")

    kept = sum(end - start for start, end in spans)
    print(f"Removed {len(cuts)} ranges: {total_frames / rate:.3f} s -> {kept / rate:.3f} s")


if __name__ == "__main__":
    main()
