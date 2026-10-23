import shutil
import os
import sys
from datetime import datetime


def clean_path(text):
    """Turn what the user typed into a usable absolute path.

    Handles '~' (home folder) and the quotes a terminal adds when you
    drag a folder into it, e.g. '/home/me/My Documents'.
    """
    text = text.strip().strip("'\"")
    return os.path.abspath(os.path.expanduser(text))


def ask(prompt, default=None):
    """Ask a question; return the default if the user just presses Enter."""
    suffix = f" [{default}]" if default else ""
    answer = input(f"{prompt}{suffix}: ").strip()
    return answer or default or ""


def create_backup(source_dir=None, backup_dir=None, backup_name=None):
    # --- CONFIGURATION ---
    # Values can come from the command line:  python3 backup.py SOURCE DESTINATION [NAME]
    # Anything not given is asked for interactively. If both paths are given,
    # nothing is asked, so the script can run unattended (e.g. from cron).
    print("--- Automatic Backup Tool ---")
    interactive = not (source_dir and backup_dir)
    source_dir = clean_path(source_dir or ask("Enter the path of the folder you want to backup"))
    backup_dir = clean_path(backup_dir or ask("Enter the path where you want to save the backup"))
    default_name = os.path.basename(source_dir)
    if not backup_name:
        backup_name = ask("Enter a name for this backup", default=default_name) if interactive else default_name

    # 1. Check that the source is an existing folder (not a file or a typo)
    if not os.path.isdir(source_dir):
        print(f"❌ Error: Source folder '{source_dir}' does not exist.")
        return False

    # 2. Refuse to save the backup inside the folder being backed up.
    #    The zip would end up containing itself and grow until the disk is full.
    if os.path.commonpath([source_dir, backup_dir]) == source_dir:
        print("❌ Error: The backup location cannot be inside the folder you are backing up.")
        print("   Choose a folder outside it, e.g. an external drive or ~/Backups.")
        return False

    # 3. Create the backup directory if it doesn't exist
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
        print(f"Created backup directory: {backup_dir}")

    # 4. Generate a timestamp (Year-Month-Day_Hour-Minute-Second) so every backup gets a unique name
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    # 5. Create the full path for the zip file (shutil adds .zip automatically)
    backup_path = os.path.join(backup_dir, f"{backup_name}_{timestamp}")

    print(f"Starting backup of: {source_dir}")

    try:
        # 6. Create the ZIP archive
        archive_name = shutil.make_archive(backup_path, 'zip', source_dir)

        # 7. Get file size for feedback
        file_size = os.path.getsize(archive_name) / (1024 * 1024)  # Convert to MB

        print(f"✅ Success! Backup created at: {archive_name}")
        print(f"Size: {file_size:.2f} MB")
        return True

    except Exception as e:
        print(f"❌ Backup failed: {e}")
        return False


if __name__ == "__main__":
    ok = create_backup(*sys.argv[1:4])
    sys.exit(0 if ok else 1)
