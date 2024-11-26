#!/bin/bash

python -m molbart.fine_tune \
  --dataset uspto_50 \
  --data_path ./data/seq-to-seq_datasets/uspto_50.pickle \
  --model_path ./models/pre-trained/combined/step_1000000.ckpt \
  --task backward_prediction \
  --epochs 50 \
  --lr 0.001 \
  --schedule cycle \
  --batch_size 128 \
  --acc_batches 4 \
  --augment all \
  --aug_prob 0.5 \
  --decoder_train \
  --gpus 1 \

