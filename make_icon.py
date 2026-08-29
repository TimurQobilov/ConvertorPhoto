from PIL import Image, ImageDraw

# Создаем красивую иконку 256x256
img = Image.new("RGBA", (256, 256), color=(0, 0, 0, 0))
draw = ImageDraw.Draw(img)

draw.ellipse([8, 8, 248, 248], fill=(99, 102, 241))
draw.ellipse([24, 24, 232, 232], fill=(139, 92, 246))
draw.rounded_rectangle([64, 80, 192, 192], radius=24, outline=(255, 255, 255), width=12)
draw.ellipse([104, 112, 152, 160], outline=(255, 255, 255), width=12)
draw.ellipse([160, 96, 176, 112], fill=(52, 211, 153))

img.save("app_icon.ico", format="ICO", sizes=[(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)])
print("Файл app_icon.ico успешно создан в текущей папке!")