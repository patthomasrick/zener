# Zener

A Discord Bot.

[Add Zener to your server (may require explicit permission from me)](https://discord.com/api/oauth2/authorize?client_id=967217448384331776&permissions=2159029248&scope=bot%20applications.commands)

## Install

[Python](https://www.python.org/downloads/) 3.10 was used. You can probably go lower, but support is at your own risk.

I strongly recommend setting up a `venv`, but this can be skipped:

```sh
python -m venv .venv

# Linux
source .venv/bin/activate
# # Windows (Powershell)
# ps .venv/Scripts/Activate.ps1
```

Install requirements:

```sh
pip install -r requirements.txt
```

Save your bot token to `secret.txt`. Contents should just be the token itself on the first line. Newline doesn't matter.

Launch:

```sh
python -m zener
```

### Via Docker

You can also start the application via [Docker](https://www.docker.com/) or [Docker Compose](https://docs.docker.com/compose/).

Docker Compose is also provided purely for convenience and for hosting.

#### Docker

<!-- prettier-ignore -->
_From [https://hub.docker.com/\_/python/](https://hub.docker.com/_/python/)._

```sh
docker build -t my-python-app .
docker run -it --rm --name my-running-app my-python-app
```

#### Docker Compose

```sh
docker compose up --build
```

## Commands

All commands are accessible through Discord's bot application command integrations. Typing `/` should bring up this bot's commands.

The commands are refreshed on bot restart for every guild that the application has access to.

### YouTube

#### `/join`

Join the sender's current voice channel.

#### `/leave`

Leave the bot's voice channel on the current guild. Does not require that the sender is in the same voice channel.

#### `/play <YouTube URL>`

_Aliases:_

- `/youtube <YouTube URL>`
- `/yt <YouTube URL>`

Play the specified link in the bot's current voice channel.

If the bot is not in a voice channel and the sender is, then the bot will first join the sender's voice channel and then play the audio of the URL.

#### `/stop`

Stop the currently playing song but stay in the voice channel. A song must be playing for this to be successful.

### Utilities

#### `/rm messages_by_exact_text <Message contents>`

Find all messages that exactly match the first argument and prompt if those messages should be deleted.

This operation must be confirmed for it to occur.

#### `/rm messages_by_start_text <Message contents>`

Find all messages that start with the first argument and prompt if those messages should be deleted.

This operation must be confirmed for it to occur.

## Why is it named Zener?

It is named Zener because of my favorite electrical component, the [Zener diode](https://en.wikipedia.org/wiki/Zener_diode).
