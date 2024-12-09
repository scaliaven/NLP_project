#!/bin/bash

python -m molbart.fine_tune \
  --dataset UsptoTXT \
  --data_path /scratch/zl4789/hhj_updated.txt \
  --model_path /scratch/zl4789/NLP/project/Chemformer-release-1.0/models/pre-trained/combined/step=1000000.ckpt \
  --task backward_prediction \
  --epochs 100 \
  --lr 0.001 \
  --schedule cycle \
  --batch_size 128 \
  --acc_batches 4 \
  --augment all \
  --aug_prob 0.5 \
  --gpus 1 \
  # --fix_encoder \
  # --fix_decoder \
  # --add_end_layer \
  # --insert_mid_layer \

