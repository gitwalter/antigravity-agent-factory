from pathlib import Path
import shutil

base_dir = Path(
    r"d:\Users\wpoga\Documents\Python Scripts\antigravity-agent-factory\.agent\patterns\workflows"
)

categories = [
    "universal",
    "agile",
    "quality",
    "operations",
    "ai-ml",
    "blockchain",
    "trading",
    "sap",
]

for category in categories:
    target_dir = base_dir / category
    if not target_dir.exists():
        print(f"Creating directory: {target_dir}")
        target_dir.mkdir(parents=True, exist_ok=True)

    # Process both .md and .yaml files
    for file_path in base_dir.glob(f"{category}-*"):
        if file_path.is_file():
            new_name = file_path.name.replace(f"{category}-", "", 1)
            new_path = target_dir / new_name

            print(f"Moving {file_path.name} -> {category}/{new_name}")
            shutil.move(str(file_path), str(new_path))

print("Done moving files.")
