#!/usr/bin/env bash

cd $(dirname $0)

if [ "$1" = "flake8" ]; then
    FLAKE8=true
    MYPY=false
    TEST=false
elif [ "$1" = "mypy" ]; then
    FLAKE8=false
    MYPY=true
    TEST=false
elif [ "$1" = "test" ]; then
    FLAKE8=false
    MYPY=false
    TEST=true
else
    FLAKE8=true
    MYPY=true
    TEST=true
fi

EXIT_STATUSES=()

if $FLAKE8 ; then
    echo ---- flake8 ----
    flake8 .
    EXIT_STATUSES=(${EXIT_STATUSES[@]} $?)
fi

if $MYPY ; then
    echo ---- mypy ----
    mypy --ignore-missing-imports tokaido
    EXIT_STATUSES=(${EXIT_STATUSES[@]} $?)
fi

if $TEST ; then
    echo ---- unit test ---
    py.test -s -vv --cov=tokaido --cov-report=term-missing .
    EXIT_STATUSES=(${EXIT_STATUSES[@]} $?)
fi

for (( I = 0; I < ${#EXIT_STATUSES[@]}; I++ )) do
    if test ${EXIT_STATUSES[$I]} -ne 0; then
        exit 1
    fi
done

exit 0
