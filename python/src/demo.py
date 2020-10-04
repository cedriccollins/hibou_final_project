from datetime import timedelta
from minio import Minio
from minio.error import (ResponseError, BucketAlreadyOwnedByYou, BucketAlreadyExists)
from os import environ

minioClient = Minio('minio:9000',
                    access_key=environ['MINIO_ACCESS_KEY'],
                    secret_key=environ['MINIO_SECRET_KEY'],
                    secure=False)

if __name__ == '__main__':
    try:
        minioClient.make_bucket('cutedogs')
    except BucketAlreadyOwnedByYou as err:
        pass
    except BucketAlreadyExists as err:
        pass
    except ResponseError as err:
        raise

    try:
        # upload a picture of my dog being super cute
        minioClient.fput_object('cutedogs', 'cute_dog.jpg', '/tmp/cute_dog.jpg')
    except ResponseError as err:
        print(err)

    url = minioClient.presigned_get_object('cutedogs', 'cute_dog.jpg', expires=timedelta(hours=24))
    print(url)