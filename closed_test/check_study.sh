#!/bin/sh
optuna studies --storage "postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_ENDPOINT}:5432/${POSTGRES_DB}" | grep closed_test > /dev/null
echo $?