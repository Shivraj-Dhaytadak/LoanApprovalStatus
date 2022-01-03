import { Admin } from "../models/admin.js";

export const validateAdmin = async (req, res) => {
  const admin = await Admin.findOne({ username: req.body.admin.username });
  if (admin.password == req.body.admin.password) {
    res.redirect("/bankdashboard");
  } else {
    res.json({ message: "Wrong" });
  }
};
