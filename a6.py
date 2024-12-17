import os
import sys
import requests
import zipfile
import shutil


def download_extract_and_copy(file_url, destination_folder, copy_to_path):
    """
    Download a file, extract it into the destination folder, 
    and copy the extracted folder to a specified location.
    Handles existing folders by replacing them if necessary.
    """
    # Ensure destination folder exists
    os.makedirs(destination_folder, exist_ok=True)
    
    # Get the file name from the URL
    file_name = os.path.basename(file_url)
    file_path = os.path.join(destination_folder, file_name)
    
    # Start the download
    response = requests.get(file_url, stream=True)
    if response.status_code != 200:
        raise Exception(f"Failed to download file: {file_url}. Status code: {response.status_code}")
    
    total_size = int(response.headers.get('content-length', 0))  # File size in bytes
    chunk_size = 1024 * 1024  # 1 MB chunk size
    downloaded = 0
    
    print(f"Starting download: {file_name} ({total_size / (1024 * 1024):.2f} MB)")
    with open(file_path, 'wb') as file:
        while True:
            chunk = response.raw.read(chunk_size)
            if not chunk:
                break
            file.write(chunk)
            downloaded += len(chunk)
            progress_bar(downloaded, total_size)
    
    print(f"\nFile downloaded: {file_path}")
    
    # Extract the file
    extracted_folder_path = None
    if zipfile.is_zipfile(file_path):
        print(f"Extracting {file_name} into {destination_folder}...")
        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            # Extract and get the folder name
            folder_name = zip_ref.namelist()[0].split('/')[0]
            extracted_folder_path = os.path.join(destination_folder, folder_name)
            
            # Delete existing extracted folder if present
            if os.path.exists(extracted_folder_path):
                print(f"Existing folder found: {extracted_folder_path}. Deleting...")
                shutil.rmtree(extracted_folder_path)
            
            zip_ref.extractall(destination_folder)
            print(f"Extraction complete: {extracted_folder_path}")
        
        os.remove(file_path)  # Optional: Remove the downloaded ZIP file after extraction
    
    else:
        raise Exception(f"The downloaded file is not a valid ZIP archive: {file_path}")
    
    # Copy the extracted folder to the destination path
    if extracted_folder_path:
        copy_destination = os.path.join(copy_to_path, os.path.basename(extracted_folder_path))
        print(f"Copying folder to {copy_destination}...")
        
        # Delete existing folder at the destination if present
        if os.path.exists(copy_destination):
            print(f"Existing folder found at copy destination: {copy_destination}. Deleting...")
            shutil.rmtree(copy_destination)
        
        shutil.copytree(extracted_folder_path, copy_destination)
        print(f"Copied folder to {copy_destination}")


def progress_bar(current, total, bar_length=50):
    """
    Display a progress bar for the download process.
    """
    progress = current / total
    block = int(bar_length * progress)
    percentage = progress * 100
    bar = f"[{'#' * block}{'.' * (bar_length - block)}] {percentage:.2f}%"
    sys.stdout.write(f"\r{bar}")
    sys.stdout.flush()


def get_latest_file_url(base_url):
    """
    Get the latest folder and find the required file in its subdirectories.
    """
    response = requests.get(base_url)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch URL: {base_url}. Status code: {response.status_code}")
    
    # Parse the HTML to extract links
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')
    links = [link.get('href') for link in soup.find_all('a') if link.get('href')]
    
    # Filter for folders only
    folders = [link for link in links if link.endswith('/')]
    if not folders:
        raise Exception("No folders found at the specified URL.")
    
    # Get the latest folder
    latest_folder = sorted(folders, key=lambda x: x.strip('/'))[-1]
    latest_url = base_url + latest_folder
    print(f"Latest folder: {latest_folder}")
    
    # Search for the file in the latest folder and its subdirectories
    response = requests.get(latest_url)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch URL: {latest_url}. Status code: {response.status_code}")
    
    soup = BeautifulSoup(response.text, 'html.parser')
    sub_links = [link.get('href') for link in soup.find_all('a') if link.get('href')]
    
    for link in sub_links:
        if link.endswith("T-NKLDWWC_1312.2_USB_Common.zip"):
            return latest_url + link
    
    raise Exception("Required file not found in the latest folder.")


if __name__ == "__main__":
    # Configuration
    base_url = "http://repos.net/2024/working/Nikel/"
    destination_folder = "/local/temp/downloads"
    copy_to_path = "/final/destination/folder"
    
    try:
        # Get the latest file URL
        file_url = get_latest_file_url(base_url)
        print(f"File URL: {file_url}")
        
        # Download, extract, and copy the folder
        download_extract_and_copy(file_url, destination_folder, copy_to_path)
    
    except Exception as e:
        print(f"Error: {e}")