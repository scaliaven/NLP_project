#!/bin/bash

python -m molbart.fine_tune \
  --dataset uspto_50 \
  --data_path /gpfsnyu/scratch/hh3043/Chemformer/data/seq-to-seq_datasets/uspto_50.pickle \
  --model_path /gpfsnyu/scratch/hh3043/Chemformer/models/pre-trained/combined/step_1000000.ckpt \
  --task backward_prediction \
  --epochs 100 \
  --lr 0.001 \
  --schedule cycle \
  --batch_size 128 \
  --acc_batches 4 \
  --augment all \
  --aug_prob 0.5 \
  --gpus 1 \
  --fix_encoder \
  # --encoder_lora \
  --fix_encoder \
  # --fix_encoder \
  # --fix_decoder \
  # --add_end_layer \
  # --insert_mid_layer \

