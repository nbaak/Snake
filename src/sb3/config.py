
import os

TIMESTEPS = 10_000  # save every n steps

# saving
OUT_FILE_NAME  = "PPOv7" # should contain the algorithm
out_models_dir = f"models/{OUT_FILE_NAME}"

# loading
IN_FILE_NAME = "PPOv6"
in_model_file = "2940000"
in_models_dir = f"models/{IN_FILE_NAME}"
in_model_path = f"{in_models_dir}/{in_model_file}"

# logging
logdir = "logs"

def ensure_dirs():
    if not os.path.exists(out_models_dir):
        os.makedirs(out_models_dir)
        
    if not os.path.exists(logdir):
        os.makedirs(logdir)