import enum
from typing import List, Optional
from sqlalchemy import (
    create_engine, Column, ForeignKey, Table, Text, Boolean, String, Date, 
    Time, DateTime, Float, Integer, Enum
)
from sqlalchemy.ext.declarative import AbstractConcreteBase
from sqlalchemy.orm import (
    column_property, DeclarativeBase, Mapped, mapped_column, relationship
)
from datetime import datetime as dt_datetime, time as dt_time, date as dt_date

class Base(DeclarativeBase):
    pass

# Definitions of Enumerations
class StatutReservation(enum.Enum):
    Terminee = "Terminee"
    En_Attente = "En_Attente"
    Confirmee = "Confirmee"
    Annulee = "Annulee"


# Tables definition for many-to-many relationships
elementcentre_reservation = Table(
    "elementcentre_reservation",
    Base.metadata,
    Column("reservation", ForeignKey("reservation.id"), primary_key=True),
    Column("elementcentre_3", ForeignKey("elementcentre.id"), primary_key=True),
)

# Tables definition
class Indisponibilite(Base):
    __tablename__ = "indisponibilite"
    id: Mapped[int] = mapped_column(primary_key=True)
    dateDebut: Mapped[dt_datetime] = mapped_column(DateTime)
    dateFin: Mapped[dt_datetime] = mapped_column(DateTime)
    motif: Mapped[str] = mapped_column(String(100))
    type: Mapped[str] = mapped_column(String(100))
    elementcentre_2_id: Mapped[int] = mapped_column(ForeignKey("elementcentre.id"))

class Reservation(Base):
    __tablename__ = "reservation"
    id: Mapped[str] = mapped_column(String(100), primary_key=True)
    dateCreation: Mapped[dt_datetime] = mapped_column(DateTime)
    dateDebut: Mapped[dt_datetime] = mapped_column(DateTime)
    dateFin: Mapped[dt_datetime] = mapped_column(DateTime)
    delaiConfirmation: Mapped[int] = mapped_column(Integer)
    montantTotal: Mapped[float] = mapped_column(Float)
    notes: Mapped[str] = mapped_column(String(100))
    statut: Mapped[StatutReservation] = mapped_column(Enum(StatutReservation))

class Tarif(Base):
    __tablename__ = "tarif"
    id: Mapped[int] = mapped_column(primary_key=True)
    prixJournalier: Mapped[float] = mapped_column(Float)
    prixDemiJournee: Mapped[float] = mapped_column(Float)
    dateDebut: Mapped[dt_datetime] = mapped_column(DateTime)
    dateFin: Mapped[dt_datetime] = mapped_column(DateTime)
    elementcentre_1_id: Mapped[int] = mapped_column(ForeignKey("elementcentre.id"))

class ElementCentre(Base):
    __tablename__ = "elementcentre"
    id: Mapped[str] = mapped_column(String(100), primary_key=True)
    nom: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(String(100))
    capaciteMax: Mapped[int] = mapped_column(Integer)
    dureeMiniLocation: Mapped[int] = mapped_column(Integer)
    actif: Mapped[bool] = mapped_column(Boolean)
    centredecongres_1_id: Mapped[int] = mapped_column(ForeignKey("centredecongres.id"))

class Gestionnaire(Base):
    __tablename__ = "gestionnaire"
    id: Mapped[str] = mapped_column(String(100), primary_key=True)
    nom: Mapped[str] = mapped_column(String(100))
    prenom: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(100))
    emailReferent: Mapped[str] = mapped_column(String(100))

class CentreDeCongres(Base):
    __tablename__ = "centredecongres"
    id: Mapped[str] = mapped_column(String(100), primary_key=True)
    nom: Mapped[str] = mapped_column(String(100))
    adresse: Mapped[str] = mapped_column(String(100))
    telephone: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(100))
    delaiConfirmationDefaut: Mapped[int] = mapped_column(Integer)
    gestionnaire_id: Mapped[int] = mapped_column(ForeignKey("gestionnaire.id"), unique=True)

class Prestation(Base):
    __tablename__ = "prestation"
    nom: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(String(100))
    prixUnitaire: Mapped[float] = mapped_column(Float)
    id: Mapped[str] = mapped_column(String(100), primary_key=True)
    lignereservation_1_id: Mapped[int] = mapped_column(ForeignKey("lignereservation.id"))
    type_spec: Mapped[str] = mapped_column(String(50))
    __mapper_args__ = {
        "polymorphic_identity": "prestation",
        "polymorphic_on": "type_spec",
    }

class PrestationGlobale(Prestation):
    __tablename__ = "prestationglobale"
    id: Mapped[int] = mapped_column(ForeignKey("prestation.id"), primary_key=True)
    unite: Mapped[str] = mapped_column(String(100))
    quantiteMin: Mapped[int] = mapped_column(Integer)
    __mapper_args__ = {
        "polymorphic_identity": "prestationglobale",
    }

class PrestationDimensionnee(Prestation):
    __tablename__ = "prestationdimensionnee"
    id: Mapped[int] = mapped_column(ForeignKey("prestation.id"), primary_key=True)
    nbParticipantsMin: Mapped[int] = mapped_column(Integer)
    nbParticipantsMax: Mapped[int] = mapped_column(Integer)
    __mapper_args__ = {
        "polymorphic_identity": "prestationdimensionnee",
    }

class StockMateriel(Base):
    __tablename__ = "stockmateriel"
    id: Mapped[int] = mapped_column(primary_key=True)
    quantiteTotale: Mapped[int] = mapped_column(Integer)
    quantiteEnPanne: Mapped[int] = mapped_column(Integer)
    dateMaj: Mapped[dt_datetime] = mapped_column(DateTime)
    materiel_id: Mapped[int] = mapped_column(ForeignKey("materiel.id"))

class Materiel(Base):
    __tablename__ = "materiel"
    id: Mapped[str] = mapped_column(String(100), primary_key=True)
    nom: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(String(100))
    prixUnitaire: Mapped[float] = mapped_column(Float)
    quantiteMinimale: Mapped[int] = mapped_column(Integer)

class Evenement(Base):
    __tablename__ = "evenement"
    id: Mapped[str] = mapped_column(String(100), primary_key=True)
    nom: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(String(100))
    nbParticipantsPrevus: Mapped[int] = mapped_column(Integer)
    dateDebut: Mapped[dt_datetime] = mapped_column(DateTime)
    dateFin: Mapped[dt_datetime] = mapped_column(DateTime)
    reservation_2_id: Mapped[int] = mapped_column(ForeignKey("reservation.id"), unique=True)

class LigneReservation(Base):
    __tablename__ = "lignereservation"
    id: Mapped[int] = mapped_column(primary_key=True)
    quantite: Mapped[int] = mapped_column(Integer)
    dateDebut: Mapped[dt_date] = mapped_column(Date)
    dateFin: Mapped[dt_date] = mapped_column(Date)
    sousTotal: Mapped[float] = mapped_column(Float)
    materiel_1_id: Mapped[int] = mapped_column(ForeignKey("materiel.id"), unique=True)
    reservation_1_id: Mapped[int] = mapped_column(ForeignKey("reservation.id"), unique=True)


#--- Relationships of the indisponibilite table
Indisponibilite.elementcentre_2: Mapped["ElementCentre"] = relationship("ElementCentre", back_populates="indisponibilite", foreign_keys=[Indisponibilite.elementcentre_2_id])

#--- Relationships of the reservation table
Reservation.elementcentre_3: Mapped[List["ElementCentre"]] = relationship("ElementCentre", secondary=elementcentre_reservation, back_populates="reservation")
Reservation.evenement: Mapped["Evenement"] = relationship("Evenement", back_populates="reservation_2", foreign_keys=[Evenement.reservation_2_id])
Reservation.lignereservation: Mapped["LigneReservation"] = relationship("LigneReservation", back_populates="reservation_1", foreign_keys=[LigneReservation.reservation_1_id])

#--- Relationships of the tarif table
Tarif.elementcentre_1: Mapped["ElementCentre"] = relationship("ElementCentre", back_populates="tarif", foreign_keys=[Tarif.elementcentre_1_id])

#--- Relationships of the elementcentre table
ElementCentre.indisponibilite: Mapped[List["Indisponibilite"]] = relationship("Indisponibilite", back_populates="elementcentre_2", foreign_keys=[Indisponibilite.elementcentre_2_id])
ElementCentre.centredecongres_1: Mapped["CentreDeCongres"] = relationship("CentreDeCongres", back_populates="elementcentre", foreign_keys=[ElementCentre.centredecongres_1_id])
ElementCentre.tarif: Mapped[List["Tarif"]] = relationship("Tarif", back_populates="elementcentre_1", foreign_keys=[Tarif.elementcentre_1_id])
ElementCentre.reservation: Mapped[List["Reservation"]] = relationship("Reservation", secondary=elementcentre_reservation, back_populates="elementcentre_3")

#--- Relationships of the gestionnaire table
Gestionnaire.centredecongres: Mapped["CentreDeCongres"] = relationship("CentreDeCongres", back_populates="gestionnaire", foreign_keys=[CentreDeCongres.gestionnaire_id])

#--- Relationships of the centredecongres table
CentreDeCongres.gestionnaire: Mapped["Gestionnaire"] = relationship("Gestionnaire", back_populates="centredecongres", foreign_keys=[CentreDeCongres.gestionnaire_id])
CentreDeCongres.elementcentre: Mapped[List["ElementCentre"]] = relationship("ElementCentre", back_populates="centredecongres_1", foreign_keys=[ElementCentre.centredecongres_1_id])

#--- Relationships of the prestation table
Prestation.lignereservation_1: Mapped["LigneReservation"] = relationship("LigneReservation", back_populates="prestation", foreign_keys=[Prestation.lignereservation_1_id])

#--- Relationships of the stockmateriel table
StockMateriel.materiel: Mapped["Materiel"] = relationship("Materiel", back_populates="stockmateriel", foreign_keys=[StockMateriel.materiel_id])

#--- Relationships of the materiel table
Materiel.stockmateriel: Mapped[List["StockMateriel"]] = relationship("StockMateriel", back_populates="materiel", foreign_keys=[StockMateriel.materiel_id])
Materiel.lignereservation_2: Mapped["LigneReservation"] = relationship("LigneReservation", back_populates="materiel_1", foreign_keys=[LigneReservation.materiel_1_id])

#--- Relationships of the evenement table
Evenement.reservation_2: Mapped["Reservation"] = relationship("Reservation", back_populates="evenement", foreign_keys=[Evenement.reservation_2_id])

#--- Relationships of the lignereservation table
LigneReservation.materiel_1: Mapped["Materiel"] = relationship("Materiel", back_populates="lignereservation_2", foreign_keys=[LigneReservation.materiel_1_id])
LigneReservation.prestation: Mapped[List["Prestation"]] = relationship("Prestation", back_populates="lignereservation_1", foreign_keys=[Prestation.lignereservation_1_id])
LigneReservation.reservation_1: Mapped["Reservation"] = relationship("Reservation", back_populates="lignereservation", foreign_keys=[LigneReservation.reservation_1_id])

# Database connection
DATABASE_URL = "sqlite:///Class_Diagram.db"  # SQLite connection
engine = create_engine(DATABASE_URL, echo=True)

# Create tables in the database
Base.metadata.create_all(engine, checkfirst=True)