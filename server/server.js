const express = require("express");
const app = express();
const cors = require("cors");
const routes = require("./routes");
// const fs = require("fs"); // gone for now, may bring back

// setup app
app.use(express.urlencoded({extended: false}));
app.use(express.json());
app.use(routes);
app.use(cors());

const port = 3000;

// run server
const server = app.listen(port, (err) => {
    if(err) {throw err;}
    console.log(`listening to port ${port}`);
});
