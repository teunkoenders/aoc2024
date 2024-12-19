import argparse

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', dest='test', action='store_true')
    parser.add_argument('-2', dest='defragment_by_file_size', action='store_true')
    return parser.parse_args()

args = parse_args()

def read_input():
    with open(f"day9_disk_fragmenter/input.{'test' if args.test else 'prd'}") as f:
        string = f.read().strip()
    return string

class Block:
    def __init__(self, index):
        self.is_free_space = bool(index % 2)
        self.identifier = int(index/2) if not self.is_free_space else -1

def convert_disk_map_to_disk_blocks(disk_map):
    tmp = []
    for index, block_size in enumerate(disk_map):
        tmp.extend([Block(index)] * int(block_size))
    return tmp

def defragment_disk_blocks(disk_content: list[Block]):
    index = 0
    while True:
        if len(disk_content) == index:
            return
        if disk_content[index].is_free_space:
            while block_at_the_end := disk_content.pop():
                if not block_at_the_end.is_free_space:
                    break
            disk_content[index] = block_at_the_end
        index += 1

def calculate_checksum(disk: list[Block]):
    checksum = 0
    for index, block in enumerate(disk):
        if not block.is_free_space:
            checksum += int(block.identifier) * index
    return checksum

def solve1():
    disk_map = read_input()
    blocks = convert_disk_map_to_disk_blocks(disk_map)
    defragment_disk_blocks(blocks)
    checksum = calculate_checksum(blocks)
    print(checksum)

class File:
    def __init__(self, index, size):
        self.is_free_space = bool(index % 2)
        self.identifier = int(index/2) if not self.is_free_space else -1
        self.size = size
        self.is_defragmented = False

    def __repr__(self):
        return f"{self.identifier if not self.is_free_space else '.'}" * self.size

def convert_disk_map_to_disk_files(disk_map):
    tmp = []
    for index, block_size in enumerate(disk_map):
        tmp.append(File(index, int(block_size)))
    return tmp

def find_free_space_with_size_and_update(disk_content: list[File], size, before):
    for index, file in enumerate(disk_content[:before]):
        if file.is_free_space and file.size >= size:
            file.size = file.size - size
            return index
        
def find_index_of_unfragmented_file(disk_content: list[File]):
    last_index = len(disk_content) - 1
    for index in range(len(disk_content)):
        file = disk_content[last_index - index]
        if not file.is_free_space and not file.is_defragmented:
            return last_index - index

def defragment_disk_files(disk_content: list[File]):
    while True:
        index_of_unfragmented_file = find_index_of_unfragmented_file(disk_content)
        if not index_of_unfragmented_file:
            break
        else:
            file_at_the_end = disk_content.pop(index_of_unfragmented_file)
        
        index_of_free_space_with_same_size_as_file = find_free_space_with_size_and_update(disk_content, file_at_the_end.size, index_of_unfragmented_file)
        if index_of_free_space_with_same_size_as_file:
            disk_content.insert(index_of_free_space_with_same_size_as_file, file_at_the_end)
            disk_content.insert(index_of_unfragmented_file, File(1, file_at_the_end.size))
        else: 
            disk_content.insert(index_of_unfragmented_file, file_at_the_end)
        file_at_the_end.is_defragmented = True

def calculate_checksum_of_files(disk: list[File]):
    index = 0
    checksum = 0
    for file in disk:
        if not file.is_free_space:
            for _ in range(file.size):
                checksum += int(file.identifier) * index
                index += 1
        else:
            index += file.size
    return checksum

def solve2():
    disk_map = read_input()
    files = convert_disk_map_to_disk_files(disk_map)
    defragment_disk_files(files)
    checksum = calculate_checksum_of_files(files)
    print(checksum)

if __name__ == "__main__":
    if args.defragment_by_file_size:
        solve2()
    else:
        solve1()