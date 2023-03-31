import cv2
import numpy as np


def select_ROI(video_path):
    # Define a callback function for mouse events
    def select_roi(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            param['points'].append([(x, y)])
            param['dragging'] = True
        elif event == cv2.EVENT_MOUSEMOVE:
            if param['dragging']:
                param['points'][-1].append((x, y))
        elif event == cv2.EVENT_LBUTTONUP:
            param['dragging'] = False

    # Open the video file
    cap = cv2.VideoCapture(video_path)

    # Read the first frame
    ret, frame = cap.read()

    # Initialize the ROI parameters
    roi_params = {'points': [], 'dragging': False}

    # Create a window to display the frame
    cv2.namedWindow('Select ROI', cv2.WINDOW_NORMAL)

    # Set the callback function for mouse events
    cv2.setMouseCallback('Select ROI', select_roi, roi_params)

    # Loop over the frames in the video
    while True:
        # Copy the frame
        roi_frame = frame.copy()

        # Draw the polygons on the ROI frame if the user is selecting regions
        if len(roi_params['points']) > 0:
            for points in roi_params['points']:
                points = np.array(points, np.int32)
                cv2.fillPoly(roi_frame, [points], (0, 255, 0))

        # Display the ROI frame
        cv2.imshow('Select ROI', roi_frame)

        # Wait for a key press
        key = cv2.waitKey(1) & 0xFF

        # If the 'q' key is pressed, exit the loop
        if key == ord('q'):
            break

    # Release the video capture object and destroy the window
    cap.release()
    cv2.destroyAllWindows()

    # Combine the points into a single array and delete duplicates
    final_points = np.array(roi_params['points'][0], np.int32)
    for points in roi_params['points'][1:]:
        final_points = np.append(final_points, points, axis=0)

    print(final_points)
    return final_points


def is_in_roi(x, y, roi_arr):
    if cv2.pointPolygonTest(roi_arr, (x, y), False) >= 0:
        return True
    else:
        return False