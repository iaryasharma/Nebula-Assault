import cv2
import mediapipe as mp
import math
import time

class FingerTracker:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands()
        self.mp_drawing = mp.solutions.drawing_utils
        self.cap = cv2.VideoCapture(0)  # Initialize webcam
        self.last_gun_pose_time = 0
        self.gun_pose_cooldown = 0.5  # 0.5 seconds cooldown

    def calculate_distance(self, point1, point2):
        """Calculate the Euclidean distance between two points."""
        return math.sqrt((point1.x - point2.x) ** 2 + (point1.y - point2.y) ** 2)

    def is_gun_trigger_pose(self, hand_landmarks):
        """Check if the index finger is bent to imitate a gun trigger."""
        index_finger_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_TIP]
        index_finger_dip = hand_landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_DIP]
        index_finger_pip = hand_landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_PIP]

        # Check if the index finger is bent (distance between TIP and DIP is small)
        return self.calculate_distance(index_finger_tip, index_finger_dip) < self.calculate_distance(index_finger_dip, index_finger_pip) * 0.5

    def is_index_finger_straight(self, hand_landmarks):
        """Check if the index finger is straight, used for movement."""
        index_finger_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_TIP]
        index_finger_pip = hand_landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_PIP]
        index_finger_mcp = hand_landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_MCP]

        # Check if the index finger is straight by comparing distances
        return self.calculate_distance(index_finger_tip, index_finger_pip) > self.calculate_distance(index_finger_pip, index_finger_mcp) * 0.8

    def track_fingers(self):
        ret, frame = self.cap.read()
        frame = cv2.flip(frame, 1)  # Flip horizontally for better UX
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = self.hands.process(frame_rgb)

        if result.multi_hand_landmarks:
            for hand_landmarks in result.multi_hand_landmarks:
                self.mp_drawing.draw_landmarks(frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)

                # Check for gun trigger pose to trigger shooting
                if self.is_gun_trigger_pose(hand_landmarks):
                    current_time = time.time()
                    if current_time - self.last_gun_pose_time > self.gun_pose_cooldown:
                        self.last_gun_pose_time = current_time
                        return None, None, "shoot"

                # Check if the index finger is straight for movement
                if self.is_index_finger_straight(hand_landmarks):
                    index_finger_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_TIP]
                    return index_finger_tip.x * frame.shape[1], index_finger_tip.y * frame.shape[0], "move"

        cv2.imshow('Finger Tracking', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            return None, None, None

        return None, None, None

    def release(self):
        self.cap.release()
        cv2.destroyAllWindows()
