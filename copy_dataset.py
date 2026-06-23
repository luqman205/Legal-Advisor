import re

log_path = "/Users/mac/.gemini/antigravity-ide/brain/aa66cfc1-ccff-4616-9802-d808a6c85713/.system_generated/tasks/task-185.log"
target_path = "/Users/mac/Documents/legal advisor/legal_ai/dataset/legal_dataset.json"

with open(log_path, "r", encoding="utf-8") as f:
    content = f.read()

start_marker = "===DATASET_START===\n"
end_marker = "\n===DATASET_END==="

start_idx = content.find(start_marker)
end_idx = content.find(end_marker)

if start_idx != -1 and end_idx != -1:
    json_str = content[start_idx + len(start_marker):end_idx]
    with open(target_path, "w", encoding="utf-8") as f:
        f.write(json_str)
    print("Successfully copied JSON dataset to legal_ai/dataset/legal_dataset.json")
else:
    # Fallback to regex if markers are not exact
    match = re.search(r"===DATASET_START===\s*(.*?)\s*===DATASET_END===", content, re.DOTALL)
    if match:
        json_str = match.group(1)
        with open(target_path, "w", encoding="utf-8") as f:
            f.write(json_str)
        print("Successfully copied JSON dataset using regex search")
    else:
        print("Failed to find dataset markers in log file.")
