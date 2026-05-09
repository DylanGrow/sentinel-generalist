#!/bin/bash
# SENTINEL GENERALIST - Remote Server Setup Script
# This script is designed to run on a fresh Ubuntu 24.04 instance on DigitalOcean

set -e # Exit on error

echo "🚀 Starting Sentinel Generalist Setup..."

# 1. System Updates
apt update && apt upgrade -y
apt install -y python3.11 python3.11-venv python3-pip git curl wget gnupg2

# 2. Install AMD ROCM 7.0
echo "💎 Installing AMD ROCm 7.0..."
wget -q -O - https://repo.radeon.com/rocm/rocm.gpg.key | gpg --dearmor | tee /etc/apt/trusted.gpg.d/rocm.gpg > /dev/null
echo "deb [arch=amd64] https://repo.radeon.com/rocm/apt/7.0/ noble main" | tee /etc/apt/sources.list.d/rocm.list
apt update
apt install -y rocm-dkms rocm-libs rocm-dev

# 3. Environment Variables
cat >> ~/.bashrc << 'EOF'
export ROCM_HOME=/opt/rocm
export LD_LIBRARY_PATH=/opt/rocm/lib:$LD_LIBRARY_PATH
export PATH=/opt/rocm/bin:$PATH
export HSA_OVERRIDE_GFX_VERSION=gfx942
EOF
source ~/.bashrc

# 4. App Directory Setup
mkdir -p /app/backend
mkdir -p /data/models
cd /app/backend

# 5. Python Environment
python3.11 -m venv venv
source venv/bin/activate

echo "🐍 Installing Python dependencies (this takes a few minutes)..."
pip install --upgrade pip
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/rocm6.0
pip install transformers accelerate pillow numpy fastapi uvicorn python-multipart pydantic optimum[onnxruntime]

echo "✅ Setup Complete!"
echo "Next step: Run 'huggingface-cli login' and then download the model weights."
