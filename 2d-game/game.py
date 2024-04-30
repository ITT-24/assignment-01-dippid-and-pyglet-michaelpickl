import pyglet
import random
from DIPPID import SensorUDP

PORT = 5700
sensor = SensorUDP(PORT)

# Constants
window_width = 1280
window_height = 720
fruits = []
fall_speed = 50

window = pyglet.window.Window(window_width, window_height)
knife_img = pyglet.image.load('knife.png')
knife = pyglet.sprite.Sprite(knife_img)

list_fruits = ['apricot.png', 'banana.png', 'blue_berry.png', 'blueberrys.png', 'cherry.png', 'cherry2.png', 'citron.png', 'drachenfrucht.png'
                'drachenfrucht1.png', 'drachenfrucht2.png', 'green_apple.png', 'green_banana.png', 'green_berry.png', 'lime.png', 'orange_banana.png'
                'pearl.png', 'pfirisch.png', 'pineapple.png', 'purple_berry.png', 'red_apple.png', 'strawberry.png', 'yellow_apple.png']

def get_random_image():
    number = random.randrange(0, 5)
    match number:
        case 1:
            fruit = 'apricot.png'
            return fruit
        case 2:
            fruit = 'banana.png'
            return fruit
        case 3:
            fruit = 'blue_berry.png'
            return fruit
        case 4:
            fruit = 'blueberrys.png'
            return fruit
        case 5:
            fruit = 'cherry.png'
            return fruit
    
    



def get_random_int():
    number = random.randrange(4, 10)
    return number
def get_random_rotation():
    rotation = random.randrange(0, 360)
    return rotation




def create(dt):
    fruit = get_random_image()
    if fruit == None:
        fruit = 'apricot.png'
    print(fruit)
    scale_number = get_random_int()
    rotation = get_random_rotation()
    fruit_img = pyglet.image.load(str(fruit))
    x = random.randint(int(fruit_img.width), int(window_width - fruit_img.width))  
    y = random.randint(int(window_height/2), int(window_height - fruit_img.height)) 
    fruit = pyglet.sprite.Sprite(fruit_img, x, y)
    fruit.scale = scale_number
    fruit.rotation = rotation
    fruits.append(fruit)

def handle_accelerometer(data):
    acc_x = data.get("x")
    acc_y = data.get("y")

    knife.x = knife.x + acc_x * 5
    knife.y = knife.y + acc_y * 5

    if knife.x > window_width:
        knife.x = window_width
    elif knife.x < 0:
        knife.x = 0
    elif knife.y > window_height:
        knife.y = window_height
    elif knife.y < 0:
        knife.y = 0

    check_collision()

sensor.register_callback('gyroscope', handle_accelerometer)

def check_collision():
    global fruits
    for fruit in fruits:
        if knife.x < fruit.x + fruit.width and \
            knife.x + knife.width > fruit.x and \
            knife.y < fruit.y + fruit.height and \
            knife.y + knife.height > fruit.y:
            fruits.remove(fruit)

def update(dt):
    for fruit in fruits:
        fruit.y -= fall_speed * dt
        

@window.event
def on_draw():
    window.clear()
    for fruit in fruits:
        fruit.draw()
    knife.draw()

pyglet.clock.schedule_interval(create, 2)
pyglet.clock.schedule_interval(update, 1/60)

pyglet.app.run()