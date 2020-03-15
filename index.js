
const BOT_TOKEN = require('./config');
const Discord = require('discord.js');
const bot = new Discord.Client();

const token = BOT_TOKEN;

bot.on('ready', () => {
    console.log('Bot online');
});



var ashamed_users = [];

async function getChannelName(channelID) {
    const name = await bot.channels.fetch(channelID).then((channel) => (channel.name) );
    
    return name;
}

bot.on('voiceStateUpdate', (oldMember, newMember) => {
    console.log('VoiceStateChange');
    // console.log(oldMember);
    // console.log(newMember);

    (async () => {
        var newChannelName = await getChannelName(newMember.channelID);
    

        if (newChannelName == 'Skammekroken') {
            console.log('Skam deg!');
            
        }
    })();
    
});


bot.login(token);
