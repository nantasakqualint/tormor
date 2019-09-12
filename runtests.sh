#!/bin/bash
set -eux
cd $(dirname 0)
bash tormor/tests/cleanup.sh
bash tormor/tests/bootstrap.sh
export SCHEMA_PATH="$(pwd)/tests/Schema" && pytest -v $*
