# Brueba Tecnica

Este proyecto implementa un pipeline de Machine Learning para el conjunto de datos Iris, abarcando desde la carga de datos hasta la implementación de una API web para realizar predicciones.

## Estructura del Proyecto

- **iris_pipeline.py:** Define un pipeline de Kubeflow (KFP) que incorpora componentes de lectura de datos, preprocesamiento, división de datos y entrenamiento del modelo utilizando Google Cloud AI Platform.

- **load_iris_data.py:** Crea y sube el conjunto de datos Iris a Google Cloud Storage.

- **manage_gcp_secrets.py:** Utiliza Google Cloud Secret Manager para acceder a un secreto necesario en el proyecto.

- **Dockerfile:** Define un contenedor Docker para la aplicación Flask.

- **requirements.txt:** Lista las dependencias necesarias para ejecutar la aplicación.

- **bigquery_upload.py:** Carga el conjunto de datos Iris en BigQuery.

- **app.py:** Una aplicación Flask que carga un modelo entrenado y proporciona un endpoint para realizar predicciones.

## Configuración

Antes de ejecutar los scripts, asegúrate de configurar adecuadamente las variables de entorno y los archivos de configuración. Puedes encontrar la configuración en los scripts correspondientes.
