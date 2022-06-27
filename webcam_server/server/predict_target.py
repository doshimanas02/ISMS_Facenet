import connector as c
from detect_faces_dlib import dlib_corrected
from process_dataset import create_array_from_image
import pandas as pd
from generate_embeddings import get_embedding
import math
import cv2


def predict(file_path):
    data = pd.DataFrame(columns=['img'])
    pixel_array = create_array_from_image(file_path)
    print(pixel_array.shape)
    data = data.append({'img': pixel_array}, ignore_index=True)
    data_image = dlib_corrected(data, data_type='test')
    print(data_image.shape)
    cv2.imwrite('img.jpg', data_image[0])
    embedding = get_embedding(data_image[0])
    # target_statement = ''
    # for i, value in zip(range(len(embedding)), embedding):
    #     target_statement += 'select %d as dimension, %s as value' % (i, str(value))  # sqlite
    #     # target_statement += 'select %d as dimension, %s as value from dual' % (i, str(value)) #oracle
    #
    #     if i < (len(embedding) - 1):
    #         target_statement += ' union all '
    target_statement = ""
    for i, value in enumerate(embedding):
        target_statement += "select %d as dimension, %s as value" % (i, str(value))  # sqlite
        # target_statement += "select %d as dimension, %s as value from dual" % (i, str(value)) #oracle

        if i < len(embedding) - 1:
            target_statement += " union all "
    print(target_statement)

    select_statement = f"""
        select * 
        from (
            select img_name, sum(subtract_dims) as distance_squared
            from (
                select img_name, (source - target) * (source - target) as subtract_dims
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

    results = c.cursor.execute(select_statement)

    instances = []
    for result in results:
        img_name = result[0]
        distance_squared = result[1]

        instance = []
        instance.append(img_name)
        instance.append(math.sqrt(distance_squared))
        instances.append(instance)

    result_df = pd.DataFrame(instances, columns=["img_name", "distance"])

    print(result_df)


def main():
    predict(r'C:\Users\Administrator\Pictures\target.jpg')


if __name__ == "__main__":
    main()
