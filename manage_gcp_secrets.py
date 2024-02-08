from google.cloud import secretmanager
import os

# Configuración
PROJECT_ID = 'project_id'
SECRET_NAME = 'secret_name'

def access_secret_version(project_id, secret_name):
    """Accede a la versión más reciente del secreto."""
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{project_id}/secrets/{secret_name}/versions/latest"
    response = client.access_secret_version(request={"name": name})
    secret_string = response.payload.data.decode("UTF-8")
    return secret_string

if __name__ == "__main__":
    secret = access_secret_version(PROJECT_ID, SECRET_NAME)
    print(f"El valor del secreto es: {secret}")
