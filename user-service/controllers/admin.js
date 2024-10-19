import dotenv from "dotenv";
import path from 'path';
import { User , Admin} from "../model/models.js";
import bcrypt from "bcrypt";
import jwt from 'jsonwebtoken';

const { genSaltSync, hashSync, compareSync } = bcrypt;

import { fileURLToPath } from 'url';
import { dirname } from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);
// Configure dotenv
dotenv.config({ path: path.resolve(__dirname, "../env") });

export async function loginAdmin(req, res) {
    let { email, password } = req.body;

    // Check if email exists
    const admin = await Admin.find({ email: email });

    if (admin === null) {
        return res.status(404).json({ msg: "Create account" });
    }

    // Compare the password
    const isPasswordValid = compareSync(password, admin[0].password);
    if (!isPasswordValid) {
        return res.status(401).json({ message: 'Invalid email or password' });
    }

    let jwt_secret = process.env.JWT_SECRET || '';

    const token = jwt.sign({ email, id: admin[0].id, role: 'admin' }, jwt_secret, {
        expiresIn: '1h',
        algorithm: 'HS256'
    });

    return res.json({ token });
}

// Register function
export async function registerAdmin(req, res) {
    // console.log(req.body);
    let { email, password, name } = req.body;

    // Check if user already exists
    const admin = await Admin.find({ email: email });
    // console.log(user);

    if (admin.length !== 0) {
        return res.status(300).json({ msg: "User already exists" });
    }

    // Hash password
    const salt = genSaltSync(10);
    password = hashSync(password, salt);

    // Create new entry in db
    const data = { email, password, name };
    const result = await Admin.create(data);
    console.log(`A document was inserted with the _id: ${result?.id}`);

    res.status(200).json({ msg: "OK" });
}