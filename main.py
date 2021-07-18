import base64
from BlackPearl.bp import storage
def start():
    if token == 'paste_token_here' or token is None or not isinstance(token, str):
        print("Invalid Token, open the run.py file and provide a valid token of the bot and try again...")
        return
    else:
        run_bot()

def run_bot():
    no_dc = False
    no_tz = False
    no_sftp = False

    try:
        import discord
    except:
        no_dc = True
    try:
        import pytz
    except:
        no_tz = True

    import subprocess as sp
    if no_dc or no_tz or no_sftp: print("Installing required files, please wait...")
    if no_dc: sp.run('pip install discord.py', shell=True)
    if no_tz: sp.run('pip install pytz', shell=True)

    from BlackPearl.bp import blackPearl
    b = blackPearl.get_json('bot')
    b['token'] = token
    blackPearl.dump_json('bot', b)
    blackPearl.bot.run(token)
import keep_alive
keep_alive.keep()
token = "ODUyMzk2MzUyNzE2NTM3ODY4.YMGN9w.teHr2G0ybuzaPa0V2xHIvUfFQsY"
start()
