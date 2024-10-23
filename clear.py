import sys
import pathlib
import shutil

if __name__ != "__main__":
    print("This script should not be run directly.")
    sys.exit(1)


# Remove images/ folder if it exists
if pathlib.Path("images").exists():
    shutil.rmtree("images")

# Remove all .csv files
for file in pathlib.Path().glob("*.csv"):
    file.unlink()

# Remove all .pdf files
for file in pathlib.Path().glob("*.pdf"):
    file.unlink()

print("All files removed successfully.")
