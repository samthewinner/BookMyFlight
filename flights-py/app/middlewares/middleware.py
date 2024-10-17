from fastapi import Request,HTTPException

def checkRole(req:Request):
    role = req.headers.get('role')
    if role is None :
        raise HTTPException(status_code=401 , detail="Unauthorized, no token found")
    if role != "admin":
        raise HTTPException(status_code=401 , detail="Unauthorized, user can't access this!!")
    

    
    
