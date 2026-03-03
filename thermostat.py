from device import Device, time

class Thermostat(Device):
    def __init__(self, device_ID: str, power_rate: float):
        super().__init__(device_ID, power_rate)
        self.__current_temperature: float = 20.0
        self.__target_temperature: float = 20.0
        self.__private_rate: float = 0.5
        self.__emergency_mode = False 

    def turn_off(self) -> bool:
        if self.__emergency_mode:
            self.__power_status = True
            return False
        return super().turn_off()   
    
    def get_current_temperature(self) -> float:
        if self.is_on():
            now = time.time()
            time_passed = now - self.__last_update_timestamp
            minutes_passed = time_passed / 60

            gap = self.__target_temperature - self.__current_temperature
            max_change = self.__private_rate * minutes_passed
            if gap > 0:
                actual_change = min(max_change, gap)
                self.__current_temperature += actual_change
                if self.__current_temperature < 5:
                    self.__emergency_mode = True
                elif self.__current_temperature > 30:
                    self.__emergency_mode = True
                else: 
                    self.__emergency_mode = False
                return self.__current_temperature
            elif gap < 0:
                actual_change = min(max_change, gap)
                self.__current_temperature -= actual_change
                if self.__current_temperature < 5:
                    self.__emergency_mode = True
                elif self.__current_temperature > 30:
                    self.__emergency_mode = True
                else: 
                    self.__emergency_mode = False
                return self.__current_temperature
            else:
                self. __current_temperature = self.__current_temperature
                if self.__current_temperature < 5:
                    self.__emergency_mode = True
                elif self.__current_temperature > 30:
                    self.__emergency_mode = True
                else: 
                    self.__emergency_mode = False
                return self.__current_temperature
        else:
            if self.__current_temperature < 5:
                self.__emergency_mode = True
            elif self.__current_temperature > 30:
                    self.__emergency_mode = True
            else: 
                self.__emergency_mode = False
            return self.__current_temperature    
    
    def set_temperature(self, target: float):
        if self.is_on:
            if -10 < target < 50:
                self.__target_temperature = target
                return True
            else:
                return False
        else:
            return False
    
    def get_target_temperature(self):
        return self.__target_temperature
    
    def get_status(self) -> str:
        if self.is_on():
            return f"ON - Current Temperature: {self.get_current_temperature} | Target Temperature: {self.get_target_temperature}"
        
        else:
            return f"{self.get_device_id} is OFF"