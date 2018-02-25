import face_recognition
from PIL import Image, ImageDraw, ImageFont
import sys


def main(known_person, known_image_file):
    try:
        # Load known image
        known_image = face_recognition.load_image_file(known_image_file)
        known_image_encoding = face_recognition.face_encodings(known_image)[0]

        # Load unknown image
        unknown_image = face_recognition.load_image_file("unknown.jpg")
        #face_locations = face_recognition.face_locations(unknown_image, number_of_times_to_upsample=0, model="cnn")
        unknown_face_locations = face_recognition.face_locations(unknown_image)
        unknown_face_encoding = face_recognition.face_encodings(unknown_image, unknown_face_locations)

    except IndexError as e:
        print('I cant recognize any faces in at least one of the images. Aborting...')
        raise e

    known_faces_encodings = [known_image_encoding]
    known_faces_names = [known_person.capitalize()]

    pil_image = Image.fromarray(unknown_image)
    draw = ImageDraw.Draw(pil_image)

    if unknown_face_locations:
        print("[+] Detected some faces")

        for (top, right, bottom, left), face_encoding in zip(unknown_face_locations, unknown_face_encoding):
            matches = face_recognition.compare_faces(known_faces_encodings, face_encoding)

            name = "Unknown"

            if True in matches:
                first_match_index = matches.index(True)
                name = known_faces_names[first_match_index]
                print("[+] Found known face: {}".format(name))

            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 15)
            width, height = pil_image.size
            draw.rectangle([0, height * 0.95, width, height], fill="#000000")
            draw.text((width * 0.05, height * 0.965), "Faces detected: " + str(len(unknown_face_locations)))

            draw.line(((left, bottom),(right, bottom)), width = 2, fill="#ff0000")
            draw.line(((left, top), (right, top)), width = 2, fill="#ff0000")
            draw.line(((left, bottom), (left, top)), width = 2, fill="#ff0000")
            draw.line(((right, bottom), (right, top)), width = 2, fill="#ff0000")
            draw.rectangle([left - 1, bottom, right, bottom + 20], fill="#ff0000")
            draw.text((left + 1, bottom), name, font=font)

    pil_image.save("Result.png", format="png")
    del draw
    #pil_image.show()

if __name__ == "__main__":
    person = sys.argv[1]
    known_person_file = sys.argv[2]
    main(person, known_person_file)
