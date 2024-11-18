#!/bin/bash

if ! command -v conda &> /dev/null
then
    echo "Conda is not available. Please install conda."
    wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O miniconda.sh
    bash miniconda.sh -b -p $HOME/miniconda
    echo "$HOME/miniconda/bin" >> $GITHUB_PATH
    source $HOME/miniconda/bin/activate
    conda init bash
fi

# Create conda env
ENV_NAME="genai-env"
conda create --name $ENV_NAME python=3.10 -y

# Activate conda env
source $HOME/miniconda/bin/activate $ENV_NAME

# install dependencies
pip install -r requirements.txt

echo "Virtual environment $ENV_NAME created and dependencies installed."
