import time
import supports_Draft_2 as sp

## Initiate connections to stm32
prt = sp.stm_32_comm(port_name="/dev/ttyACM0")
prt.initiate()
# Set up the STM32F3Discovery custom LED class
led = sp.LED()
# Set up the STM32F3Discovery custom gyro class
gyro = sp.gyroscp()

## Blink all LED to indicate successful system start
print("Checking LED")
for i in range(8):
    # get the led message to light up chosen led, then write to send it to the Stm32
    prt.write(led.generate_packet(i),sleep_time=0)
    time.sleep(0.1)
prt.write(led.generate_packet(0),sleep_time=0)
print("System started\n")

## A Super loop 
while True:
    ui = input("A. Run\nB. Calibrate\nE. Exit\nChoose (A/B/E): ").lower()
    
    # The following will constantly request gyro data and update the led to indicate the direction of tilt
    if ui == "a":
        print("Running system, Press \"CTR + C\" to stop")
        while True:
            
            # A try catch statement is used in the loop, so as to have closed loop that will run until an interrupt event is evoked by user
            try:
                
                # Request the gyro data from the STM32F3Discovery, and process it.
                val = str(prt.write(gyro.generate_packet(),sleep_time=0))
                val = val.split(":")[1:]
                if len(val) > 1:
                    
                    # the processed data is then seperated into the x and y gyro data
                    x_gyro = float(val[0].split(",")[0])
                    y_gyro = float(val[1].split("\n")[0])
                    
                    # The following checks in which direction the STM32F3Discovery is tilted
                    # Negative pitch
                    if x_gyro> gyro.x_max and gyro.x_max_bool: 
                        prt.write(led.generate_packet(0),sleep_time=0.1)
                        gyro.reset_xy_bool()
                        gyro.x_max_bool = False
                    
                    # Positive pitch
                    elif x_gyro<gyro.x_min and gyro.x_min_bool:
                        prt.write(led.generate_packet(4),sleep_time=0.1)
                        gyro.reset_xy_bool()
                        gyro.x_min_bool = False

                    # Positive Roll
                    elif y_gyro> gyro.y_max and gyro.y_max_bool:
                        prt.write(led.generate_packet(6),sleep_time=0.1)
                        gyro.reset_xy_bool()
                        gyro.y_max_bool = False

                    # Negative roll
                    elif y_gyro< gyro.y_min and gyro.y_min_bool:
                        prt.write(led.generate_packet(2),sleep_time=0.1)
                        gyro.reset_xy_bool()
                        gyro.y_min_bool = False

            # Custom user interrupt event (When user presses ctr+c)
            except KeyboardInterrupt:
                print("Going back to main menu")
                break
    
    # Since all gyro's might not have the same sensitivity, the following will help calibrate the threshold at which the system detects a tilt
    elif ui == "b":
        print("Calibrating")
        gyro.calibrate(prt)

    # User chose to end ui
    elif ui == "e":
        print("Exiting")
        break
    # Validation, in case user mistypes something
    else:
        print("Choose on of the given option")
    print("\n")


# close port conncetion
prt.end()
