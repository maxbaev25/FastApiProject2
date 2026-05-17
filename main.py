from fastapi import FastAPI
import uvicorn
import os
import platform
import subprocess
import logging

# app
app = FastAPI()
# logger
logger = logging.getLogger(name="main")
logger.setLevel(level=logging.DEBUG)
# file_handler
file_handler = logging.FileHandler(
    filename="main.log", encoding="utf-8")
logger.addHandler(file_handler)


@app.get("/create_file")
async def create_file_cmd(filename: str = None, content: str = None):
    logger.debug("GET /create_file")
    # общие проверки
    if filename is None or filename == "." or filename == "..":
        return {"message": "Имя файла не указано!"}
    if filename.count(".") != 1 or filename.split(".")[1] not in ["txt"]:  # тестовое разрешение
        return {"message": "Укажите корректное разрешение файла!"}
    # разделение на переменные для удобства
    name = filename.split(".")[0]
    # проверки имени файла
    for s in """/ '"!;|&\\""":
        if s in name:
            return {"message": "В имени файла используются запрещенные символы, удалите их и попробуйте снова!"}
    if os.path.exists(filename):
        return {"message": f"Файл {filename} уже существует!"}
    else:
        if platform.system() == "Linux":
            subprocess.run(f"touch {filename}", shell=True)
            subprocess.run(f"echo {content} > {filename}", shell=True)
        else:
            with open(filename, "w") as file:
                file.write(content)
    return {"message": f"Файл {filename} успешно создан!"}

uvicorn.run(app, host="0.0.0.0", port=8002)
