import re
import sys
from pathlib import Path
import shutil


def get_path():
    try:
        f_path = Path(sys.argv[1])
        return f_path
    except IndexError:
        print('You did not enter an argument')


folder_path = get_path()


cyrillic_characters = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ'
latin_equivalent = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t",
                    "u", "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "u", "ja", "je", "ji", "g")
dict_for_translate = {}
for cyr, lat in zip(cyrillic_characters, latin_equivalent):
    dict_for_translate[ord(cyr)] = lat
    dict_for_translate[ord(cyr.upper())] = lat.upper()


images_list = []
documents_list = []
audio_list = []
video_list = []
archives_list = []
other_list = []

all_files = {
    'images': images_list,
    'documents': documents_list,
    'audio': audio_list,
    'video': video_list,
    'archives': archives_list,
    'other': other_list,
}


def normalize(file_path: Path) -> str:
    trans_name = file_path.name.translate(dict_for_translate)
    trans_name = re.sub(r'\W', '_', trans_name[:-(len(file_path.suffix)):])
    trans_name = f'{trans_name}{file_path.suffix}'
    return trans_name


def create_folders(path_dir: Path) -> None:
    (path_dir / 'images').mkdir(exist_ok=True, parents=True)
    (path_dir / 'documents').mkdir(exist_ok=True, parents=True)
    (path_dir / 'audio').mkdir(exist_ok=True, parents=True)
    (path_dir / 'video').mkdir(exist_ok=True, parents=True)
    (path_dir / 'archives').mkdir(exist_ok=True, parents=True)
    (path_dir / 'other').mkdir(exist_ok=True, parents=True)


def delete_dirs(path: Path) -> None:
    for ob in path.iterdir():
        if ob.is_dir() and ob.name in ('archives', 'video', 'audio', 'documents', 'images', 'other'):
            continue
        shutil.rmtree(ob)


def analysis_and_sorting(path: Path):
    for ob in path.iterdir():
        if ob.is_dir() and ob.name in ('archives', 'video', 'audio', 'documents', 'images', 'other'):
            continue
        if ob.is_dir():
            analysis_and_sorting(ob)
        else:
            if ob.suffix[1:] in ('jpeg', 'png', 'jpg', 'svg'):
                images_list.append(normalize(ob))
                shutil.move(ob, folder_path / 'images' / normalize(ob))
                continue
            if ob.suffix[1:] in ('doc', 'docx', 'txt', 'pdf', 'xlsx', 'pptx'):
                documents_list.append(normalize(ob))
                shutil.move(ob, Path(folder_path / 'documents' / normalize(ob)))
                continue
            if ob.suffix[1:] in ('mp3', 'ogg', 'wav', 'amr'):
                audio_list.append(normalize(ob))
                shutil.move(ob, folder_path / 'audio' / normalize(ob))
                continue
            if ob.suffix[1:] in ('avi', 'mp4', 'mov', 'mkv'):
                video_list.append(normalize(ob))
                shutil.move(ob, folder_path / 'video' / normalize(ob))
                continue
            if ob.suffix[1:] in ('zip', 'zg', 'tar'):
                (folder_path / 'archives' / normalize(ob).replace(ob.suffix, '')).mkdir(exist_ok=True, parents=True)
                shutil.unpack_archive(ob, folder_path / 'archives' / normalize(ob).replace(ob.suffix, ''))
                archives_list.append(normalize(ob))
                shutil.move(ob, folder_path / 'archives' / normalize(ob))
                continue
            elif ob.suffix[1:] != '':
                other_list.append(normalize(ob))
                shutil.move(ob, folder_path / 'other' / normalize(ob))
        continue


def main():
    create_folders(folder_path)
    analysis_and_sorting(folder_path)
    delete_dirs(folder_path)
    print(all_files)


if __name__ == '__main__':
    main()
