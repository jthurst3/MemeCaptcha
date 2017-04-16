#!/bin/bash

./setup_env_for_mvn.sh
mvn package
python extract_text_features.py sentences.txt out.txt