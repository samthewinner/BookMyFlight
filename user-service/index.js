// import config from "./config";

import { config } from "dotenv";
import { resolve } from "path";

// Setting __filename and __dirname for ES modules
// import { fileURLToPath } from 'url';
// import { dirname } from 'path';

// const __filename = fileURLToPath(import.meta.url);
// const __dirname = dirname(__filename);

// Load environment variables from .env file
// config({ path: resolve(__dirname, ".env") });

import { registerWithEureka } from "./eureka-client.js";
import express, { json } from "express";
import { connectDB } from "./model/models.js";
import { router as registerRoute } from "./routes/userRoutes.js";
import { router as adminRouter } from "./routes/admin.js";


// Connect to the database
connectDB();

// Initialize Express app
const app = express();
const port = 3000;

// Register the service with Eureka
registerWithEureka('node-service', port);

// Middleware to parse incoming JSON requests
app.use(json());

// Register the /user route
app.use('/user', registerRoute);
app.use('/admin',adminRouter);
// Define a basic route for testing
app.get('/', (req, res) => {
  res.send('Hi from node world!');
});

// Start the server on port 3000
app.listen(port, () => {
  console.log(`Example app listening on port ${port}`);
});
