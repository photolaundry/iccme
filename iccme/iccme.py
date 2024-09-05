import argparse
from concurrent.futures import ThreadPoolExecutor
import configparser
import os
from pathlib import Path

from wand.image import Image


CONFIG_FILENAME = ".iccme"


class ICCMe:
    def __init__(self, icc_path : str):
        with open(icc_path, "rb") as icc_file:
            self.icc_data = icc_file.read()
    
    def apply_icc_to_image(self, image_path : Path) -> None:
        if not image_path.exists():
            raise ValueError(f"Image not found: {image_path}")

        print(f"  Processing {image_path}...")
        with Image(filename=image_path) as image:
            image.profiles["icc"] = self.icc_data
            image.save(filename=image_path)


def find_config_path() -> Path:
    # search cwd, then homedir, then start searching parent directories for the
    # .iccme config file
    all_config_locations =  [Path.cwd(), Path.home()] + list(Path.cwd().parents)
    for d in all_config_locations:
        possible_path = d / CONFIG_FILENAME
        if possible_path.exists():
            return possible_path


def cli():
    parser = argparse.ArgumentParser(
        description="Batch apply an ICC profile to images.")
    parser.add_argument(
            "images",
            nargs="+",
            help="The image files to apply the ICC profile to."
    )

    parser.add_argument(
            "--profile",
            default=None,
            help="The path to the ICC file to use."
    )

    args = parser.parse_args()

    config = configparser.ConfigParser()
    
    config_path = find_config_path()
    # need the parent to know where to reference a relative path in the config
    config_path_parent = config_path.parent

    config.read(find_config_path())
    if args.profile:
        icc_path = args.profile
    else:
        icc_path = config_path_parent / config["ICCME"]["profile"]

    if not icc_path.exists():
        raise ValueError(f"ICC profile not found: {icc_path}")

    iccme = ICCMe(icc_path)

    # run in parallel, up to 10 files at a time
    with ThreadPoolExecutor(max_workers=10) as ex:
        ex.map(iccme.apply_icc_to_image, (Path(x) for x in args.images))


if __name__ == "__main__":
    cli()
