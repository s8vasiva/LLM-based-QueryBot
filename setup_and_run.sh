#!/bin/bash

# ----------------------------
# Step 0: Variables
# ----------------------------
ENV_NAME="myvenv"
PYTHON_VERSION="3.11"
APP_FILE="bot.py"  # change if your app filename is different
CONDA_DIR="$HOME/miniconda3"

# ----------------------------
# Step 1: Download Miniconda for Mac M1/M2/M4 (Apple Silicon)
# ----------------------------
if [ ! -d "$CONDA_DIR" ]; then
    echo "Downloading Miniconda for Apple Silicon..."
    curl -O https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-arm64.sh
    bash Miniconda3-latest-MacOSX-arm64.sh -b -p "$CONDA_DIR"
    rm Miniconda3-latest-MacOSX-arm64.sh
    # Initialize Conda for zsh
    eval "$($CONDA_DIR/bin/conda shell.zsh hook)"
    conda init zsh
else
    echo "Miniconda already installed at $CONDA_DIR"
    eval "$($CONDA_DIR/bin/conda shell.zsh hook)"
fi

# ----------------------------
# Step 2: Create the environment (if not exists)
# ----------------------------
if ! conda info --envs | grep -q "$ENV_NAME"; then
    echo "Creating Conda environment '$ENV_NAME' with Python $PYTHON_VERSION..."
    conda create -y -n $ENV_NAME python=$PYTHON_VERSION
else
    echo "Environment '$ENV_NAME' already exists."
fi

# ----------------------------
# Step 3: Activate the environment
# ----------------------------
conda activate $ENV_NAME

# ----------------------------
# Step 4: Install required packages
# ----------------------------
echo "Installing packages..."
pip install --upgrade pip
pip install streamlit huggingface-hub transformers sentence-transformers torch faiss-cpu

# ----------------------------
# Step 5: Run your Streamlit app
# ----------------------------
echo "Launching Streamlit app..."
streamlit run $APP_FILE
