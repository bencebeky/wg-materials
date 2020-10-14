import re
import os
from os import path
import sys

ignore_things = ['lib', 'README.md', 'badge']
ignore_prefixes = ['.', '_']
sep = "\n\n---\n\n"

def spider (directory):
    index = []
    sys.stderr.write(f"* scanning {directory}...\n")
    things = os.scandir(directory)
    dirs = nat_sort([i.name for i in things if i.is_dir() and filter_thing(i)])
    files = nat_sort([i.name for i in things if i.is_file() and filter_thing(i)])
    for name in dirs:
        index.append(f"- [{name}/]({name}/README.md)")
    for name in files:
        index.append(f"- [{name}]({name})")
    write_index(directory, index)
    for dir_name in dirs:
        spider(path.join(directory, dir_name))

def filter_thing(thing):
    if thing.name in ignore_things: return False
    for ignore in ignore_prefixes:
        if thing.name.startswith(ignore): return False
    return True

def nat_sort(l):
    convert = lambda text: int(text) if text.isdigit() else text.lower() 
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
    return sorted(l, key = alphanum_key)

def write_index(directory, index):
    readme_path = f"{directory}/README.md"
    if path.exists(readme_path):
        with open(readme_path, 'r') as fh:
            existing = fh.read()
            try:
                preserve = existing[:existing.index(sep)+len(sep)]
            except ValueError:
                preserve = f"{existing}{sep}"
        with open(readme_path, 'w') as fh:
            fh.write(preserve)
            fh.write("\n".join(index))
        sys.stderr.write("  Updated README.\n")
    else:
        with open(readme_path, 'w') as fh:
            fh.write(f"# {directory}\n\n")
            fh.write(sep)
            fh.write("\n".join(index))
        sys.stderr.write("  Created README.\n")



if __name__ == "__main__":
    import sys
    spider(sys.argv[1])