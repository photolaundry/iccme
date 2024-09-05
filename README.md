# ICCME
A simple script to batch apply an ICC profile to image files.

## Installation
TODO: update this when the wheel is easier to find/download.
The scripts are written and tested in Python 3.12, but likely works for Python 3.10 and newer. To install, use either `pip` or `pipx` to install the `frontier-scans-cleanup` package.

*[ImageMagick](https://docs.wand-py.org/en/latest/guide/install.html#install-imagemagick-on-debian-ubuntu)* must be installed for the script to work. For MacOS users, you can also use Homebrew to install it: `brew install imagemagick`

## Config (optional)
The script will look for a `.iccme` file in the current directory, the home directory, and then all parent directories (in that order). If a `.iccme` file is found, it should have the following format:

```ini
[ICCME]
profile = ./path/to/profile/profile.icc
```

## Run
Run `iccme` and specify all image files you want to apply the ICC profile to as arguments:

```sh
iccme *.tif
```

 If the optional config file is not found, then you should provide the path to your ICC profile using `--profile`:

```sh
iccme --profile ./path/to/profile/profile.icc *.tif
```
