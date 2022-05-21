# DictatorBot

This is a discord bot used in my own discord server.

### Current features
* Keeping user locked in a "jail" voice channel
* audioplaying
* memeposting
* logging

Here is an example of how the jail feature looks for the users:

<table>
  <tr>
    <td>Admins perspective</td>
    <td>Users perspective</td>
  </tr>
  <tr>
    <td> <img src="./images/dictatorbot_example_admin.gif"> </td>
    <td> <img src="./images/dictatorbot_example_user.gif"> </td>
  </tr>
</table>

### Tech stack
* [Python](https://www.python.org/)
* [Discord API](https://pypi.org/project/discord.py/)
* [Docker](https://www.docker.com/)
* [Github actions](https://github.com/features/actions)
* [Linode](https://www.linode.com/)

## Getting started
Requires Docker and Docker compose.

### Running locally
1. Clone the project
2. Create a file containing the bot-token for the discord bot used for development at `DictatorBot/secrets/dev_bot_token.txt`
3. Start the bot by running `docker-compose up`
