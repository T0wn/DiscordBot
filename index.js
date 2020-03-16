const { TOKEN } = require('./config.json');
const Discord = require('discord.js');
const bot = new Discord.Client();

bot.on('ready', () => {
    console.log('Bot online');
});


const ashamed_users = [];

// voiceStateUpdate triggres på all voiceChannel change, inkludert mute, deafen, etc.
bot.on('voiceStateUpdate', (oldMember, newMember) => {
    console.log('VoiceStateChange');

    const verdiloosRole = newMember.guild.roles.cache.find(role => role.name == 'Verdiløs');

    const newChannel = newMember.channel;
    const oldChannel = oldMember.channel;
    const newUser = newMember.member;
    const oldUser = oldMember.member;

    if (newChannel != null) {
        if (newChannel.name == 'Skammekroken' && oldChannel.id != newChannel.id) {
            ashamed_users.push({ userID: oldUser.id, roles: oldUser.roles.cache });
            newUser.roles.set([verdiloosRole]);
        }
        else if (newChannel != 'Skammekroken' && newChannel != null && oldChannel.id != newChannel.id) {
            const originalRoles = ashamed_users.find(usr => usr.userID == oldUser.id).roles;
            newUser.roles.set(originalRoles);
        }
    }
});


bot.login(TOKEN);
