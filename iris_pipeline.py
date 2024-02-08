import kfp
from kfp.v2 import compiler
from kfp.v2.dsl import pipeline, component
from kfp.v2.dsl import Input, Output, Dataset, Model
from google_cloud_pipeline_components import aiplatform as gcc_aip

PROJECT_ID = 'project_id'
BUCKET_NAME = 'bucket_de_gcs'
PIPELINE_ROOT = f'gs://{BUCKET_NAME}/pipeline_root'

@component(packages_to_install=['google-cloud-storage', 'pandas'])
def read_data_from_gcs(gcs_path: str, output_data_path: Output[Dataset]):
    from google.cloud import storage
    import pandas as pd
    import os

    storage_client = storage.Client()
    bucket = storage_client.bucket(BUCKET_NAME)


    blob = bucket.blob(gcs_path)
    data = blob.download_as_string()
    df = pd.read_csv(data)
    df.to_csv(output_data_path.path)


@component(packages_to_install=['pandas'])
def preprocess_data(input_data: Input[Dataset], output_data: Output[Dataset]):
    import pandas as pd

    df = pd.read_csv(input_data.path)
    df_clean = df.dropna()
    df_clean.to_csv(output_data.path, index=False)

@component(packages_to_install=['pandas', 'sklearn'])
def split_data(input_data: Input[Dataset], train_data: Output[Dataset], test_data: Output[Dataset]):
    from sklearn.model_selection import train_test_split
    import pandas as pd

    df = pd.read_csv(input_data.path)
    train, test = train_test_split(df, test_size=0.2)
    train.to_csv(train_data.path, index=False)
    test.to_csv(test_data.path, index=False)


@pipeline(
    name='iris_training_pipeline',
    pipeline_root=PIPELINE_ROOT
)
def pipeline(project_id: str = PROJECT_ID):
    read_data_op = read_data_from_gcs(gcs_path='iris_data/iris.csv')

    preprocess_data_op = preprocess_data(read_data_op.output)

    split_data_op = split_data(preprocess_data_op.output)

    train_model_op = gcc_aip.CustomContainerTrainingJobRunOp(
        project=project_id,
        display_name='train_iris_model',
        container_uri='gcr.io/tu_project_id/iris_trainer:latest',
        model_display_name='iris-model',
        dataset=split_data_op.outputs['train_data'],
        model_serving_container_image_uri='gcr.io/tu_project_id/iris_predictor:latest',
        replica_count=1,
        machine_type='n1-standard-4'
    )

    deploy_model_op = gcc_aip.ModelDeployOp(
        model=train_model_op.outputs['model'],
        project=project_id
    )


compiler.Compiler().compile(
    pipeline_func=pipeline,
    package_path='iris_training_pipeline_job.json'
)
