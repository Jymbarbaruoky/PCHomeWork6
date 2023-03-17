import argparse
from pathlib import Path

parser = argparse.ArgumentParser(description="Sorter folder")
parser.add_argument('-sf', '--sorting_folder', type=str, help='folder path to sort')
parser.add_argument('-rf', '--result_folder', type=str, help='path to result folder')
path = parser.parse_args()
sf = Path(path.sorting_folder)
if path.result_folder:
    rf = Path(path.result_folder)
else:
    rf = sf


def analysis_and_sorting(path: str):
    pass


if __name__ == '__main__':
    print(sf, rf)
