import cv2
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import constant


def display(img):
    import matplotlib.pyplot as plt
    plt.imshow(img)
    plt.show()


def add_border_to_image(im, bordersize=5, rgb=[45, 33, 31]):
    border = cv2.copyMakeBorder(im, top=bordersize, bottom=bordersize, left=bordersize, right=bordersize,
                                borderType=cv2.BORDER_CONSTANT, value=rgb)
    return border


def write_text(image, text, pos, font_scale=0.55, linetype=1, fontcolor= (255, 255, 255), font=cv2.FONT_HERSHEY_DUPLEX):
    cv2.putText(image, text, pos, font, font_scale, fontcolor, linetype)


def write_text_pil(image, text, pos, cv2_image=True, size=20, fontcolor=(255,255,255), font=constant.FONT_ROBOTO_PATH):
    # if cv2_image:
    #     image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = Image.fromarray(image)
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(font, size=size)
    draw.text(pos, text, fill=fontcolor, font=font)
    image = np.array(image)
    return image


def transparentOverlay(src, overlay, pos=(0, 0), scale=1):
    """
    :param src: Input Color Background Image
    :param overlay: transparent Image (BGRA)
    :param pos:  position where the image to be blit.
    :param scale : scale factor of transparent image.
    :return: Resultant Image
    """
    overlay = cv2.resize(overlay, (0, 0), fx=scale, fy=scale)
    h, w, _ = overlay.shape  # Size of foreground
    rows, cols, _ = src.shape  # Size of background Image
    y, x = pos[0], pos[1]  # Position of foreground/overlay image

    # loop over all pixels and apply the blending equation
    for i in range(h):
        for j in range(w):
            if x + i >= rows or y + j >= cols:
                continue
            alpha = float(overlay[i][j][3] / 255.0)  # read the alpha channel
            src[x + i][y + j] = alpha * overlay[i][j][:3] + (1 - alpha) * src[x + i][y + j]
    return src


def addImageWatermark(LogoImage, MainImage, pos, opacity=100):
    opacity = opacity / 100

    OriImg = MainImage
    waterImg = LogoImage


    tempImg = OriImg.copy()

    overlay = transparentOverlay(tempImg, waterImg, pos)
    output = OriImg.copy()
    # apply the overlay
    cv2.addWeighted(overlay, opacity, output, 1 - opacity, 0, output)
    return output


if __name__ == '__main__':
    logo = '/home/ben/personal/discord-dota-bot/data/medals/immortal-10.png'
    bg = '/home/ben/personal/discord-dota-bot/data/background/items_background_final_1.jpg'
    logo = cv2.imread(logo, -1)
    logo = cv2.resize(logo, (100, 100))
    bg = cv2.imread(bg)
    c = addImageWatermark(logo, bg, (50, 90))
    display(c)
    exit()


