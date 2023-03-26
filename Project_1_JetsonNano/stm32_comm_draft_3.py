# STM32F3Discovery usb communication class handler
class stm_32_comm:
    
    # load the necessary port details
    def __init__(self,port_name="",baud_rate=9600,timeout=1):
        self.port_name = port_name
        self.set_port_name(port_name=port_name)
        self.baud_rate = baud_rate
        self.time_out = timeout
        return
    
    
    # Setting up the JetsonNano to STM32F3Discovery port
    def set_port_name(self, port_name = ""):
        
        # Given a custom port name, the following will check if it exists and update the port name (i.e. ttyACM0)
        if port_name != "":
            if self.does_port_exist(port_name=port_name):
                self.port_name = port_name
            else:
                print(f"{port_name} isn't found")
        
        # if port name is not given, get all available/ possible port name that starts with ttyA, and set up a suitable one
        else:
            
            # Get all port name that start with ttyA
            port_list = os.popen("ls /dev/ttyA*").read().split("\n")[:-1]
            
            # If the number of port name is bigger than 0 do the following
            if len(port_list)>0:
                for ind,prt in enumerate(port_list):
                    print(f"{ind+1}. {prt}")
                
                # Get user to select a port of all the available ports
                try:
                    ui = int(input("Choose one of the above option: "))-1
                    self.port_name = port_list[ui]
                    print(f"Connection to {self.port_name} established\n")
                except:
                    print(f"Choose one of the given option (1~{len(port_list)})")
                    
            # If the number of port name is 0 do the following
            else:
                print("Check usb physical connection\n")
        return
    
    
    # The following will check the given/(stored port name) with the ports that are connected to see if such port exists 
    def does_port_exist(self,port_name=""):
        
        # Get all port names
        port_list = os.popen("ls /dev/ttyA*").read().split("\n")[:-1]
        
        # If there are no open ports do the following
        if len(port_list) == 0:
            raise Exception ("No usb connection found")
            
        # If stored port name is available do the following
        elif (self.port_name in port_list) and (port_name==""):
            return True
        
        # if given port_name is available do the following
        elif port_name in port_list:
            return True
        
        # For all else do the following
        return False
    
    
    # Establish a connection between the device and the STM32F3Discovery
    def initiate(self):
        if self.does_port_exist():
            try:
                
                # Set up a connection
                self.stm32 = serial.Serial(self.port_name, self.baud_rate, timeout=self.time_out)
                return True
            
            # For any errors that might be rised do the following
            except Exception as e:
                error = str(e)
                
                #if the error raised is due to a known issue, Give them a solution to troubleshoot it
                if error == "[Errno 13] could not open port /dev/ttyACM0: [Errno 13] Permission denied: '/dev/ttyACM0'":
                    raise Exception (f"Run command:\n Terminal: 'sudo chmod 666 {self.port_name}'")
                    return False
        # If the port name attempted to connect doesnt exist, let user know connection wasnt successful
        else:
            print("Connection not established")
        return False
    
    # Transmit data from device 
    def write(self,packet,sleep_time = 0.1):
        
        # Attempt 5 times to transmit and recieve acknowledgement
        for i in range(5):
            
            # Transmit the given data
            self.stm32.write(packet)
            time.sleep(sleep_time)
            
            # Read the return message
            data = self.stm32.readline().decode("utf-8")
            time.sleep(sleep_time)
            
            # Check if the return message has acknowledgement
            if ("OK" in data):
                return data
            elif ("x:" in data):
                return data
            
            #else:
            #    print(f"Attempt {i}/5: Failed, retrying...")
            #return data
        return
    
    # Close the open stm32 connection
    def end(self):
        self.stm32.close()
        return