import serial
import time
import os

class LED:
    def __init__(self):
        self.led_pins = tuple(list(range(8)))
        '''self.led_sides = tuple(["N","NE","E","ES","S","SW","W","WN"])
        self.led_property = {}
        for ind, key in enumerate(self.led_key):
            self.led_property[key] = self.led_sides[ind]'''
        return
    
    def generate_packet(self, led_pin):
        if led_pin<len(self.led_pins) and led_pin>=0:
            packet = bytearray()
            packet.append(0x01)
            packet.append(led_pin)
        return packet
    
class stm_32_comm:
    def __init__(self,port_name="",baud_rate=9600,timeout=1):
        self.port_name = port_name
        self.set_port_name(port_name=port_name)
        self.baud_rate = baud_rate
        self.time_out = timeout
        return
    
    def set_port_name(self, port_name = ""):
        if port_name != "":
            if self.does_port_exist(port_name=port_name):
                self.port_name = port_name
            else:
                print(f"{port_name} isn't found")
        else:
            port_list = os.popen("ls /dev/ttyA*").read().split("\n")[:-1]
            if len(port_list)>0:
                for ind,prt in enumerate(port_list):
                    print(f"{ind+1}. {prt}")
                try:
                    ui = int(input("Choose one of the above option: "))-1
                    self.port_name = port_list[ui]
                    print(f"Connection to {self.port_name} established\n")
                except:
                    print(f"Choose one of the given option (1~{len(port_list)})")
            else:
                print("Check usb physical connection\n")
        return
    
    def does_port_exist(self,port_name=""):
        port_list = os.popen("ls /dev/ttyA*").read().split("\n")[:-1]
        if len(port_list) == 0:
            raise Exception ("No usb connection found")
        elif (self.port_name in port_list) and (port_name==""):
            return True
        elif port_name in port_list:
            return True
        return False
    
    def initiate(self):
        if self.does_port_exist():
            try:
                self.stm32 = serial.Serial(self.port_name, self.baud_rate, timeout=self.time_out)
                return True
            except Exception as e:
                error = str(e)
                if error == "[Errno 13] could not open port /dev/ttyACM0: [Errno 13] Permission denied: '/dev/ttyACM0'":
                    raise Exception (f"Run command:\n Terminal: 'sudo chmod 666 {self.port_name}'")
                    return False
        else:
            print("Connection not established")
        return False
    
    def write(self,packet,sleep_time = 0.1):
        for i in range(5):
            self.stm32.write(packet)
            time.sleep(sleep_time)
            data = self.stm32.readline().decode("utf-8")
            time.sleep(sleep_time)
            if ("OK" in data):
                return data
            elif ("x:" in data):
                return data
            #else:
            #    print(f"Attempt {i}/5: Failed, retrying...")
            #return data
        return
    
    def end(self):
        self.stm32.close()
        return
    
    '''def is_port_permitted(self):
        return
    
    def setup_port(self):
        return'''

class gyroscp:
    def __init__(self,x_max = 65000, x_min = -52535, y_max = 65000, y_min = -65000):
        self.x_max = x_max
        self.x_max_bool = True
        self.x_min = x_min
        self.x_min_bool = True
        self.y_max = y_max
        self.y_max_bool = True
        self.y_min = y_min
        self.y_min_bool = True
        return
    
    def get_val(self, obj, txt, tm = 3):
        x=[]
        y=[]
        input(f"Enter to start, tilt {txt}")
        start_time = time.time()
        while tm - (time.time()-start_time)>0:
            print(f"Tilt {txt} \t {tm - (time.time()-start_time)} seconds left")
            val = str(obj.write(self.generate_packet()))
            val = val.split(":")[1:]
            x_gyro = float(val[0].split(",")[0])
            y_gyro = float(val[1].split("\n")[0])
            x.append(abs(x_gyro))
            y.append(abs(y_gyro))
        print(x)
        print(y)
        return max(x),max(y)
    
    def calibrate(self,obj):
        while True:
            ui = input(f"\nA. Update X min ({self.x_min})\t(pitch - counter clockwise)\nB. Update X max ({self.x_max})\t\t(pitch - clockwise)\nC. Update Y min ({self.y_min})\t(roll - counter clockwise)\nD. Update Y max ({self.y_max})\t\t(roll - clockwise)\nE. Return\nChoose (A/B/C/D/E): ").lower()
            if ui == "a":
                self.x_min = -self.get_val(obj, "counter clockwise in x axis")[0]
            elif ui == "b":
                self.x_max = self.get_val(obj, "clockwise in x axis")[0]
            elif ui == "c":
                self.y_min = -self.get_val(obj, "counter clockwise in y axis")[1]
            elif ui == "d":
                self.y_max = self.get_val(obj, "clockwise in y axis")[1]
            elif ui == "e":
                break
            else:
                print("Choose from given option")
        return
    
    def reset_xy_bool(self):
        self.x_max_bool = True
        self.x_min_bool = True
        self.y_max_bool = True
        self.y_min_bool = True
        return
    
    def generate_packet(self):
        packet = bytearray()
        packet.append(0x02)
        return packet
