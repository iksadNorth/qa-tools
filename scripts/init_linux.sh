#!/bin/bash

# Install Python
sudo apt update
sudo apt install python3 python3-pip curl

# Install UV
curl -Ls https://astral.sh/uv/install.sh | sh

# Set Env Var
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
