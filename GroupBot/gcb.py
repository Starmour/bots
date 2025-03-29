import asyncio
import datetime
from aiogram import Dispatcher, Bot, Router
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.exceptions import AiogramError
from aiogram.filters import ChatMemberUpdatedFilter, JOIN_TRANSITION
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message, ChatMemberUpdated

time = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")
print(f"{time}\nProcessing...")
router = Router()

file = open('C:/Users/Aqua/Desktop/py/bots/GroupBot/src/conf.txt', 'r')
TOKEN = file.read()

wlcmdoc = open('C:/Users/Aqua/Desktop/py/bots/GroupBot/src/wlcm.txt', 'r')
wlcmsg = wlcmdoc.read()
# rules_doc = open('C:/Users/Aqua/Desktop/py/bots/GroupBot/src/rls.txt', 'r')
# rules_msg = rules_doc.read()
print(wlcmsg)


@router.message(Command("start"))
async def test(message: Message) -> None:
    # sticker = open('src/stickers/welcome_bender.tgs', 'rb')
    # message.reply(sticker)
    welcome_name = f'{message.from_user.first_name} {message.from_user.last_name}'
    welcome_msg = (f'Здравствуйте, {welcome_name}\n'
                   f'Я - ваш чат-ассистент, и я буду помогать Вам в этом чате.\n '
                   f'Ключевые слова, которые Вы можете использовать для получения информации:\n '
                   f'...__Описание ключевых слов__...\n '
                   f'{wlcmsg}')
    await message.reply(welcome_msg)


@router.chat_member(ChatMemberUpdatedFilter(JOIN_TRANSITION))
async def start(event: ChatMemberUpdated):
    await event.answer(wlcmsg)


async def start_bot(dp: Dispatcher, bot: Bot) -> None:
    try:
        await dp.start_polling(
            bot,
            skip_updates=True
        )
    except AiogramError:
        pass
    finally:
        await bot.session.close()


async def main():
    storage = MemoryStorage()

    bot = Bot(
        token=TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dp = Dispatcher(
        storage=storage,
    )
    dp.include_router(router)
    await start_bot(
        bot=bot,
        dp=dp,
    )


if __name__ == "__main__":
    asyncio.run(main())
