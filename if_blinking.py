import math
LEFT_EYE_POINTS = [36, 37, 38, 39, 40, 41]
RIGHT_EYE_POINTS = [42, 43, 44, 45, 46, 47]
LEFT_EYE_POINTS_2 = [10,11,12,13,14,15]
RIGHT_EYE_POINTS_2 = [16,17,18,19,20,21]
def list_ratio(ratio_list,ratio):
    length = len(ratio_list)
    ratio_list[0] = ratio_list[1]
    ratio_list[1] = ratio_list[2]
    ratio_list[2] =ratio_list[3]
    ratio_list[3] = ratio_list[4]
    ratio_list[4] = ratio
    ratio_avg = (ratio_list[0]+ratio_list[1]+ratio_list[2]+ratio_list[3])/4
    return ratio_list,ratio_avg
def middle_point(p1, p2):
    """Returns the middle point (x,y) between two points

    Arguments:
        p1 (dlib.point): First point
        p2 (dlib.point): Second point
    """
    x = int((p1.x + p2.x) / 2)
    y = int((p1.y + p2.y) / 2)
    return (x, y)

def blinking_ratio_1(landmarks, side):
    """Calculates a ratio that can indicate whether an eye is closed or not.
    It's the division of the width of the eye, by its height.

    Arguments:
        landmarks (dlib.full_object_detection): Facial landmarks for the face region
        points (list): Points of an eye (from the 68 Multi-PIE landmarks)

    Returns:
        The computed ratio
    """
    if side == 0:
        points = LEFT_EYE_POINTS
    else:
        points = RIGHT_EYE_POINTS
    left = (landmarks.part(points[0]).x, landmarks.part(points[0]).y)
    right = (landmarks.part(points[3]).x, landmarks.part(points[3]).y)
    top = middle_point(landmarks.part(points[1]), landmarks.part(points[2]))
    bottom = middle_point(landmarks.part(points[5]), landmarks.part(points[4]))

    eye_width = math.hypot((left[0] - right[0]), (left[1] - right[1]))
    eye_height = math.hypot((top[0] - bottom[0]), (top[1] - bottom[1]))

    try:
        ratio = eye_width / eye_height

    except ZeroDivisionError:
        ratio = None

    return ratio
def blinking_ratio_2(landmarks, side):
    """Calculates a ratio that can indicate whether an eye is closed or not.
    It's the division of the width of the eye, by its height.

    Arguments:
        landmarks (dlib.full_object_detection): Facial landmarks for the face region
        points (list): Points of an eye (from the 68 Multi-PIE landmarks)

    Returns:
        The computed ratio
    """
    if side == 0:
        points = LEFT_EYE_POINTS_2
    else:
        points = RIGHT_EYE_POINTS_2
    left = (landmarks.part(points[0]).x, landmarks.part(points[0]).y)
    right = (landmarks.part(points[3]).x, landmarks.part(points[3]).y)
    top = middle_point(landmarks.part(points[1]), landmarks.part(points[2]))
    bottom = middle_point(landmarks.part(points[5]), landmarks.part(points[4]))

    eye_width = math.hypot((left[0] - right[0]), (left[1] - right[1]))
    eye_height = math.hypot((top[0] - bottom[0]), (top[1] - bottom[1]))

    try:
        ratio = eye_width / eye_height

    except ZeroDivisionError:
        ratio = None

    return ratio
def excute_parallel(landmarks):
    left_face = [landmarks.part(0).x, landmarks.part(0).y]
    right_face = [landmarks.part(16).x, landmarks.part(16).y]
    left_eye = [landmarks.part(36).x, landmarks.part(36).y]
    right_eye = [landmarks.part(45).x, landmarks.part(45).y]
    return (left_eye[0] - left_face[0])/(right_face[0]-right_eye[0])
def excute_vertical(landmarks):
    top = landmarks.part(27).y
    middle = (landmarks.part(33).y+landmarks.part(30).y)/2
    bottom = landmarks.part(8).y
    return  (middle-top)/(bottom-middle)