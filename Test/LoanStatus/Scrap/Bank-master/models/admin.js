import mongoose from "mongoose";
const Schema = mongoose.Schema;

const AdminSchema = Schema({
  username: {
    type: String,
    required: true,
  },
  password: {
    type: String,
    required: true,
  },
});

export const Admin = mongoose.model("Admin", AdminSchema);
