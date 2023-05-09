import os
import re
import moviepy
from moviepy.editor import *

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
                       ".mov", ".mp4", ".avi", ".webm")


# Define the function to display the artist name and title
def display_artist_and_title(artist_name: str, title: str, duration: float, font_size: int, artist_font: str, title_font: str, bg_color: str, size: tuple):

    # Create a black clip for the artist name display
    artist_name_clip = TextClip(
        artist_name,
        fontsize=font_size, font=artist_font, color="white", align="center"
    ).set_duration(duration)

    # Create a black clip for the title display
    delay = 0.25
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
    # Create a black clip for the artist name display
    artist_name_clip = TextClip(
        artist_name,
        fontsize=font_size, font=font, color="white", align="center",
        bg_color=bg_color, size=size
    ).set_position("center").set_duration(duration).set_bg_color(bg_color)

    return artist_name_clip


def display_title(title: str, duration: float, font_size: int, font: str, bg_color: str, size: tuple):
    # Create a black clip for the title display
    title_clip = TextClip(
        title, fontsize=font_size, font=font, color="white", align="right",
        bg_color=bg_color, size=size
    ).set_position("right", -50).set_duration(duration).set_bg_color(bg_color)

    return title_clip


# Define the function to create a clip from a media file
def create_media_clip(media_path, media_duration=7, size=(1920, 1080)):
    # Determine if the media file is an image or video
    if media_path.lower().endswith((".jpg", ".jpeg", ".png", ".webp")):
        media_clip = ImageClip(media_path, duration=media_duration)
        media_clip = media_clip.set_duration(media_duration)
    elif media_path.lower().endswith((".mov", ".mp4", ".avi", ".webm")):
        media_clip = VideoFileClip(media_path)

    media_clip = resize(media_clip, size).set_position("center")
    return media_clip


def resize(clip, size=(1920, 1080), enlarge=True):

    if clip is VideoFileClip:
        # clip.w and clip.h are wrong and reversed
        clip_w = clip.h
        clip_h = clip.w
    else:
        clip_w = clip.w
        clip_h = clip.h

    # Calculate the aspect ratios of the clip and the screen
    clip_ratio = clip_w / clip_h
    screen_ratio = size[0] / size[1]
    
    # Determine whether to resize based on width or height
    if screen_ratio > clip_ratio:
        # Resize based on height
        new_h = size[1]
        new_w = int(new_h * clip_ratio)
    else:   
        # Resize based on width
        new_w = size[0]
        new_h = int(new_w / clip_ratio)
    
    # Resize the clip
    if enlarge and new_w > clip_w and new_h > clip_h:
        # enlarge to fit
        clip = clip.resize((new_w, new_h))
    elif new_w < clip_w or new_h < clip_h:
        # shrink to fit
        clip = clip.resize((new_w, new_h))

    # if clip.w > clip.h:
    #     if clip.w > size[0]:
    #         clip = clip.resize(width=size[0])
    # else:
    #     if clip.h > size[1]:
    #         clip = clip.resize(height=size[1])

    return clip


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
                        os.path.join(path, f), recursive=recursive, base_path=base_path))
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
    # Get the artist name final directory in the media path
    artist_name = os.path.basename(os.path.dirname(media_path))

    # convert _ to spaces
    artist_name = artist_name.replace("_", " ")

    # capitalize the first letter of each word
    artist_name = artist_name.title()

    return artist_name


def get_title(media_path):
    # Get the title from the media filename
    title = os.path.splitext(os.path.basename(media_path))[0]

    # remove ordering:
    # if the title starts with any number of digits and then underscore, remove those
    title = re.sub(r"^\d+_", "", title)

    # convert _ to spaces
    title = title.replace("_", " ")

    return title


# create a video from a list of media files
def create_video(media_list, video_size, bg_color, 
                 artist_font, title_font, font_size,
                 fade_duration, media_duration, title_duration,
                 output_settings="", output_file="output.mp4",
                 audio=True, 
                 base_path="",
                 promo_clip=None, promo_interval=300.0):
    if media_list == []:
        print("No media files found.")
        return

    print("Creating video from", len(media_list), "media files.")
    print("Video size:", video_size)
    print("Background color:", bg_color)
    print("Artist font:", artist_font)
    print("Title font:", title_font)
    print("Font size:", font_size)
    print("Fade duration:", fade_duration)
    print("Media duration:", media_duration)
    print("Title duration:", title_duration)
    print("Output settings:", output_settings)
    print("Output file:", output_file)
    print("Audio:", audio)
    print("Base path:", base_path)
    print("Promo clip:", promo_clip is not None)
    print("Promo interval:", promo_interval)

    time_since_promo = -1
    if promo_clip is not None:
        # resize the promo clip
        promo_clip = resize(promo_clip, size=video_size)
        # fade in and out
        promo_clip = fade_in_out(promo_clip, fade_duration)
        time_since_promo = promo_interval

    # Create a list of clips for each artist's works
    clips = []
    previous_artist = ""
    for media_path in media_list:
        # Get the artist name and title from the media filename
        artist_name = get_artist_name(media_path)
        title = get_title(media_path)

        if artist_name == "" or title == "":
            print("Skipping", media_path)
            if artist_name == "":
                print("Artist name not found.")
            if title == "":
                print("Title not found.")
            continue
        
        print("Adding clip for", artist_name, "-", title)

        # skip if no output file
        if output_file == "": continue

        if previous_artist == artist_name:
            # reduce time between clips
            media_duration_multiplier = 0.85
        else: # new artist
            media_duration_multiplier = 1.0

            # handle promo clip
            if time_since_promo >= 0 and time_since_promo >= promo_interval:
                clips.append(promo_clip)
                time_since_promo = 0

        intro_clip = display_artist_and_title(
            artist_name, title, title_duration * media_duration_multiplier, 
            font_size, artist_font, title_font, bg_color, video_size)

        # Create a clip for the media file
        media_clip = create_media_clip(
            os.path.join(base_path, media_path), media_duration, video_size)

        crossfade_duration = fade_duration * 2.0
        artist_clip = CompositeVideoClip([
            intro_clip.fx(
                vfx.fadein, fade_duration
            ),
            media_clip.set_start(title_duration * media_duration_multiplier - crossfade_duration)
            .crossfadein(crossfade_duration)
            .fx(
                vfx.fadeout, fade_duration
            )
        ])

        clips.append(artist_clip)
        previous_artist = artist_name
        time_since_promo += artist_clip.duration

    # Write the final video to a file
    if output_file != "":
        # Concatenate all the artist clips into one final video
        final_clip = concatenate_videoclips(clips)

        # prefer hevc codec for mp4 files
        codec = "libx264"
        if output_file.endswith(".mp4"):
            codec = "hevc"
        
        final_clip.write_videofile(
            output_file, fps=30, codec=codec, threads=4, audio=audio)
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
    print("Available colors:", sorted(TextClip.list('color')))


if __name__ == "__main__":
    # accept arguments from the command line
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "path_to_list", nargs="?", help="path to directory or text file with list of directories")
    parser.add_argument("--base_path", type=str, default="", help="base directory path for media files")
    parser.add_argument("--video_size", type=tuple,
                        default=default_video_size, help="size of final video")
    parser.add_argument("--title_duration", type=float,
                        default=default_title_duration, help="duration of title display")
    parser.add_argument("--media_duration", type=float,
                        default=default_media_duration, help="duration of media display")
    parser.add_argument("--fade_duration", type=float, default=default_fade_duration,
                        help="duration (sec) of fade in and fade out")
    parser.add_argument("--artist_font", type=str, default=default_font,
                        help="font for artist name")
    parser.add_argument("--title_font", type=str, default=default_font,
                        help="font for artwork title")
    parser.add_argument("--font_size", type=int, default=default_font_size,
                        help="font size for artist name and title displays")
    parser.add_argument("--bg_color", type=str, default=default_bg_color,
                        help="background color for artist name and title displays")
    parser.add_argument("--output_file", type=str,
                        default="", help="path to output file")
    parser.add_argument("--output_settings", type=str,
                        default="", help="path to output settings file")
    parser.add_argument("--no_audio", default=False,
                        action='store_true', help="remove audio from video")
    parser.add_argument("--promo_clip", type=str,
                        default="", help="path to promo clip that plays interspersed with media clips")
    parser.add_argument("--promo_interval", type=str,
                        default="", help="time to wait between promo clips")
    # info
    parser.add_argument("--version", action="version", version="%(prog)s 1.0")
    parser.add_argument("--info", action="store_true", help="print moviepy info and exit")
    
    args = parser.parse_args()

    if args.info:
        print_moviepy_info()
        parser.exit()

    # convert time string to seconds
    promo_interval = -1.0
    if args.promo_interval != "":
        promo_interval = time_string_to_seconds(args.promo_interval)

    # normalize paths, ensure ends with separator
    if args.base_path != "":
        args.base_path = os.path.normpath(args.base_path)
        args.base_path = args.base_path + os.sep

    # parse the list of media files
    if (args.path_to_list.endswith(".txt")):
        media_list = parse_list(args.path_to_list, base_path=args.base_path)
    else:
        if args.path_to_list == "":
            args.path_to_list = os.getcwd()
        args.path_to_list = os.path.normpath(args.path_to_list)
        media_list = get_all_files(args.path_to_list, recursive=True, base_path=args.base_path)
        # save settings to file named after the final directory
        filename = os.path.basename(args.path_to_list)
        args.output_settings = filename + ".txt"

    media_list = sorted(media_list)

    # handle promo clip
    promo_clip = None
    if args.promo_clip != "":
        args.promo_clip = os.path.join(args.base_path, os.path.normpath(args.promo_clip))
        promo_clip = create_media_clip(args.promo_clip, args.media_duration, args.video_size)
        if args.promo_interval == "":
            promo_interval = 5 * 60.0 # five minute default

    # create the video
    create_video(media_list,
                 video_size=args.video_size,
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
                 base_path=args.base_path,
                 promo_clip=promo_clip,
                 promo_interval=promo_interval)
