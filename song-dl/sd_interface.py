import yt_dlp as yt
import tkinter as tk
import threading
import sys
import sd_metadata
import os


class SongDownloader:

    def __init__(self, master):
        frame1 = tk.Frame(master)
        frame1.grid(row=1, column=0, columnspan=3)
        self.data_collector = sd_metadata.MetaDataCollector()
        self.song_links = []
        sd_label = tk.Label(master, text="Song Downloader", padx=20)
        sd_label.grid(row=0, column=0, columnspan=3)

        # Song Links Entry
        links_label = tk.Label(frame1, text="Link(s):")
        links_label.grid(row=0, column=0, sticky=tk.E)
        links_entry = tk.Entry(frame1, borderwidth=5, border=5)
        links_entry.grid(row=0, column=1)
        add_button = tk.Button(frame1, text="Add", command=lambda: self.add(links_entry.get()))
        add_button.grid(row=0, column=2)

        # Remove Link
        remove_label = tk.Label(frame1, text="Remove Link #:")
        remove_label.grid(row=1, column=0, sticky=tk.E)
        remove_entry = tk.Entry(frame1, borderwidth=5, border=5)
        remove_entry.grid(row=1, column=1)
        remove_button = tk.Button(frame1, text="Remove", command=lambda: self.remove(remove_entry.get()))
        remove_button.grid(row=1, column=2)

        # Playlist Name Entry
        playlist_label = tk.Label(frame1, text="Playlist Name:")
        playlist_label.grid(row=2, column=0)
        playlist_name = tk.Entry(frame1, borderwidth=5)
        playlist_name.grid(row=2, column=1)

        # Instructions
        instr1 = tk.Label(master,
                          text="1. Enter the song url(s) you want to download (Youtube Link)")
        instr2 = tk.Label(master,
                          text="2. If multiple links make sure to separate them with commas. (EX: link1,link2,...)"
                               "\nPlease ensure there are no spaces.")
        instr3 = tk.Label(master,
                          text="3. Then press the Add button after entering links. Note this will just add the links\n"
                               "into a list, if you need to add more links, you still can following steps 1 through 3.")
        instr4 = tk.Label(master,
                          text="4. After each time you press \"Add\", the list of links will show below assigned with\n"
                               "a value. This number is important if you want to remove a certain link.")
        instr5 = tk.Label(master,
                          text="5. You can remove links one at a time just enter the correct assigned value for that\n"
                               "link and then press the \"Remove\" button to remove it.\n"
                               "The list will update below with new assigned values.")
        instr6 = tk.Label(master,
                          text="6. Don't forget to name your playlist! When ready click the \"Download\" button to\n"
                               "start the download. Playlist will show up on your desktop when done.")

        instr1.grid(row=2, column=0, columnspan=3)
        instr2.grid(row=3, column=0, columnspan=3)
        instr3.grid(row=4, column=0, columnspan=3)
        instr4.grid(row=5, column=0, columnspan=3)
        instr5.grid(row=6, column=0, columnspan=3)
        instr6.grid(row=7, column=0, columnspan=3)

        download_button = tk.Button(master, text="Download", borderwidth=5, border=5,
                                    command=lambda: self.download_thread(playlist_name.get()))
        download_button.grid(row=8, column=0, columnspan=3)

        self.console_box = tk.Text(master, height=5)
        self.console_box.grid(row=9, column=0, columnspan=3)

        # Redirect the standard output and error channels to show up on the GUI
        sys.stdout = self.TextRedirector(self.console_box)
        sys.stderr = self.TextRedirector(self.console_box)

        self.progress_label = tk.Label(master, text="Progress: Idle")
        self.progress_label.grid(row=10, column=0, columnspan=3, sticky=tk.W)

    def update_progress(self, counter, total):
        counter += 1
        percent = round((counter / total) * 100)
        self.progress_label['text'] = f'[{percent}%] - [{"#" * percent + " " * (100 - percent)}]'
        return counter

    def add(self, links):
        duplicates = False
        links = links.replace(" ", "")
        new_links = links.split(",")
        for url in new_links:
            if url in self.song_links:
                if not duplicates:
                    duplicates = True
                continue
            self.song_links.append(url)
        if duplicates:
            print("Duplicate entries were not added")
        self.update_links_list()

    def remove(self, number):
        if self.song_links:
            num = int(number)
            if num > len(self.song_links) or num <= 0:
                print("Link number doesn't exist! Try again with the correct number.")
            else:
                self.song_links.pop(int(number) - 1)
                self.update_links_list()
        else:
            print("You have no links added to the list!")

    def download(self, playlist: str):
        self.data_collector.run()
        options = {
            'format': 'bestaudio/best',
            'keepvideo': False,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'aac',
            }]
        }
        count = 0
        progress = len(self.song_links) * 3
        desktop = os.path.join(os.path.expanduser("~"), 'Desktop\\')
        # desktop = desktop.replace('\\', '/')
        self.progress_label['text'] = f'[0%] - [{" " * 100}]'
        for url in self.song_links:
            options['outtmpl'] = f"{desktop}{playlist}\\temp.aac"
            with yt.YoutubeDL(options) as ydl:
                ydl.download(url)
            count = self.update_progress(count, progress)
            album_img, title, artist, album, year = self.data_collector.get_metadata(url)
            count = self.update_progress(count, progress)
            os.system(f'ffmpeg -n -i "{desktop}{playlist}\\temp.aac"'
                      f' -id3v2_version 3 -metadata title="{title}" -metadata album_artist="{artist}"'
                      f' -metadata album="{album}" -metadata date="{year}"'
                      f' "{desktop}{playlist}\\temp.mp3"')
            os.remove(f"{desktop}{playlist}\\temp.aac")
            os.system(
                f'ffmpeg -n -i "{desktop}{playlist}\\temp.mp3" -i "{album_img}"'
                f' -c:a copy -c:v copy -map 0:0 -map 1:0 -id3v2_version 3'
                f' "{desktop}{playlist}\\{title} - {artist}.mp3"')
            os.remove(f"{desktop}{playlist}\\temp.mp3")
            count = self.update_progress(count, progress)
        self.progress_label['text'] = 'Progress: Complete!'
        self.data_collector.finish()
        music_folder = os.path.join(os.path.expanduser("~"), 'Music\\temp\\')
        os.system(f'rd /s /q {music_folder}')

    def download_thread(self, playlist):
        t = threading.Thread(target=lambda: self.download(playlist))
        t.start()

    def update_links_list(self):
        print("Current Song Link List:")
        if self.song_links:
            for idx, url in enumerate(self.song_links):
                print(f'{idx + 1}. {url}')
            print("End of List")
        else:
            print("Empty!")

    class TextRedirector(object):
        def __init__(self, widget):
            self.widget = widget

        def write(self, string):
            self.widget.insert(tk.END, string)
            self.widget.see(tk.END)

        def flush(self):
            pass


if __name__ == '__main__':
    root = tk.Tk()
    root.title('Song Downloader')
    root.iconbitmap('./images/download.ico')
    root.geometry('640x456')
    sd = SongDownloader(root)
    root.mainloop()