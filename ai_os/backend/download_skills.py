import urllib.request
import zipfile
import os
import shutil

def setup_skills():
    target_dir = os.path.join(os.path.dirname(__file__), "app", "skills", "data")
    if os.path.exists(target_dir):
        # Already exists, just make sure there are files
        if len(os.listdir(target_dir)) > 100:
             print("Skills already present.")
             return

    print("Downloading skills repository...")
    url = "https://github.com/sickn33/antigravity-awesome-skills/archive/refs/heads/main.zip"
    zip_path = "skills.zip"
    urllib.request.urlretrieve(url, zip_path)

    print("Extracting...")
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall("extracted_skills")

    # The zip contains a root folder "antigravity-awesome-skills-main"
    src_dir = os.path.join("extracted_skills", "antigravity-awesome-skills-main", "skills")

    if os.path.exists(target_dir):
        shutil.rmtree(target_dir)

    shutil.copytree(src_dir, target_dir)

    print(f"Successfully bundled {len(os.listdir(target_dir))} skills.")

    # Cleanup
    os.remove(zip_path)
    shutil.rmtree("extracted_skills")

if __name__ == "__main__":
    setup_skills()
