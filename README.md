# Auto video

## Install

```
$ conda create --prefix env/
$ conda activate env/
$ pip install moviepy
```

moviepy uses imagemagick PDF to create text and that has a security issue so the disabling of that has to be removed:

```
$ identify -list policy
```
the first line should tell you where your policy.xml file is located. My policy.xml file is located at `/etc/ImageMagick-6/policy.xml`

open that file, and goto to the end and comment out (or remove the line that reads)

```svg
<policy domain="path" rights="none" pattern="@*" />
```

since this is xml, you can comment out this line by appending the line with `<!--` and ending it with `-->`