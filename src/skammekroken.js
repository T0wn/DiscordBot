const { log_shame } = require("./logging.js");

const ashamed_users = [];

module.exports.should_be_shamed = (oldMember, newMember, bot, skammekroken) => {
  const newChannel = newMember.channel;
  const oldChannel = oldMember.channel;
  const newUser = newMember.member;

  if (newUser.user != bot.user) {
    if (newChannel != null && oldChannel != null) {
      if (newChannel.name == skammekroken && oldChannel.id != newChannel.id) {
        return true;
      }
    }
  }
  return false;
};

module.exports.should_be_unshamed = (
  oldMember,
  newMember,
  bot,
  skammekroken
) => {
  const newChannel = newMember.channel;
  const oldChannel = oldMember.channel;
  const newUser = newMember.member;

  if (newUser.user != bot.user) {
    if (newChannel != null && oldChannel != null) {
      if (
        newChannel.name != skammekroken &&
        newChannel != null &&
        oldChannel.id != newChannel.id
      ) {
        return true;
      }
    }
  }
  return false;
};

module.exports.shame = async (oldMember, newMember, verdilos) => {
  const verdiloosRole = newMember.guild.roles.cache.find(
    (role) => role.name == verdilos
  );

  const newChannel = newMember.channel;
  const newUser = newMember.member;
  const oldUser = oldMember.member;

  ashamed_users.push({ userID: oldUser.id, roles: oldUser.roles.cache });
  newUser.roles.set([verdiloosRole]).catch((error) => {
    console.log(error);
  });
  newUser.voice.setMute(true);

  log_shame(newUser);

  const connenction = await newChannel.join();
  const dispatcher = connenction.play("./audio/shame-1.mp3", {
    volume: 0.5,
  });

  dispatcher.on("finish", () => {
    dispatcher.destroy();
    connenction.disconnect();
  });
};

module.exports.unshame = (oldMember, newMember) => {
  const oldUser = oldMember.member;
  const newUser = newMember.member;

  const originalUser = ashamed_users.find((usr) => usr.userID == oldUser.id);
  if (originalUser) {
    newUser.roles.set(originalUser.roles);
    newUser.voice.setMute(false);
  }
};
