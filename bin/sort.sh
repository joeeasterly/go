#!/usr/bin/env bash

for file in *.json; do
    prefix=${file:0:1}
    subfolder=${file:1:1}

    mkdir -p "../$prefix/$subfolder"
    mv "$file" "../$prefix/$subfolder/$file"
done

