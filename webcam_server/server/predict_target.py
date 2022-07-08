import concurrent
import os
import sqlite3
from collections import defaultdict
from .detect_faces_dlib import dlib_deepface
import pandas as pd
from .generate_embeddings import get_embedding
import cupy as cp
import numpy as np
from PIL import Image
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import multiprocessing
import time
from collections import Counter
from concurrent.futures import as_completed, wait


def most_frequent(ls):
    return max(set(ls), key=ls.count)


connection = sqlite3.connect(
    r'C:\Users\Administrator\PycharmProjects\ISMS_DeepFace\webcam_server\server\database\facialdb.db',
    check_same_thread=False)


# cursor = c()
def predict(image):
    connection = sqlite3.connect(
        r'C:\Users\Administrator\PycharmProjects\ISMS_DeepFace\webcam_server\server\database\facialdb.db',
        check_same_thread=False)
    cursor = connection.cursor()
    data = pd.DataFrame(columns=['img'])
    pixel_array = np.asarray(image)
    # print(pixel_array.shape)
    data = data.append({'img': pixel_array}, ignore_index=True)
    data_image = dlib_deepface(data, data_type='test')
    if np.isnan(data_image).any():
        return 'unknown'
    embedding = get_embedding(data_image[0])
    target_statement = ""
    for i, value in enumerate(embedding):
        target_statement += "select %d as dimension, %s as value" % (i, str(value))  # sqlite
        # target_statement += "select %d as dimension, %s as value from dual" % (i, str(value)) #oracle

        if i < len(embedding) - 1:
            target_statement += " union all "
    select_statement = f"""
        select * 
        from (
            select img_name, sum(subtract_dims) as distance_squared
            from (
                select img_name, source, target
                from (
                    select meta.img_name, emb.value as source, target.value as target
                    from face_meta meta left join face_embeddings emb
                    on meta.id = emb.face_id
                    left join (
                        {target_statement}  
                    ) target
                    on emb.dimension = target.dimension
                )
            )
            group by img_name
        )
        where distance_squared < 100
        order by distance_squared asc
    """
    # print(target_statement)
    select_statement2 = f"""
        select img_name, source, target from ( 
        select meta.img_name, emb.value as source, target.value as target from 
        face_meta meta left join face_embeddings emb on meta.id = emb.face_id 
        left join ( {target_statement} ) target on emb.dimension = target.dimension )
    """
    results = cursor.execute(select_statement2)
    vector = defaultdict(list)
    sim_dict = dict()
    for result in results:
        vector[result[0]].append((result[1], result[2]))
    # start_time = time.perf_counter()
    for key, value in vector.items():
        arr1 = []
        arr2 = []
        for source, target in value:
            arr1.append(source)
            arr2.append(target)
        source = np.asarray(arr1, dtype='float64')
        target = np.asarray(arr2, dtype='float64')
        sim = findCosineSimilarity(source, target)
        sim_dict[key] = sim
    temp = min(sim_dict.values())
    res = [key for key in sim_dict if sim_dict[key] == temp]
    # print(temp, res)
    if temp < np.float64(0.3):
        return res
    else:
        return 'unknown'


def findCosineSimilarity(source_representation, test_representation):
    a = np.matmul(np.transpose(source_representation), test_representation)
    b = np.sum(np.multiply(source_representation, source_representation))
    c = np.sum(np.multiply(test_representation, test_representation))
    return 1 - (a / (np.sqrt(b) * np.sqrt(c)))


def predict_all(images):
    start_time = time.perf_counter()
    results = []
    with ThreadPoolExecutor(max_workers=10) as executor:
        # submit tasks and collect futures
        futures = [executor.submit(predict, i) for i in images]
        wait(futures, return_when=concurrent.futures.ALL_COMPLETED)
        finish_time = time.perf_counter()
        print('after wait: ', finish_time - start_time)
        for future in as_completed(futures):
            # get the downloaded url data
            results.append(future.result()[0])

        # print(results)
        # finish_time = time.perf_counter()
        # print(f"Program finished in {finish_time - start_time} seconds")
        avg_res = most_frequent(results)
        # print("Avg Res: ", avg_res)
        return 0


def main():
    start_time = time.perf_counter()
    path = 'C:/Users/Administrator/Datasets/dataset/315627910626/'
    # predict(Image.open(path + 'photo0.png'))
    images = []
    for image in os.listdir(path):
        image = Image.open(path + image)
        images.append(image)
        predict(image)
    # predict_all(images)
    finish_time = time.perf_counter()
    print('Process took: ', finish_time - start_time)
    # predict_all(images)


if __name__ == '__main__':
    main()
