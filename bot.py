import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import requests
from config import BOT_TOKEN, HUGGINGFACE_API_KEY

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

WELCOME_MESSAGE = """🎨 Привет! Я — БЕСПЛАТНЫЙ Арт-Бот! 

Создаю изображения по твоим описаниям!

Пиши: /арт красивый закат над океаном
Или: /арт кот в космосе

✨ Бесплатно и без ограничений!
"""

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(WELCOME_MESSAGE)

@dp.message(Command("арт"))
async def cmd_art(message: types.Message):
    description = message.text[4:].strip()
    
    if not description:
        await message.answer("Пиши: /арт [описание]. Например: /арт кот в супергеройском костюме")
        return
    
    await message.answer("🎨 Создаю арт... Жди 20-60 секунд ⏳")
    
    try:
        API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2-1"
        headers = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}
        payload = {"inputs": f"digital art, {description}, detailed, beautiful"}
        
        response = requests.post(API_URL, headers=headers, json=payload)
        
        if response.status_code == 200:
            await message.answer_photo(
                photo=response.content,
                caption=f"🎨 Готово!\n'{description}'"
            )
        else:
            await message.answer("🎨 Модель загружается... Попробуй через 1-2 минуты!")
                
    except Exception as e:
        await message.answer("🎨 Ошибка 😅 Попробуй позже!")

@dp.message()
async def handle_message(message: types.Message):
    await message.answer("🎨 Пиши: /арт [описание]")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
