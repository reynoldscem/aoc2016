import re

def main():
    string = '11110010111001001'
    target_len = 272
    target_len = 35651584

    while len(string) <= target_len:
        string = string + '0' + ''.join(
            [
                '1' if x == '0' else '0'
                for x in string[::-1]
            ]
        )
    checksum = string[:target_len]
    # print(checksum)

    while len(checksum) % 2 == 0:
        pairs = re.findall('..', checksum)
        pairs = [
            '1' if chunk[0] == chunk[1] else '0'
            for chunk in pairs
        ]
        checksum = ''.join(pairs)

    print(checksum)

if __name__ == '__main__':
    main()
