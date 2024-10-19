import dotenv from "dotenv";
import path from 'path';
import { User } from "../model/models.js";
import bcrypt from "bcrypt";
import jwt from 'jsonwebtoken';

const { genSaltSync, hashSync, compareSync } = bcrypt;

import { fileURLToPath } from 'url';
import { dirname } from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);
// Configure dotenv
dotenv.config({ path: path.resolve(__dirname, "../env") });

// Login function
export async function loginUser(req, res) {
    let { email, password } = req.body;

    // Check if email exists
    const user = await User.find({ email: email });

    if (user === null) {
        return res.status(404).json({ msg: "Create account" });
    }

    // Compare the password
    const isPasswordValid = compareSync(password, user[0].password);
    if (!isPasswordValid) {
        return res.status(401).json({ message: 'Invalid email or password' });
    }

    let jwt_secret = process.env.JWT_SECRET || '';

    const token = jwt.sign({ email, userid: user[0].userid, role: 'user' }, jwt_secret, {
        expiresIn: '1h',
        algorithm: 'HS256'
    });

    return res.json({ token });
}

// Register function
export async function registerUser(req, res) {
    console.log(req.body);
    let { email, password, phone, name } = req.body;

    // Check if user already exists
    const user = await User.find({ email: email });
    console.log(user);

    if (user.length !== 0) {
        return res.status(300).json({ msg: "User already exists" });
    }

    // Hash password
    const salt = genSaltSync(10);
    password = hashSync(password, salt);

    // Create new entry in db
    const data = { email, password, phone, name };
    const result = await User.create(data);
    console.log(`A document was inserted with the _id: ${result?.id}`);

    res.status(200).json({ msg: "OK" });
}

// Update flight history function
export async function updateFlightHistory(req, res) {
    const { user_id, flight_id } = req.query;

    if (!user_id || !flight_id) {
        return res.status(400).json({ message: 'user_id and flight_id are required' });
    }

    try {
        // Find the user by user_id
        const user = await User.findOne({ userid: user_id });

        if (!user) {
            return res.status(404).json({ message: 'User not found' });
        }

        // Append the flight_id to the flightHistory array
        user.flightHistory.push(flight_id);

        // Save the updated user document
        await user.save();

        return res.status(200).json({
            message: 'Flight history updated successfully',
            flightHistory: user.flightHistory,
        });
    } catch (error) {
        return res.status(500).json({ message: 'Internal Server Error', error });
    }
}
