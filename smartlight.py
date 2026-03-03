from device import Device, time

class SmartLight(Device):
    def __init__(self, device_ID: str, power_rate: float):
        super().__init__(device_ID, power_rate)
        self.__brightness: int = 0
        self.__color_mode: str = ""
        self.__color_modes: list = ["warm", "cold", "RGB"]

    def get_status(self) -> str:
        if self.is_on():
            return f"ON - {self.__brightness}% Brightness, {self.__color_mode}"
        else:
            return f"OFF - Last brightness {self.__brightness}%, {self.__color_mode}"  
        
    def turn_on(self) -> bool:
        last = self.__brightness
        return super().turn_on()

    def turn_off(self) -> bool:
        last = self.__brightness
        self.__brightness = 0
        return super().turn_off()   

    def set_brightness(self, level: int) -> bool:
        if self.is_on():
            if 0 <= level <= 100:
                self.__brightness = level
                self.__power_rate = self.__power_rate * (self.__brightness / 100)
                return True 
            else:
                return False
        else:
            self.__brightness = 0
            return False

    def set_color(self, mode: str):
        if self.is_on():
            if mode.lower() in self.__color_modes: 
                self.__color_mode = mode
                self.__power_rate = self.__power_rate * (self.__brightness / 100)
                return True 
            else:
                return False
        else:
            return False
    
    def get_brightness(self):
        return self.__brightness
    
    def get_color(self):
        return self.__color_mode
    
    def get_energy_usage(self) -> float:
        self.__power_rate = self.__power_rate * (self.__brightness / 100)
        return super().get_energy_usage()