from typing import List
from pydantic import BaseModel
from app.models.otp import Otp
from fastapi import APIRouter, Depends, HTTPException
from app.config.database import get_db  # Dépendance pour obtenir la session
from sqlalchemy.orm import Session

otprouter = APIRouter()

class OtpCreate(BaseModel):
    otp_code : str
    username : str

@otprouter.post("/otp/")
async def store_otp(
    otp:OtpCreate,
    db: Session = Depends(get_db)  # Utilisez AsyncSession ici
):
    try:
        # Créer une instance Otp avec les données reçues
        otp = Otp(username=otp.username, otp_code=otp.otp_code)
        
        # Ajouter l'instance à la session pour la stocker dans la base de données
        db.add(otp)
        db.commit()  # Sauvegarder dans la base de données
        # Rafraîchir l'instance pour récupérer l'ID généré
        db.refresh(otp) 
        # Retourner un message de succès
        return otp
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la sauvegarde de l'OTP: {str(e)}")
    
# Route pour lister tous les OTP enregistrés
@otprouter.get("/otp-list/", response_model=List[Otp])
async def list_otps(db: Session = Depends(get_db)):
    try:
        # Récupérer tous les OTP enregistrés
        otps = db.query(Otp).all()    
        return otps
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la récupération des OTP: {str(e)}")