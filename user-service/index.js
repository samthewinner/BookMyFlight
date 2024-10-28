import { config } from "dotenv";
import { resolve } from "path";

import { registerWithEureka } from "./eureka-client.js";
import express, { json } from "express";
import { connectDB } from "./model/models.js";
import { router as registerRoute } from "./routes/userRoutes.js";
import { router as adminRouter } from "./routes/admin.js";

connectDB();

const app = express();
const port = 3000;

// Register the service with Eureka
registerWithEureka('node-service', port);

app.use(json());

// Register the /user route
app.use('/user', registerRoute);
app.use('/admin',adminRouter);

app.get('/', (req, res) => {
  res.send('Hi from node world!');
});

app.listen(port, () => {
  console.log(`App listening on port ${port}`);
});
