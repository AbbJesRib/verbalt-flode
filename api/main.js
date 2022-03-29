const express = require("express");
const jwt = require("jsonwebtoken");
const { PrismaClient } = require("@prisma/client");

const prisma = new PrismaClient();

const app = express();

// status
// - 0: not started
// - 1: started
// - 2: finished

app.post("/test", async (req, res) => {
  // Create new test
  const { id } = await prisma.test.create({ data: {} });
  const token = jwt.sign({ id }, process.env.JWT_SECRET);

  res.send({ id, token });
});

app.get("/test/:id", async (req, res) => {
  const { id } = req.params;
  const token = req.headers.authorization.split(" ")[1];

  let isValid = false;

  try {
    const decoded = jwt.verify(token, process.env.JWT_SECRET);
    if (decoded.id === id) isValid = true;
  } catch (err) {
    console.log(err);
  }

  if (!isValid) {
    res.code(401).send({ error: "invalid token" });
    return;
  }

  const test = await prisma.test.findUnique({
    where: { id },
  });

  // test is null if not found
  if (!test) {
    res.code(404).send({ error: "test not found" });
    return;
  }

  res.send(test);
});

app.put("/test/:id", async (req, res) => {
  // analyze audio
  // save result
  // return ok

  const data = await req.file();

  // todo: validate data

  // todo: upload to s3

  res.send({ result: "ok" });
});

app.all("*", (req, res) => {
  res.code(404).send({ error: "not found" });
});

app.listen(process.env.PORT, (err, address) => {
  if (err) {
    app.log.error(err);
    process.exit(1);
  }
});
