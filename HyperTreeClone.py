# Hyper Tree Clone
# https://github.com/tildesarecool/Hyper-Tree-Clone.git
# initial start 12 July 2024

import os, shutil, time, threading, argparse
import multiprocessing as mp
from multiprocessing import Pool
#import ctypes

# Flag to control the progress indicator thread
progress_indicator_running = False

# Hardcoded source and destination directories for development purposes
#SOURCE_DIR = "C:\\Users\\Keith\\Documents\\tiny11\\win11"
#SOURCE_DIR = "C:\\Users\\Keith\\Documents\\New folder\\Win11\\efi"
#DESTINATION_DIR = "C:\\Users\\Keith\\Documents\\tiny11\\New Folder"
#DESTINATION_DIR = "e:\\new folder"

# Constants
FAT32_MAX_FILE_SIZE = 4 * 1024 * 1024 * 1024  # 4 GB


def get_drive_format(path):
    """Return the file system format of the given path."""
    drive = os.path.splitdrive(path)[0]
    if not drive:
        raise ValueError("Invalid path: no drive letter found.")
    drive_info = os.popen(f'fsutil fsinfo volumeinfo {drive}').read()
    if 'FAT32' in drive_info:
        return 'FAT32'
    return 'OTHER'

def copy_file(file_info):
    src, dest = file_info
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    shutil.copy2(src, dest)    
    
    
def copy_files(source_dir, destination_dir):
    # Check the destination file system format
    drive_format = get_drive_format(destination_dir)

    # If the destination is FAT32, check for files larger than 4GB
    if drive_format == 'FAT32':
        for root, _, files in os.walk(source_dir):
            for file in files:
                src_path = os.path.join(root, file)
                if os.path.getsize(src_path) > FAT32_MAX_FILE_SIZE:
                    print(f"Error: The file {src_path} exceeds the 4GB limit of FAT32 file system.")
#                    print(f"Options - Assuming WIM file: \n1. Split the WIM file into two files (beyond the scope of this script). \
#\n2. Select a destination not formatted with FAT32 and see if WIM file can be shrunk then try copy again.")
                    print("Copy operation aborted.")
                    return False

    # Gather all files to be copied
    file_list = []
    for root, _, files in os.walk(source_dir):
        for file in files:
            src_path = os.path.join(root, file)
            rel_path = os.path.relpath(src_path, source_dir)
            dest_path = os.path.join(destination_dir, rel_path)
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
    return True

def copy_files_chunk(file_chunk):
    for file_info in file_chunk:
        copy_file(file_info)

def progress_indicator():
    """Print a period to indicate progress every 20 seconds."""
    global progress_indicator_running
    start_time = time.time()
    
    while progress_indicator_running:
        time.sleep(1)
        elapsed_time = time.time() - start_time
        if int(elapsed_time) % 20 == 0:
            print("#", end="", flush=True)

def main():
    # Copy files from the source directory to the destination directory using multiprocessing

    global progress_indicator_running



    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Hyper Tree Clone Utility")
    parser.add_argument("source", help="Source directory")
    parser.add_argument("destination", help="Destination directory")
    args = parser.parse_args()

    source_dir = args.source
    destination_dir = args.destination

#    source_dir = "\"" + source_dir
#    source_dir = source_dir + "\""
    print(f"value of source dir is {source_dir} and file type is {type(source_dir)}")

    start_time = time.time()
    
    # progress indicator thread 

    progress_indicator_running = True
    indicator_thread = threading.Thread(target=progress_indicator)
    indicator_thread.start()

    try:
        # start the copy operation
        print(f"starting file copy...\n")
        copyOperation = copy_files(source_dir, destination_dir)
    finally:
        # stop progress indicator thread
        progress_indicator_running = False
        indicator_thread.join()

    end_time = time.time()
    elapsed_time = end_time - start_time
    
    minutes = int(elapsed_time // 60)
    seconds = elapsed_time % 60
    if minutes > 0:
        total_elapsed_time = f"{minutes} minutes and {seconds:.2f} seconds"
    else:
        total_elapsed_time = f"{seconds:.2f} seconds"

    if copyOperation:
        print(f"\nFile copying completed in {total_elapsed_time}.")



if __name__ == "__main__":
    main()
#     drive_format = get_drive_format(DESTINATION_DIR)
#     print(f"value of drive format is {drive_format}")