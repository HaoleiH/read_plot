import re
num_header_lines = 0
filepath = r"..\data\0115202201_PL_5pct_P1.txt"
with open(filepath, 'r') as f:
    for line in f:
        if re.search('[A-Za-z]{2,}', line):
            # count the header here
            num_header_lines += 1
        else:
            break
print(num_header_lines)
# Example usage:



