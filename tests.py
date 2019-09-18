from PIL import Image, ImageFont, ImageDraw, ImageFilter

"""
[2, 2],
[0, 3],
[3, 0],
[0, 2],
[2, 0],
[2, 2],
[2, -2],
[2, -2],
[0, -3],
[3, 0],
[0, -2],
[2, 0],
"""

offset = [[0, 3], [-2, 2], [-3, 0], [-2, -2], [0, -3], [2, -2], [3, 0]]

print(offset)
message = 'Keril'
img = Image.open('memelib/kokainum.jpg')
img = img.convert('RGBA')
draw = ImageDraw.ImageDraw(img)
font = ImageFont.truetype('fonts/Lobster.ttf', 150)
for point in offset:
    x, y = 50 + point[0], 50 + point[1]
    draw.text((x, y), message, (0, 0, 0), font)

draw = ImageDraw.ImageDraw(img)
draw.text((50, 50), message, (255, 255, 255), font)
img.save('test.png')
