from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from ursina.prefabs.health_bar import HealthBar

import random

app = Ursina()

window.fps_counter.enabled = True
window.exit_button.visible = False

punch = Audio('assets/punch')

music = Audio('assets/music')
music.play()

camera.ui_size = 40

health_bar_1 = HealthBar(
    max_value=300,
    bar_color=color.lime.tint(-.25),
    roundness=.5,
    value=50,
    position = (-0.88,-0.4,0.1),
    animation_duration = 0.2,
    scale_x = 0.7,
    scale_y = 0.04
)

player = FirstPersonController(
    y=9,
    x=3,
    z=3,
    speed = 6,
    gravity = 0.5,
    jump_height = 1,
    air_time = 0,
    height = 2,
)

blocks = [
    load_texture('assets/grass.png'), # 0
    load_texture('assets/grass.png'), # 1
    load_texture('assets/stone.png'), # 2
    load_texture('assets/gold.png'),  # 3
    load_texture('assets/lava.png'),  # 4
    load_texture('assets/dirt_block.png'), #5
    load_texture('assets/brick_block.png')  #6
]

block_id = 1

def input(key):
    global block_id, hand
    if key.isdigit():
        block_id = int(key)
        if block_id >= len(blocks):
            block_id = len(blocks) - 1
        hand.texture = blocks[block_id]

    if key == 'escape':
        application.quit()

sky = Entity(
    parent=scene,
    model='sphere',
    texture=load_texture('assets/sky.jpg'),
    scale=500,
    double_sided=True
)

hand = Entity(
    parent=camera.ui,
    model='assets/block',
    texture=blocks[block_id],
    scale=0.2,
    rotation=Vec3(-10, -10, 10),
    position=Vec2(0.6, -0.6)
)

def update():
    if held_keys['left mouse'] or held_keys['right mouse']:
        punch.play()
        hand.position = Vec2(0.4, -0.5)
    else:
        hand.position = Vec2(0.6, -0.6)

    if health_bar_1.value == 0:
        descr = dedent('<red>You dead\n' + '<red>Try again?')
        Text.default_resolution = 1080 * Text.size
        Text(text=descr, origin=(0, -5), background=True)

    if player.y < -1:
        health_bar_1.value -= 1


class Voxel(Button):
    def __init__(self, position=(0, 0, 0), texture='assets/grass.png'):
        super().__init__(
            parent=scene,
            position=position,
            model='assets/block',
            origin_y=0.5,
            texture=texture,
            color=color.color(0, 0, random.uniform(0.9, 1.0)),
            scale=0.5
        )

    def input(self, key):
        if self.hovered:
            if key == 'left mouse down':
                destroy(self)
            elif key == 'right mouse down':
                Voxel(position=self.position + mouse.normal, texture=blocks[block_id])

for z in range(random.randint(15,20)):
    for x in range(random.randint(7,20)):
        grass = Voxel(position=(x, 8, z), texture='assets/grass.png')

for z in range(random.randint(7,20)):
    for x in range(random.randint(7,20)):
        for y in range(1,2):
            underground = Voxel(position=(x, y, z), texture='assets/gold.png')

for z in range(random.randint(7,20)):
    for x in range(random.randint(7,20)):
        for y in range(2,5):
            stone = Voxel(position=(x, y, z), texture='assets/stone.png')

for z in range(random.randint(10,20)):
    for x in range(random.randint(7,20)):
        for y in range(5,8):
            dirt = Voxel(position=(x, y, z), texture='assets/dirt_block.png')

if __name__ == "__main__":
    app.run()