const Discord = require("discord.js");

const { TOKEN } = require("./config.json");
const { setupGuild } = require("./src/setup.js");
const {
  shame,
  unshame,
  should_be_shamed,
  should_be_unshamed,
} = require("./src/skammekroken.js");

const bot = new Discord.Client();
const skammekroken = "Skammekroken";
const verdilos = "Verdiløs";

bot.on("ready", () => {
  console.log(`${bot.user.tag} online!`);
});

bot.on("guildCreate", (newGuild) =>
  setupGuild(newGuild, skammekroken, verdilos)
);

// voiceStateUpdate triggres på all voiceChannel change, inkludert mute, deafen, etc.
bot.on("voiceStateUpdate", async (oldMember, newMember) => {
  if (should_be_shamed(oldMember, newMember, bot, skammekroken)) {
    shame(oldMember, newMember, verdilos);
  }
  if (should_be_unshamed(oldMember, newMember, bot, skammekroken)) {
    unshame(oldMember, newMember);
  }
});

bot.login(TOKEN);
