import rasterio
import rasterio.features
import rasterio.warp
from rasterio.plot import show, show_hist
import os
import matplotlib.colors as matplotcolors
import numpy as np
from rasterio.transform import Affine
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image, ImageEnhance
import json  # подключили библиотеку для работы с json
from pprint import pprint  # подключили Pprint для красоты выдачи текста

"""
Пример входных данных с подписями
data_sample = [1,  # admin                                                              0
               37,  # relief_hight                                                      1
               168.69006,  # relief_aspect                                              2
               1.4604452,  # relief_slope                                               3
               1,  # vineyards                                                          4
               0,  # water                                                              5
               5,  # landcover                                                          6
               160,  # sunny_days                                                       7
               [39, 33, 33, 34, 35, 45, 34, 39, 35, 33, 46, 51],  # prec                8
               [8, 15, 45, 108, 158, 205, 233, 227, 179, 121, 68, 32],  # tavg          9
               [-18, -13, 12, 71, 118, 164, 191, 184, 136, 84, 37, 5],  # tmin          10
               [35, 78, 111, 144, 197, 246, 275, 270, 222, 158, 98, 59],  # tmax        11
               1] # soil_texture                                                        12
"""

"""
Основная функция поиска координат под запрашиваемые данные и диапазон
data - запрашиваемые данные как на примере выше
delta_array - массив отклонений от запрашиваемых данных
all_data - массив тифов
"""
def find_similar_land(data, delta_array, all_data):
    # resulting coordinates
    result_coord = []
    # 4 - есть ли виноградник. У нас это значение всегда будет 1
    # А мы должны искать из мест, где виноградника нет
    if data[4] != 0:
        data[4] = 0
    # Подготавливаем массив с результатми. сначала в нём все возможные координаты, которые будут удаляться в цикле
    for x in range(0, 4096):
        for y in range(0, 4096):
            result_coord.append((x, y))
    # основной цикл по параметрам (их 13)
    for i in range(13):
        # Если в дельте -1, то данные не важны для выборки
        delta = delta_array[i]
        if (delta == -1):
            continue
        # Для этих элементов данные представлены числом
        if (i in range(0, 8) or (i == 13)):
            channel = 0
            result_coord = find_coord_in_data(data[i],
                                              delta,
                                              all_data[i],
                                              channel,
                                              result_coord)
        # Для этих данных массивом из 12 элементов
        elif i in range(8, 12):
            for channel in range(12):
                result_coord = find_coord_in_data(data[i][channel],
                                                  delta[channel],
                                                  all_data[i],
                                                  channel,
                                                  result_coord)
    return result_coord


"""
Удаляет из ref_coord координаты, которые не подходят под запрос
val - значение с которым сравниваемся
delta - отклонение от значения
tiff_data - данные тифа по которому происходит выборка
channel - уровень данных в тифе. Для prec tavg tmin tmax уровень изменяется от 0 до 11, для остальных всегда 0
ref_coord - результирующий массив координат
"""
def find_coord_in_data(val, delta, tiff_data, channel, ref_coord):
    # теперь дельта - абсолютное отклонение
    delta = val * delta
    # массив в который скопируем подходящие координаты
    ref_coord_export = []
    # Бежим по всем результирующим координатам
    for i in range(len(ref_coord)):
        # Берем значение по координате из тифа
        data_val = tiff_data[channel][ref_coord[i][1]][ref_coord[i][0]]
        # Проверяем, что данные лежат в заданном отклонении
        if ((data_val >= val - delta) and (data_val <= val + delta)):
            ref_coord_export.append(ref_coord[i])
    return ref_coord_export


"""
Находим тифы из списка и добавляем данные из нах в массив res_list
"""
def get_all_tiff(path):
    # Результат - массив из 13 элементов. Каждый элемент - данные из тифа
    res_list = []
    # Абсолютные путь до тифа. Определяется в цикле
    tif_files_abs_paths = [None] * 13
    # Имена всех нужных тифов
    tif_filename_list = [
        "KRA_ADMIN_100m.tif",
        "KRA_RELIEF_HEIGHT_100m.tif",
        "KRA_RELIEF_ASPECT_100m.tif",
        "KRA_RELIEF_SLOPE_100m.tif",
        "KRA_VINEYARDS_100m.tif",
        "KRA_WATER_SEASONALYTY_100m.tif",
        "KRA_LANDCOVER_100m.tif",
        "KRA_SUNNY_DAYS_APR_OCT_100m.tif",
        "KRA_PREC_100m.tif",
        "KRA_TAVG_100m.tif",
        "KRA_TMIN_100m.tif",
        "KRA_TMAX_100m.tif",
        "KRA_SOILTEXTURE_100m.tif"
    ]
    # Бегаем по папке и ищем тифы
    for root, dirs, files in os.walk(path):
        for file in files:
            if (file in tif_filename_list):
                # Чтобы расставить тифы в массиве в порядке приоритета находим индекс тифа по имени файла
                index = tif_filename_list.index(file)
                tif_files_abs_paths[index] = (os.path.join(root, file))
    # Добавляем тифы в массив в порядке приоритета
    for tiff_file in tif_files_abs_paths:
        res_list.append(rasterio.open(tiff_file).read())
    return res_list


"""
Изменяет данные тифа выделяя нужные координаты добавлением константного значенияв тиф
"""
def append_to_res_tif(ds_result, result):
    for i in range(len(result)):
        ds_result[0][result[i][1]][result[i][0]] = 0
        ds_result[0][result[i][1]][result[i][0]] += 10000
    return ds_result


"""
Основная функция поиска
numbers_of_vino - список номеров виноградников
delta_sample - массив отклонений от данных
"""
def find_vino(numbers_of_vino, delta_sample):
    # Путь до данных
    data_path = r'../../AgroCodeHack_VINEYARDS'
    # Путь до сохранения картиинки
    res_pic_path = r'../../Resulting_pic'
    # читаем json
    with open(os.path.join(data_path, 'VINEYARDS.geojson'), 'r', encoding='utf-8') as f:
        text = json.load(f)  # загнали все, что получилось в переменную
        #pprint(text)  # вывели результат на экран
    print("json ready")
    # Читаем все тифы в порядке приоритета и заносим в массив. Каждый элемент массива - данные из тифа
    ds_array = get_all_tiff(data_path)
    print("tiff array ready")
    # подхватываем координаты нужных виноградников из json
    information = []
    for number in numbers_of_vino:
        point = text['features'][number - 1]
        found_flag = False
        if (point['properties']['n'] == number):
            lon = point['properties']['x']
            lat = point['properties']['y']
            found_flag = True
        if found_flag:
            # свойства виноградников по координатам
            res = []
             # admin
            res.append(ds_array[0][0][(5209600 - lat) // 100][(lon - 310000) // 100])
            # relief_hight
            res.append(ds_array[1][0][(5209600 - lat) // 100][(lon - 310000) // 100])
            # relief_aspect
            res.append(ds_array[2][0][(5209600 - lat) // 100][(lon - 310000) // 100])
            # relief_slope
            res.append(ds_array[3][0][(5209600 - lat) // 100][(lon - 310000) // 100])
            # vineyards
            res.append(ds_array[4][0][(5209600 - lat) // 100][(lon - 310000) // 100])
            # water
            res.append(ds_array[5][0][(5209600 - lat) // 100][(lon - 310000) // 100])
            # landcover
            res.append(ds_array[6][0][(5209600 - lat) // 100][(lon - 310000) // 100])
            # sunny_days
            res.append(ds_array[7][0][(5209600 - lat) // 100][(lon - 310000) // 100])
            res.append([])
            # prec
            for i in range(12):
                res[-1].append(ds_array[8][i][(5209600 - lat) // 100][(lon - 310000) // 100])
            res.append([])
            # tavg
            for i in range(12):
                res[-1].append(ds_array[9][i][(5209600 - lat) // 100][(lon - 310000) // 100])
            res.append([])
            # tmin
            for i in range(12):
                res[-1].append(ds_array[10][i][(5209600 - lat) // 100][(lon - 310000) // 100])
            # tmax
            res.append([])
            for i in range(12):
                res[-1].append(ds_array[11][i][(5209600 - lat) // 100][(lon - 310000) // 100])
            # landcover
            res.append(ds_array[12][0][(5209600 - lat) // 100][(lon - 310000) // 100])
            # добавляем найденные значения в массив
            information.append(res)
            print("Got all info about vineyard number: ", number)

    print("Got all info about vineyards")
    for data_sample in information:
        # Получаем координаты, которые подходят под запрос пользователя
        result = find_similar_land(data_sample, delta_sample, ds_array)
        print("Got resulting coord for vineyard")
        im = Image.open(os.path.join(res_pic_path, 'sample.JPEG')).convert('L')
        enhancer = ImageEnhance.Contrast(im)
        factor = 42  # increase contrast
        im = enhancer.enhance(factor)
        # Создаём картинку и оси
        fig, ax = plt.subplots()
        # Выводим картинку
        ax.imshow(im, cmap='Greys_r')
        for coord in result:
            # Create a Rectangle patch
            rect = patches.Rectangle(coord, 20, 20, linewidth=1, edgecolor='r', facecolor='r')
            # Add the patch to the Axes
            ax.add_patch(rect)
        plt.axis('off')
        plt.savefig(os.path.join(res_pic_path, 'result.JPEG'), format='jpeg', dpi=1000, pad_inches=0,
                    bbox_inches='tight')
        plt.axis('off')
    return 0

if __name__ == '__main__':
    """       
        # Массив с данными о выбраном винограднике
        data_sample = [
        1,  # admin
        37,  # relief_hight
        168.69006,  # relief_aspect
        1.4604452,  # relief_slope
        1,  # vineyards
        0,  # water
        5,  # landcover
        160,  # sunny_days
        [39, 33, 33, 34, 35, 45, 34, 39, 35, 33, 46, 51],  # prec
        [8, 15, 45, 108, 158, 205, 233, 227, 179, 121, 68, 32],  # tavg
        [-18, -13, 12, 71, 118, 164, 191, 184, 136, 84, 37, 5],  # tmin
        [35, 78, 111, 144, 197, 246, 275, 270, 222, 158, 98, 59],  # tmax
        1  # landcover
    ]"""
    # Номера виноградников
    numbers_of_vino = [2]
    # Массив с отклонениями в долях. -1 данные не используются
    delta_sample = [0.2, 0.2, 0.2, 0.2, -1, -1, -1, -1, -1, -1, -1, -1, -1]
    find_vino(numbers_of_vino, delta_sample)

