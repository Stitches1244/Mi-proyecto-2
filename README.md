# Valorant Agent Advisor

## Descripción del Proyecto

Valorant Agent Advisor es una aplicación de consola desarrollada en Python que consume datos reales desde una API externa de Valorant.

La herramienta permite consultar información de un agente específico del videojuego Valorant, mostrando datos como nombre, rol, descripción, nombre técnico dentro de la API y habilidades principales.

La aplicación está diseñada para ejecutarse de forma puntual desde consola o dentro de un contenedor Docker. No requiere un servidor web en ejecución continua.

## Stakeholder

El stakeholder principal es un jugador casual o semicompetitivo de Valorant que necesita consultar rápidamente información de un agente antes de una partida.

Este usuario requiere conocer el rol, descripción y habilidades del agente para tomar mejores decisiones al momento de seleccionar personaje.

## Problema

Los jugadores nuevos o en proceso de mejora pueden confundirse con la cantidad de agentes, roles y habilidades disponibles en Valorant.

Buscar manualmente esta información en páginas externas puede tomar tiempo y no siempre entrega los datos de forma clara y resumida.

## Solución

La aplicación automatiza la consulta de información usando una API externa de Valorant.

El usuario puede indicar el agente que desea consultar mediante una variable de entorno o ingresarlo manualmente por consola. Luego, la aplicación procesa los datos obtenidos y muestra un resumen ordenado con información relevante del agente.

## Propuesta de Valor

Valorant Agent Advisor reduce el tiempo necesario para revisar información de agentes y ayuda al jugador a tomar decisiones rápidas antes de una partida.

La herramienta entrega información clara, directa y basada en datos reales obtenidos desde una API externa.

## API Utilizada

La aplicación consume datos desde Valorant-API:

https://valorant-api.com/v1/agents

Endpoint utilizado:

https://valorant-api.com/v1/agents?language=es-ES&isPlayableCharacter=true

## Datos Procesados

La aplicación procesa los siguientes campos obtenidos desde la API:

- Nombre del agente
- Rol del agente
- Descripción del agente
- Nombre técnico en la API
- Habilidades del agente
- Tipo de habilidad
- Descripción de cada habilidad

## Manejo de Errores

La aplicación maneja distintos tipos de errores, entre ellos:

- Error 404 cuando el recurso no existe.
- Timeout cuando la API tarda demasiado en responder.
- Error de conexión cuando no hay acceso a internet o la API no está disponible.
- Error HTTP general.
- Error de formato JSON inválido.
- Error por campos faltantes en la respuesta de la API.

## Variables de Entorno

La aplicación utiliza variables de entorno para evitar valores rígidos dentro del código y permitir configuración externa.

| Variable | Descripción | Valor sugerido |
|---|---|---|
| VALORANT_API_LANGUAGE | Define el idioma de respuesta de la API | es-ES |
| AGENTE_VALORANT | Define el agente que se consultará automáticamente | Gekko |

Ejemplo en Linux:

    export VALORANT_API_LANGUAGE="es-ES"
    export AGENTE_VALORANT="Gekko"
    python3 app.py

Ejemplo en Windows PowerShell:

    $env:VALORANT_API_LANGUAGE="es-ES"
    $env:AGENTE_VALORANT="Gekko"
    python app.py

## Ejecución Local

Instalar dependencias:

    pip3 install -r requirements.txt

Ejecutar usando variable de entorno:

    export AGENTE_VALORANT="Gekko"
    python3 app.py

Ejecutar de forma manual:

    unset AGENTE_VALORANT
    python3 app.py

En modo manual, la aplicación mostrará la lista de agentes disponibles y solicitará al usuario escribir el nombre del agente que desea consultar.

## Ejecución con Docker

El proyecto incluye un script de automatización llamado build.sh.

Este script realiza las siguientes acciones:

1. Genera el archivo Dockerfile.
2. Construye la imagen Docker.
3. Elimina un contenedor previo si existe.
4. Ejecuta el contenedor.
5. Finaliza la ejecución de la aplicación con código de salida 0.

Dar permisos de ejecución:

    chmod +x build.sh

Ejecutar el script:

    ./build.sh

Comandos Docker utilizados por el script:

    docker build -t valorant-agent-advisor .
    docker run --name samplerunning -e AGENTE_VALORANT=Gekko valorant-agent-advisor

## Evidencias Docker

La evidencia de Docker se encuentra en:

    evidencias/docker/output.txt

Este archivo contiene:

- Salida de docker ps -a.
- Logs del contenedor.
- Datos reales obtenidos desde la API.
- Confirmación de finalización correcta de la consulta.

## Jenkins

El proyecto debe ejecutarse mediante Jenkins usando dos trabajos.

### BuildAppJob

Trabajo de estilo libre encargado de:

1. Clonar el repositorio desde GitHub usando credenciales seguras.
2. Ejecutar el script build.sh.
3. Construir la imagen Docker.
4. Ejecutar el contenedor.
5. Mostrar en consola los datos reales obtenidos desde la API.

### SamplePipeline

Trabajo tipo Pipeline que ejecuta dos etapas secuenciales:

1. Preparation: detiene y elimina el contenedor previo si existe.
2. Build: ejecuta el trabajo BuildAppJob.

Script usado en Jenkins:

    node {
     stage('Preparation') {
      catchError(buildResult: 'SUCCESS') {
       sh 'docker stop samplerunning'
       sh 'docker rm samplerunning'
      }
     }
     stage('Build') {
      build 'BuildAppJob'
     }
    }

## Evidencias Jenkins

Las evidencias de Jenkins deben guardarse en:

    evidencias/jenkins/

Archivos requeridos:

- stage_view.png
- console_output_build.png
- credentials.png
- pipeline_script.txt

## Estructura del Proyecto

    Mi-proyecto-2/
    ├── app.py
    ├── build.sh
    ├── requirements.txt
    ├── .gitignore
    ├── README.md
    └── evidencias/
        ├── docker/
        │   └── output.txt
        └── jenkins/
            ├── stage_view.png
            ├── console_output_build.png
            ├── credentials.png
            └── pipeline_script.txt

## Seguridad

El proyecto no almacena claves, tokens ni credenciales dentro del código fuente.

Las configuraciones se manejan mediante variables de entorno. Las credenciales de GitHub utilizadas en Jenkins deben almacenarse en el gestor de credenciales de Jenkins y no deben escribirse directamente en archivos del repositorio.