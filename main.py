from telethon import TelegramClient
import os, json

api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")

SOURCE = os.getenv("SOURCE_CHANNEL")
TARGETS = os.getenv("TARGET_CHANNELS").split(",")

DB = "last_id.json"

client = TelegramClient("session", api_id, api_hash)


def load_last():
    if not os.path.exists(DB):
        return 0
    return json.load(open(DB)).get("last_id", 0)


def save_last(mid):
    json.dump({"last_id": mid}, open(DB, "w"))


async def main():
    await client.start()

    last_id = load_last()

    msgs = await client.get_messages(SOURCE, limit=20)
    msgs = sorted(msgs, key=lambda x: x.id)

    for m in msgs:
        if m.id > last_id:

            try:
                # 🔥 核心：直接复制消息（不会崩）
                for t in TARGETS:
                    await client.forward_messages(t, m)

                last_id = m.id
                print("转发:", m.id)

            except Exception as e:
                print("失败:", e)

    save_last(last_id)


with client:
    client.loop.run_until_complete(main())
