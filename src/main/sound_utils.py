import os
import urllib.request

import boto3
import botocore

from file_utils import get_filename, listdir_nohidden

SOUNDS_DIRNAME = os.environ.get('SOUNDS_DIRNAME')
SOUNDS_URL = os.environ.get('SOUNDS_URL')
SCHOOL_UUID = os.environ.get('SCHOOL_UUID')

S3_ENDPOINT = os.environ.get('S3_ENDPOINT')
S3_REGION = os.environ.get('S3_REGION')
S3_BUCKET = os.environ.get('S3_BUCKET')
S3_ACCESS_KEY_ID = os.environ.get('S3_ACCESS_KEY_ID')
S3_SECRET_ACCESS_KEY = os.environ.get('S3_SECRET_ACCESS_KEY')

s3client = boto3.client('s3', endpoint_url=S3_ENDPOINT,
                        aws_access_key_id=S3_ACCESS_KEY_ID,
                        aws_secret_access_key=S3_SECRET_ACCESS_KEY,
                        region_name=S3_REGION)


def get_sounds_in_folder(dir="bells"):
    if not os.path.isdir(SOUNDS_DIRNAME + "/" + dir):
        return []
    return list(map(get_filename, listdir_nohidden(SOUNDS_DIRNAME + "/" + dir)))


def get_sounds():
    return {
        "announcements": get_sounds_in_folder("announcements"),
        "bells": get_sounds_in_folder("bells")
    }


def download_sound(uuid, type="bells"):
    downloaded_sounds = get_sounds()[type]
    if uuid in downloaded_sounds:
        print("Звук", uuid, "уже загружен")
        return
    print("Звук", uuid, "загружается...")

    s3_path = "schools/" + SCHOOL_UUID + "/" + type + "/" + uuid + ".mp3"
    save_path = SOUNDS_DIRNAME + "/" + type + "/"

    if not os.path.isdir(save_path):
        os.mkdir(save_path)
    try:
        s3client.download_file(S3_BUCKET, s3_path, save_path + uuid + ".mp3")
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            print("The object does not exist.")
        else:
            raise

    print("Звук", uuid, "успешно загружен")


def delete_sound(uuid, type="bell"):
    downloaded_sounds = get_sounds()[type]
    if uuid not in downloaded_sounds:
        print("Звук", uuid, "уже удалён")
        return
    print("Звук", uuid, "удаляется...")

    saved_path = SOUNDS_DIRNAME + "/" + type + "/"+ uuid + ".mp3"
    os.remove(saved_path)

    print("Звук", uuid, "успешно удалён")
