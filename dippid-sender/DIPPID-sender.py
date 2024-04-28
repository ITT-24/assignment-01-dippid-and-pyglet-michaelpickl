import socket
import time
import numpy as np
import random


IP = '192.168.2.101'
PORT = 5700

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


# function generating accelerometer data
# https://numpy.org/doc/stable/reference/generated/numpy.sin.html
# https://stackoverflow.com/questions/5028374/changing-amplitude-frequency-of-numpy-sinwt-in-pylab
def generate_accelerometer():
    t = time.time()
    frequency = [1, 2, 0.5]
    x = np.sin(np.pi * t * frequency[0])
    y = np.sin(np.pi * t * frequency[1])
    z = np.sin(np.pi * t * frequency[2])
    return x, y, z


# function generating button data
# https://www.w3schools.com/python/ref_random_randrange.asp
def generate_button ():
    button = random.randrange(0, 2)
    return button


while True:
    accelerometer_data = generate_accelerometer()
    button_data = generate_button()
    #print(accelerometer_data)
    #print(button_data)

    dippid_data = '{' +  '"accelerometer":{"x":' + str(accelerometer_data[0]) + ', "y":' + str(accelerometer_data[1]) + ',"z":' + str(accelerometer_data[2]) + '}' + ',' + '"button_1":' + str(button_data) + '}'

    sock.sendto(dippid_data.encode(), (IP, PORT))

    time.sleep(0.5)