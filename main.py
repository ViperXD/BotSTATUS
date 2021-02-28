import os
import time
import datetime

import pyrogram

# your session strings
user_session_string = os.environ.get("SESSION_STRING")

# your all bots username without '@' with a space 1 to another
bots = [i.strip() for i in os.environ.get("BOTS").split(' ')]

# your username without '@'
bot_owner = os.environ.get("BOT_OWNER")

# your channel username without '@'
update_channel = os.environ.get("UPDATE_CHANNEL")

# message id of your channel bot status message
status_message_id = int(os.environ.get("STATUS_MESSAGE_ID"))

# api strings from my.telegram.org
api_id = int(os.environ.get("API_ID"))
api_hash = os.environ.get("API_HASH")

# time in minutes for sleeping
time = int(os.environ.get("TIME"))

user_client = pyrogram.Client(
    user_session_string, api_id=api_id, api_hash=api_hash)


def main():
    with user_client:
        while True:
            print("[INFO] starting to check uptime..")
            edit_text = f"<b>My Bots status:</b>\n(Updated every 15 mins)\n\n"
            for bot in bots:
                print(f"[INFO] checking @{bot}")
                snt = user_client.send_message(bot, '/start')

                time.sleep(time)

                msg = user_client.get_history(bot, 1)[0]
                if snt.message_id == msg.message_id:
                    print(f"[WARNING] @{bot} is down")
                    edit_text += f"<b>➲ [{bot}](https://telegram.me/{bot}) :</b> ❎\n"
                    user_client.send_message(bot_owner,
                                             f"@{bot} status: `Down`")
                else:
                    print(f"[INFO] all good with @{bot}")
                    edit_text += f"<b>➲ [{bot}](https://telegram.me/{bot}) :</b> ✅</b>\n"
                user_client.read_history(bot)

            utc_now = datetime.datetime.utcnow()
            ist_now = utc_now + datetime.timedelta(minutes=30, hours=5)

            edit_text += f"""\n<b>Last checked</b> :- [{str(utc_now)} UTC](https://www.google.com/search?q={utc_now}+UTC+local+time)\n<code>Updated every hours</code>"""

            user_client.edit_message_text(update_channel, status_message_id,
                                         edit_text)
            print(f"[INFO] everything done! sleeping for 15 mins...")

            time.sleep(time * 60)


main()
