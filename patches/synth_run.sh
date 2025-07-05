#!/usr/bin/env bash

datasets=("synthetic_iid" "synthetic_0_0" "synthetic_0.5_0.5" "synthetic_1_1")
drop_percents=(0.0 0.5 0.9)
mu_values=(0.001 0.01 0.1 1)

for dataset in "${datasets[@]}"; do
    for drop_percent in "${drop_percents[@]}"; do
        echo "Running with dataset: $dataset and drop_percent: $drop_percent"

        python3 -u main.py --dataset="$dataset" --optimizer='fedavg' \
            --learning_rate=0.01 --num_rounds=200 --clients_per_round=10 \
            --eval_every=1 --batch_size=1024 \
            --num_epochs=20 \
            --model='mclr' \
            --drop_percent="$drop_percent"

        for mu in "${mu_values[@]}"; do
            python3 -u main.py --dataset="$dataset" --optimizer='fedprox' \
                --learning_rate=0.01 --num_rounds=200 --clients_per_round=10 \
                --eval_every=1 --batch_size=1024 \
                --num_epochs=20 \
                --model='mclr' \
                --drop_percent="$drop_percent" \
                --mu="$mu"
        done
    done
done

