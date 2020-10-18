const { TOKEN } = require("./config.json");
const woodlotCustomLogger = require("woodlot").customLogger;
const Discord = require("discord.js");

const bot = new Discord.Client();
const skammekroken = "Skammekroken";
const Verdilos = "Verdiløs";

const woodlot = new woodlotCustomLogger({
  streams: ["./logs/skammekroken.log"],
  stdout: false,
  format: {
    type: "json",
    options: {
      spacing: 4,
      separator: "\n",
    },
  },
});

bot.on("ready", () => {
  console.log(`${bot.user.tag} online!`);
});

bot.on("guildCreate", (newGuild) => {
  const skammekrokenChannel = newGuild.channels.cache.find(
    (channel) => channel.name == skammekroken
  );
  const verdiloosRole = newGuild.roles.cache.find(
    (role) => role.name == Verdilos
  );

  if (!skammekrokenChannel) {
    newGuild.channels.create(skammekroken, {
      type: "voice",
      position: newGuild.channels.cache.size,
    });
  }
  if (!verdiloosRole) {
    newGuild.roles.create({
      data: {
        name: Verdilos,
        permissions: 1050624,
      },
    });
  }
});

const ashamed_users = [];

// voiceStateUpdate triggres på all voiceChannel change, inkludert mute, deafen, etc.
bot.on("voiceStateUpdate", async (oldMember, newMember) => {
  console.log("VoiceStateChange");

  const verdiloosRole = newMember.guild.roles.cache.find(
    (role) => role.name == Verdilos
  );

  const newChannel = newMember.channel;
  const oldChannel = oldMember.channel;
  const newUser = newMember.member;
  const oldUser = oldMember.member;

  if (newUser.user != bot.user) {
    if (newChannel != null && oldChannel != null) {
      if (newChannel.name == skammekroken && oldChannel.id != newChannel.id) {
        ashamed_users.push({ userID: oldUser.id, roles: oldUser.roles.cache });
        newUser.roles.set([verdiloosRole]).catch((error) => {
          console.log(error);
        });
        newUser.voice.setMute(true);

        const connenction = await newChannel.join();
        const dispatcher = connenction.play("./audio/shame-1.mp3", {
          volume: 0.5,
        });

        dispatcher.on("finish", () => {
          dispatcher.destroy();
          connenction.disconnect();
        });

        woodlot.info({
          event: "skammekroken-join",
          guild: {
            id: newUser.guild.id,
            name: newUser.guild.name,
          },
          user: {
            id: newUser.user.id,
            username: newUser.user.username,
          },
        });
      } else if (
        newChannel != skammekroken &&
        newChannel != null &&
        oldChannel.id != newChannel.id
      ) {
        const originalUser = ashamed_users.find(
          (usr) => usr.userID == oldUser.id
        );
        if (originalUser) {
          newUser.roles.set(originalUser.roles);
          newUser.voice.setMute(false);
        }
      }
    }
  }
});

bot.login(TOKEN);
