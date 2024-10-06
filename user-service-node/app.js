const express = require('express');
const app = express();
const PORT = process.env.PORT || 3000;
const eurekaHelper = require('./eureka-client');

app.listen(PORT, () => {
  console.log("user-service on 3000");
})

app.get('/', (req, res) => {
 res.json("I am user-service")
})

eurekaHelper.registerWithEureka('node-service', PORT);