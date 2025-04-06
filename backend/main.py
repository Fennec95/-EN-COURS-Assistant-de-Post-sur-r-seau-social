from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext
from fastapi.openapi.utils import get_openapi
from backend.socials import get_best_posting_time

app = FastAPI()

# Clé secrète pour signer les tokens (à garder confidentielle)
SECRET_KEY = "supersecretkey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")



# Fonction pour vérifier le token JWT
def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Utilisateur non authentifié")
        return username
    except JWTError:
        raise HTTPException(status_code=401, detail="Token invalide")


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Post Assistant API",
        version="1.0.0",
        description="API pour gérer les posts Instagram, TikTok et YouTube Shorts",
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi


# Simule une base de données avec un seul utilisateur
fake_users_db = {
    "admin": {
        "username": "admin",
        "hashed_password": "$2b$12$xWyS14Tt1Zq3rfpe86/Dm.d32GYzvL9Lx/8yewhBws/f3cEp7xWRe", 
    }
}

# Utilitaire pour hacher les mots de passe
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 pour gérer les tokens
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# Fonction pour vérifier le mot de passe
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


# Fonction pour générer un token JWT
def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# Route pour obtenir un token
@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = fake_users_db.get(form_data.username)
    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Identifiants incorrects")
    
    access_token = create_access_token(data={"sub": user["username"]}, expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    
    return {"access_token": access_token, "token_type": "bearer"}


# Route protégée (nécessite un token)
@app.get("/protected")
async def protected_route(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Utilisateur non authentifié")
        return {"message": f"Bienvenue, {username}!"}
    except JWTError:
        raise HTTPException(status_code=401, detail="Token invalide")

@app.get("/api/best_time")
async def get_best_time(user: str = Depends(get_current_user)):
    insta = get_best_posting_time("instagram")
    tiktok = get_best_posting_time("tiktok")
    youtube = get_best_posting_time("youtube")

    return {
        "message": f"Bonjour {user}, voici les meilleurs horaires pour poster :",
        "Instagram": insta,
        "TikTok": tiktok,
        "YouTube": youtube
    }