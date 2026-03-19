from datetime import datetime, date, time
from typing import Any, List, Optional, Union, Set
from enum import Enum
from pydantic import BaseModel, field_validator

from abc import ABC, abstractmethod

############################################
# Enumerations are defined here
############################################

class StatutReservation(Enum):
    Terminee = "Terminee"
    En_Attente = "En_Attente"
    Confirmee = "Confirmee"
    Annulee = "Annulee"

############################################
# Classes are defined here
############################################
class IndisponibiliteCreate(BaseModel):
    type: str
    motif: str
    dateFin: datetime
    dateDebut: datetime


class ReservationCreate(BaseModel):
    statut: StatutReservation
    notes: str
    montantTotal: float
    delaiConfirmation: int
    id: str
    dateCreation: datetime
    dateDebut: datetime
    dateFin: datetime
    evenement: int  # 1:1 Relationship (mandatory)
    lignereservation: int  # 1:1 Relationship (mandatory)
    elementcentre_3: List[int]  # N:M Relationship


class TarifCreate(BaseModel):
    dateFin: datetime
    dateDebut: datetime
    prixDemiJournee: float
    prixJournalier: float
    elementcentre_1: int  # N:1 Relationship (mandatory)


class ElementCentreCreate(ABC, BaseModel):
    capaciteMax: int
    id: str
    nom: str
    dureeMiniLocation: int
    description: str
    actif: bool
    reservation: List[int]  # N:M Relationship
    centredecongres_1: int  # N:1 Relationship (mandatory)
    indisponibilite: Optional[List[int]] = None  # 1:N Relationship
    tarif: Optional[List[int]] = None  # 1:N Relationship


class GestionnaireCreate(BaseModel):
    nom: str
    id: str
    prenom: str
    email: str
    emailReferent: str


class CentreDeCongresCreate(BaseModel):
    nom: str
    email: str
    delaiConfirmationDefaut: int
    id: str
    telephone: str
    adresse: str
    gestionnaire: int  # 1:1 Relationship (mandatory)
    elementcentre: Optional[List[int]] = None  # 1:N Relationship


class PrestationCreate(ABC, BaseModel):
    nom: str
    id: str
    description: str
    prixUnitaire: float
    lignereservation_1: int  # N:1 Relationship (mandatory)


class PrestationGlobaleCreate(PrestationCreate):
    unite: str
    quantiteMin: int


class PrestationDimensionneeCreate(PrestationCreate):
    nbParticipantsMax: int
    nbParticipantsMin: int


class StockMaterielCreate(BaseModel):
    quantiteEnPanne: int
    quantiteTotale: int
    dateMaj: datetime
    materiel: int  # N:1 Relationship (mandatory)


class MaterielCreate(BaseModel):
    nom: str
    description: str
    id: str
    prixUnitaire: float
    quantiteMinimale: int
    stockmateriel: Optional[List[int]] = None  # 1:N Relationship
    lignereservation_2: int  # 1:1 Relationship (mandatory)


class EvenementCreate(BaseModel):
    dateFin: datetime
    description: str
    dateDebut: datetime
    id: str
    nom: str
    nbParticipantsPrevus: int
    reservation_2: int  # 1:1 Relationship (mandatory)


class LigneReservationCreate(BaseModel):
    dateDebut: date
    quantite: int
    sousTotal: float
    dateFin: date
    prestation: Optional[List[int]] = None  # 1:N Relationship
    materiel_1: int  # 1:1 Relationship (mandatory)
    reservation_1: int  # 1:1 Relationship (mandatory)


