from device import Device
import datetime

class Hub:
    def __init__(self):
        self.__list_of_registered_device: dict = {}
        self.__schedule_rules: dict = {}
        self.__energy_log: dict = {}
        self._log: list = []
    def register_device(self, device: Device)  -> bool:
        if not isinstance(device, Device):
            return False
        
        device_id = device.get_device_id()

        if device_id in self.__list_of_registered_device:
            return False
        
        self.__list_of_registered_device[device_id] = device
        self.__energy_log[device_id] = 0.0
        return True
            

    
    def unregistered_device(self, device_id: str) -> bool:
        if device_id not in self.__list_of_registered_device:
            return False

        del self.__list_of_registered_device[device_id]

        if device_id in self.__energy_log:
            del self.__energy_log[device_id]

        return True
    
    def add_schedule(self, time: str, command: str, device_id: str) -> bool:
        if len(time) != 5 or time[2] != ":":
            return False
        hour, minute = time.split(":")
        
        if not (hour.isdigit() and minute.isdigit()):
            return False

        if not (0 <= int(hour) <= 23 and 0 <= int(minute) <= 59):
            return False
        
        if device_id not in self.__list_of_registered_device:
            return False
        device = self.__list_of_registered_device[device_id]

        if not isinstance(device, Device):
            return False
        
        if time in self.__schedule_rules:
            self.__schedule_rules[time].append(device_id +"."+ command)
            return True
        
        action = device_id +"."+ command
        self.__schedule_rules[time] = [action]
        return True

    def execute_schedules(self, current_time) -> None:

        if isinstance(current_time, datetime):            
            time_key = current_time.strftime("%H:%M")
        else:
            time_key = str(current_time)

        commands = self.__schedule_rules[time_key]
        if not commands:
            return
        for command in commands:
            device_id, action = command.spilt(".", 1)
            method_name, args_part = action.split("(", 1)
            args_part =args_part.rstrip(")")
            device = self.__list_of_registered_device[device_id]
            if not device:
                return
            method = getattr(device, method_name, None)
            if not callable(method):
                return
            if args_part == "":
                method()
            else:
                args = []
                for arg in args_part.split(","):
                    arg = arg.strip()
                    if arg.isdigit():
                        args.append(int(arg))
                method(*args)
    def clear_fault(self, device_id: str) -> bool:
        if device_id not in self.__list_of_registered_device:
            return False
        device: Device = self.__list_of_registered_device[device_id]

        if device is None or not device.is_faulty:
            return False
        
        device._fault_detected = False
        self._log.append(f"Fault cleared for {device_id}")
        return True
        

