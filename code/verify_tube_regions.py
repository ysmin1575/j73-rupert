"""Verify every shipped j45-region-v1 region with the checker v2 kernel."""
from pathlib import Path
import sys
sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent/'checker'))
from check import replay_region, regions

if __name__ == '__main__':
    import json
    print(json.dumps(regions(Path(__file__).resolve().parents[1])))
