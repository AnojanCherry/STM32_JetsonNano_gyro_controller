import time
import supports_Draft_2 as sp

## Initiate connections to stm32
prt = sp.stm_32_comm(port_name="/dev/ttyACM0")
prt.initiate()
led = sp.LED()
gyro = sp.gyroscp()

## Blink all LED to indicate successful system start
print("Checking LED")
for i in range(8):
    prt.write(led.generate_packet(i),sleep_time=0)
    time.sleep(0.1)
prt.write(led.generate_packet(0),sleep_time=0)
print("System started\n")

while True:
    ui = input("A. Run\nB. Calibrate\nE. Exit\nChoose (A/B/E): ").lower()
    if ui == "a":
        print("Running system, Press \"CTR + C\" to stop")
        while True:
            try:
                val = str(prt.write(gyro.generate_packet(),sleep_time=0))
                val = val.split(":")[1:]
                if len(val) > 1:
                    ##print(val)
                    x_gyro = float(val[0].split(",")[0])
                    y_gyro = float(val[1].split("\n")[0])
                    if x_gyro> gyro.x_max and gyro.x_max_bool:
                        #print(val)
                        prt.write(led.generate_packet(0),sleep_time=0.1)
                        gyro.reset_xy_bool()
                        gyro.x_max_bool = False

                    elif x_gyro<gyro.x_min and gyro.x_min_bool:
                        #print(val)
                        prt.write(led.generate_packet(4),sleep_time=0.1)
                        gyro.reset_xy_bool()
                        gyro.x_min_bool = False


                    elif y_gyro> gyro.y_max and gyro.y_max_bool:
                        #print(val)
                        prt.write(led.generate_packet(6),sleep_time=0.1)
                        gyro.reset_xy_bool()
                        gyro.y_max_bool = False


                    elif y_gyro< gyro.y_min and gyro.y_min_bool:
                        #print(val)
                        prt.write(led.generate_packet(2),sleep_time=0.1)
                        gyro.reset_xy_bool()
                        gyro.y_min_bool = False


            except KeyboardInterrupt:
                print("Going back to main menu")
                break
    elif ui == "b":
        print("Calibrating")
        gyro.calibrate(prt)

    elif ui == "e":
        print("Exiting")
        break
    else:
        print("Choose on of the given option")
    print("\n")

prt.end()
