# Hyper Tree Clone
# https://github.com/tildesarecool/Hyper-Tree-Clone.git
# initial start 12 July 2024

import os
import shutil
import multiprocessing as mp
from multiprocessing import Pool
import time
import ctypes


# Hardcoded source and destination directories for development purposes
SOURCE_DIR = "C:\\Users\\Keith\\Documents\\tiny11\\win11"
#SOURCE_DIR = "C:\\Users\\Keith\\Documents\\New folder\\Win11\\efi"
DESTINATION_DIR = "e:\\"

# Constants
FAT32_MAX_FILE_SIZE = 4 * 1024 * 1024 * 1024  # 4 GB


def get_drive_format(drive):
    """Return the file system format of the given drive."""
    drive_info = os.popen(f'fsutil fsinfo volumeinfo {drive}').read()
    if 'FAT32' in drive_info:
        return 'FAT32'
    elif 'exFAT' in drive_info:
        return 'exFAT'
    return 'UNKNOWN'


#def copy_file(file_info):
#    src, dest = file_info
#    if os.path.getsize(src) > FAT32_MAX_FILE_SIZE:
#        print(f"Skipping {src} (exceeds 4 GB)")
#        return
#    os.makedirs(os.path.dirname(dest), exist_ok=True)
#    try:
#        shutil.copy2(src, dest)
#    except OSError as e:
#        print(f"Error copying {src} to {dest}: {e}")

def copy_file(file_info):
    src, dest = file_info
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    shutil.copy2(src, dest)

def copy_files(source_dir, destination_dir):
    # Check the destination file system format
    drive_format = get_drive_format(destination_dir)

    file_list = []
    for root, _, files in os.walk(source_dir):
        for file in files:
            src_path = os.path.join(root, file)
            rel_path = os.path.relpath(src_path, source_dir)
            dest_path = os.path.join(destination_dir, rel_path)
            if drive_format == 'FAT32' and os.path.getsize(src_path) > FAT32_MAX_FILE_SIZE:
                print(f"File {src_path} exceeds FAT32 file size limit and will be skipped.")
                continue
            file_list.append((src_path, dest_path))

    # Determine the number of CPUs to use
    total_cpus = mp.cpu_count()
    avg_file_size = sum(os.path.getsize(f[0]) for f in file_list) // len(file_list) if file_list else 0
    cpu_count = min(total_cpus, max(1, avg_file_size // (sum(os.path.getsize(f[0]) for f in file_list) // total_cpus)))

    # Divide the file list into chunks for multiprocessing
    chunk_size = len(file_list) // cpu_count
    file_chunks = [file_list[i:i + chunk_size] for i in range(0, len(file_list), chunk_size)]

    with Pool(processes=cpu_count) as pool:
        pool.map(copy_files_chunk, file_chunks)
        
def copy_files_chunk(file_chunk):
    for file_info in file_chunk:
        copy_file(file_info)
        
def main():
    # Copy files from the source directory to the destination directory using multiprocessing
    print(f"starting file copy...\n")
    start_time = time.time()

    copy_files(SOURCE_DIR, DESTINATION_DIR)

    end_time = time.time()
    elapsed_time = end_time - start_time


    print(f"File copying completed in {elapsed_time:.2f} seconds")
    
if __name__ == "__main__":
    main()