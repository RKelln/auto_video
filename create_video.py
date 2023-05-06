import os
import random
from moviepy.editor import *

# Define default values for the command line arguments

# Define the path to the text file with the list of directories
path_to_list = "artists.txt"

# Define the path to the output file
output_file = "output.mp4"

# Define the duration of the artist name and title displays
artist_name_duration = 5
title_duration = 7

# Define the size of the final video
video_size = (1920, 1080)

# Define the background color for the artist name and title displays
bg_color = (0, 0, 0)

# Define the font and font size for the artist name and title displays
font = "Arial"
font_size = 50

# Define the duration of the fade in and fade out and image duration
fade_duration = 1
media_duration = 7


# Define the function to display the artist name and title
def display_artist_and_title(artist_name, title, title_duration, font_size, font, bg_color):
    # Create a black clip for the artist name display
    artist_name_clip = TextClip(
        artist_name, fontsize=font_size, font=font, color="white", align="center"
    ).set_position("center").set_duration(artist_name_duration).set_bg_color(bg_color)
    
    # Create a black clip for the title display
    title_clip = TextClip(
        title, fontsize=font_size, font=font, color="white", align="center"
    ).set_position("center", 0.25).set_duration(title_duration).set_bg_color(bg_color)

    # Concatenate the artist name and title clips
    display_clip = CompositeVideoClip([artist_name_clip, title_clip])
    
    return display_clip


# Define the function to display the artist name and title
def display_artist(artist_name, artist_name_duration, font_size, font, bg_color):
    # Create a black clip for the artist name display
    artist_name_clip = TextClip(
        artist_name, fontsize=font_size, font=font, color="white", align="center"
    ).set_position("center").set_duration(artist_name_duration).set_bg_color(bg_color)
    
    return display_clip


def display_title(title, title_duration, font_size, font, bg_color):
    # Create a black clip for the title display
    title_clip = TextClip(
        title, fontsize=font_size, font=font, color="white", align="right"
    ).set_position("right", -50).set_duration(title_duration).set_bg_color(bg_color)
    
    return title_clip


# Define the function to create a clip from a media file
def create_media_clip(media_path, fade_duration=1, media_duration=7):
    # Determine if the media file is an image or video
    if media_path.lower().endswith((".jpg", ".jpeg", ".png", ".gif", ".webp")):
        media_clip = ImageClip(media_path)
    else:
        media_clip = VideoFileClip(media_path)
        
    # Create a clip that fades in, displays for media_duration seconds, and fades out
    media_clip = media_clip.fx(
        vfx.fadein, fade_duration
    ).set_duration(media_duration).fx(
        vfx.fadeout, fade_duration
    )
    
    return media_clip


def parse_list(path_to_list):
    # Create an empty list to store the media files
    media_list = []
    
    # Open the text file with the list of directories
    with open(path_to_list, "r") as f:
        # Read each line in the text file
        for line in f:
            # Remove the newline character
            line = line.strip()
            
            # Check if the line is a directory
            if os.path.isdir(line):
                # Get the list of media files in the directory
                media_files = os.listdir(line)
                
                # Get the full path to each media file
                media_files = [os.path.join(line, f) for f in media_files]
                
                # Add the list of media files to the media_list
                media_list.extend(media_files)
            else:
                # Add the file to the media_list
                media_list.append(line)
    
    return media_list


def get_artist_name(media_path):
    # Get the artist name from the media filename
    artist_name = os.path.basename(os.path.dirname(media_path))
    
    return artist_name

def get_title(media_path):
    # Get the title from the media filename
    title = os.path.splitext(os.path.basename(media_path))[0]
    
    return title


# create a video from a list of media files
def create_video(media_list, video_size, bg_color, font, font_size, title_pos, fade_duration, media_duration):

    # Create a list of clips for each artist's works
    clips = []
    current_artist = None
    for media_path, next_media_path in zip(media_list, media_list[1:]):
        # Get the artist name and title from the media filename
        artist_name = get_artist_name(media_path)
        if artist_name != current_artist:
            # if the current artist is not None, then we need to complete the previous artist
            if current_artist is not None:
                artist_clip = concatenate_videoclips([intro_clip, media_clip])
                artist_clips.append(artist_clip)

            # start a new artist
            current_artist = artist_name

            # if the next media file is from a different artist, create a clip for the artist and title
            if next_media_path is not None and artist_name != get_artist_name(next_media_path):
                title = get_title(media_path)
                intro_clip = display_artist_and_title(artist_name, title, title_duration, font_size, font, bg_color)
                media_clip = create_media_clip(media_path)
                
            else:
                # Create a clip for the artist name display, they have multiple works coming
                display_clip = display_artist(artist_name, artist_name_duration, font_size, font, bg_color)
                
        title = os.path.splitext(os.path.basename(media_path))[0]
        title_clip = display_title(title, title_duration, font_size, font, bg_color)

        # Create a clip for the media file
        media_clip = create_media_clip(media_path)
        
        
        # Concatenate the display clip and media clip
        artist_clip = concatenate_videoclips([display_clip, media_clip])
        
        artist_clips.append(artist_clip)

    # Concatenate all the artist clips into one final video
    final_clip = concatenate_videoclips(artist_clips)

    #Write the final video to a file
    final_clip.write_videofile("output.mp4", fps=30, codec="libx264")

if __name__ == "__main__":
    # accept arguments from the command line
    import argparse
    parser = argparse.ArgumentParser()  
    parser.add_argument("path_to_list", help="path to directory or text file with list of directories")
    parser.add_argument("--artist_name_duration", type=float, default=artist_name_duration, help="duration of artist name display")
    parser.add_argument("--title_duration", type=float, default=title_duration, help="duration of title display")
    parser.add_argument("--video_size", type=tuple, default=video_size, help="size of final video")
    parser.add_argument("--bg_color", type=tuple, default=bg_color, help="background color for artist name and title displays")
    parser.add_argument("--font", type=str, default=font, help="font for artist name and title displays")
    parser.add_argument("--font_size", type=int, default=font_size, help="font size for artist name and title displays")
    parser.add_argument("--fade_duration", type=float, default=fade_duration, help="duration (sec) of fade in and fade out")
    parser.add_argument("--media_duration", type=float, default=media_duration, help="duration of media display")
    parser.add_argument("--output_file", type=str, default=output_file, help="path to output file")
    parser.add_argument("--output_settings", type=str, default=output_file, help="path to output file")
    args = parser.parse_args()

    # parse the list of media files
    if (args.path_to_list.endswith(".txt")):
        media_list = parse_list(args.path_to_list)
    else:
        # add all sub-directories
        media_list = []
        for root, dirs, files in os.walk(args.path_to_list):
            for name in dirs:
                media_list.append(os.path.join(root, name))

    print(media_list)

    # create the video
    #create_video(media_list, args.video_size, args,bg_color, args.font, args.font_size, args.title_pos, args.fade_duration, args.media_duration)
