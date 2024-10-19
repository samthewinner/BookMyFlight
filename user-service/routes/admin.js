import { Router } from "express";
import { loginAdmin , registerAdmin } from "../controllers/admin.js";

const router = Router();

router.post('/login',loginAdmin);
router.post('/register',registerAdmin);

export {router};