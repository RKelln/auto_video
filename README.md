# Auto video

A very simple prototype python script that can create a video from a structure of folders and/or text file containing a list of media. Each image or video incorporated is preceded by a title containing the artist/author and the title of the work. Intended for use for looping videos of art exhibitions.

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
  - Artist Name
    - Title_of_the_Work_(2023).png
    - Title_of_work_(2021).png
  - Artist Name 2
    - 01_Order_by_Number_not_title_(2023).jpg
    - 02_Another_title_(2023).mp4
    - _ignore-files_starting_with_underscores in the automatic list generation.jpg

Underscores are converted to spaces in the auto-titling. File extensions are removed.


## Running:

```
$ python3 create_video.py --base_path ../works --output_settings all_works.txt ../works/
```

Then you can edit that `all_works.txt` file to curate the list (removing works and ordering) and then run:

```
$ python3 create_video.py --base_path ../works --output_file video.mp4 all_works.txt
```

I can be helpful to set up a file with all the consistent settings between videos:
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

Media wil lbe appended to the video in order specified in the textfile:

```
Artist Name1/Work Title1 (YEAR).jpg
Artist Name1/Work Title2 (YEAR).jpg
Artist Name2/Work Title1 (YEAR).mp4
```