import cv2
from pathlib import Path
from contextlib import closing, contextmanager
from main import VideoWriter
from utils import Paths


@contextmanager
def temp_file(path: Path):
    if isinstance(path, str):
        path = Path(path)

    try:
        yield path
    finally:
        if path.exists():
            path.unlink()


def test_video_size():
    image_paths = sorted((Paths.root / "images").glob("*.png"))
    assert len(image_paths) == 90

    with temp_file("test_video.mp4") as output_path, closing(
        VideoWriter(output_path)
    ) as writer:
        for image_path in image_paths:
            image = cv2.imread(str(image_path))
            writer.write(image)

        assert writer.path.stat().st_size == 12_320_812
