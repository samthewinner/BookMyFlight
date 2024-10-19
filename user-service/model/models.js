import mongoose from 'mongoose';
import { v4 as uuidv4 } from 'uuid';
import dotenv from "dotenv";
import path from 'path';
import { fileURLToPath } from 'url';
import { dirname } from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

dotenv.config({ path: path.resolve(__dirname, "../.env") });

// Define the User schema 
const UserSchema = new mongoose.Schema({
  userid: { type: String, required: true, unique: true, default: uuidv4 },
  name: { type: String, required: true },
  email: { type: String, required: true, unique: true },
  password: { type: String, required: true },
  phone: { type: String, required: true },
  flightHistory: { type: [String], required: false },
});

// Create the User model
const User = mongoose.model('User', UserSchema);

// MongoDB connection string (from environment variable)
const uri = process.env.MONGO_URI || "";

const AdminSchema = new mongoose.Schema({
  id: { type: String, required: true, unique: true, default: uuidv4 },
  name: {type: String , required: true, },
  email: { type: String, required: true, unique: true },
  password: { type: String, required: true }
})

const Admin = mongoose.model('Admin',AdminSchema)

// Connect to MongoDB function
const connectDB = async () => {
  try {
    await mongoose.connect(uri, {
      autoIndex: true
    });
    console.log('MongoDB Atlas connected!');
  } catch (err) {
    console.error('Connection error:', err);
  }
};

// Export User model and connectDB function
export { User, Admin , connectDB };
