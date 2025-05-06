import re
import os
from argparse import ArgumentParser


def print_ignored_files(project_path: str) -> None:
    """Print ignored files from .gitignore"""

    if not os.path.exists(os.path.join(project_path, ".gitignore")):
        print(f".gitignore doesn't exist in directory {project_path}")
        return

    with open(os.path.join(project_path, ".gitignore")) as git_ignore:
        ignored = tuple(map(lambda x: x.strip(), git_ignore))

        ignored_rexp = {
            x: os.path.join(project_path, x.replace(".", "\."))
            if "*" not in x
            else ".{}".format(x.replace(".", "\."))
            for x in ignored
        }

        print("Ignored files:")
        for root, _, files in os.walk(project_path):
            for file in files:
                abs_file = os.path.join(root, file)
                for rexp in ignored_rexp:
                    if re.fullmatch(ignored_rexp[rexp], abs_file):
                        print(
                            f"{os.path.relpath(abs_file, project_path)} ignored by expression {rexp}"
                        )


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument(
        "--project_path",
        type=str,
        required=True,
        help="path to the directory containing the .gitignore",
    )
    args = parser.parse_args()
    print_ignored_files(args.project_path)
