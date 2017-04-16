#!/bin/bash
TEXT_FEATURES_DIR=$HOME/MemeCaptcha/FeatureExtraction/text-features/
export MALT_PARSER=${TEXT_FEATURES_DIR}maltparser-1.8.1/
export MALT_MODEL=${TEXT_FEATURES_DIR}engmalt.linear-1.7.mco
export CLASSPATH=${TEXT_FEATURES_DIR}stanford-english-corenlp-2016-10-31-models.jar:${TEXT_FEATURES_DIR}stanford-postagger-2016-10-31/stanford-postagger.jar:${TEXT_FEATURES_DIR}stanford-ner-2016-10-31/stanford-ner.jar
export STANFORD_MODELS=${TEXT_FEATURES_DIR}stanford-ner-2016-10-31/classifiers/:${TEXT_FEATURES_DIR}stanford-ner-2016-10-31/stanford-parser-full-2016-10-31/:${TEXT_FEATURES_DIR}stanford-postagger-2016-10-31/models/
echo "${TEXT_FEATURES_DIR}stanford-postagger-2016-10-31/models/"
