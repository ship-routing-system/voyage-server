import os


def gcp_project():
    return os.environ['PROJECT_NAME']


def function_name():
    return os.environ['FUNCTION_NAME']


def region():
    return os.environ.get("FUNCTION_REGION", "asia-northeast3")


def bucket_name():
    return os.environ['BUCKET_NAME']


def dataset_name():
    return os.environ['DATASET_NAME']


def table_name():
    return os.environ['TABLE_NAME']