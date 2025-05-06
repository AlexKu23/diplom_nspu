import logging
import os
import time
from argparse import ArgumentParser


def trash_cleanup(trash_path: str, age_thr: int) -> None:
    """Killed files from trash directory"""

    logging.basicConfig(filename="clean_trash.log", level=logging.INFO)

    while True:
        for root, _, files in os.walk(trash_path):
            for file in files:
                abs_file = os.path.join(root, file)
                mod_file = os.path.getmtime(abs_file)  # seconds
                if time.time() - mod_file > age_thr:
                    os.remove(abs_file)
                    logging.info(abs_file)

        for root, dirs, _ in os.walk(trash_path, topdown=False):
            for dir in dirs:
                abs_dir = os.path.join(root, dir)
                if not os.listdir(abs_dir):
                    os.rmdir(abs_dir)
                    logging.info(abs_dir)
        time.sleep(1)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument(
        "--trash_folder_path",
        type=str,
        required=True,
        help="path to the trash folder",
    )
    parser.add_argument(
        "--age_thr",
        type=int,
        required=True,
        help="time in seconds, after expiration the files will be killed",
    )
    args = parser.parse_args()
    trash_cleanup(args.trash_folder_path, args.age_thr)
