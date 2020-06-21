import os

HOST_NAME = 'frws0'
PORT = 15676

SAVE_DIRS = [
    '/mnt/hgfs/mingdfs/frws'
]

for SAVE_DIR in SAVE_DIRS:
    if not os.path.exists(SAVE_DIR):
        os.makedirs(SAVE_DIR) # mkdir -p