import os
import threading
import requests
import time

NUM_THREADS = 8  
FILE_URL = "https://example.com/largefile.zip"  # Replace with a valid file URL
OUTPUT_FILE = "downloaded_file.zip"

# Lock for writing to file (for safety, although each thread writes to its own file region)
file_lock = threading.Lock()

def get_file_size(url):
    """Get the file size from the Content-Length header."""
    response = requests.head(url)
    if "Content-Length" in response.headers:
        size = int(response.headers["Content-Length"])
        print(f"File size: {size} bytes")
        return size
    else:
        raise ValueError("Cannot fetch file size. Server might not support range requests.")

def download_chunk(url, start, end, thread_id, output_file, speed_dict, progress_dict):
    """Download a specific chunk of the file and track speed."""
    headers = {"Range": f"bytes={start}-{end}"}
    response = requests.get(url, headers=headers, stream=True)

    # Check if server supports range requests
    if response.status_code != 206:
        print(f"Thread {thread_id}: Warning! Server did not return Partial Content (206). Got {response.status_code}.")
    
    start_time = time.time()
    total_downloaded = 0

    with open(output_file, "r+b") as f:
        f.seek(start)
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                # Write chunk under a lock for safety (each thread writes to its own region)
                with file_lock:
                    f.write(chunk)
                total_downloaded += len(chunk)
                progress_dict[thread_id] = total_downloaded

                elapsed_time = time.time() - start_time
                if elapsed_time > 0:
                    # Save speed in KB/s
                    speed_dict[thread_id] = (total_downloaded / elapsed_time) / 1024

    print(f"\nThread {thread_id} finished downloading {total_downloaded} bytes.")

def print_speed(speed_dict, progress_dict, total_size):
    """Continuously print the download speed of each thread and overall speed."""
    while any(thread.is_alive() for thread in threads):
        total_speed = sum(speed_dict.values())  # Overall speed in KB/s
        downloaded_size = sum(progress_dict.values())
        percent_complete = (downloaded_size / total_size) * 100

        # Build a string showing each thread's speed
        speed_info = ""
        for i in range(NUM_THREADS):
            speed_info += f"Thread {i+1}: {speed_dict[i]:.2f} KB/s | "
        print(f"\r{speed_info}Total: {total_speed:.2f} KB/s | {percent_complete:.2f}% completed", end="", flush=True)
        
        time.sleep(1)
    print("")

def multi_thread_download(url, output_file, num_threads):
    """Download a file using multiple threads and display speed per thread."""
    file_size = get_file_size(url)
    chunk_size = file_size // num_threads

    # Create an empty file of the correct size
    with open(output_file, "wb") as f:
        f.truncate(file_size)

    global threads
    threads = []
    speed_dict = {i: 0 for i in range(num_threads)}      # Speed per thread (KB/s)
    progress_dict = {i: 0 for i in range(num_threads)}   # Bytes downloaded per thread

    # Start download threads
    for i in range(num_threads):
        start = i * chunk_size
        end = (start + chunk_size - 1) if i < num_threads - 1 else file_size - 1
        thread = threading.Thread(target=download_chunk, args=(url, start, end, i, output_file, speed_dict, progress_dict))
        threads.append(thread)
        thread.start()

    # Start speed monitor thread
    speed_thread = threading.Thread(target=print_speed, args=(speed_dict, progress_dict, file_size), daemon=True)
    speed_thread.start()

    for thread in threads:
        thread.join()

    print("\nDownload complete!")

if __name__ == "__main__":
    multi_thread_download(FILE_URL, OUTPUT_FILE, NUM_THREADS)