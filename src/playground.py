# %%

import cv2 as cv

cap = cv.VideoCapture(0)
width = 1920
cap.set(cv.CAP_PROP_FRAME_WIDTH, width)

for a in dir(cv):
    if a.startswith("CAP_"):
        i = getattr(cv, a)
        v = cap.get(i)
        if v not in [-1.0, 0.0]:
            print(f"{a}={v}")

# backend = cap.getBackendName()
# print(".", end="")
# ret, frame = cap.read()
# cv.imwrite(f"../images2/{backend}2.png", frame)


# frame_rgb = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
# %matplotlib inline
# from matplotlib import pyplot as plt
# plt.imshow(frame_rgb)
# plt.title('my picture')
# plt.show()
# cv.imshow("frame", frame)

# cv.waitKey(0)
# cv.destroyAllWindows()
