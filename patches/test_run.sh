#!/usr/bin/env bash
python3  -u main.py --dataset=synthetic_iid --optimizer='fedavg'  \
            --learning_rate=0.01 --num_rounds=1 --clients_per_round=10 \
            --eval_every=1 --batch_size=10 \
            --num_epochs=20 \
            --model='mclr' \
            --drop_percent=0 \

