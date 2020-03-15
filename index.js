const { TOKEN } = require('./config.json');
const Discord = require('discord.js');
const bot = new Discord.Client();

bot.on('ready', () => {
    console.log('Bot online');
});


// let ashamed_users = [];

async function getChannelName(channelID) {
    const name = await bot.channels.fetch(channelID).then((channel) => (channel.name));
    return name;
}

bot.on('voiceStateUpdate', (oldMember, newMember) => {
    console.log('VoiceStateChange');
    // console.log(oldMember);
    // console.log(newMember);

    (async () => {
        const newChannelName = await getChannelName(newMember.channelID);
        const user = await oldMember.guild.members.fetch('153951942677233665').then((member) => (member.user));

        console.log(user);

        if (newChannelName == 'Skammekroken') {
            console.log('Skam deg!');
        }
    })();
});


bot.login(TOKEN);
