# Auto video

A very simple python script that can create a video from a structure of folders and/or text file containing a list of media. Each image or video incorporated is preceded by a title containing the artist/author and the title of the work. Intended for use for creating looping videos of art for exhibitions.

## Install

```
$ conda create --prefix env/
$ conda activate env/
$ pip install moviepy
```

On Linux `moviepy` uses `imagemagick` PDF to create text and that has a security issue so the disabling of that has to be removed:

```
$ identify -list policy
```
the first line should tell you where your policy.xml file is located. My policy.xml file is located at `/etc/ImageMagick-6/policy.xml`

open that file, and goto to the end and comment out (or remove the line that reads)

```svg
<policy domain="path" rights="none" pattern="@*" />
```

since this is xml, you can comment out this line by appending the line with `<!--` and ending it with `-->`


# Usage

This is designed to work with well-named file structures, for example:

- Works
  - Artist_Name_1
    - Title_of_the_Work_(2023).png
    - Title_of_work_(2021).png
  - Artist Name 2
    - 01_Order_by_Number_not_title_(2023).jpg
    - 02_Another_title_(2023).mp4
    - _ignore_files_starting_with_underscores in the automatic list generation.jpg

Underscores are converted to spaces in the auto-titling. File extensions are removed as are numbers preceding the title.


## Running:

```
$ python3 auto_video.py --base_path ../works --output_settings all_works.txt ../works/
```

Then you can edit that `all_works.txt` file to curate the list (removing works and ordering) and then run:

```
$ python3 auto_video.py --base_path ../works --output_file video.mp4 all_works.txt
```

It can be helpful to set up a file (e.g. `default_args.txt`) with all the consistent settings between videos:
```
--artist_font
Lato-Bold
--title_font
Lato-LightItalic
--fade_duration
0.5
--title_duration
4.0
--media_duration
14.0
--video_size
1920x1080
--base_path
../works
```

Which can be included like so:
```
$ python3 auto_video.py --base_path ../works --output_file video.mp4 @default_args.txt all_works.txt
```

## Text file format

Media will be appended to the video in order specified in the text file:

```
Artist_Name_1/Work Title1 (YEAR).jpg
Artist_Name_1/Work_Title2_(YEAR).jpg
Artist Name 2/Work Title1 (YEAR).mp4
```

You can do series of works by numbering the works and having the first work of the series be titles and the rest untitled, like so:

```
Artist_Name/001_Series_Title_(YEAR).webp
Artist_Name/002_.webp
Artist_Name/003_.webp
Artist_Name/004_Series_Title_2_(YEAR).webp
Artist_Name/005_.webp
Artist_Name/006_.mp4
```


# Options

```
usage: auto_video.py [-h] [--base_path BASE_PATH] 
                     [--video_size VIDEO_SIZE] [--codec CODEC] [--fps FPS]
                     [--title_duration TITLE_DURATION]
                     [--media_duration MEDIA_DURATION] 
                     [--fade_duration FADE_DURATION]
                     [--artist_font ARTIST_FONT] [--title_font TITLE_FONT]
                     [--font_size FONT_SIZE] [--bg_color BG_COLOR] 
                     [--output_file OUTPUT_FILE] [--output_settings OUTPUT_SETTINGS]
                     [--no_audio]
                     [--promo_clip PROMO_CLIP] [--promo_interval PROMO_INTERVAL]
                     [--no_titles] [--dry_run] [--verbose] [--version] [--info]
                     [path_to_list]

positional arguments:
  path_to_list          path to directory or text file with list of directories

options:
  -h, --help            show this help message and exit
  --base_path BASE_PATH, --base-path BASE_PATH
                        base directory path for media files
  --video_size VIDEO_SIZE, --video-size VIDEO_SIZE
                        size of final video
  --codec CODEC         codec for final video
  --fps FPS             frames per second for final video
  --title_duration TITLE_DURATION, --title-duration TITLE_DURATION
                        duration of title display
  --media_duration MEDIA_DURATION, --media-duration MEDIA_DURATION
                        duration of media display
  --fade_duration FADE_DURATION, --fade-duration FADE_DURATION
                        duration (sec) of fade in and fade out
  --artist_font ARTIST_FONT, --artist-font ARTIST_FONT
                        font for artist name
  --title_font TITLE_FONT, --title-font TITLE_FONT
                        font for artwork title
  --font_size FONT_SIZE, --font-size FONT_SIZE
                        font size for artist name and title displays
  --bg_color BG_COLOR, --bg-color BG_COLOR
                        background color for artist name and title displays
  --output_file OUTPUT_FILE, --output-file OUTPUT_FILE
                        path to output file
  --output_settings OUTPUT_SETTINGS, --output-settings OUTPUT_SETTINGS
                        path to output settings file
  --no_audio, --no-audio
                        remove audio from video
  --promo_clip PROMO_CLIP, --promo-clip PROMO_CLIP
                        path to promo clip that plays interspersed with media clips
  --promo_interval PROMO_INTERVAL, --promo-interval PROMO_INTERVAL
                        time to wait between promo clips
  --no_titles, --no-titles
                        Do not display artist name and title
  --dry_run, --dry-run  Create a test video with single frame per clip
  --verbose             Print extra information
  --version             show program's version number and exit
  --info                print moviepy info and exit
```

Note that times specified in the arguments can be time strings in the form of 00:00:00.000 or just a float value in seconds.

### Promo image/video

You can add a repeating splash/promo image/video interspersed into the video that will repeat after at least PROMO_INTERVAL (but only between different artists).