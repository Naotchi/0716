#!/bin/bash
mkdir imgs
python3 take_a_picture.py
python3 predict.py
rm -r imgs
