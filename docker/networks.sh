#!/bin/bash

NETWORK_NAME="services_network"

# Проверка, существует ли сеть
if ! docker network ls | grep -q "$NETWORK_NAME"; then
  echo "Сеть $NETWORK_NAME не существует. Создаём сеть..."
  docker network create "$NETWORK_NAME"
else
  echo "Сеть $NETWORK_NAME уже существует. Пропускаем создание."
fi
