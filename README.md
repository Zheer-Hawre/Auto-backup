# Project 2: Automatic Backup

### What it is
A CLI tool that takes a folder you care about (like your "Documents" or a "Coding" folder) and saves a compressed `.zip` copy of it in a backup location. Every backup gets a date and time in its name (e.g. `Documents_2026-10-23_14-05-09.zip`), so you can keep many versions side by side and go back to any of them.

### Why it's useful
- **Protects against mistakes**: deleted a file or broke your code? Unzip yesterday's backup.
- **Before risky changes**: back up a project before a big refactor, an OS upgrade, or running a script that edits files (like the renamer in project 3).
- **Easy to move**: one `.zip` file is simple to copy to a USB drive, external disk, or cloud folder (Google Drive, Dropbox).
- **Automatable**: because it accepts arguments, it can run on a schedule with `cron` (see below), so backups happen without you remembering.

Note: this is a *backup* tool, not a sync tool. Each run creates a new full zip; it doesn't keep two folders mirrored.

### How it works
1. **Paths**: it takes the folder to back up (source) and where to save the zip (destination), either from the command line or by asking you. `~` and quotes (added when you drag a folder into the terminal) are handled.
2. **Safety checks**: it stops if the source folder doesn't exist, or if the destination is *inside* the source. (Otherwise the zip would try to include itself and grow until your disk is full.)
3. **Timestamping**: it uses the current date and time, down to the second, so two backups never overwrite each other.
4. **Zipping**: it uses Python's built-in `shutil.make_archive` to compress the whole folder, including sub-folders, into one `.zip`.
5. **Verification**: it prints where the backup was saved and its size.

### Requirements
Python 3.8+ only. No extra libraries.

### How to run it

**Interactive** (it asks you questions):
```bash
cd auto_backup
python3 backup.py
```
```
--- Automatic Backup Tool ---
Enter the path of the folder you want to backup: ~/Documents
Enter the path where you want to save the backup: ~/Backups
Enter a name for this backup [Documents]:            <- press Enter to accept
Created backup directory: /home/you/Backups
Starting backup of: /home/you/Documents
✅ Success! Backup created at: /home/you/Backups/Documents_2026-10-23_14-05-09.zip
Size: 12.40 MB
```

**With arguments** (no questions, good for scripts):
```bash
python3 backup.py SOURCE DESTINATION [NAME]
python3 backup.py ~/Documents /media/usb/Backups
python3 backup.py "~/coding/automation projects" ~/Backups automation
```
Put paths with spaces in quotes. The exit status is `0` on success and `1` on failure.

### Run it automatically every day (Linux/macOS)
Open your crontab with `crontab -e` and add a line like this to back up every day at 18:00:
```
0 18 * * * /usr/bin/python3 /full/path/to/auto_backup/backup.py /home/you/Documents /home/you/Backups
```
Use full paths in cron. Old backups are not deleted automatically, so clear out old zips now and then.

### Restoring a backup
Unzip it anywhere: double-click it in your file manager, or run `unzip Documents_2026-10-23_14-05-09.zip -d restored/`.

### Limitations
- Each backup is a full copy, so large folders produce large zips every time.
- Symlinks are followed and empty folders may be skipped (normal `shutil` zip behaviour).
- Files that are open and changing during the backup may be saved half-written.
