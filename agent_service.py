import win32serviceutil
import win32service
import win32event
import servicemanager
import asyncio
import websockets
import mss
import cv2
import numpy as np
from app import encrypt
import time

SERVER_URL = "ws://10.4.197.13:8000/stream"   # server IP

class ScreenShareService(win32serviceutil.ServiceFramework):
    _svc_name_ = "LocalScreenShareAgent"
    _svc_display_name_ = "Local Screen Sharing Agent"
    _svc_description_ = "Secure screen sharing agent for local admin monitoring."

    def __init__(self, args):
        super().__init__(args)
        self.stop_event = win32event.CreateEvent(None, 0, 0, None)
        self.running = True

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        self.running = False
        win32event.SetEvent(self.stop_event)

    def SvcDoRun(self):
        servicemanager.LogInfoMsg("Screen Share Service Started")
        self.main()

    def main(self):
        asyncio.run(self.stream_loop())

    async def stream_loop(self):
        with mss.mss() as sct:
            while self.running:
                screenshot = sct.grab(sct.monitors[1])
                img = np.array(screenshot)
                _, jpeg = cv2.imencode(".jpg", img, [1, 40])
                encrypted = encrypt(jpeg.tobytes())

                try:
                    async with websockets.connect(SERVER_URL) as ws:
                        await ws.send(encrypted)
                except:
                    pass

                await asyncio.sleep(0.3)   # ~3 FPS


if __name__ == '__main__':
    win32serviceutil.HandleCommandLine(ScreenShareService)
