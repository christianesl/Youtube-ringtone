import argparse
import os
import subprocess
import sys


def create_ringtone(youtube_url: str, output_file: str, duration: float) -> None:
  temp_wav = "temp_ringtone_raw.wav"

  # 1. Extract raw WAV audio using yt-dlp
  yt_dlp_cmd = [
      "yt-dlp",
      "-x",
      "--audio-format",
      "wav",
      "--no-playlist",
      "-o",
      temp_wav,
      youtube_url,
  ]

  # 2. Enhance audio for smartphone speakers & apply fade-out using ffmpeg
  fade_start = max(0.0, duration - 0.8)
  audio_filters = (
      "highpass=f=110,"
      "equalizer=f=3000:width_type=q:width=1.5:g=3,"
      "acompressor=threshold=-18dB:ratio=3:attack=10:release=100,"
      "alimiter=limit=-1dB,"
      f"afade=t=out:st={fade_start}:d=0.8"
  )

  ffmpeg_cmd = [
      "ffmpeg",
      "-y",  # Overwrite output if it exists
      "-i",
      temp_wav,
      "-af",
      audio_filters,
      "-to",
      str(duration),
      output_file,
  ]

  try:
    print(f"Downloading audio from: {youtube_url}")
    subprocess.run(yt_dlp_cmd, check=True)

    print(f"Enhancing and trimming audio to {duration}s...")
    subprocess.run(ffmpeg_cmd, check=True)

    print(f"\nSuccess! Ringtone saved as: {output_file}")

  except subprocess.CalledProcessError as e:
    print(f"\nError running external tool: {e}", file=sys.stderr)
    sys.exit(1)
  except FileNotFoundError as e:
    print(
        "\nMissing dependency: Make sure both 'yt-dlp' and 'ffmpeg' are"
        f" installed and in your PATH.\nDetails: {e}",
        file=sys.stderr,
    )
    sys.exit(1)
  finally:
    # Clean up the intermediate WAV file
    if os.path.exists(temp_wav):
      os.remove(temp_wav)


if __name__ == "__main__":
  parser = argparse.ArgumentParser(
      description=(
          "Download a YouTube audio clip and enhance it as a phone ringtone."
      )
  )
  parser.add_argument("url", help="YouTube video URL")
  parser.add_argument(
      "-o",
      "--output",
      default="ringtone_enhanced.ogg",
      help="Output filename (.ogg or .m4a recommended, default: ringtone_enhanced.ogg)",
  )
  parser.add_argument(
      "-d",
      "--duration",
      type=float,
      default=17.3,
      help="Max duration in seconds before fade-out completes (default: 17.3)",
  )

  args = parser.parse_args()
  create_ringtone(args.url, args.output, args.duration)