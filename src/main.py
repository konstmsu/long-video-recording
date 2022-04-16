from dataclasses import dataclass
from pathlib import Path
from time import sleep
from typing import Dict, List

import cv2
from cv2 import Mat

from timed import FpsCounter, TimedCode


def imwrite(path: Path, frame: Mat) -> None:
    retval = cv2.imwrite(path, frame)
    if not retval:
        raise Exception(f"Failed to write to {path}")


class VideoWriter:
    def __init__(self, path: Path):
        self.path = path
        self.vid_cod = None
        self.output = None

    def write(self, frame: Mat) -> None:
        if self.output is None:
            height, width, _channels = frame.shape
            self.vid_cod = cv2.VideoWriter_fourcc(*"XVID")
            self.output = cv2.VideoWriter(
                str(self.path), self.vid_cod, 30.0, (width, height)
            )

        self.output.write(frame)

    def close(self) -> None:
        if self.output:
            self.output.release()


def main():
    timed = TimedCode()

    with timed.section("setup"):
        cap = cv2.VideoCapture(0)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)

        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        vid_cod = cv2.VideoWriter_fourcc(*"XVID")
        output = cv2.VideoWriter("cam_video.mp4", vid_cod, 30.0, (width, height))

    fps_counter = FpsCounter()
    while True:
        with timed.section("read frame"):
            ret, frame = cap.read()

        imwrite(f"./images/{fps_counter.frame_count}.png", frame)

        with timed.section("write frame"):
            output.write(frame)

        fps_counter.increment()
        if fps_counter.frame_count % 10 == 0:
            print(fps_counter.summary())


def main2():
    cap = cv2.VideoCapture(cv2.CAP_VFW)

    fourcc = cv2.VideoWriter_fourcc(*"X264")
    out = cv2.VideoWriter("output2.avi", fourcc, 20.0, (640, 480))

    frames_written = 0
    while cap.isOpened() and frames_written < 100:
        ret, frame = cap.read()
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break
        frame = cv2.flip(frame, 0)
        # write the flipped frame
        out.write(frame)
        frames_written += 1

    print("done")


if __name__ == "__main__":
    main()
