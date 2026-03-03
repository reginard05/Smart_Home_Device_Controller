from device import Device, time

class SmartLight(Device):
    def __init__(self, device_ID: str, power_rate: float):
        super().__init__(device_ID, power_rate)
        self.__recording_status: bool = False
        self.__motion_detection: bool = False
        
    def turn_off(self) -> bool:
        if self.__recording_status ==  True:
            return False
        else:
            return super().turn_off()

    def start_recording(self) -> bool:
        if self.is_on():
          if self.__motion_detection:
              self.__recording_status = True
              return True
          else:
              self.__motion_detection = True
              self.__recording_status = True
              return True
        else:
            return False
        
    def stop_recording(self):
        self.__recording_status = False
        self.__motion_detection = False

    def enable_motion(self):
        self.__motion_detection = True
    
    def disable_motion(self):
        self.__motion_detection = False
    
    def is_recording(self) -> bool:
        return self.__recording_status
    
    def get_status(self) -> str:
        if self.is_on():
            if self.__motion_detection and self.__recording_status:
                return "ON - Recording Active, Motion dectected"
            
            elif not self.__recording_status and self.__motion_detection:
                return f"ON - Idle, Motion dectected"
            else:
                return "ON - Idle, Motion Detection Disabled"
        else:
            return f"OFF - Idle, Motion Detection Disabled"