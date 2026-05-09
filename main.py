from fastapi import FastAPI
import uvicorn
import os

app = FastAPI()


@app.get("/create_file")
async def create_file_cmd(filename: str = None, content: str = None):
    # общие проверки
    if filename is None or filename == "." or filename == "..":
        return {"message": "Имя файла не указано!"}
    if filename.count(".") != 1 or filename.split(".")[1] not in ["txt"]: # тестовое разрешение
        return {"message": "Укажите корректное разрешение файла!"}
    # разделение на переменные для удобства
    name = filename.split(".")[0]
    # проверки имени файла
    for s in """/ '"!;|&\\""":
        if s in name:
            return {"message": "В имени файла используются запрещенные символы, удалите их и попробуйте снова!"}
    with open(filename, "w") as file:
         file.write(content)
    return {"message": f"Файл {filename} успешно создан!"}

uvicorn.run(app, host="127.0.0.1", port=8002)
