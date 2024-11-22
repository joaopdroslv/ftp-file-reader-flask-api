from typing import List


def remove_duplicates(input_list: List[str]) -> List[str]:
    seen = set()
    unique_list = []
    for item in input_list:
        if item not in seen:
            unique_list.append(item)
            seen.add(item)
    return unique_list
