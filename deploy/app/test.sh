#!/bin/sh

/bin/sh /code/deploy/app/common.sh;
/code/deploy/app/wait-for-it.sh db:5432 -- invoke initialize_database_schema;
invoke coverage;
if [[ $RUN_COVERALLS ]]; then
    coveralls
fi