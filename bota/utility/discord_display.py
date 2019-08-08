def cvt_dict_to_discord_pretty_text(value, spaces=18, custom_space={}, rename_keys={}):
    """
    Given list of dictionaries pretties them for display purpose:
    eg: input: [{a:1, b:2}, {a:3, b:4]
    output:    a      b
               1      2
               3      4
    :param value: list of dictionaries
    :param spaces: number of spaces after each keys
    :custom spaces: a dictionary where specific space for each key eg: {key1: 18, key2: 14}
    :param rename_keys: if you want to rename any of the keys in dictionary eg: {a: new_a, b: new_b}
    :return: a string
    """
    temp_string = ''
    header_position = []
    header_name = []
    for i, dictionary in enumerate(value):
        temp_string += f"{i + 1}. "
        for j, (key_name, value) in enumerate(dictionary.items()):
            # very bad practice of aligning for display purpose
            if i == 0:
                header_position.append(len(temp_string))
                key_name = key_name if key_name not in rename_keys.keys() else rename_keys[key_name]
                header_name.append(key_name)
            if i == 0:
                temp_val = f"{value}"
                if key_name in custom_space:
                    remain_space = custom_space[key_name] - len(temp_val)
                else:
                    remain_space = spaces - len(temp_val)
                if remain_space > 0:
                    temp_string += temp_val + (' ' * remain_space)
                else:
                    temp_string += temp_val[:spaces]
            elif i != 0:
                current_len = header_position[j] - len(temp_string.split('\n')[-1])
                if current_len < 0:
                    temp_string = temp_string[:current_len]
                    temp_string += f"{value}        "
                else:
                    temp_string += ' ' * current_len + f"{value}        "
            else:
                temp_string += f"{value}        "
        temp_string += "\n"
    temp_header_str = ['*'] * 150
    for position, header in zip(header_position, header_name):
        temp_header_str[position:position + len(header)] = header.upper()
    temp_header_str = ''.join(temp_header_str)
    temp_header_str = temp_header_str.replace('*', ' ')
    temp_header_str = temp_header_str.rstrip()
    final_text = f"{temp_header_str}\n{temp_string}"

    # embed into code eg: ```css\nfinal_text``` to make it look pretty
    return final_text


if __name__ == '__main__':
    value = [{'a': 'bendangnuksung', 'b': '2', 'c': 3},
             {'a': 1, 'b': '2', 'c': 3},
             {'a': 1, 'b': '2', 'c': 3},
             {'a': 1, 'b': '2', 'c': 3}]
    string = cvt_dict_to_discord_pretty_text(value , custom_space={'a': 13, 'b': 5})
    print(string)