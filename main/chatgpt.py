import torch, numpy as np, platform, sys
print("torch:", torch.__version__, "| CUDA:", torch.version.cuda)
print("torch.cuda.is_available:", torch.cuda.is_available())
print("numpy:", np.__version__)
print("python:", platform.python_version())
