import os
import time
import datetime

import pyrogram

# owner session strings
user_session_string = os.environ.get("user_session_string")

# your all bots username without '@' with a space 1 to another
bots = [i.strip() for i in os.environ.get("bots").split(' ')]

# owner username
bot_owner = os.environ.get("bot_owner")

# your channel username without '@'
update_channel = os.environ.get("update_channel")

# message id of your channel message
status_message_id = int(os.environ.get("status_message_id"))

# api strings from my.telegram.org
api_id = int(os.environ.get("api_id"))
api_hash = os.environ.get("api_hash")

# time in minutes for sleeping
time = int(os.environ.get("time"))

user_client = pyrogram.Client(
    user_session_string, api_id=api_id, api_hash=api_hash)


def main():
    with user_client:
        while True:
            print("[INFO] starting to check uptime..")
            edit_text = f"<b>@{update_channel}'s bots status:</b>\n(Updated every 15 mins)\n\n"
            for bot in bots:
                print(f"[INFO] checking @{bot}")
                snt = user_client.send_message(bot, '/start')

                time.sleep(time)

                msg = user_client.get_history(bot, 1)[0]
                if snt.message_id == msg.message_id:
                    print(f"[WARNING] @{bot} is down")
                    edit_text += f"<b>➲ @{bot} :</b> ❌\n\n"
                    user_client.send_message(bot_owner,
                                             f"@{bot} status: `Down`")
                else:
                    print(f"[INFO] all good with @{bot}")
                    edit_text += f"<b>➲ @{bot} :** ✅</b>\n\n"
                user_client.read_history(bot)

            utc_now = datetime.datetime.utcnow()
            ist_now = utc_now + datetime.timedelta(minutes=30, hours=5)

            edit_text += f"\n<b>Last checked</b> :- [{str(utc_now)} UTC](https://www.google.com/search?q={utc_now}+local+time)"

            user_client.edit_message_text(update_channel, status_message_id,
                                         edit_text)
            print(f"[INFO] everything done! sleeping for 15 mins...")

            time.sleep(time * 60)


main()
