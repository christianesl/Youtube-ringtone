# YouTube Ringtone

Download audio from a YouTube video and create an enhanced, trimmed ringtone.
The script uses `yt-dlp` to download the audio, then `ffmpeg` to apply audio
enhancements and trim the result to a specified duration.

## Requirements

- Python 3
- [`yt-dlp`](https://github.com/yt-dlp/yt-dlp)
- [`ffmpeg`](https://ffmpeg.org/)

Both `yt-dlp` and `ffmpeg` must be available in your `PATH`.

For example, you can install `yt-dlp` with:

```bash
python3 -m pip install -U yt-dlp
```

Install `ffmpeg` using your operating system's package manager. For example,
on Debian/Ubuntu:

```bash
sudo apt install ffmpeg
```

## Usage

```text
python3 make_ringtone.py URL [--output FILE] [--duration SECONDS]
```

### Basic usage

This uses the default 17.3-second duration and creates
`ringtone_enhanced.ogg`:

```bash
python3 make_ringtone.py "https://www.youtube.com/watch?v=0B_TDuvTduY"
```

### Custom output and duration

Create a 25-second M4A ringtone:

```bash
python3 make_ringtone.py "https://www.youtube.com/watch?v=0B_TDuvTduY" \
  --output blues_ringtone.m4a \
  --duration 25
```

The short options `-o` and `-d` are also supported:

```bash
python3 make_ringtone.py "VIDEO_URL" -o ringtone.m4a -d 25
```

Run `python3 make_ringtone.py --help` to show the command-line options.

## Command-line options

| Option | Description | Default |
| --- | --- | --- |
| `url` | YouTube video URL | Required |
| `-o`, `--output` | Output filename | `ringtone_enhanced.ogg` |
| `-d`, `--duration` | Maximum ringtone duration in seconds | `17.3` |

The file extension determines the output format. `.ogg` and `.m4a` are
recommended, and `ffmpeg` must have a suitable encoder available for the
selected format.

## Audio processing

The script applies these `ffmpeg` filters:

- High-pass filter to remove low-frequency rumble below 110 Hz
- EQ boost around 3000 Hz for clearer smartphone playback
- Dynamic range compression for more consistent volume
- Limiting to -1 dB to prevent clipping
- A 0.8-second fade-out that ends at the requested duration

For durations shorter than 0.8 seconds, the fade starts at the beginning of
the audio. Playlist downloading is disabled, so the script processes only the
provided video.

## Implementation notes

- Uses argument lists with `subprocess.run()` instead of a shell command,
  which safely handles URL characters such as `?`, `&`, and `=`.
- Extracts the source audio as a temporary WAV file named
  `temp_ringtone_raw.wav`.
- Overwrites an existing output file.
- Removes the temporary WAV file automatically, including after download or
  conversion errors.
- Reports missing tools or external command failures to standard error and
  exits with status code 1.
