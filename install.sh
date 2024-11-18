#!/bin/bash

if ! command -v conda &> /dev/null
then
    echo "Conda is not available. Please install conda."
    exit 1
fi

# Create conda env
ENV_NAME="genai-env"
conda create --name $ENV_NAME python=3.10 -y

# Activate conda env
source activate $ENV_NAME

# install dependencies
pip install -r requirements.txt

echo "Virtual environment $ENV_NAME created and dependencies installed."
