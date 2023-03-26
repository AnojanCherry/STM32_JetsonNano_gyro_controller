# An led class handler
class LED:
    
    #Initial system
    def __init__(self):
        # Led pins references
        self.led_pins = tuple(list(range(8)))
        return
    
    
    # Given an led pin number, generate the message needed to set it on
    def generate_packet(self, led_pin):
        if led_pin<len(self.led_pins) and led_pin>=0:
            packet = bytearray()
            packet.append(0x01)
            packet.append(led_pin)
        return packet