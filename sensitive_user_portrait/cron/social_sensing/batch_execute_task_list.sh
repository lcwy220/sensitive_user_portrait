#!/bin/bash

for i in {1..144}
do
    echo $i
    python task_list.py $i
done
