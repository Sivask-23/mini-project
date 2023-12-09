import cv2
import mediapipe as mp
import pyautogui as pl
import time

def count_fingers(lst):
    count = 0

    thresh = (lst.landmark[0].y*100 - lst.landmark[9].y*100) / 2    # thresh is the half of palm length

    if (lst.landmark[5].y*100 - lst.landmark[8].y*100) > thresh:        # mappinmg fingers finger1
        count += 1

    if (lst.landmark[9].y*100 - lst.landmark[12].y*100) > thresh:        # finger2
        count += 1

    if (lst.landmark[13].y*100 - lst.landmark[16].y*100) > thresh:        # finger3
        count += 1

    if (lst.landmark[17].y*100 - lst.landmark[20].y*100) > thresh:        # finger4
        count += 1

    if (lst.landmark[5].x*100 - lst.landmark[4].x*100) > 5:     # calculation for thumb finger
        count += 1

    return count


cap = cv2.VideoCapture(0)   # creating object cap for opencv

drawing = mp.solutions.drawing_utils    # for drawing keypoints of hands on frame
hands = mp.solutions.hands  # for refernce
hands_obj = hands.Hands(max_num_hands=1)   # CREATING OBJ AND passing max num of hands should detect in a frame

start_init = False

prev = -1

while True:  # starting infifnity true loop

    end_time = time.time()
    _, frm = cap.read()     # reading frames from cap and store it in frm object
    frm = cv2.flip(frm, 1)

    result = hands_obj.process(cv2.cvtColor(frm, cv2.COLOR_BGR2RGB))    # convrting to rgb

    if result.multi_hand_landmarks:
        hand_keypoints = result.multi_hand_landmarks[0]

        count = count_fingers(hand_keypoints)     # passing count of fingers


        if not(prev == count):
            if not(start_init):
                start_time = time.time()
                start_init = True
            elif (end_time - start_time) > 0.5:
                if (count == 1):
                    pl.press("right")
                elif (count == 2):
                    pl.press("left")
                elif (count == 3):
                    pl.press("up")
                elif (count == 4):
                    pl.press("down")
                elif (count == 5):
                    pl.press("space")
                prev == count
                start_init = False


        drawing.draw_landmarks(frm, hand_keypoints, hands.HAND_CONNECTIONS)


    cv2.imshow("window", frm)   # showng frame to user

    if cv2.waitKey(1) == 27:   # 27 is the code for escape button and exit while true loop when esc is pressed
        cv2.destroyAllWindows()
        cap.release()    # releasing camera resourse from cap
        break