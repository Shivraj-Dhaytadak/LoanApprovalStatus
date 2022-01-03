import express from "express";
import mongoose from "mongoose";
import ejsMate from "ejs-mate";
import path from "path";
import { createUser, validateUser } from "./controllers/user.js";
import { validateAdmin } from "./controllers/admin.js";

const app = express();
const __dirname = path.resolve();

app.engine("ejs", ejsMate);
app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.set("view engine", "ejs");
app.set("views", path.join(__dirname, "views"));
app.use(express.static(path.join(__dirname, "public")));

mongoose.connect("mongodb://localhost:27017/bankuser");

app.get("/", (req, res) => {
  res.json({ message: "Hello listening here shetta" });
});

app.get("/userlogin", (req, res) => {
  res.render("users/userLogin");
});

app.post("/userlogin", validateUser);

app.post("/usersignup", createUser);

app.get("/adminlogin", (req, res) => {
  res.render("admin/adminLogin");
});

app.post("/adminlogin", validateAdmin);

app.get("/bankdashboard", (req, res) => {
  res.send("This is bank dashboard");
});
app.listen(3000, () => {
  console.log("Server is listening on port 3000");
});
