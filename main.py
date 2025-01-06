from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

from sqlmodel import SQLModel
from fastapi.middleware.cors import CORSMiddleware

from app.config.database import init_db
from app.routers.otp_route import otprouter 
import logging


# Charger les variables d'environnement
load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DOMAINS = os.getenv("DOMAINS")


def domains_origins():
    try:
        domain = DOMAINS.split(",")
        return domain
    except:
        return [DOMAINS]


DATABASE_URL = os.getenv("DATABASE_URL")

logger.warning("DATABASE_URL is %s", DATABASE_URL)
# Créer un moteur asynchrone
engine = create_async_engine(DATABASE_URL, echo=True)

# Créer une fabrique de sessions asynchrones
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

# Créez les tables au démarrage de l'application
init_db()

app = FastAPI(
    title="AUTH USER | OIDC",
    description="FastAPI | Keycloak | Python",
    version="0.0.1",
    contact={
        "url": "https://st2i.net",
    },
)
logger.warning(f"DOMAINS {domains_origins()}")

app.add_middleware(
    CORSMiddleware,
    allow_origins=domains_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Inclure les routes
app.include_router(otprouter, prefix="/receive", tags=["@Otp"])




