from channels.generic.websocket import AsyncWebsocketConsumer
import json
import cv2
import mediapipe as mp
import time
import asyncio

class SomeConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

        # Initialize video capture
        self.cap = cv2.VideoCapture(0)

        # Initialize MediaPipe Hands
        self.mpHands = mp.solutions.hands.Hands()
        self.mpDraw = mp.solutions.drawing_utils

        # Time variables for FPS calculation
        self.pTime = 0

        # Start processing frames asynchronously
        asyncio.create_task(self.process_frames())

    async def disconnect(self, close_code):
        # Release video capture and cleanup
        self.cap.release()
        cv2.destroyAllWindows()

    async def process_frames(self):
        while self.cap.isOpened():
            success, img = self.cap.read()
            if not success:
                break

            # Mirror the image
            img = cv2.flip(img, 1)

            imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            results = self.mpHands.process(imgRGB)

            if results.multi_hand_landmarks:
                for handLms in results.multi_hand_landmarks:
                    for id, lm in enumerate(handLms.landmark):
                      if id==8:
                        h, w, c = img.shape
                        cx, cy = int(lm.x * w), int(lm.y * h)
                        cv2.circle(img, (cx, cy), 15, (139, 0, 0), cv2.FILLED)
                        # Send coordinates to WebSocket client
                        data = {"x": cx, "y": cy}
                        print('coordinares are :',cx,":",cy)
                        
                        await self.send(text_data=json.dumps(data))

                    # Draw hand landmarks (update according to your MediaPipe version)
                    self.mpDraw.draw_landmarks(img, handLms, mp.solutions.hands.HAND_CONNECTIONS)

            # Calculate FPS and display on the frame
            cTime = time.time()
            fps = 1 / (cTime - self.pTime)
            self.pTime = cTime

            cv2.putText(
                img,
                f"FPS: {int(fps)}",
                (10, 70),
                cv2.FONT_HERSHEY_SIMPLEX,
                3,
                (139, 0, 0),
                3,
            )

            cv2.imshow("Image", img)

            if cv2.waitKey(1) & 0xFF == ord('q'):
              break

            # Delay to match frame rate (optional)
            await asyncio.sleep(0.1)  # Adjust as needed for desired frame rate

        self.cap.release()
        cv2.destroyAllWindows()