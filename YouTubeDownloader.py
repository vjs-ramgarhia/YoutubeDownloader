import tkinter as tk
from tkinter import ttk, messagebox, filedialog, PhotoImage
import yt_dlp as yt
import threading
import os

# Global variables to hold progress values
downloaded_bytes = 0
total_bytes = 0
location = r"C:/YoutubeDownloads"

# YouTube Video Properties Setting
opts = {
    'format': 'best',
    'outtmpl': os.path.join(location, '%(title)s.%(ext)s'),
    'progress_hooks': []
}

def YTDownload(link, progress_callback):
    """Download video from YouTube."""
    with yt.YoutubeDL(opts) as ytd:
        try:
            ytd.add_progress_hook(progress_callback)
            vid = ytd.extract_info(link, download=True)
            return True, vid.get('title', 'Unknown Title')
        except yt.utils.DownloadError as e:
            return False, f"Download error: {str(e)}"
        except yt.utils.ExtractorError as e:
            return False, f"Extractor error: {str(e)}"
        except Exception as e:
            return False, f"An unexpected error occurred: {str(e)}"

def progress_hook(d):
    """Update the progress of the download."""
    global downloaded_bytes, total_bytes
    if d['status'] == 'downloading':
        downloaded_bytes = d['downloaded_bytes']
        total_bytes = d['total_bytes']
    elif d['status'] == 'finished':
        downloaded_bytes = total_bytes

def update_progress():
    """Update the progress bar and label."""
    if total_bytes > 0:
        progress_value = int(downloaded_bytes / total_bytes * 100)
        progress_bar['value'] = progress_value
        progress_label.config(text=f'{progress_value}%')
    window.after(100, update_progress)

def download_video():
    """Handle video download process."""
    global downloaded_bytes, total_bytes

    YoutubeLink = entry.get().strip()
    if not YoutubeLink or not YoutubeLink.startswith("http"):
        messagebox.showwarning('Warning', 'Please enter a valid YouTube URL.')
        download_button.config(state=tk.NORMAL)
        return

    downloaded_bytes = 0
    total_bytes = 0
    progress_bar['value'] = 0
    progress_label.config(text='0%')

    flag, title = YTDownload(YoutubeLink, progress_hook)

    if flag:
        op_label.config(text=f'"{title}" downloaded!')
    else:
        op_label.config(text='Error!')
        messagebox.showerror('Error', f'Error: {title}')
    
    download_button.config(state=tk.NORMAL)

def download_button_click():
    """Start download in a separate thread."""
    download_button.config(state=tk.DISABLED)
    download_thread = threading.Thread(target=download_video)
    download_thread.start()
    update_progress()

def clear_button_click():
    """Clear the input and output fields."""
    global total_bytes, downloaded_bytes
    entry.delete(0, tk.END)
    op_label.config(text="")
    progress_bar['value'] = 0
    total_bytes = 0
    downloaded_bytes = 0
    progress_label.config(text="0%")
    download_button.config(state=tk.NORMAL)

def about_button_click():
    """Show about information."""
    messagebox.showinfo('About', 'YouTube Downloader v1.0\nCreated by Vikramjit Singh')

def select_location():
    """Select a directory for downloads."""
    global opts, location
    selected_path = filedialog.askdirectory()
    if selected_path:
        location = selected_path
        opts['outtmpl'] = os.path.join(location, '%(title)s.%(ext)s')
        download_location.config(text=f'Current download location: {location}')

def open_download_location():
    """Open the download location in file explorer"""
    if os.path.exists(location):
        os.startfile(location)
    else:
        if messagebox.askyesno("Location Not Found", f"The download location '{location}' does not exist. Do you want to create it?"):
            try:
                os.makedirs(location)
                messagebox.showinfo("Success", f"The location '{location}' has been created.")
                os.startfile(location)  # Open the newly created directory
            except Exception as e:
                messagebox.showerror("Error", f"Could not create the directory: {str(e)}")

# Creating Main Window
window = tk.Tk()
window.title("YouTube Downloader")
window.geometry("700x300")
window.iconbitmap(r'C:\Users\HP\Documents\PythonLearning\YouTubeDownloader\youtube.ico')
taskbar_icon = PhotoImage(file=r'C:\Users\HP\Documents\PythonLearning\YouTubeDownloader\youtube.png')
window.iconphoto(False, taskbar_icon)

# Initialise the Style
style = ttk.Style()

# Configure Button Styling
style.configure('TButton', font=('Calibri', 12), padding=3)
style.configure('TLabel', font=('Calibri', 12))
style.configure('TEntry', font=('Calibri', 18))

# Creating Label
label = ttk.Label(window, text="Enter YouTube URL")
label.pack(pady=(10, 5))

# Creating Entry and Path Frame
entry_and_location_frame = ttk.Frame(window)
entry_and_location_frame.pack(pady=(10, 10))

# Creating Entry Widget
entry = ttk.Entry(entry_and_location_frame, width=80)
entry.pack(side=tk.LEFT, pady=(10, 10), padx=(10, 0))

# Creating Download Location Selection Button
location_button = ttk.Button(entry_and_location_frame, text="Download Location", command=select_location)
location_button.pack(side=tk.LEFT, padx=(10, 10))

# Creating Label for Current Download Location
download_location = ttk.Label(window, text=f"Current download location: {location}")
download_location.pack(pady=(0, 10))

# Creating Frame for Progress
progress_frame = ttk.Frame(window)
progress_frame.pack(pady=(10, 10))

# Creating Progress Bar
progress_bar = ttk.Progressbar(progress_frame, length=400, mode='determinate')
progress_bar.pack(side=tk.LEFT, padx=(0, 10))

# Creating Percentage Progress Label
progress_label = ttk.Label(progress_frame, text="0%")
progress_label.pack(side=tk.LEFT, padx=(10, 0))

# Creating Output Label
op_label = ttk.Label(window, text="")
op_label.pack(pady=(5, 10))

# Creating Frame for Buttons
button_frame = ttk.Frame(window)
button_frame.pack(pady=(10, 10))

# Creating Download Button
download_button = ttk.Button(button_frame, text="Download", command=download_button_click)
download_button.pack(side=tk.LEFT, padx=(0, 10))

# Creating Clear Button
clear_button = ttk.Button(button_frame, text="Clear", command=clear_button_click)
clear_button.pack(side=tk.LEFT, padx=(0, 10))

# Creating Open Download Location Button
open_folder_button = ttk.Button(button_frame, text="Open Location", command=open_download_location)
open_folder_button.pack(side=tk.LEFT, padx=(0, 10))

# Creating Exit Button
exit_button = ttk.Button(button_frame, text="Exit", command=window.destroy)
exit_button.pack(side=tk.LEFT, padx=(0, 10))

# Creating About Button
about_button = ttk.Button(button_frame, text="About", command=about_button_click)
about_button.pack(side=tk.LEFT)

# Starting the app
window.mainloop()
