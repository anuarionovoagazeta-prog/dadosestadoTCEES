import os
import json
import re

PATTERN = re.compile(r'^(?P<year>20\d{2})_(?P<key>.+?)\.json$')

def is_json_file(name):
    return name.lower().endswith('.json')

def main():
    workspace = os.getcwd()
    data = {}

    for name in os.listdir(workspace):
        if not is_json_file(name):
            continue
        if name == 'dados.json':
            continue
        if name.startswith('.'):  # skip dotfiles
            continue

        m = PATTERN.match(name)
        if not m:
            # skip other json files
            continue

        year = m.group('year')
        key = m.group('key')

        try:
            with open(os.path.join(workspace, name), 'r', encoding='utf-8') as fh:
                obj = json.load(fh)
        except Exception as e:
            print(f'WARN: failed to parse {name}: {e}')
            continue

        if year not in data:
            data[year] = {}
        # if key already exists, attempt to merge if both dicts, else overwrite
        if key in data[year] and isinstance(data[year][key], dict) and isinstance(obj, dict):
            # shallow merge
            data[year][key].update(obj)
        else:
            data[year][key] = obj

    # write consolidated file
    out_path = os.path.join(workspace, 'dados.json')
    try:
        with open(out_path, 'w', encoding='utf-8') as fh:
            json.dump(data, fh, ensure_ascii=False, indent=2, sort_keys=True)
        print(f'WROTE: {out_path} ({len(data)} years)')
    except Exception as e:
        print(f'ERROR: failed to write {out_path}: {e}')

if __name__ == '__main__':
    main()