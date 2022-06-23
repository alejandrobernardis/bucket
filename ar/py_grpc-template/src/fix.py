import sys
from pathlib import Path

root: Path = Path(__file__).parent
sys.path.insert(0, root.joinpath("proto").as_posix())
