from abc import ABC, abstractmethod
import time

class Device(ABC):
    def __init__(self, device_ID: str, power_rate: float):
        self.__device_ID: str = device_ID
        self.__power_status: bool = False
        self.__power_rate: float = power_rate
        self.__cumulative_energy: float = 0.0
        self.__last_update_timestamp: float = time.time()
        self.__last_reset_timestamp: float = time.time()
        self._fault_detected: bool = False
        
    @abstractmethod
    def get_device_id(self) -> str:
        return self.__device_ID
    
    @abstractmethod
    def turn_on(self) ->  bool:
        if self.__power_status == False:
            self.__power_status = True
            return True
        
        if self._fault_detected == True:
            self.__power_status = False
            return False

        if self.__power_status == True:
            self.__power_status = True
            return True
        self.__last_update_timestamp = time.time()

    @abstractmethod
    def turn_off(self) -> bool:
        self.get_energy_usage()
        if self.__power_status == False:
            self.__power_status = False
            return True
            
        if self._fault_detected == True:
            self.__power_status = False
            return True

        if self.__power_status == True:
            self.__power_status =  False
            return True
      
    @abstractmethod
    def is_on(self) -> bool:
        return self.__power_status

    @abstractmethod
    def get_status(self) -> str:
        if self.__power_status == True:
            return f"{self.get_device_id} is ON"
        else:
            return f"{self.get_device_id} is OFF"

    @abstractmethod
    def get_energy_usage(self) -> float:
        current_time = time.time()
        seconds_passed = current_time - self.__last_update_timestamp
        hours_passed = seconds_passed / 3600
        if self.is_on():
            new_energy = self.__power_rate * hours_passed
            self.__cumulative_energy += new_energy
        self.__last_update_timestamp = time.time()
        return self.__cumulative_energy


    @abstractmethod
    def reset_energy_usage(self) -> str:
        self.__cumulative_energy = 0.0
        self.__last_reset_timestamp = time.time()
        return "Successfully Reseted"

    @property
    @abstractmethod
    def  is_faulty(self) -> bool:
        return self._fault_detected
    
    @is_faulty.setter
    def is_faulty(self, value: bool):
        if value == True:
            self._fault_detected = True
        else:
            raise PermissionError(
                "Faults can only be cleared by the central hub Controller. "
                "Go - to - the - central Hub"
            )