# Proyecto de libros
## Instrucciones de ejecucion
1. Clona el proyecto
2. Crea un virtual enviorement:
   1. En la consola ejecuta: `pipenv --python <version de python 3>` ej: `pipenv --python 3.10.12` 
   2. Ingresa en el virtual env: `pipenv shell`
   3. Instala las bibliotecas necesarias dentro del entorno ejecutando: `pipenv install -r requirements.txt`
3. Muevete a la carpeta del proyecto ejecutando ` cd proyecto_libros` donde debe estar el archivo `manage.py` 
4. Crea y ejecuta las migraciones para la creacion de la base de datos, ejecuta:
   1. `python manage.py makemigrations users mi_app`
   2. `python manage.py migrate` 
5. Corre el servidor de desarrollo ejecutando: `python manage.py runserver` 

## Creacion de usuario admin
1. Crea un super usuario y completa los datos, ejecutando: `python manage.py createsuperuser`