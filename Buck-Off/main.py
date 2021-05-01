import os
import subprocess
import time
import busio
import board
import digitalio
from adafruit_bno08x import BNO_REPORT_ACCELEROMETER
from adafruit_bno08x.i2c import BNO08X_I2C
import adafruit_gps
import serial
from rgbmatrix import graphics, RGBMatrix, RGBMatrixOptions

def inst_i2c():
    '''
        Params:
            gps     - ultimate gps board instantiation
            uart    - Initalizes the UART serial connection 
        Returns: 
            gps
    '''

    uart = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=3000)
    
    gps = adafruit_gps.GPS(uart, debug=False)
    
    return(gps)

def enable_accelerometer(bno):
    '''
        Params: 
            None
        Returns: 
            None
    '''

    bno.enable_feature(BNO_REPORT_ACCELEROMETER)

def get_accelerometer(bno):
    '''
        Params:
            x       - x coordinate
            y       - y coordinate
            z       - z coordinate
        Returns: 
            x, y, z
    '''
    x, y, z = bno.acceleration # (meters/s)^2

    # Convert to mph/s
    
    return(round(x),round(y),round(z))

def inst_pir():
    '''
        Params:
            pir
            pir.direction
        Returns:
            pir, pir.direction
    '''
    pir = digitalio.DigitalInOut(board.D22)
    
    pir.direction = digitalio.Direction.INPUT
    

    #print(pir)
    #print(pir.direction)
    return(pir, pir.direction)


def inst_gps(gps):
    '''
        Purpose:
            Instantiate GPS Connection
    '''

    gps.send_command(b"PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0")
    gps.send_command(b"PMTK220,1000")
    gps.send_command(b"PGCMD_ANTENNA")
    

def matrix_options():
    '''
        Params:
            options     - Display Board connection options
            matrix      - Sets the options
        Returns:
            matrix, offscreen_canvas
    '''
    
    options = RGBMatrixOptions()

    options.rows = 16
    options.cols = 32
    options.gpio_slowdown = 4
    options.brightness = 100
    options.chain_length = 1
    options.parallel = 1
    options.row_address_type = 0
    options.pwm_bits = 11
    options.pwm_lsb_nanoseconds = 130
    options.led_rgb_sequence = 'RGB' 
    options.pixel_mapper_config = ''
    #options.panel_type = '' # -> supported: str('FM6126A')
    options.show_refresh_rate = 0
    #options.hardware_mapping = 'regular'

    matrix = RGBMatrix(options = options)
    
    offscreen_canvas = matrix.CreateFrameCanvas()

    return (matrix, offscreen_canvas)

def get_font():
    '''
        Params:
            font        - Font for text
            d_font      - Font for distance
        Returns:
            font -> str, d_font -> str
    '''
    font = graphics.Font()
    d_font = graphics.Font() #distance font small

    font.LoadFont('/home/pi/Buck-Off/Buck-Off/fonts/7x13.bdf')
    d_font.LoadFont('/home/pi/Buck-Off/Buck-Off/fonts/6x13.bdf')

    return (font, d_font)

def get_colors():
    '''
        Params:
            red         - Sets value for color red
            green       - Sets value for color green
            blue        - Sets value for color blue
        Returns:
            red, green, blue
    '''
    red = graphics.Color(255,0,0)
    green = graphics.Color(0,255,0)
    blue = graphics.Color(0,0,255)

    return (red, green, blue)


if __name__ == "__main__":
    
    #Instantiate board and i2c bus
    gps = inst_i2c()
     
    #Instantiate gps
    inst_gps(gps)
    
    #Instantiate display matrix
    matrix, offscreen_canvas = matrix_options()
    
    #get font
    font, d_font = get_font()
    
    #get color: red, green, blue
    red, green, blue = get_colors()

    #Instantiate pir motion sensor
    pir, pir.direction = inst_pir()

    #Enable the Accelerometer --> not needed at the moment
    #enable_accelerometer(bno)
    
    old_value = pir.value
    
    last_print = time.monotonic()
    
    subprocess.run(['sh','/home/pi/Buck-Off/Buck-Off/fix.sh'])

    time.sleep(1)

    while True:
        gps.update()
        
        pir_value = pir.value
    
        #print(pir_value)
        if pir_value is True:

            current = time.monotonic()
            #print(current)
            if current - last_print >= 1.0:
                last_print = current
                if gps.has_fix:
                    if gps.speed_knots > 0.0:
                        
                        #convert knots to mph -> 1.151x=y
                        knots = gps.speed_knots
                        mph = round(1.151 * knots,2)
                        
                        if mph >= 30:
                               
                            for count in range(5,0,-1):
                                 graphics.DrawText(matrix, font, 2, 12, red, 'BACK')

                                 time.sleep(1) # Displays text for 1 second
                                 matrix.Clear()
                                 time.sleep(0.1)
    
                                 graphics.DrawText(matrix, font, 10, 10, red, '')
    
                                 matrix.Clear()
                                 time.sleep(0.1)
                                
                                 graphics.DrawText(matrix, font, 10, 11, red, 'UP')
                                 time.sleep(1) # Displays text for 1 second
                                 matrix.Clear()
                                 time.sleep(0.1)

                                 distance = round(((mph/60)*(2/60))*5280)

                                 graphics.DrawText(matrix, d_font, 1, 12, green, str(distance) + 'ft')

                                 time.sleep(1.5) # Displays text for 1.5 second
                                 matrix.Clear()
                                 time.sleep(0.1)

 
