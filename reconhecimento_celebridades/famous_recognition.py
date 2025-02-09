from pathlib import Path

import boto3
from mypy_boto3_rekognition.type_defs import CelebrityTypeDef
from PIL import Image, ImageDraw

def get_path(file_name: str) -> str:
    return str(Path(__file__).parent / "images" / file_name)

def recognize_celebrities(image_path):
    
    client = boto3.client("rekognition")

    with open(image_path, 'rb') as image:
        response = client.recognize_celebrities(Image={'Bytes': image.read()})

    print('Detected faces for ' + image_path)
    for celebrity in response['CelebrityFaces']:
        print('Nome: ' + celebrity['Name'])
        print('Info')
        for url in celebrity['Urls']:
            print('   ' + url)
        print()
    return response['CelebrityFaces']

def draw_boxes(image_path: str, output_path: str, face_details: list[CelebrityTypeDef]) -> None:
    image = Image.open(image_path)
    draw = ImageDraw.Draw(image)

    width, height = image.size

    for face in face_details:
        box = face["Face"]["BoundingBox"]  # type: ignore
        left = int(box["Left"] * width)  # type: ignore
        top = int(box["Top"] * height)  # type: ignore
        right = int((box["Left"] + box["Width"]) * width)  # type: ignore
        bottom = int((box["Top"] + box["Height"]) * height)  # type: ignore

        draw.rectangle([left, top, right, bottom], outline="red", width=3)

        name = face["Name"]
        similarity = face["MatchConfidence"]  # type: ignore
        draw.text((left, top - 10), f"{name}, {similarity:.1f}%", fill="red")

    image.save(output_path)
    print(f"Imagem salva com resultados em: {output_path}")


if __name__ == "__main__":
    image_path = get_path("selfie-oscar.jpg")
    output_image_path = get_path("resultado_oscar.jpg")
    celeb_faces = recognize_celebrities(image_path)
    celeb_count = len(celeb_faces)
    
    if celeb_count > 0:
        print("Número de celebridades encontradas: " + str(celeb_count))
        draw_boxes(image_path, output_image_path, celeb_faces)
    else:
        print("Nenhuma celebridade foi encontrada.")

