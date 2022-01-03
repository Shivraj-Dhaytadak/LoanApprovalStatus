import { User } from "../models/user.js";

export const validateUser = async (req, res) => {
  const user = await User.findOne({ username: req.body.user.username });
  if (!user) {
    res.json({ message: "No user found" });
  } else {
    res.render("users/userDashboard", { user });
  }
};

export const createUser = async (req, res) => {
  const { username, email, password, cpassword } = req.body.user;
  if (cpassword == password) {
    const user = await new User(req.body.user);
    user.save();
    res.redirect("/");
  } else {
    res.redirect("/");
  }
};
