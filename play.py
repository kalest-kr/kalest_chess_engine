from PIL import Image, ImageDraw

# 빈 이미지 생성 (RGB, 크기: 800x800, 색상: 흰색)
image = Image.new("RGB", (640, 640), color="white")

# 이미지를 조작할 도구 생성
draw = ImageDraw.Draw(image)

# 직사각형 패턴 그리기
for a in range(0, 8, 2):
    for i in range(4):  # 반복문을 통해 세 줄 생성
        # 첫 번째 직사각형 (흰색)
        draw.rectangle((0 + a * 80, 160 * i, 80 + a * 80, 160 * i + 80), fill="white", outline="black")

        # 두 번째 직사각형 (녹색)
        draw.rectangle((0 + a * 80, 160 * i + 80, 80 + a * 80, 160 * i + 160), fill="green", outline="black")

for a in range(1, 9, 2):
    for i in range(4):  # 반복문을 통해 세 줄 생성
        # 첫 번째 직사각형 (흰색)
        draw.rectangle((0 + a * 80, 160 * i, 80 + a * 80, 160 * i + 80), fill="green", outline="black")

        # 두 번째 직사각형 (녹색)
        draw.rectangle((0 + a * 80, 160 * i + 80, 80 + a * 80, 160 * i + 160), fill="white", outline="black")

# 이미지 저장
image.save("generated_image.png")

# 이미지 보기
image.show()

