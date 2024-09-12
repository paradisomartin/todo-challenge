#!/bin/bash

# Asegúrate de que el script se detenga si hay algún error
set -e

# Función para ejecutar comandos de Django
run_django_command() {
    docker-compose run --rm backend python manage.py "$@"
}

# Manejo de comandos
case "$1" in
    makemigrations)
        run_django_command makemigrations "${@:2}"
        ;;
    migrate)
        run_django_command migrate "${@:2}"
        ;;
    createsuperuser)
        run_django_command createsuperuser "${@:2}"
        ;;
    test)
        run_django_command test "${@:2}"
        ;;
    shell)
        run_django_command shell_plus "${@:2}"
        ;;
    *)
        echo "Uso: $0 {makemigrations|migrate|createsuperuser|test|shell}"
        exit 1
        ;;
esac
