import heapq
import os
import tempfile

# Устанавливаем допустимый порог попамяти
MEMORY_SIZE_MB = 8 # 8МБ
MEMORY_SIZE = MEMORY_SIZE_MB * 8 * 1024 * 1024 # в битах

# Получение полного пути директории исполняемого файла
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

# Входной файл
input_file_path = 'large_file.txt'

# Выходной файл
output_file_path = 'output_file.txt'


def set_chunk_to_temp_file(tmp_dir_name: str, tmp_file_data: list[int]) -> str:
    """
    Создать временный файл с отсортированными значениями очередного chunk

    Args:
        tmp_dir_name (str): Абсолютный путь временной директории
        tmp_file_data (list[int]): list с элементами для записи

    Returns:
        str: Абсолютный путь созданного временного файла
    """
    tmp_file_data.sort()
    tmp_file = tempfile.NamedTemporaryFile(dir=tmp_dir_name, delete=False, mode='w', encoding='utf-8')
    tmp_file.writelines(f'{v}\n' for v in tmp_file_data)
    tmp_file.close()
    return tmp_file.name


if __name__ == '__main__':
    print(f'Запуск сортировки файла: {input_file_path}')
    # Создание временной директории для временных файлов
    temp_dir = tempfile.TemporaryDirectory(dir=os.path.join(ROOT_DIR, 'temp_splitted_files'))

    # Словарь для хранения объектов временных файлов
    temp_files = {}

    try:
        # Разделение входного файла на временные файлы
        with open(input_file_path, mode='r', encoding='utf-8') as input_file:

            temp_size = 0
            temp_file_data = []

            for line in input_file:
                value = int(line.strip())

                # Проверяем превысим ли мы допустимый порог по используемой памяти
                if temp_size + value.bit_length() > MEMORY_SIZE:
                    # Сортировка и запись временного файла
                    temp_file_name = set_chunk_to_temp_file(temp_dir.name, temp_file_data)
                    temp_files[temp_file_name] = None

                    temp_size = 0
                    temp_file_data = []

                temp_file_data.append(value)
                temp_size += value.bit_length()

            # Запись последнего временного файла
            if temp_file_data:
                temp_file_name = set_chunk_to_temp_file(temp_dir.name, temp_file_data)
                temp_files[temp_file_name] = None

        # Объединение временных файлов в итоговый отсортированный файл
        with open(output_file_path, mode='w', encoding='utf-8') as output_file:
            # Создание кучи для выборки минимального значения из временных файлов
            heap = []
            for temp_file_path, _ in temp_files.items():
                temp_file = open(temp_file_path, 'r')
                temp_files[temp_file_path] = temp_file
                value = int(temp_file.readline().strip())
                heapq.heappush(heap, (value, temp_file.name))

            # Выборка минимальных значений и запись в итоговый файл
            while heap:
                min_value, min_file_name = heapq.heappop(heap)
                output_file.write(f'{min_value}\n')
                min_file = temp_files[min_file_name]
                next_line = min_file.readline().strip()
                if next_line:
                    next_value = int(next_line)
                    heapq.heappush(heap, (next_value, min_file_name))
                else:
                    min_file.close()
        print(f'Отсортированные значение сохранены в файл: {output_file_path}')
    except Exception as exc:
        # Логика обработки ошибки
        # Запись в лог файл
        # Alert в третью систему
        # и т.д. зависит от требований
        pass
    finally:
        # Очистка
        for _, file in temp_files.items():
            if file is not None:
                file.close()
        temp_dir.cleanup()
