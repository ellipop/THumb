import cv2
import mediapipe as mp

mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_draw = mp.solutions.drawing_utils
cap = cv2.VideoCapture(0)

finger_tips = [8, 12, 16, 20]
thumb_tip = 4
finger_hold_status = []

while True:
    ret,img = cap.read()
    img = cv2.flip(img, 1)
    h,w,c = img.shape
    results = hands.process(img)


    if results.multi_hand_landmarks:
        for hand_landmark in results.multi_hand_landmarks:
            # Acceder a los puntos de referencia por su posición
            Im_list=[]
            for id ,tip in enumerate(hand_landmark.landmark):
                Im_list.append(tip)

             # El código va aquí  
            x,y = int(Im_list[tip].x*w), int(Im_list[tip].y*h)
            cv2.circle(img, (x,y), 15, (255,0,0), cv2.FILLED)

            if Im_list[tip].x < Im_list[tip -3].x:
                cv2.circle(img, (x,y), 15, (0,255,0), cv2.FILLED)
                finger_hold_status.append(True)
            else:
                finger_hold_status.append(False)

            if all(finger_hold_status):
                if Im_list[thumb_tip].y < Im_list[thumb_tip-1].y < Im_list[thumb_tip-2].y:
                    print("thumbs up")
                    cv2.putText(img, "thumbs up", (20,30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 3)
                if Im_list[thumb_tip].y > Im_list[thumb_tip-1].y > Im_list[thumb_tip-2].y:
                    print("thumbs down")
                    cv2.putText(img, "thumbs down", (20,30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 3)



            mp_draw.draw_landmarks(img, hand_landmark,
            mp_hands.HAND_CONNECTIONS, mp_draw.DrawingSpec((0,0,255),2,2),
            mp_draw.DrawingSpec((0,255,0),4,2))
    

    cv2.imshow("Rastreo de manos", img)
    cv2.waitKey(1)
