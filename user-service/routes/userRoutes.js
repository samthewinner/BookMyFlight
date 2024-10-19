import { Router } from "express";
import { registerUser,loginUser,updateFlightHistory } from "../controllers/user.js";
import { loginAdmin , registerAdmin } from "../controllers/admin.js";

const router = Router();

// router.route('/').post(registerUser);
router.post('/register',registerUser);
router.post('/login',loginUser)
router.post('/updateFlightHistory',updateFlightHistory);



export {router};