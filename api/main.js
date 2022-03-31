const express = require("express");
const jwt = require("jsonwebtoken");
const { PrismaClient } = require("@prisma/client");
const aws = require("aws-sdk");
const multer = require("multer");
const multerS3 = require("multer-s3");

const prisma = new PrismaClient();
const app = express();

const s3 = new aws.S3({
  accessKeyId: process.env.AWS_ACCESS_KEY_ID,
  secretAccessKey: process.env.AWS_SECRET_ACCESS_KEY,
});

const storage = multerS3({
  s3,
  bucket: "game-intelligence",
  key: (req, file, cb) => {
    const fileExtension = file.originalname.split(".").pop();
    cb(null, `${Date.now().toString()}.${fileExtension}`);
  },
});

const upload = multer({ storage });

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

// Middleware for validating JWT token
app.use("/test/:id", async (req, res, next) => {
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
    res.status(401).send({ error: "invalid token" });
    return;
  }

  res.locals.id = id;

  next();
});

app.get("/test/:id", async (req, res) => {
  const { id } = res.locals;

  const test = await prisma.test.findUnique({
    where: { id },
  });

  // test is null if not found
  if (!test) {
    res.status(404).send({ error: "test not found" });
    return;
  }

  res.send(test);
});

app.put("/test/:id", upload.array("audio", 1), async (req, res) => {
  // analyze audio
  // save result
  // return ok

  const { id } = res.locals;

  // todo: validate id

  // form data
  // const { audio } = req.body;
  console.log(req.files);

  // todo: validate file
  // console.log(data);

  // const params = {
  //   Bucket: "testBucket", // pass your bucket name
  //   Key: `${id}-1.ogg`, // file will be saved as testBucket/contacts.csv
  //   Body: JSON.stringify(data, null, 2),
  // };

  // todo: upload to s3

  res.send({ result: "ok" });
});

app.all("*", (req, res) => {
  res.status(404).send({ error: "not found" });
});

app.listen(process.env.PORT, (err) => {
  console.log(`Listening on port ${process.env.PORT}`);
});
