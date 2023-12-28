#!/bin/bash

files=(
https://storage.yandexcloud.net/datasouls-ods/materials/f90231b6/items.csv
https://storage.yandexcloud.net/datasouls-ods/materials/6503d6ab/users.csv
https://storage.yandexcloud.net/datasouls-ods/materials/04adaecc/interactions.csv
)
for str in ${files[@]}; do
  wget $str -P ./data
done
