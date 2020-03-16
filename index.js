const { TOKEN } = require('./config.json');
const Discord = require('discord.js');
const bot = new Discord.Client();

bot.on('ready', () => {
    console.log('Bot online');
});


let ashamed_users = [];

bot.on('voiceStateUpdate', (oldMember, newMember) => {
    console.log('VoiceStateChange');

    const verdiloosRole = newMember.guild.roles.cache.find(role => role.name == 'verdiløs');
    // console.log(verdiloosRole);

    const newChannel = newMember.channel;
    const newUser = newMember.member;
    const oldUser = oldMember.member;

    // console.log(user.roles.cache);

    if (newChannel != null) {
        if (newChannel.name == 'Skammekroken') {
            ashamed_users.push({ ...oldUser });
            console.log(ashamed_users);

            newUser.roles.set([verdiloosRole]);
            console.log('verdiløs');
        }
        else {
            console.log('ikke verdiløs lenger');
            const originalRoles = ashamed_users.find(usr => usr.id == oldUser.id).roles.cache;
            console.log(originalRoles);
        }
    }
});


bot.login(TOKEN);
