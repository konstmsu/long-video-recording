import cv2


def main():
    from pathlib import Path
    import timeit

    cap = cv2.VideoCapture(0)
    width = 1920
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    vid_cod = cv2.VideoWriter_fourcc(*"XVID")
    output = cv2.VideoWriter("cam_video.mp4", vid_cod, 20.0, (640, 480))

    frame_count = 0
    started_at = timeit.default_timer()
    while True:
        ret, frame = cap.read()
        output.write(frame)

        elapsed = timeit.default_timer() - started_at
        frame_count += 1
        fps = frame_count / elapsed
        if frame_count % 10 == 0:
            print(f"{fps=}")


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
