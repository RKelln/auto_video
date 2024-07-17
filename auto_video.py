import os
import re
import moviepy
from moviepy.editor import *

VERSION = "1.1"

# Define default values for the command line arguments

# Define the path to the text file with the list of directories
path_to_list = "artists.txt"

# Define the durations
default_title_duration = 4
default_fade_duration = 0.5
default_media_duration = 14

# Define the size of the final video
default_video_size = (1920, 1080)

# Define the background color for the artist name and title displays
default_bg_color = "black"

# Define the font and font size for the artist name and title displays
default_font = "Arial"
default_font_size = 50

# Accepted file extensions
accepted_extensions = (".jpg", ".jpeg", ".png", ".webp",
                       ".mov", ".mp4", ".avi", ".webm", ".mkv")


# Define the function to display the artist name and title
def display_artist_and_title(artist_name: str, title: str, duration: float, font_size: int, artist_font: str, title_font: str, bg_color: str, size: tuple):

    # Create a black clip for the artist name display
    artist_name_clip = TextClip(
        artist_name,
        fontsize=font_size, font=artist_font, color="white", align="center"
    ).set_duration(duration)

    # Create a black clip for the title display
    delay = 0.25 if duration > 4.0 else 0.0
    title_clip = TextClip(
        title,
        fontsize=font_size, font=title_font, color="white", align="center",
        size=size
    ).set_duration(duration - delay)

    # Concatenate the artist name and title clips
    display_clip = CompositeVideoClip([
        artist_name_clip.set_position("center"), 
        title_clip.set_start(delay).set_position(("center", font_size * 2.0))], # relative to artist_name_clip
        size=size)

    return display_clip


# Define the function to display the artist name and title
def display_artist(artist_name: str, duration: str, font_size: int, font: str, bg_color: str, size: tuple):
    # Create a clip for the artist name display
    artist_name_clip = TextClip(
        artist_name,
        fontsize=font_size, font=font, color="white", align="center",
        bg_color=bg_color, size=size
    ).set_position("center").set_duration(duration).set_bg_color(bg_color)

    return artist_name_clip


def display_title(title: str, duration: float, font_size: int, font: str, bg_color: str, size: tuple):
    # Create a clip for the title display
    title_clip = TextClip(
        title, fontsize=font_size, font=font, color="white", align="right",
        bg_color=bg_color, size=size
    ).set_position("right", -50).set_duration(duration).set_bg_color(bg_color)

    return title_clip


# Define the function to create a clip from a media file
def create_media_clip(media_path, media_duration=7, size=(1920, 1080), trim=False):
    # Determine if the media file is an image or video
    if media_path.lower().endswith((".jpg", ".jpeg", ".png", ".webp")):
        media_clip = ImageClip(media_path, duration=media_duration)
        media_clip.set_duration(media_duration)
    elif media_path.lower().endswith((".mov", ".mp4", ".avi", ".webm")):
        media_clip = VideoFileClip(media_path)
        if trim: # only display start of video
            media_clip = media_clip.subclip(0, media_duration)
    else:
        raise ValueError("Unsupported file type: " + media_path)
    
    if media_clip.size != size:
        print("Resizing from", media_clip.size, "to", size)
        clip_ratio = media_clip.w / media_clip.h
        if clip_ratio > 1:
            media_clip = media_clip.resize(width=size[0])
        else:
            media_clip = media_clip.resize(height=size[1])

    return media_clip


def fade_in_out(media_clip, fade_duration=1):
    # Create a clip that fades in, displays for media_duration seconds, and fades out
    media_clip = media_clip.fx(
        vfx.fadein, fade_duration
    ).fx(
        vfx.fadeout, fade_duration
    )
    return media_clip


def get_all_files(path, recursive=False, base_path=""):
    files = []

    if base_path == "" and not path.startswith(base_path):
        path = os.path.join(base_path, path)

    if os.path.isdir(path):
        # Get the list of media files in the directory
        media_files = os.listdir(path)

        # Get the full path to each media file
        for f in media_files:
            if os.path.isdir(os.path.join(path, f)):
                # ignore if starts with _ or .
                if f.startswith("_") or f.startswith("."):
                    continue
                if recursive:
                    files.extend(get_all_files(
                        os.path.join(path, f), recursive=recursive))
            elif f.lower().endswith(accepted_extensions):
                files.append(os.path.join(path, f))
    elif path.lower().endswith(accepted_extensions):
        # Add the file to the media_list
        files.append(path)

    # remove base_path from the start of file paths
    if base_path != "":
        files = [f.removeprefix(base_path) for f in files]

    return files


def parse_list(path_to_list, base_path=""):
    # Create an empty list to store the media files
    media_list = []

    # Open the text file with the list of directories
    with open(path_to_list, "r") as f:
        # Read each line in the text file
        for line in f:
            # Remove the newline character
            line = line.strip()

            # ignore comments and blank lines
            if line.startswith("#") or line == "":
                continue

            media_list.extend(get_all_files(line, base_path=base_path))

    return media_list


def get_artist_name(media_path):
    # Get the artist name first directory in the media path
    artist_name = os.path.dirname(media_path).split(os.sep)[0]
    
    # convert _ to spaces
    artist_name = artist_name.replace("_", " ")

    # capitalize the first letter of each word
    artist_name = artist_name.title()

    return artist_name


def get_title(media_path, expected_number=0):
    # Get the title from the media filename
    title = os.path.splitext(os.path.basename(media_path))[0]

    # remove ordering:
    # if the title starts with any number of digits and then underscore, remove those
    # if expected number > 0 then only remove if the number is not the expected number (proceeded by any number of zeros)
    if expected_number > 0:
        title = re.sub(r"^0*"+str(expected_number)+"_", "", title)
    else:
        title = re.sub(r"^\d+_", "", title)

    # convert _ to spaces
    title = title.replace("_", " ")

    return title


# create a video from a list of media files
def create_video(media_list, video_size, fps,
                 bg_color, artist_font, title_font, font_size,
                 fade_duration, media_duration, title_duration,
                 output_settings="", output_file="output.mp4",
                 audio=True, codec = "libx264",
                 base_path="",
                 promo_clip=None, promo_interval=300.0,
                 titles=True, dryrun=False, verbose=False):
    if media_list == []:
        print("No media files found.")
        return

    if verbose:
        print("Creating video from", len(media_list), "media files.")
        print("Video size:", video_size)
        print("Codec:", codec)
        print("FPS:", fps)
        print("Background color:", bg_color)
        print("Font size:", font_size)
        print("Fade duration:", fade_duration)
        print("Media duration:", media_duration)
        if titles:
            print("Artist font:", artist_font)
            print("Title font:", title_font)
            print("Title duration:", title_duration)
        else:
            print("No titles")
        print("Output settings:", output_settings)
        print("Output file:", output_file)
        print("Audio:", audio)
        print("Base path:", base_path)
        print("Promo clip:", promo_clip is not None)
        print("Promo interval:", promo_interval)

    time_since_promo = -1
    if promo_clip is not None and promo_clip != "":
        if isinstance(promo_clip) == str:
            promo_clip_path = os.path.join(base_path, promo_clip)
            promo_clip = create_media_clip(
            media_path=promo_clip_path, 
            media_duration=media_duration, 
            size=video_size, 
            trim=dryrun)
        # fade in and out
        promo_clip = fade_in_out(promo_clip, fade_duration)
        time_since_promo = promo_interval # set to play immediately
    else:
        promo_clip = None

    # Create a list of clips for each artist's works
    clips = []
    artist_name = ""
    previous_artist = ""
    media_list = sorted(media_list) # sort media files
    expected_title_number = 1
    for media_path in media_list:
        if titles:
            # Get the artist name and title from the media filename
            artist_name = get_artist_name(media_path)
            # reset expected title number if new artist
            if artist_name != previous_artist:
                expected_title_number = 1
            
            title = get_title(media_path, expected_number = expected_title_number)

            if artist_name == "":
                print("ERROR: Artist name not found: ", media_path)
                continue
            if title == "":
                print("Warning: Title not found: ", media_path)
        
            if verbose:
                print("Adding clip for", artist_name, "-", title)
            expected_title_number += 1

        # skip if no output file
        if output_file == "": continue

        if titles and previous_artist == artist_name:
            # reduce time between clips
            media_duration_multiplier = 0.85
        else: # new artist or no artist
            if titles:
                media_duration_multiplier = 1.0

            # handle promo clip
            if time_since_promo >= 0 and time_since_promo >= promo_interval:
                clips.append(promo_clip)
                time_since_promo = 0

        if titles and title != "" and title_duration > 0:
            intro_clip = display_artist_and_title(
                artist_name, title, title_duration * media_duration_multiplier, 
                font_size, artist_font, title_font, bg_color, video_size)

        # Create a clip for the media file
        media_clip = create_media_clip(
            media_path=os.path.join(base_path, media_path), 
            media_duration=media_duration, 
            size=video_size, 
            trim=dryrun)

        if titles and title != "" and title_duration > 0:
            # create a composite video clip with titles crossfading to art
            crossfade_duration = fade_duration * 2.0
            artist_clip = CompositeVideoClip([
                intro_clip.fx(
                    vfx.fadein, fade_duration
                ),
                media_clip.set_start(title_duration * media_duration_multiplier - crossfade_duration)
                .crossfadein(crossfade_duration)
                .set_position("center")
            ],
            size=video_size)
        else:
            artist_clip = media_clip

        clips.append(artist_clip)
        previous_artist = artist_name
        if promo_clip is not None:
            time_since_promo += artist_clip.duration

    #print(clips)

    # Write the final video to a file
    if output_file != "":
        clips = [clip.crossfadein(fade_duration) for clip in clips]
        final_clip = concatenate_videoclips(clips, method="compose", padding = -fade_duration)

        # if mp4 then fast start
        ffmpeg_params=[]
        if output_file.endswith(".mp4"):
            ffmpeg_params=["-movflags", "faststart"]

        final_clip.write_videofile(
            output_file, fps=fps, codec=codec, audio=audio, threads=4,
            ffmpeg_params=ffmpeg_params)
        final_clip.close()

    if output_settings != "":
        # write media_list to file
        with open(output_settings, "w") as f:
            for media_path in media_list:
                f.write(media_path + "\n")


# parse a string time in the form of 00:00:00.000 to seconds
def time_string_to_seconds(time_str : str) -> float:
    time_str = time_str.strip()
    if time_str == "":
            return 0.0

    time_parts = time_str.split(':')
    if len(time_parts) == 0:
        return float(time_str)
    
    h = m = s = s_ms = 0.0
    if len(time_parts) == 1:
        s_ms = float(time_parts[0])
    elif len(time_parts) == 2:
        m, s_ms = map(float, time_parts)
    else:
        h, m, s_ms = map(float, time_parts)
    s, ms = map(float, f"{s_ms:0.03f}".split('.'))
    if s < 0:
        raise RuntimeError(f"Invalid time seconds: {time_str}")
    if m >= 60.0 or m < 0:
        raise RuntimeError(f"Invalid time minutes: {time_str}")
    if h < 0:
        raise RuntimeError(f"Invalid time hours: {time_str}")
    return 3600*h + 60*m + s + ms/1000.0


def print_moviepy_info():
    print("MoviePy version:", moviepy.__version__)
    print("Installed fonts:", sorted(TextClip.list('font')))
    print("Available colors:", sorted(str(b) for b in TextClip.list('color')))


if __name__ == "__main__":
    # accept arguments from the command line
    # accept parameters from a text file using @text_file: 
    # https://docs.python.org/3/library/argparse.html#fromfile-prefix-chars
    import argparse
    parser = argparse.ArgumentParser(fromfile_prefix_chars="@")
    parser.add_argument(
        "path_to_list", nargs="?", help="path to directory or text file with list of directories")
    parser.add_argument("--base_path", "--base-path", type=str, default="", help="base directory path for media files")
    parser.add_argument("--video_size", "--video-size", type=str,
                        default="1920x1080", help="size of final video")
    parser.add_argument("--codec", type=str, default="libx264", help="codec for final video")
    parser.add_argument("--fps", type=float, default=30, help="frames per second for final video")
    parser.add_argument("--title_duration", "--title-duration", type=float,
                        default=default_title_duration, help="duration of title display")
    parser.add_argument("--media_duration", "--media-duration", type=float,
                        default=default_media_duration, help="duration of media display")
    parser.add_argument("--fade_duration", "--fade-duration", type=float, default=default_fade_duration,
                        help="duration (sec) of fade in and fade out")
    parser.add_argument("--artist_font", "--artist-font", type=str, default=default_font,
                        help="font for artist name")
    parser.add_argument("--title_font", "--title-font", type=str, default=default_font,
                        help="font for artwork title")
    parser.add_argument("--font_size", "--font-size",type=int, default=default_font_size,
                        help="font size for artist name and title displays")
    parser.add_argument("--bg_color", "--bg-color", type=str, default=default_bg_color,
                        help="background color for artist name and title displays")
    parser.add_argument("--output_file", "--output-file",type=str,
                        default="", help="path to output file")
    parser.add_argument("--output_settings", "--output-settings",type=str,
                        default="", help="path to output settings file")
    parser.add_argument("--no_audio", "--no-audio", default=False,
                        action='store_true', help="remove audio from video")
    parser.add_argument("--promo_clip", "--promo-clip",type=str,
                        default="", help="path to promo clip that plays interspersed with media clips")
    parser.add_argument("--promo_interval", "--promo-interval",type=str,
                        default="", help="time to wait between promo clips")
    parser.add_argument("--no_titles", "--no-titles",default=False, 
                        action='store_true', help="Do not display artist name and title")
    parser.add_argument("--dry_run", "--dry-run", default=False, 
                        action='store_true', help="Create a test video with single frame per clip")
    parser.add_argument("--verbose", default=False,
                        action='store_true', help="Print extra information")
    # info
    parser.add_argument("--version", action="version", version="%(prog)s " + VERSION)
    parser.add_argument("--info", action="store_true", help="print moviepy info and exit")
    
    args = parser.parse_args()

    if args.info:
        print_moviepy_info()
        parser.exit()

    # convert time string to seconds
    promo_interval = -1.0
    if args.promo_interval != "":
        promo_interval = time_string_to_seconds(args.promo_interval)

    # convert video size to tuple
    video_size = default_video_size
    if args.video_size != "":
        video_size = tuple(map(int, args.video_size.split('x')))

    # normalize paths, ensure ends with separator
    if args.base_path != "":
        args.base_path = os.path.normpath(args.base_path)
        args.base_path = args.base_path + os.sep

    # check bg_color is valid
    if args.bg_color != "":
        if bytes(args.bg_color, "utf8") not in TextClip.list('color'):
            print("Invalid background color:", args.bg_color)
            print("Available colors:", sorted(str(b) for b in TextClip.list('color')))
            parser.exit()

    # parse the list of media files
    if (args.path_to_list.endswith(".txt")):
        media_list = parse_list(args.path_to_list, base_path=args.base_path)
    else:
        if args.path_to_list == "":
            args.path_to_list = os.getcwd()
        args.path_to_list = os.path.normpath(args.path_to_list)
        media_list = get_all_files(args.path_to_list, recursive=True, base_path=args.base_path)
        media_list = sorted(media_list)
        # save settings to file named after the final directory
        filename = os.path.basename(args.path_to_list)
        if args.output_settings == "":
            args.output_settings = filename + ".txt"

    # handle promo clip
    if args.promo_clip != "" and args.promo_interval == "":
        args.promo_interval = 5 * 60.0 # five minute default

    # minimize durations for dryrun
    if args.dry_run:
        args.title_duration = 1.0
        args.media_duration = 0.5
        args.fade_duration = 0.1
        args.verbose = True
        args.no_audio = True

    # create the video
    create_video(media_list,
                 video_size=video_size,
                 fps=args.fps,
                 bg_color=args.bg_color,
                 artist_font=args.artist_font,
                 title_font=args.title_font,
                 font_size=args.font_size,
                 fade_duration=args.fade_duration,
                 title_duration=args.title_duration,
                 media_duration=args.media_duration,
                 output_file=args.output_file,
                 output_settings=args.output_settings,
                 audio=(not args.no_audio),
                 codec=args.codec,
                 base_path=args.base_path,
                 promo_clip=args.promo_clip,
                 promo_interval=args.promo_interval,
                 titles=(not args.no_titles),
                 dryrun=args.dry_run,
                 verbose=args.verbose)
