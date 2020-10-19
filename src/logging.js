const woodlotCustomLogger = require("woodlot").customLogger;

const woodlot = new woodlotCustomLogger({
  streams: ["./../logs/skammekroken.log"],
  stdout: false,
  format: {
    type: "json",
    options: {
      spacing: 4,
      separator: "\n",
    },
  },
});

module.exports.log_shame = (newUser) => {
  woodlot.info({
    event: "skammekroken-join",
    guild: {
      id: newUser.guild.id,
    },
    user: {
      id: newUser.user.id,
    },
  });
  console.log("hei");
};
