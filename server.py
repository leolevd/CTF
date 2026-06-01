import fastapi
import fastapi.responses
import SQLManager
from sqlWatcher import watch
import uvicorn
import base64

flag_got = False
app = fastapi.FastAPI(docs_url=None, redoc_url=None)


@app.get("/")
def return_docs():
    return fastapi.responses.FileResponse("HTML/docs.html", status_code=200)

@app.get("/signup")
def signup(username:str, password:str, key: str):
    if not key == "MANAGER-SIGNUP-KEY1337":
        return fastapi.responses.JSONResponse({"message": "403 Forbidden"}, status_code=403)
    else:
        SQLManager.add_user(username, password, role="user")
        return {"message": "Successful"}

@app.get("/email")
def email(username:str, password:str):
    if SQLManager.vulnerable_login(username, password):
        if username == "George":
            return fastapi.responses.JSONResponse(
                {"message": "success!", "E-mail": "1: From: Grace, 2: From You to Grace, 3: From Grace", "email_body1": "Hi George! We have one hole, the code doesn't check the privelege when you promote a user to a manager via /admin, could you message Nu11Byt3 about it? I don't have his contact.", "email_body2": "Hi Grace! Good to hear from you! Currently, I don't have access to work mail. You could send it from me. My password is qwerty123", "email_body3": "Great! Thank you!"},
                status_code=418
            )
        return {"message": "success!", "E-mail": "empty"}
    return fastapi.responses.JSONResponse({"message": "Invalid credentials"}, status_code=401)

@app.get("/admin/promote")
def promote_to_manager(username: str, password: str, usernameofuser: str):
    SQLManager.update_role(usernameofuser, "manager")
    return {"message": "SUCCESS!"}



@app.get("/manager/getkey")
def getKey(username: str, password:str):
    status, role = SQLManager.safe_login(username, password)
    if status and role in ["manager", "admin", "top_admin"]:
        return {"key": "MANAGER-SIGNUP-KEY1337"}
    raise fastapi.HTTPException(401)

@app.get("/manager/delete")
def delete_user_by_id(id: int, username: str, password: str):
    status, role = SQLManager.safe_login(username, password)
    if status and role in ["manager", "admin", "top_admin"]:
        SQLManager.delete_user_by_id(id)
        return {"message": "User deleted"}
    raise fastapi.HTTPException(403)

@app.get("/manager/getid")
def get_user_id(usernameofuser: str, username: str, password: str):
    status, role = SQLManager.safe_login(username, password)
    if status and role in ["manager", "admin", "top_admin"]:
        user_id = SQLManager.get_user_id(usernameofuser)
        if user_id is not None:
            return {"id": user_id}
        raise fastapi.HTTPException(404, "User not found")
    raise fastapi.HTTPException(403)

@app.get("/topadmin/secret")
def secret(username, password):
    status, role = SQLManager.safe_login(username, password)
    if status and role == "top_admin":
        global flag_got
        if flag_got:
            return {"message": "Flag already taken!!"}
        flag_got = True
        return {"secret": "CTBYTE{TOP-FLAG-FOREVER!!!}", "msg": "Well done! You took the flag!", "caution": "Save it because nobody will be able to get it again!"} # Flag
    raise fastapi.HTTPException(403)
# === PREDICTABLE HIDDEN ENDPOINTS ===

@app.get("/manager/upgrade")
def manager_upgrade(username: str, password: str, seed: str = ""):
    status, role = SQLManager.safe_login(username, password)
    if status and role == "manager":
        if seed == "GRACE_ADMIN_SEED_1337":
            SQLManager.update_role(username, "admin")
            return {"message": "UPGRADED!"}
        return fastapi.responses.JSONResponse({"message": "Wrong seed"}, status_code=403, headers={"DEBUG": "GRACE_ADMIN_SEED_1337"}) # <-- hint for the seed
    raise fastapi.HTTPException(403)

@app.get("/admin/transfer")
def admin_transfer(username: str, password: str, key: str = ""):
    status, role = SQLManager.safe_login(username, password)
    if status and role == "admin":
        if key == "NU11BYT3_TRANSFER_KEY8530":
            SQLManager.update_role(username, "top_admin")
            return {"message": "DONE!"}
        return fastapi.responses.JSONResponse({"message": "Wrong /key"}, status_code=403)
    raise fastapi.HTTPException(403)

@app.get("/key")
def get_key(username: str, password: str):
    status, role = SQLManager.vulnerable_login(username, password)
    if status and role == "top_admin":
        return {"key": "NU11BYT3_TRANSFER_KEY8530"}
    raise fastapi.HTTPException(403)
# Hidden in source - keys are commented
# ADMIN_SEED = "GRACE_ADMIN_SEED_1337"
# TRANSFER_KEY = "NU11BYT3_TRANSFER_KEY"

# === Easter Eggs ===

@app.get("/archive")
def archive():
    raise fastapi.HTTPException(status_code=451, detail="Unavailable For Legal Reasons.") # To get the archive, you need to go to /archive/home, but this endpoint is hidden and not listed in the docs, so you need to guess it or find it in the source code. This is a hint for the hidden endpoint.
@app.get("/archive/{}")
def archive_id(anything):
    if anything == "home":
        return fastapi.responses.FileResponse("archive.zip", status_code=200, headers={"Message": "Great job finding the sourse code!"})
    raise fastapi.HTTPException(status_code=404, detail="This archive doesn't exist, go to: /archive/home")

@app.get("/easteregg")
def easteregg():
    raise fastapi.HTTPException(status_code=403, detail="Wanna the easter egg? Well, I'm not going to give it to you that easily! Go find it somewhere.")
@app.get("/somewhere") # Hahaha, the message said - somewhere, but no one would think of it that way...
def somewhere():
    return {"message": "Congratulations! You found the easter egg! Here's your reward: {}. Oh no! It's just hex! Try doing something to it....".format(base64.b64encode(b"CTBYTE{EASTER_EGG_FOUND!!!}").hex())} # Easter Egg

uvicorn.run(
    app=app,
    host="127.0.0.1",
    port=1337
)
