const express = require("express");
const fs = require("fs");

const app = express();
const PORT = 3000;

function challengeComplete(path) {
  path = path.slice(1); // remove '/'
  // open our db.json and load
  fs.readFile("db.json", "utf8", (err, data) => {
    if (err) {
      console.error("Error reading file:", err);
      return;
    }
    // convert to json
    var challengesData = JSON.parse(data);

    var challenges = challengesData.challenges;

    // get index of challenge from path
    var challengeIndex = challenges.findIndex(
      (challenge) => challenge.name === path
    );
    // update completion status
    if (challengeIndex !== -1) {
      challenges[challengeIndex].completed = true;
    } else {
      console.error("Challenge not found");
      return;
    }

    // write updated db
    fs.writeFile(
      "db.json",
      JSON.stringify(challengesData, null, 2),
      "utf8",
      (err) => {
        if (err) {
          console.error("Error writing to file:", err);
          return;
        }

        console.log(path + " marked as completed, and data written to file.");
      }
    );
  });
}

// statues endpoint to dump current database state
app.get("/statuses", (req, res) => {
  var db = JSON.parse(fs.readFileSync("./db.json", "utf8"));
  res.send(db);
});

app.get("/*", (req, res) => {
  res.status(200);
  res.send();
  challengeComplete(String(req.path));
});

app.listen(PORT, (error) => {
  if (!error)
    console.log("Server is Successfully Running, http://localhost:" + PORT);
  else console.log("Error occurred, server can't start", error);
});
