const createCsvWriter = require("csv-writer").createObjectCsvWriter;
var moment = require("moment");

const csvWriter = createCsvWriter({
  path: "./logs/skammekroken.csv",
  header: [
    { id: "time", title: "time" },
    { id: "guildID", title: "guildID" },
    { id: "userID", title: "userID" },
  ],
  append: true,
});

module.exports.log_shame = (newUser) => {
  csvWriter.writeRecords([
    {
      time: moment().toISOString(),
      guildID: newUser.guild.id,
      userID: newUser.user.id,
    },
  ]);
};
