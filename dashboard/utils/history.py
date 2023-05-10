import json
import os


def add_to_json_file(filepath: str, *j_data: dict):
    if not os.path.exists(filepath):
        with open(filepath, 'w') as f:
            json.dump([], f, indent=4)
            f.truncate()
    with open(filepath, 'r+') as f:
        file_content = json.load(f)
        for data in j_data:
            file_content.append(data)
        f.seek(0)
        json.dump(file_content, f, indent=4, default=str)
        f.truncate()


def get_json_file_data(filepath: str) -> list[dict]:
    if not os.path.exists(filepath):
        return []
    with open(filepath, 'r') as f:
        return json.load(f)


async def add_to_json_file_async(filepath: str, *j_data: dict):
    """similar to add_to_json_file but works asynchronously."""
    if not os.path.exists(filepath):
        with open(filepath, 'w') as f:
            json.dump([], f, indent=4)
            f.truncate()

    with open(filepath, 'r+') as f:
        file_content = await json.load(f)
        for data in j_data:
            file_content.append(data)
        await f.seek(0)
        await json.dump(file_content, f, indent=4)
        await f.truncate()

