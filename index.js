const { TOKEN } = require('./config.json');
const Discord = require('discord.js');
const bot = new Discord.Client();

bot.on('ready', () => {
    console.log('Bot online');
});


// let ashamed_users = [];

bot.on('voiceStateUpdate', (oldMember, newMember) => {
    console.log('VoiceStateChange');

    const verdiloosRole = newMember.guild.roles.cache.find(role => role.name == 'verdiløs');
    // console.log(verdiloosRole);

    const newChannelName = newMember.channel.name;
    const user = oldMember.member;

    // console.log(user.roles.cache);

    if (newChannelName == 'Skammekroken') {
        user.roles.set([verdiloosRole]);
    }
});


bot.login(TOKEN);
