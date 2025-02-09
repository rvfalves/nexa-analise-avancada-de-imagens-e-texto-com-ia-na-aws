import json
from pathlib import Path
from typing import Dict, List, Tuple

import boto3
from botocore.exceptions import ClientError
from mypy_boto3_textract.type_defs import DetectDocumentTextResponseTypeDef


def get_document_data(file_name: str) -> bytearray:
    with open(file_name, "rb") as file:
        doc_bytes = file.read()
        print(f"Imagem carregada {file_name}")
    return doc_bytes


def analyze_document() -> None:
    client = boto3.client("textract")
    file_path = str(Path(__file__).parent / "images" / "lista-material-escolar.jpeg")
    doc_bytes = get_document_data(file_path)
    response = client.detect_document_text(
        Document={"Bytes": doc_bytes},  # type: ignore
    )
    with open("response.json", "w") as response_file:
        response_file.write(json.dumps(response))


def get_lines() -> List:
    line_list = []
    blocks = []

    try:
        with open("response.json", "r") as file:
            blocks = json.loads(file.read())["Blocks"]
    except IOError:
        analyze_document()
        with open("response.json", "r") as file:
            blocks = json.loads(file.read())["Blocks"]

    for block in blocks:
        if block["BlockType"] == "LINE":  # type: ignore
            line_list.append(block["Text"])  # type: ignore

    return line_list

def text_generate(line_list: List) -> str:
    text = ""
    for line in line_list:
        text += line + "\n"
    return text.rstrip()


if __name__ == "__main__":
    line_list = get_lines()
    text = text_generate(line_list)
    print(text)