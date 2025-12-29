import os
import re
import json
import zipfile
import shutil
import urllib.request

# ===== CONFIG =====
GITHUB_REPO = "https://github.com/TouchController/TouchController"
BRANCH = "main"
NEW_MC_VERSION = "1.21.11"
OUTPUT_ZIP = "updated-mod-source.zip"
WORK_DIR = "workdir"
# ==================

def download_repo():
    zip_url = f"{GITHUB_REPO}/archive/refs/heads/{BRANCH}.zip"
    print("⬇️ Downloading repo...")
    urllib.request.urlretrieve(zip_url, "repo.zip")

def extract_repo():
    print("📦 Extracting repo...")
    with zipfile.ZipFile("repo.zip", "r") as z:
        z.extractall(WORK_DIR)

def find_file(root, filename):
    for root_dir, _, files in os.walk(root):
        if filename in files:
            return os.path.join(root_dir, filename)
    return None

def update_gradle_properties(path):
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    content = re.sub(
        r"minecraft_version\s*=\s*.*",
        f"minecraft_version={NEW_MC_VERSION}",
        content
    )

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

    print("✅ Updated gradle.properties")

def update_fabric_mod_json(path):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    if "depends" in data:
        data["depends"]["minecraft"] = f">={NEW_MC_VERSION}"

    if "version" in data:
        data["version"] = data["version"].split("+")[0] + f"+fabric-{NEW_MC_VERSION}"

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    print("✅ Updated fabric.mod.json")

def zip_result():
    print("🗜️ Creating output ZIP...")
    with zipfile.ZipFile(OUTPUT_ZIP, "w", zipfile.ZIP_DEFLATED) as z:
        for folder, _, files in os.walk(WORK_DIR):
            for file in files:
                full_path = os.path.join(folder, file)
                rel_path = os.path.relpath(full_path, WORK_DIR)
                z.write(full_path, rel_path)

def cleanup():
    shutil.rmtree(WORK_DIR, ignore_errors=True)
    os.remove("repo.zip")

def main():
    download_repo()
    extract_repo()

    extracted_root = os.path.join(WORK_DIR, os.listdir(WORK_DIR)[0])

    gradle = find_file(extracted_root, "gradle.properties")
    fabric = find_file(extracted_root, "fabric.mod.json")

    if gradle:
        update_gradle_properties(gradle)
    else:
        print("⚠️ gradle.properties not found")

    if fabric:
        update_fabric_mod_json(fabric)
    else:
        print("⚠️ fabric.mod.json not found")

    zip_result()
    cleanup()

    print("\n🎉 DONE")
    print(f"📥 Download: {OUTPUT_ZIP}")

if __name__ == "__main__":
    main()
