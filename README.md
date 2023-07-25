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
$ python3 create_video.py --base_path ../works --output_settings all_works.txt ../works/
```

Then you can edit that `all_works.txt` file to curate the list (removing works and ordering) and then run:

```
$ python3 create_video.py --base_path ../works --output_file video.mp4 all_works.txt
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
$ python3 create_video.py --base_path ../works --output_file video.mp4 @default_args.txt all_works.txt
```

## Text file format

Media wil lbe appended to the video in order specified in the text file:

```
Artist_Name_1/Work Title1 (YEAR).jpg
Artist_Name_1/Work_Title2_(YEAR).jpg
Artist Name 2/Work Title1 (YEAR).mp4
```

# Options

```
usage: auto_video.py [-h] [--base_path BASE_PATH] [--video_size VIDEO_SIZE]
                     [--codec CODEC] [--title_duration TITLE_DURATION]
                     [--media_duration MEDIA_DURATION]
                     [--fade_duration FADE_DURATION]
                     [--artist_font ARTIST_FONT] [--title_font TITLE_FONT]
                     [--font_size FONT_SIZE] [--bg_color BG_COLOR]
                     [--output_file OUTPUT_FILE]
                     [--output_settings OUTPUT_SETTINGS] [--no_audio]
                     [--promo_clip PROMO_CLIP]
                     [--promo_interval PROMO_INTERVAL] [--version] [--info]
                     [path_to_list]

positional arguments:
  path_to_list          path to directory or text file with list of
                        directories

options:
  -h, --help            show this help message and exit
  --base_path BASE_PATH
                        base directory path for media files
  --video_size VIDEO_SIZE
                        size of final video [default: 1920x1080]
  --codec CODEC         codec for final video [default: libx264]
  --title_duration TITLE_DURATION
                        duration of title display [default: 4 (seconds)]
  --media_duration MEDIA_DURATION
                        duration of media display [default: 14 (seconds)]
  --fade_duration FADE_DURATION
                        duration (sec) of fade in and fade out [default: 0.5 (seconds)]
  --artist_font ARTIST_FONT
                        font for artist name [default: Arial]
  --title_font TITLE_FONT
                        font for artwork title  [default: Arial]
  --font_size FONT_SIZE
                        font size for artist name and title displays  [default: 50]
  --bg_color BG_COLOR   background color for artist name and title displays  [default: black]
  --output_file OUTPUT_FILE
                        path to output file
  --output_settings OUTPUT_SETTINGS
                        path to output settings file
  --no_audio            remove audio from video
  --promo_clip PROMO_CLIP
                        path to promo clip that plays interspersed with media
                        clips
  --promo_interval PROMO_INTERVAL
                        time to wait between promo clips
  --version             show program's version number and exit
```

Note that times specified in the arguments can be time strings in the form of 00:00:00.000 or just a float value in seconds.

### Promo image/video

You can add a repeating splash/promo image/video interspersed into the video that will repeat after at least PROMO_INTERVAL (but only between different artists).