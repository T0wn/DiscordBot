const { TOKEN } = require('./config.json');
const Discord = require('discord.js');
const bot = new Discord.Client();

bot.on('ready', () => {
    console.log('Bot online');
});


const ashamed_users = [];

// voiceStateUpdate triggres på all voiceChannel change, inkludert mute, deafen, etc.
bot.on('voiceStateUpdate', async (oldMember, newMember) => {
    console.log('VoiceStateChange');

    const verdiloosRole = newMember.guild.roles.cache.find(role => role.name == 'Verdiløs');
    // const skammekrokenChannel = newMember.guild.channels.cache.find(channel => channel.name == 'Skammekroken');
    // console.log(skammekrokenChannel);

    const newChannel = newMember.channel;
    const oldChannel = oldMember.channel;
    const newUser = newMember.member;
    const oldUser = oldMember.member;

    // console.log('newChannel: ' + newChannel);
    // console.log('oldChannel: ' + oldChannel);
    // console.log('newUser: ' + newUser);
    // console.log('oldUser: ' + oldUser);

    if (newChannel != null && oldChannel != null) {
        if (newChannel.name == 'Skammekroken' && oldChannel.id != newChannel.id) {
            ashamed_users.push({ userID: oldUser.id, roles: oldUser.roles.cache });
            newUser.roles.set([verdiloosRole]);
            newUser.voice.setMute(true);

            const connenction = await newChannel.join();
            const dispatcher = connenction.play('./audio/shame-1.mp3', { volume: 0.5 });

            dispatcher.on('finish', () => {
                dispatcher.destroy();
                connenction.disconnect();
            });
        }
        else if (newChannel != 'Skammekroken' && newChannel != null && oldChannel.id != newChannel.id) {
            const originalUser = ashamed_users.find(usr => usr.userID == oldUser.id);
            if (originalUser) {
                newUser.roles.set(originalUser.roles);
                newUser.voice.setMute(false);
            }
        }
    }
});


bot.login(TOKEN);
