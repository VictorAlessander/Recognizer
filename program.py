import face_recognition
from PIL import Image, ImageDraw, ImageFont


def main():

    known_image = face_recognition.load_image_file("Michael.jpg")
    unknown_image = face_recognition.load_image_file("desconhecidos.jpg")


    try:
        known_image_encoding = face_recognition.face_encodings(known_image)[0]
        unknown_image_encoding = face_recognition.face_encodings(unknown_image)[0]

    except IndexError as e:
        print('I cant recognize any faces in at least one of the images. Aborting...')
        raise e

    known_faces = [known_image_encoding]

    face_locations = face_recognition.face_locations(unknown_image, number_of_times_to_upsample=0, model="cnn")

    if face_locations:
        print("Detected some faces")

        result = face_recognition.compare_faces(known_faces, unknown_image_encoding)

        pil_image = Image.fromarray(unknown_image)
        draw = ImageDraw.Draw(pil_image)
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 15)
        width, height = pil_image.size
        draw.rectangle([0, height * 0.95, width, height], fill="#000000")
        draw.text((width * 0.05, height * 0.965), "Faces detected: " + str(len(face_locations)))

        for face_location in face_locations:
            top, right, bottom, left = face_location
            draw.line(((left, bottom),(right, bottom)), width = 2, fill="#ff0000")
            draw.line(((left, top), (right, top)), width = 2, fill="#ff0000")
            draw.line(((left, bottom), (left, top)), width = 2, fill="#ff0000")
            draw.line(((right, bottom), (right, top)), width = 2, fill="#ff0000")
            draw.rectangle([left - 1, bottom, right, bottom + 20], fill="#ff0000")
            draw.text((left + 1, bottom), "face", font=font)

        pil_image.save("Testing.png", format="png")

if __name__ == "__main__":
    main()
