import cv2
import numpy as np


def select_roi(frame):
    """Select ROI manually using mouse"""
    roi_box = cv2.selectROI("Select ROI", frame, showCrosshair=True)
    cv2.destroyWindow("Select ROI")
    return roi_box


def detect_lanes(roi):
    """Detect lane lines inside ROI"""

    # Dilation
    kernel = np.ones((5, 5), np.uint8)
    dilated = cv2.dilate(roi, kernel, iterations=1)

    # Convert to grayscale
    gray = cv2.cvtColor(dilated, cv2.COLOR_BGR2GRAY)

    # Detect white color
    mask = cv2.inRange(gray, 215, 255)
    bitwise = cv2.bitwise_and(gray, gray, mask=mask)

    # Threshold
    thresh_val, thresh = cv2.threshold(bitwise, 150, 255, cv2.THRESH_BINARY)

    # Canny edge detection
    edges = cv2.Canny(thresh, 0.3 * thresh_val, thresh_val)

    # Hough transform
    lines = cv2.HoughLinesP(
        edges,
        rho=2,
        theta=np.pi / 180,
        threshold=30,
        minLineLength=15,
        maxLineGap=40
    )

    return lines


def main(video_path):

    cap = cv2.VideoCapture(video_path)

    ret, first_frame = cap.read()
    if not ret:
        print("Error reading video")
        return

    # Select ROI once
    x, y, w, h = select_roi(first_frame)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Crop ROI
        roi = frame[y:y + h, x:x + w]

        # Detect lanes
        lines = detect_lanes(roi)

        # Draw ROI rectangle
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

        # Draw detected lane lines
        if lines is not None:
            for line in lines:
                x1, y1, x2, y2 = line[0]

                # Adjust coordinates to original frame
                cv2.line(
                    frame,
                    (x1 + x, y1 + y),
                    (x2 + x, y2 + y),
                    (0, 255, 0),
                    3
                )

        cv2.imshow("Lane Detection", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    video_path = "../data/road01.mp4"
    main(video_path)

