import random

OUTPUT_FILE = 'large_file.txt'
LINES = 10_000_000

if __name__ == '__main__':
    with open(file=OUTPUT_FILE, encoding='utf-8', mode='w+') as file:
        for i in range(LINES):
            file.write(str(random.randint(0, 1000)) + '\n')