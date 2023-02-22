import os
from argparse import ArgumentParser

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--path', type=str, help="Root directory of ouput and clean_vocals folder.")
    args = parser.parse_args()
    path = args.path
    if path is None or not os.path.isdir(path):
        print("Please specify --path as the root directory")
        exit(0)

    for root, dirs, files in os.walk(path):
        for file in files:
            stem, ext = os.path.splitext(file)
            if len(stem.split('_')) > 4:
                path_to_remove = os.path.join(root, file)
                print("Remove {}".format(path_to_remove))
                os.remove(path_to_remove)
