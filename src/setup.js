module.exports.setupGuild = function (newGuild, skammekroken, verdilos) {
  const skammekrokenChannel = newGuild.channels.cache.find(
    (channel) => channel.name == skammekroken
  );
  const verdiloosRole = newGuild.roles.cache.find(
    (role) => role.name == verdilos
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
        name: verdilos,
        permissions: 1050624,
      },
    });
  }
};
