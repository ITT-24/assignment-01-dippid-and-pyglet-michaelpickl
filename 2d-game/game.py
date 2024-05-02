import pyglet
import random
from DIPPID import SensorUDP

#connect phone with game
PORT = 5700
sensor = SensorUDP(PORT)

#window size
window_width = 1280
window_height = 720

#lists 
fruits = []
#for randomizing same variables
sizes = [0.05, 0.075, 0.1, 0.2, 0.3]
times = [0.5, 0.75, 1, 1.25, 1.5, 1.75, 2]
fall_speed = [50, 60, 70, 80, 90, 100]

window = pyglet.window.Window(window_width, window_height)
#background was taken from opengamerart
#https://opengameart.org/content/light-wood-1024x1024
background_img = pyglet.image.load('pictures/wood.png')
background = pyglet.sprite.Sprite(background_img)
background.scale = 1.5
#fruits was taken from vecteezy.com
#https://www.vecteezy.com/vector-art/11993354-paring-knife-cooking-knife-icon-isolated-on-white-background-vector-illustration-in-flat-style-utensils-for-cooking-kitchenware-vector-illustration
knife_img = pyglet.image.load('pictures/knife.png')
knife = pyglet.sprite.Sprite(knife_img)
knife.scale = 0.05

acceleration = 1

# gets one of five different fruits
def get_random_image():
    #fruits was taken from vecteezy.com
    #https://www.vecteezy.com/vector-art/6647916-vector-fruit-apple-banana-melon-orange-coconut-blueberry-watermelon-cherry-strawberry-kiwi-lemon-pear-grape-peach-pineapple-avocado-mango
    number = random.randrange(0, 5)
    match number:
        case 1:
            fruit = 'pictures/cherry.png'
            return fruit
        case 2:
            fruit = 'pictures/lemon.png'
            return fruit
        case 3:
            fruit = 'pictures/pear.png'
            return fruit
        case 4:
            fruit = 'pictures/apple.png'
            return fruit
        case 5:
            fruit = 'pictures/strawberry.png'
            return fruit
        
#returns a random number from list
def get_random_int():
    number = random.choice(sizes)
    return number
#returns random number in range
def get_random_rotation():
    rotation = random.randrange(0, 360)
    return rotation

#create fruit
# image, size, rotation
def create(dt):
    fruit = get_random_image()
    if fruit == None:
        fruit = 'pictures/apple.png'
    print(fruit)
    scale_number = get_random_int()
    rotation = get_random_rotation()

    # AS: avoid loading images from disk during runtime
    fruit_img = pyglet.image.load(str(fruit))
    x = random.randint(int(100), int(window_width - 100))  
    y = random.randint(int(window_height/2), int(window_height - 100)) 
    fruit = pyglet.sprite.Sprite(fruit_img, x, y)
    fruit.scale = scale_number
    fruit.rotation = rotation
    fruits.append(fruit)

#get data from gyroscope
def handle_gyroscope(data):
    acc_x = data.get("x")
    acc_y = data.get("y")

    global acceleration
    knife.x = knife.x + acc_x * acceleration
    knife.y = knife.y + acc_y * acceleration

    if knife.x > window_width:
        knife.x = window_width
    elif knife.x < 0:
        knife.x = 0
    elif knife.y > window_height:
        knife.y = window_height
    elif knife.y < 0:
        knife.y = 0

    check_collision()

sensor.register_callback('gyroscope', handle_gyroscope)

#checks if knife hits fruit
#removes fruit if hit
def check_collision():
    for fruit in fruits:
        if knife.x < fruit.x + fruit.width and \
            knife.x + knife.width > fruit.x and \
            knife.y < fruit.y + fruit.height and \
            knife.y + knife.height > fruit.y:
            fruits.remove(fruit)

#update the fruits, make them fall
def update(dt):
    for fruit in fruits:
        fruit.y -= random.choice(fall_speed) * dt

#draw the game elements   
@window.event
def on_draw():
    window.clear()
    background.draw()
    for fruit in fruits:
        fruit.draw()
    knife.draw()

# set timer for creation and update
pyglet.clock.schedule_interval(create, random.choice(times))
pyglet.clock.schedule_interval(update, 1/60)

pyglet.app.run()
