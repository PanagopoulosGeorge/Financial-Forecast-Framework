import requests
from pathlib import Path

def download_local(url: str, out_path: Path, parent_mkdir: bool) -> bool:
    """Downloads from a URL to a local path."""
    if not isinstance(out_path, Path):
        raise ValueError(f"out_path: {out_path} must be a pathlib.Path object.")
    if parent_mkdir:
        out_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise ValueError(f"Error downloading {url}: {e}")
        return False

    with open(out_path, 'wb') as f:
        data = response.content
        f.write(data)
    return True