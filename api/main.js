const fastify = require("fastify");
const jwt = require("jsonwebtoken");
const { PrismaClient } = require("@prisma/client");

const prisma = new PrismaClient();

const app = fastify({ logger: true });
app.register(require("fastify-multipart"));

const privateKey = "secret";

// status
// - 0: not started
// - 1: started
// - 2: finished

app.get("/", (req, res) => {
  res.send({ hello: "world" });
});

app.post("/test", async (req, res) => {
  // create new test
  // return test id, token

  const { id } = await prisma.test.create({ data: {} });
  const token = jwt.sign({ id }, privateKey);

  res.send({ id, token });
});

app.get("/test/:id", async (req, res) => {
  const { id } = req.params;
  const token = req.headers.authorization.split(" ")[1];

  try {
    jwt.verify(token, privateKey);

    // todo: validate test id
  } catch (err) {
    console.log(err);
    res.code(401).send({ error: "invalid token" });
    return;
  }

  const test = await prisma.test.findUnique({
    where: { id },
  });

  res.send(test);
});

app.put("/test/:id", async (req, res) => {
  // analyze audio
  // save result
  // return ok

  const data = await req.file();

  // todo: validate data

  // todo: send to google api

  res.send({ result: "ok" });
});

app.listen(process.env.PORT, (err, address) => {
  if (err) {
    app.log.error(err);
    process.exit(1);
  }
});
