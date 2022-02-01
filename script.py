import aiosqlite
import asyncio
from email.message import EmailMessage

import aiosmtplib


async def go():
    conn = await aiosqlite.connect('contacts.db')
    cur = await conn.cursor()
    await cur.execute("SELECT * FROM contacts")
    ret = await cur.fetchall()
    await conn.close()
    return ret


async def send_email():
    users = await go()
    for user in users:
        first_name = user[1]
        last_name = user[2]
        to_email = user[3]
        from_email = 'root@localhost'

        message = EmailMessage()
        message["From"] = from_email
        message["To"] = to_email
        message["Subject"] = "Thank you for your support!"
        message.set_content(f'Уважаемый {first_name, last_name}!\n '
                            f'Спасибо, что пользуетесь нашим сервисом объявлений.')

        await aiosmtplib.send(message, hostname="127.0.0.1", port=8080)

event_loop = asyncio.get_event_loop()
event_loop.run_until_complete(send_email())