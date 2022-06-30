import sqlite3
from collections import defaultdict
from .detect_faces_dlib import dlib_corrected
import pandas as pd
from .generate_embeddings import get_embedding
import cupy as np

connection = sqlite3.connect(
    r'C:\Users\Administrator\PycharmProjects\ISMS_DeepFace\webcam_server\server\database\facialdb.db',
    check_same_thread=False)
cursor = connection.cursor()


# cursor = c()
def predict(image):
    data = pd.DataFrame(columns=['img'])
    pixel_array = np.asarray(image)
    # print(pixel_array.shape)
    data = data.append({'img': pixel_array}, ignore_index=True)
    data_image = dlib_corrected(data, data_type='test')
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
        # print(result)
        vector[result[0]].append((result[1], result[2]))

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
    # print(vector)
    temp = min(sim_dict.values())
    res = [key for key in sim_dict if sim_dict[key] == temp]
    print(temp, res)
    if temp < 0.3:
        return res
    else:
        return 'unknown'


def findCosineSimilarity(source_representation, test_representation):
    a = np.matmul(np.transpose(source_representation), test_representation)
    b = np.sum(np.multiply(source_representation, source_representation))
    c = np.sum(np.multiply(test_representation, test_representation))
    return 1 - (a / (np.sqrt(b) * np.sqrt(c)))


def main():
    pass
    # predict(r'C:\Users\Administrator\Datasets\temp.jpg')


if __name__ == '__main__':
    main()
