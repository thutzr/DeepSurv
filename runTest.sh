#!/bin/bash

rm train_ci.pdf
rm total_weight.h5
echo '' >> total_weight.h5

for((i=1;i<=3;i++))
do
    python total-copy.py
done
