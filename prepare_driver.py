import os
import re
import urllib.request
import zipfile
import subprocess
from pathlib import Path

def get_edge_version():
    try:
        result = subprocess.check_output(
            r'reg query "HKEY_CURRENT_USER\Software\Microsoft\Edge\BLBeacon" /v version',
            shell=True, text=True
        )
        match = re.search(r'version\s+REG_SZ\s+([\d.]+)', result)
        return match.group(1) if match else None
    except Exception as e:
        print("❌ Nelze zjistit verzi Edge:", e)
        return None

def download_edgedriver(version: str, dest_folder: Path):
    url = f"https://msedgedriver.azureedge.net/{version}/edgedriver_win64.zip"
    zip_path = dest_folder / "edgedriver.zip"

    print(f"📥 Stahuji Edge WebDriver verze {version}...")
    try:
        urllib.request.urlretrieve(url, zip_path)
    except Exception as e:
        print("❌ Chyba při stahování:", e)
        return False

    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(dest_folder)
        print("✅ WebDriver rozbalen do:", dest_folder)
    except Exception as e:
        print("❌ Chyba při rozbalování:", e)
        return False
    finally:
        zip_path.unlink(missing_ok=True)

    return True

def main():
    version = get_edge_version()
    if not version:
        print("❌ Nelze pokračovat bez zjištěné verze Edge.")
        return

    driver_dir = Path(__file__).parent / "driver"
    driver_dir.mkdir(exist_ok=True)

    success = download_edgedriver(version, driver_dir)
    if success:
        print("🎉 WebDriver je připraven.")
    else:
        print("⚠️ WebDriver nebyl stažen.")

if __name__ == "__main__":
    main()