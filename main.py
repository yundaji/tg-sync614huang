from telethon import TelegramClient
import os, json, requests

api_id = int(os.getenv("37199356"))
api_hash = os.getenv("d9156458a8520ad1d227f14c43ee19e7")

SOURCE = os.getenv("@madou_7777")
BOT_TOKEN = os.getenv("8970432708:AAHbdyqeDCM57p9ljmkzyYa0DBaIiyTyqR4")

# 👇 多目标频道（重点）
TARGET_CHANNELS = os.getenv("@sanji912,@sanji255").split(",")

DB = "last_id.json"

client = TelegramClient("session", api_id, api_hash)


def load_last():
    if not os.path.exists(DB):
        return 0
    return json.load(open(DB)).get("last_id", 0)


def save_last(mid):
    json.dump({"last_id": mid}, open(DB, "w"))


def send(text=None, file=None):
    for target in TARGET_CHANNELS:

        if file:
            url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument"
            requests.post(
                url,
                data={"chat_id": target},
                files={"document": open(file, "rb")}
            )
        else:
            url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
            requests.post(
                url,
                data={"chat_id": target, "text": text}
            )


async def main():
    await client.start()

    last_id = load_last()

    msgs = await client.get_messages(SOURCE, limit=20)
    msgs = sorted(msgs, key=lambda x: x.id)

    for m in msgs:
        if m.id > last_id:

            try:
                if m.media:
                    file = await m.download_media()
                    send(file=file)
                else:
                    send(text=m.text)

                last_id = m.id
                print("发送:", m.id)

            except Exception as e:
                print("错误:", e)

    save_last(last_id)


with client:
    client.loop.run_until_complete(main())
