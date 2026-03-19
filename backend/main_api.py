import uvicorn
import os, json
import time as time_module
import logging
from fastapi import Depends, FastAPI, HTTPException, Request, status, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from pydantic_classes import *
from sql_alchemy import *

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

############################################
#
#   Initialize the database
#
############################################

def init_db():
    SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./data/Class_Diagram.db")
    # Ensure local SQLite directory exists (safe no-op for other DBs)
    os.makedirs("data", exist_ok=True)
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        connect_args={"check_same_thread": False},
        pool_size=10,
        max_overflow=20,
        pool_pre_ping=True,
        echo=False
    )
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)
    return SessionLocal

app = FastAPI(
    title="Class_Diagram API",
    description="Auto-generated REST API with full CRUD operations, relationship management, and advanced features",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_tags=[
        {"name": "System", "description": "System health and statistics"},
        {"name": "Indisponibilite", "description": "Operations for Indisponibilite entities"},
        {"name": "Indisponibilite Relationships", "description": "Manage Indisponibilite relationships"},
        {"name": "Reservation", "description": "Operations for Reservation entities"},
        {"name": "Reservation Relationships", "description": "Manage Reservation relationships"},
        {"name": "Reservation Methods", "description": "Execute Reservation methods"},
        {"name": "Tarif", "description": "Operations for Tarif entities"},
        {"name": "Tarif Relationships", "description": "Manage Tarif relationships"},
        {"name": "Tarif Methods", "description": "Execute Tarif methods"},
        {"name": "ElementCentre", "description": "Operations for ElementCentre entities"},
        {"name": "ElementCentre Relationships", "description": "Manage ElementCentre relationships"},
        {"name": "ElementCentre Methods", "description": "Execute ElementCentre methods"},
        {"name": "Gestionnaire", "description": "Operations for Gestionnaire entities"},
        {"name": "Gestionnaire Relationships", "description": "Manage Gestionnaire relationships"},
        {"name": "Gestionnaire Methods", "description": "Execute Gestionnaire methods"},
        {"name": "CentreDeCongres", "description": "Operations for CentreDeCongres entities"},
        {"name": "CentreDeCongres Relationships", "description": "Manage CentreDeCongres relationships"},
        {"name": "CentreDeCongres Methods", "description": "Execute CentreDeCongres methods"},
        {"name": "Prestation", "description": "Operations for Prestation entities"},
        {"name": "Prestation Relationships", "description": "Manage Prestation relationships"},
        {"name": "Prestation Methods", "description": "Execute Prestation methods"},
        {"name": "PrestationGlobale", "description": "Operations for PrestationGlobale entities"},
        {"name": "PrestationGlobale Methods", "description": "Execute PrestationGlobale methods"},
        {"name": "PrestationDimensionnee", "description": "Operations for PrestationDimensionnee entities"},
        {"name": "PrestationDimensionnee Methods", "description": "Execute PrestationDimensionnee methods"},
        {"name": "StockMateriel", "description": "Operations for StockMateriel entities"},
        {"name": "StockMateriel Relationships", "description": "Manage StockMateriel relationships"},
        {"name": "StockMateriel Methods", "description": "Execute StockMateriel methods"},
        {"name": "Materiel", "description": "Operations for Materiel entities"},
        {"name": "Materiel Relationships", "description": "Manage Materiel relationships"},
        {"name": "Materiel Methods", "description": "Execute Materiel methods"},
        {"name": "Evenement", "description": "Operations for Evenement entities"},
        {"name": "Evenement Relationships", "description": "Manage Evenement relationships"},
        {"name": "Evenement Methods", "description": "Execute Evenement methods"},
        {"name": "LigneReservation", "description": "Operations for LigneReservation entities"},
        {"name": "LigneReservation Relationships", "description": "Manage LigneReservation relationships"},
        {"name": "LigneReservation Methods", "description": "Execute LigneReservation methods"},
    ]
)

# Enable CORS for all origins (for development)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or restrict to ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

############################################
#
#   Middleware
#
############################################

# Request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all incoming requests and responses."""
    logger.info(f"Incoming request: {request.method} {request.url.path}")
    response = await call_next(request)
    logger.info(f"Response status: {response.status_code}")
    return response

# Request timing middleware
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    """Add processing time header to all responses."""
    start_time = time_module.time()
    response = await call_next(request)
    process_time = time_module.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

############################################
#
#   Exception Handlers
#
############################################

# Global exception handlers
@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError):
    """Handle ValueError exceptions."""
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "error": "Bad Request",
            "message": str(exc),
            "detail": "Invalid input data provided"
        }
    )


@app.exception_handler(IntegrityError)
async def integrity_error_handler(request: Request, exc: IntegrityError):
    """Handle database integrity errors."""
    logger.error(f"Database integrity error: {exc}")

    # Extract more detailed error information
    error_detail = str(exc.orig) if hasattr(exc, 'orig') else str(exc)

    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={
            "error": "Conflict",
            "message": "Data conflict occurred",
            "detail": error_detail
        }
    )


@app.exception_handler(SQLAlchemyError)
async def sqlalchemy_error_handler(request: Request, exc: SQLAlchemyError):
    """Handle general SQLAlchemy errors."""
    logger.error(f"Database error: {exc}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "Internal Server Error",
            "message": "Database operation failed",
            "detail": "An internal database error occurred"
        }
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Handle HTTP exceptions with consistent format."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail if isinstance(exc.detail, str) else "HTTP Error",
            "message": exc.detail,
            "detail": f"HTTP {exc.status_code} error occurred"
        }
    )

# Initialize database session
SessionLocal = init_db()
# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception:
        db.rollback()
        logger.error("Database session rollback due to exception")
        raise
    finally:
        db.close()

############################################
#
#   Global API endpoints
#
############################################

@app.get("/", tags=["System"])
def root():
    """Root endpoint - API information"""
    return {
        "name": "Class_Diagram API",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/health", tags=["System"])
def health_check():
    """Health check endpoint for monitoring"""
    from datetime import datetime
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "database": "connected"
    }


@app.get("/statistics", tags=["System"])
def get_statistics(database: Session = Depends(get_db)):
    """Get database statistics for all entities"""
    stats = {}
    stats["indisponibilite_count"] = database.query(Indisponibilite).count()
    stats["reservation_count"] = database.query(Reservation).count()
    stats["tarif_count"] = database.query(Tarif).count()
    stats["elementcentre_count"] = database.query(ElementCentre).count()
    stats["gestionnaire_count"] = database.query(Gestionnaire).count()
    stats["centredecongres_count"] = database.query(CentreDeCongres).count()
    stats["prestation_count"] = database.query(Prestation).count()
    stats["prestationglobale_count"] = database.query(PrestationGlobale).count()
    stats["prestationdimensionnee_count"] = database.query(PrestationDimensionnee).count()
    stats["stockmateriel_count"] = database.query(StockMateriel).count()
    stats["materiel_count"] = database.query(Materiel).count()
    stats["evenement_count"] = database.query(Evenement).count()
    stats["lignereservation_count"] = database.query(LigneReservation).count()
    stats["total_entities"] = sum(stats.values())
    return stats


############################################
#
#   BESSER Action Language standard lib
#
############################################


async def BAL_size(sequence:list) -> int:
    return len(sequence)

async def BAL_is_empty(sequence:list) -> bool:
    return len(sequence) == 0

async def BAL_add(sequence:list, elem) -> None:
    sequence.append(elem)

async def BAL_remove(sequence:list, elem) -> None:
    sequence.remove(elem)

async def BAL_contains(sequence:list, elem) -> bool:
    return elem in sequence

async def BAL_filter(sequence:list, predicate) -> list:
    return [elem for elem in sequence if predicate(elem)]

async def BAL_forall(sequence:list, predicate) -> bool:
    for elem in sequence:
        if not predicate(elem):
            return False
    return True

async def BAL_exists(sequence:list, predicate) -> bool:
    for elem in sequence:
        if predicate(elem):
            return True
    return False

async def BAL_one(sequence:list, predicate) -> bool:
    found = False
    for elem in sequence:
        if predicate(elem):
            if found:
                return False
            found = True
    return found

async def BAL_is_unique(sequence:list, mapping) -> bool:
    mapped = [mapping(elem) for elem in sequence]
    return len(set(mapped)) == len(mapped)

async def BAL_map(sequence:list, mapping) -> list:
    return [mapping(elem) for elem in sequence]

async def BAL_reduce(sequence:list, reduce_fn, aggregator) -> any:
    for elem in sequence:
        aggregator = reduce_fn(aggregator, elem)
    return aggregator


############################################
#
#   Indisponibilite functions
#
############################################

@app.get("/indisponibilite/", response_model=None, tags=["Indisponibilite"])
def get_all_indisponibilite(detailed: bool = False, database: Session = Depends(get_db)) -> list:
    from sqlalchemy.orm import joinedload

    return database.query(Indisponibilite).all()


@app.get("/indisponibilite/count/", response_model=None, tags=["Indisponibilite"])
def get_count_indisponibilite(database: Session = Depends(get_db)) -> dict:
    """Get the total count of Indisponibilite entities"""
    count = database.query(Indisponibilite).count()
    return {"count": count}


@app.get("/indisponibilite/paginated/", response_model=None, tags=["Indisponibilite"])
def get_paginated_indisponibilite(skip: int = 0, limit: int = 100, detailed: bool = False, database: Session = Depends(get_db)) -> dict:
    """Get paginated list of Indisponibilite entities"""
    total = database.query(Indisponibilite).count()
    indisponibilite_list = database.query(Indisponibilite).offset(skip).limit(limit).all()
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "data": indisponibilite_list
    }


@app.get("/indisponibilite/search/", response_model=None, tags=["Indisponibilite"])
def search_indisponibilite(
    database: Session = Depends(get_db)
) -> list:
    """Search Indisponibilite entities by attributes"""
    query = database.query(Indisponibilite)


    results = query.all()
    return results


@app.get("/indisponibilite/{indisponibilite_id}/", response_model=None, tags=["Indisponibilite"])
async def get_indisponibilite(indisponibilite_id: int, database: Session = Depends(get_db)) -> Indisponibilite:
    db_indisponibilite = database.query(Indisponibilite).filter(Indisponibilite.id == indisponibilite_id).first()
    if db_indisponibilite is None:
        raise HTTPException(status_code=404, detail="Indisponibilite not found")

    response_data = {
        "indisponibilite": db_indisponibilite,
}
    return response_data



@app.post("/indisponibilite/", response_model=None, tags=["Indisponibilite"])
async def create_indisponibilite(indisponibilite_data: IndisponibiliteCreate, database: Session = Depends(get_db)) -> Indisponibilite:


    db_indisponibilite = Indisponibilite(
        type=indisponibilite_data.type,        motif=indisponibilite_data.motif,        dateFin=indisponibilite_data.dateFin,        dateDebut=indisponibilite_data.dateDebut        )

    database.add(db_indisponibilite)
    database.commit()
    database.refresh(db_indisponibilite)




    return db_indisponibilite


@app.post("/indisponibilite/bulk/", response_model=None, tags=["Indisponibilite"])
async def bulk_create_indisponibilite(items: list[IndisponibiliteCreate], database: Session = Depends(get_db)) -> dict:
    """Create multiple Indisponibilite entities at once"""
    created_items = []
    errors = []

    for idx, item_data in enumerate(items):
        try:
            # Basic validation for each item

            db_indisponibilite = Indisponibilite(
                type=item_data.type,                motif=item_data.motif,                dateFin=item_data.dateFin,                dateDebut=item_data.dateDebut            )
            database.add(db_indisponibilite)
            database.flush()  # Get ID without committing
            created_items.append(db_indisponibilite.id)
        except Exception as e:
            errors.append({"index": idx, "error": str(e)})

    if errors:
        database.rollback()
        raise HTTPException(status_code=400, detail={"message": "Bulk creation failed", "errors": errors})

    database.commit()
    return {
        "created_count": len(created_items),
        "created_ids": created_items,
        "message": f"Successfully created {len(created_items)} Indisponibilite entities"
    }


@app.delete("/indisponibilite/bulk/", response_model=None, tags=["Indisponibilite"])
async def bulk_delete_indisponibilite(ids: list[int], database: Session = Depends(get_db)) -> dict:
    """Delete multiple Indisponibilite entities at once"""
    deleted_count = 0
    not_found = []

    for item_id in ids:
        db_indisponibilite = database.query(Indisponibilite).filter(Indisponibilite.id == item_id).first()
        if db_indisponibilite:
            database.delete(db_indisponibilite)
            deleted_count += 1
        else:
            not_found.append(item_id)

    database.commit()

    return {
        "deleted_count": deleted_count,
        "not_found": not_found,
        "message": f"Successfully deleted {deleted_count} Indisponibilite entities"
    }

@app.put("/indisponibilite/{indisponibilite_id}/", response_model=None, tags=["Indisponibilite"])
async def update_indisponibilite(indisponibilite_id: int, indisponibilite_data: IndisponibiliteCreate, database: Session = Depends(get_db)) -> Indisponibilite:
    db_indisponibilite = database.query(Indisponibilite).filter(Indisponibilite.id == indisponibilite_id).first()
    if db_indisponibilite is None:
        raise HTTPException(status_code=404, detail="Indisponibilite not found")

    setattr(db_indisponibilite, 'type', indisponibilite_data.type)
    setattr(db_indisponibilite, 'motif', indisponibilite_data.motif)
    setattr(db_indisponibilite, 'dateFin', indisponibilite_data.dateFin)
    setattr(db_indisponibilite, 'dateDebut', indisponibilite_data.dateDebut)
    database.commit()
    database.refresh(db_indisponibilite)

    return db_indisponibilite


@app.delete("/indisponibilite/{indisponibilite_id}/", response_model=None, tags=["Indisponibilite"])
async def delete_indisponibilite(indisponibilite_id: int, database: Session = Depends(get_db)):
    db_indisponibilite = database.query(Indisponibilite).filter(Indisponibilite.id == indisponibilite_id).first()
    if db_indisponibilite is None:
        raise HTTPException(status_code=404, detail="Indisponibilite not found")
    database.delete(db_indisponibilite)
    database.commit()
    return db_indisponibilite





############################################
#
#   Reservation functions
#
############################################

@app.get("/reservation/", response_model=None, tags=["Reservation"])
def get_all_reservation(detailed: bool = False, database: Session = Depends(get_db)) -> list:
    from sqlalchemy.orm import joinedload

    # Use detailed=true to get entities with eagerly loaded relationships (for tables with lookup columns)
    if detailed:
        # Eagerly load all relationships to avoid N+1 queries
        query = database.query(Reservation)
        query = query.options(joinedload(Reservation.evenement))
        query = query.options(joinedload(Reservation.lignereservation))
        reservation_list = query.all()

        # Serialize with relationships included
        result = []
        for reservation_item in reservation_list:
            item_dict = reservation_item.__dict__.copy()
            item_dict.pop('_sa_instance_state', None)

            # Add many-to-one relationships (foreign keys for lookup columns)
            if reservation_item.evenement:
                related_obj = reservation_item.evenement
                related_dict = related_obj.__dict__.copy()
                related_dict.pop('_sa_instance_state', None)
                item_dict['evenement'] = related_dict
            else:
                item_dict['evenement'] = None
            if reservation_item.lignereservation:
                related_obj = reservation_item.lignereservation
                related_dict = related_obj.__dict__.copy()
                related_dict.pop('_sa_instance_state', None)
                item_dict['lignereservation'] = related_dict
            else:
                item_dict['lignereservation'] = None

            # Add many-to-many and one-to-many relationship objects (full details)
            elementcentre_list = database.query(ElementCentre).join(elementcentre_reservation, ElementCentre.id == elementcentre_reservation.c.elementcentre_3).filter(elementcentre_reservation.c.reservation == reservation_item.id).all()
            item_dict['elementcentre_3'] = []
            for elementcentre_obj in elementcentre_list:
                elementcentre_dict = elementcentre_obj.__dict__.copy()
                elementcentre_dict.pop('_sa_instance_state', None)
                item_dict['elementcentre_3'].append(elementcentre_dict)

            result.append(item_dict)
        return result
    else:
        # Default: return flat entities (faster for charts/widgets without lookup columns)
        return database.query(Reservation).all()


@app.get("/reservation/count/", response_model=None, tags=["Reservation"])
def get_count_reservation(database: Session = Depends(get_db)) -> dict:
    """Get the total count of Reservation entities"""
    count = database.query(Reservation).count()
    return {"count": count}


@app.get("/reservation/paginated/", response_model=None, tags=["Reservation"])
def get_paginated_reservation(skip: int = 0, limit: int = 100, detailed: bool = False, database: Session = Depends(get_db)) -> dict:
    """Get paginated list of Reservation entities"""
    total = database.query(Reservation).count()
    reservation_list = database.query(Reservation).offset(skip).limit(limit).all()
    # By default, return flat entities (for charts/widgets)
    # Use detailed=true to get entities with relationships
    if not detailed:
        return {
            "total": total,
            "skip": skip,
            "limit": limit,
            "data": reservation_list
        }

    result = []
    for reservation_item in reservation_list:
        elementcentre_ids = database.query(elementcentre_reservation.c.elementcentre_3).filter(elementcentre_reservation.c.reservation == reservation_item.id).all()
        item_data = {
            "reservation": reservation_item,
            "elementcentre_ids": [x[0] for x in elementcentre_ids],
        }
        result.append(item_data)
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "data": result
    }


@app.get("/reservation/search/", response_model=None, tags=["Reservation"])
def search_reservation(
    database: Session = Depends(get_db)
) -> list:
    """Search Reservation entities by attributes"""
    query = database.query(Reservation)


    results = query.all()
    return results


@app.get("/reservation/{reservation_id}/", response_model=None, tags=["Reservation"])
async def get_reservation(reservation_id: int, database: Session = Depends(get_db)) -> Reservation:
    db_reservation = database.query(Reservation).filter(Reservation.id == reservation_id).first()
    if db_reservation is None:
        raise HTTPException(status_code=404, detail="Reservation not found")

    elementcentre_ids = database.query(elementcentre_reservation.c.elementcentre_3).filter(elementcentre_reservation.c.reservation == db_reservation.id).all()
    response_data = {
        "reservation": db_reservation,
        "elementcentre_ids": [x[0] for x in elementcentre_ids],
}
    return response_data



@app.post("/reservation/", response_model=None, tags=["Reservation"])
async def create_reservation(reservation_data: ReservationCreate, database: Session = Depends(get_db)) -> Reservation:

    if reservation_data.elementcentre_3:
        for id in reservation_data.elementcentre_3:
            # Entity already validated before creation
            db_elementcentre = database.query(ElementCentre).filter(ElementCentre.id == id).first()
            if not db_elementcentre:
                raise HTTPException(status_code=404, detail=f"ElementCentre with ID {id} not found")

    db_reservation = Reservation(
        statut=reservation_data.statut.value,        notes=reservation_data.notes,        montantTotal=reservation_data.montantTotal,        delaiConfirmation=reservation_data.delaiConfirmation,        id=reservation_data.id,        dateCreation=reservation_data.dateCreation,        dateDebut=reservation_data.dateDebut,        dateFin=reservation_data.dateFin        )

    database.add(db_reservation)
    database.commit()
    database.refresh(db_reservation)


    if reservation_data.elementcentre_3:
        for id in reservation_data.elementcentre_3:
            # Entity already validated before creation
            db_elementcentre = database.query(ElementCentre).filter(ElementCentre.id == id).first()
            # Create the association
            association = elementcentre_reservation.insert().values(reservation=db_reservation.id, elementcentre_3=db_elementcentre.id)
            database.execute(association)
            database.commit()


    elementcentre_ids = database.query(elementcentre_reservation.c.elementcentre_3).filter(elementcentre_reservation.c.reservation == db_reservation.id).all()
    response_data = {
        "reservation": db_reservation,
        "elementcentre_ids": [x[0] for x in elementcentre_ids],
    }
    return response_data


@app.post("/reservation/bulk/", response_model=None, tags=["Reservation"])
async def bulk_create_reservation(items: list[ReservationCreate], database: Session = Depends(get_db)) -> dict:
    """Create multiple Reservation entities at once"""
    created_items = []
    errors = []

    for idx, item_data in enumerate(items):
        try:
            # Basic validation for each item

            db_reservation = Reservation(
                statut=item_data.statut.value,                notes=item_data.notes,                montantTotal=item_data.montantTotal,                delaiConfirmation=item_data.delaiConfirmation,                id=item_data.id,                dateCreation=item_data.dateCreation,                dateDebut=item_data.dateDebut,                dateFin=item_data.dateFin            )
            database.add(db_reservation)
            database.flush()  # Get ID without committing
            created_items.append(db_reservation.id)
        except Exception as e:
            errors.append({"index": idx, "error": str(e)})

    if errors:
        database.rollback()
        raise HTTPException(status_code=400, detail={"message": "Bulk creation failed", "errors": errors})

    database.commit()
    return {
        "created_count": len(created_items),
        "created_ids": created_items,
        "message": f"Successfully created {len(created_items)} Reservation entities"
    }


@app.delete("/reservation/bulk/", response_model=None, tags=["Reservation"])
async def bulk_delete_reservation(ids: list[int], database: Session = Depends(get_db)) -> dict:
    """Delete multiple Reservation entities at once"""
    deleted_count = 0
    not_found = []

    for item_id in ids:
        db_reservation = database.query(Reservation).filter(Reservation.id == item_id).first()
        if db_reservation:
            database.delete(db_reservation)
            deleted_count += 1
        else:
            not_found.append(item_id)

    database.commit()

    return {
        "deleted_count": deleted_count,
        "not_found": not_found,
        "message": f"Successfully deleted {deleted_count} Reservation entities"
    }

@app.put("/reservation/{reservation_id}/", response_model=None, tags=["Reservation"])
async def update_reservation(reservation_id: int, reservation_data: ReservationCreate, database: Session = Depends(get_db)) -> Reservation:
    db_reservation = database.query(Reservation).filter(Reservation.id == reservation_id).first()
    if db_reservation is None:
        raise HTTPException(status_code=404, detail="Reservation not found")

    setattr(db_reservation, 'statut', reservation_data.statut.value)
    setattr(db_reservation, 'notes', reservation_data.notes)
    setattr(db_reservation, 'montantTotal', reservation_data.montantTotal)
    setattr(db_reservation, 'delaiConfirmation', reservation_data.delaiConfirmation)
    setattr(db_reservation, 'id', reservation_data.id)
    setattr(db_reservation, 'dateCreation', reservation_data.dateCreation)
    setattr(db_reservation, 'dateDebut', reservation_data.dateDebut)
    setattr(db_reservation, 'dateFin', reservation_data.dateFin)
    existing_elementcentre_ids = [assoc.elementcentre_3 for assoc in database.execute(
        elementcentre_reservation.select().where(elementcentre_reservation.c.reservation == db_reservation.id))]

    elementcentres_to_remove = set(existing_elementcentre_ids) - set(reservation_data.elementcentre_3)
    for elementcentre_id in elementcentres_to_remove:
        association = elementcentre_reservation.delete().where(
            (elementcentre_reservation.c.reservation == db_reservation.id) & (elementcentre_reservation.c.elementcentre_3 == elementcentre_id))
        database.execute(association)

    new_elementcentre_ids = set(reservation_data.elementcentre_3) - set(existing_elementcentre_ids)
    for elementcentre_id in new_elementcentre_ids:
        db_elementcentre = database.query(ElementCentre).filter(ElementCentre.id == elementcentre_id).first()
        if db_elementcentre is None:
            raise HTTPException(status_code=404, detail=f"ElementCentre with ID {elementcentre_id} not found")
        association = elementcentre_reservation.insert().values(elementcentre_3=db_elementcentre.id, reservation=db_reservation.id)
        database.execute(association)
    database.commit()
    database.refresh(db_reservation)

    elementcentre_ids = database.query(elementcentre_reservation.c.elementcentre_3).filter(elementcentre_reservation.c.reservation == db_reservation.id).all()
    response_data = {
        "reservation": db_reservation,
        "elementcentre_ids": [x[0] for x in elementcentre_ids],
    }
    return response_data


@app.delete("/reservation/{reservation_id}/", response_model=None, tags=["Reservation"])
async def delete_reservation(reservation_id: int, database: Session = Depends(get_db)):
    db_reservation = database.query(Reservation).filter(Reservation.id == reservation_id).first()
    if db_reservation is None:
        raise HTTPException(status_code=404, detail="Reservation not found")
    database.delete(db_reservation)
    database.commit()
    return db_reservation

@app.post("/reservation/{reservation_id}/elementcentre_3/{elementcentre_id}/", response_model=None, tags=["Reservation Relationships"])
async def add_elementcentre_3_to_reservation(reservation_id: int, elementcentre_id: int, database: Session = Depends(get_db)):
    """Add a ElementCentre to this Reservation's elementcentre_3 relationship"""
    db_reservation = database.query(Reservation).filter(Reservation.id == reservation_id).first()
    if db_reservation is None:
        raise HTTPException(status_code=404, detail="Reservation not found")

    db_elementcentre = database.query(ElementCentre).filter(ElementCentre.id == elementcentre_id).first()
    if db_elementcentre is None:
        raise HTTPException(status_code=404, detail="ElementCentre not found")

    # Check if relationship already exists
    existing = database.query(elementcentre_reservation).filter(
        (elementcentre_reservation.c.reservation == reservation_id) &
        (elementcentre_reservation.c.elementcentre_3 == elementcentre_id)
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="Relationship already exists")

    # Create the association
    association = elementcentre_reservation.insert().values(reservation=reservation_id, elementcentre_3=elementcentre_id)
    database.execute(association)
    database.commit()

    return {"message": "ElementCentre added to elementcentre_3 successfully"}


@app.delete("/reservation/{reservation_id}/elementcentre_3/{elementcentre_id}/", response_model=None, tags=["Reservation Relationships"])
async def remove_elementcentre_3_from_reservation(reservation_id: int, elementcentre_id: int, database: Session = Depends(get_db)):
    """Remove a ElementCentre from this Reservation's elementcentre_3 relationship"""
    db_reservation = database.query(Reservation).filter(Reservation.id == reservation_id).first()
    if db_reservation is None:
        raise HTTPException(status_code=404, detail="Reservation not found")

    # Check if relationship exists
    existing = database.query(elementcentre_reservation).filter(
        (elementcentre_reservation.c.reservation == reservation_id) &
        (elementcentre_reservation.c.elementcentre_3 == elementcentre_id)
    ).first()

    if not existing:
        raise HTTPException(status_code=404, detail="Relationship not found")

    # Delete the association
    association = elementcentre_reservation.delete().where(
        (elementcentre_reservation.c.reservation == reservation_id) &
        (elementcentre_reservation.c.elementcentre_3 == elementcentre_id)
    )
    database.execute(association)
    database.commit()

    return {"message": "ElementCentre removed from elementcentre_3 successfully"}


@app.get("/reservation/{reservation_id}/elementcentre_3/", response_model=None, tags=["Reservation Relationships"])
async def get_elementcentre_3_of_reservation(reservation_id: int, database: Session = Depends(get_db)):
    """Get all ElementCentre entities related to this Reservation through elementcentre_3"""
    db_reservation = database.query(Reservation).filter(Reservation.id == reservation_id).first()
    if db_reservation is None:
        raise HTTPException(status_code=404, detail="Reservation not found")

    elementcentre_ids = database.query(elementcentre_reservation.c.elementcentre_3).filter(elementcentre_reservation.c.reservation == reservation_id).all()
    elementcentre_list = database.query(ElementCentre).filter(ElementCentre.id.in_([id[0] for id in elementcentre_ids])).all()

    return {
        "reservation_id": reservation_id,
        "elementcentre_3_count": len(elementcentre_list),
        "elementcentre_3": elementcentre_list
    }



############################################
#   Reservation Method Endpoints
############################################




@app.post("/reservation/methods/calculerMontant/", response_model=None, tags=["Reservation Methods"])
async def reservation_calculerMontant(
    database: Session = Depends(get_db)
):
    """
    Execute the calculerMontant class method on Reservation.
    This method operates on all Reservation entities or performs class-level operations.
    """
    try:
        # Capture stdout to include print outputs in the response
        import io
        import sys
        captured_output = io.StringIO()
        sys.stdout = captured_output


        # Method body not defined
        result = None

        # Restore stdout
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()

        # Handle result serialization
        if hasattr(result, '__iter__') and not isinstance(result, (str, dict)):
            # It's a list of entities
            result_data = []
            for item in result:
                if hasattr(item, '__dict__'):
                    item_dict = {k: v for k, v in item.__dict__.items() if not k.startswith('_')}
                    result_data.append(item_dict)
                else:
                    result_data.append(str(item))
            result = result_data
        elif hasattr(result, '__dict__'):
            result = {k: v for k, v in result.__dict__.items() if not k.startswith('_')}

        return {
            "class": "Reservation",
            "method": "calculerMontant",
            "status": "executed",
            "result": result,
            "output": output if output else None
        }
    except Exception as e:
        sys.stdout = sys.__stdout__
        raise HTTPException(status_code=500, detail=f"Method execution failed: {str(e)}")






@app.post("/reservation/methods/annuler/", response_model=None, tags=["Reservation Methods"])
async def reservation_annuler(
    database: Session = Depends(get_db)
):
    """
    Execute the annuler class method on Reservation.
    This method operates on all Reservation entities or performs class-level operations.
    """
    try:
        # Capture stdout to include print outputs in the response
        import io
        import sys
        captured_output = io.StringIO()
        sys.stdout = captured_output


        # Method body not defined
        result = None

        # Restore stdout
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()

        # Handle result serialization
        if hasattr(result, '__iter__') and not isinstance(result, (str, dict)):
            # It's a list of entities
            result_data = []
            for item in result:
                if hasattr(item, '__dict__'):
                    item_dict = {k: v for k, v in item.__dict__.items() if not k.startswith('_')}
                    result_data.append(item_dict)
                else:
                    result_data.append(str(item))
            result = result_data
        elif hasattr(result, '__dict__'):
            result = {k: v for k, v in result.__dict__.items() if not k.startswith('_')}

        return {
            "class": "Reservation",
            "method": "annuler",
            "status": "executed",
            "result": result,
            "output": output if output else None
        }
    except Exception as e:
        sys.stdout = sys.__stdout__
        raise HTTPException(status_code=500, detail=f"Method execution failed: {str(e)}")






@app.post("/reservation/methods/verifierDelai/", response_model=None, tags=["Reservation Methods"])
async def reservation_verifierDelai(
    database: Session = Depends(get_db)
):
    """
    Execute the verifierDelai class method on Reservation.
    This method operates on all Reservation entities or performs class-level operations.
    """
    try:
        # Capture stdout to include print outputs in the response
        import io
        import sys
        captured_output = io.StringIO()
        sys.stdout = captured_output


        # Method body not defined
        result = None

        # Restore stdout
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()

        # Handle result serialization
        if hasattr(result, '__iter__') and not isinstance(result, (str, dict)):
            # It's a list of entities
            result_data = []
            for item in result:
                if hasattr(item, '__dict__'):
                    item_dict = {k: v for k, v in item.__dict__.items() if not k.startswith('_')}
                    result_data.append(item_dict)
                else:
                    result_data.append(str(item))
            result = result_data
        elif hasattr(result, '__dict__'):
            result = {k: v for k, v in result.__dict__.items() if not k.startswith('_')}

        return {
            "class": "Reservation",
            "method": "verifierDelai",
            "status": "executed",
            "result": result,
            "output": output if output else None
        }
    except Exception as e:
        sys.stdout = sys.__stdout__
        raise HTTPException(status_code=500, detail=f"Method execution failed: {str(e)}")






@app.post("/reservation/methods/confirmer/", response_model=None, tags=["Reservation Methods"])
async def reservation_confirmer(
    database: Session = Depends(get_db)
):
    """
    Execute the confirmer class method on Reservation.
    This method operates on all Reservation entities or performs class-level operations.
    """
    try:
        # Capture stdout to include print outputs in the response
        import io
        import sys
        captured_output = io.StringIO()
        sys.stdout = captured_output


        # Method body not defined
        result = None

        # Restore stdout
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()

        # Handle result serialization
        if hasattr(result, '__iter__') and not isinstance(result, (str, dict)):
            # It's a list of entities
            result_data = []
            for item in result:
                if hasattr(item, '__dict__'):
                    item_dict = {k: v for k, v in item.__dict__.items() if not k.startswith('_')}
                    result_data.append(item_dict)
                else:
                    result_data.append(str(item))
            result = result_data
        elif hasattr(result, '__dict__'):
            result = {k: v for k, v in result.__dict__.items() if not k.startswith('_')}

        return {
            "class": "Reservation",
            "method": "confirmer",
            "status": "executed",
            "result": result,
            "output": output if output else None
        }
    except Exception as e:
        sys.stdout = sys.__stdout__
        raise HTTPException(status_code=500, detail=f"Method execution failed: {str(e)}")






@app.post("/reservation/methods/modifier/", response_model=None, tags=["Reservation Methods"])
async def reservation_modifier(
    params: dict = Body(default=None, embed=True),
    database: Session = Depends(get_db)
):
    """
    Execute the modifier class method on Reservation.
    This method operates on all Reservation entities or performs class-level operations.

    Parameters (pass as JSON body):
    - params: Any    """
    try:
        # Capture stdout to include print outputs in the response
        import io
        import sys
        captured_output = io.StringIO()
        sys.stdout = captured_output

        # Extract parameters from request body
        params = params or {}
        params = params.get('params')

        # Method body not defined
        result = None

        # Restore stdout
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()

        # Handle result serialization
        if hasattr(result, '__iter__') and not isinstance(result, (str, dict)):
            # It's a list of entities
            result_data = []
            for item in result:
                if hasattr(item, '__dict__'):
                    item_dict = {k: v for k, v in item.__dict__.items() if not k.startswith('_')}
                    result_data.append(item_dict)
                else:
                    result_data.append(str(item))
            result = result_data
        elif hasattr(result, '__dict__'):
            result = {k: v for k, v in result.__dict__.items() if not k.startswith('_')}

        return {
            "class": "Reservation",
            "method": "modifier",
            "status": "executed",
            "result": result,
            "output": output if output else None
        }
    except Exception as e:
        sys.stdout = sys.__stdout__
        raise HTTPException(status_code=500, detail=f"Method execution failed: {str(e)}")






@app.post("/reservation/methods/estModifiable/", response_model=None, tags=["Reservation Methods"])
async def reservation_estModifiable(
    database: Session = Depends(get_db)
):
    """
    Execute the estModifiable class method on Reservation.
    This method operates on all Reservation entities or performs class-level operations.
    """
    try:
        # Capture stdout to include print outputs in the response
        import io
        import sys
        captured_output = io.StringIO()
        sys.stdout = captured_output


        # Method body not defined
        result = None

        # Restore stdout
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()

        # Handle result serialization
        if hasattr(result, '__iter__') and not isinstance(result, (str, dict)):
            # It's a list of entities
            result_data = []
            for item in result:
                if hasattr(item, '__dict__'):
                    item_dict = {k: v for k, v in item.__dict__.items() if not k.startswith('_')}
                    result_data.append(item_dict)
                else:
                    result_data.append(str(item))
            result = result_data
        elif hasattr(result, '__dict__'):
            result = {k: v for k, v in result.__dict__.items() if not k.startswith('_')}

        return {
            "class": "Reservation",
            "method": "estModifiable",
            "status": "executed",
            "result": result,
            "output": output if output else None
        }
    except Exception as e:
        sys.stdout = sys.__stdout__
        raise HTTPException(status_code=500, detail=f"Method execution failed: {str(e)}")




############################################
#
#   Tarif functions
#
############################################

@app.get("/tarif/", response_model=None, tags=["Tarif"])
def get_all_tarif(detailed: bool = False, database: Session = Depends(get_db)) -> list:
    from sqlalchemy.orm import joinedload

    # Use detailed=true to get entities with eagerly loaded relationships (for tables with lookup columns)
    if detailed:
        # Eagerly load all relationships to avoid N+1 queries
        query = database.query(Tarif)
        query = query.options(joinedload(Tarif.elementcentre_1))
        tarif_list = query.all()

        # Serialize with relationships included
        result = []
        for tarif_item in tarif_list:
            item_dict = tarif_item.__dict__.copy()
            item_dict.pop('_sa_instance_state', None)

            # Add many-to-one relationships (foreign keys for lookup columns)
            if tarif_item.elementcentre_1:
                related_obj = tarif_item.elementcentre_1
                related_dict = related_obj.__dict__.copy()
                related_dict.pop('_sa_instance_state', None)
                item_dict['elementcentre_1'] = related_dict
            else:
                item_dict['elementcentre_1'] = None


            result.append(item_dict)
        return result
    else:
        # Default: return flat entities (faster for charts/widgets without lookup columns)
        return database.query(Tarif).all()


@app.get("/tarif/count/", response_model=None, tags=["Tarif"])
def get_count_tarif(database: Session = Depends(get_db)) -> dict:
    """Get the total count of Tarif entities"""
    count = database.query(Tarif).count()
    return {"count": count}


@app.get("/tarif/paginated/", response_model=None, tags=["Tarif"])
def get_paginated_tarif(skip: int = 0, limit: int = 100, detailed: bool = False, database: Session = Depends(get_db)) -> dict:
    """Get paginated list of Tarif entities"""
    total = database.query(Tarif).count()
    tarif_list = database.query(Tarif).offset(skip).limit(limit).all()
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "data": tarif_list
    }


@app.get("/tarif/search/", response_model=None, tags=["Tarif"])
def search_tarif(
    database: Session = Depends(get_db)
) -> list:
    """Search Tarif entities by attributes"""
    query = database.query(Tarif)


    results = query.all()
    return results


@app.get("/tarif/{tarif_id}/", response_model=None, tags=["Tarif"])
async def get_tarif(tarif_id: int, database: Session = Depends(get_db)) -> Tarif:
    db_tarif = database.query(Tarif).filter(Tarif.id == tarif_id).first()
    if db_tarif is None:
        raise HTTPException(status_code=404, detail="Tarif not found")

    response_data = {
        "tarif": db_tarif,
}
    return response_data



@app.post("/tarif/", response_model=None, tags=["Tarif"])
async def create_tarif(tarif_data: TarifCreate, database: Session = Depends(get_db)) -> Tarif:

    if tarif_data.elementcentre_1 is not None:
        db_elementcentre_1 = database.query(ElementCentre).filter(ElementCentre.id == tarif_data.elementcentre_1).first()
        if not db_elementcentre_1:
            raise HTTPException(status_code=400, detail="ElementCentre not found")
    else:
        raise HTTPException(status_code=400, detail="ElementCentre ID is required")

    db_tarif = Tarif(
        dateFin=tarif_data.dateFin,        dateDebut=tarif_data.dateDebut,        prixDemiJournee=tarif_data.prixDemiJournee,        prixJournalier=tarif_data.prixJournalier,        elementcentre_1_id=tarif_data.elementcentre_1        )

    database.add(db_tarif)
    database.commit()
    database.refresh(db_tarif)




    return db_tarif


@app.post("/tarif/bulk/", response_model=None, tags=["Tarif"])
async def bulk_create_tarif(items: list[TarifCreate], database: Session = Depends(get_db)) -> dict:
    """Create multiple Tarif entities at once"""
    created_items = []
    errors = []

    for idx, item_data in enumerate(items):
        try:
            # Basic validation for each item
            if not item_data.elementcentre_1:
                raise ValueError("ElementCentre ID is required")

            db_tarif = Tarif(
                dateFin=item_data.dateFin,                dateDebut=item_data.dateDebut,                prixDemiJournee=item_data.prixDemiJournee,                prixJournalier=item_data.prixJournalier,                elementcentre_1_id=item_data.elementcentre_1            )
            database.add(db_tarif)
            database.flush()  # Get ID without committing
            created_items.append(db_tarif.id)
        except Exception as e:
            errors.append({"index": idx, "error": str(e)})

    if errors:
        database.rollback()
        raise HTTPException(status_code=400, detail={"message": "Bulk creation failed", "errors": errors})

    database.commit()
    return {
        "created_count": len(created_items),
        "created_ids": created_items,
        "message": f"Successfully created {len(created_items)} Tarif entities"
    }


@app.delete("/tarif/bulk/", response_model=None, tags=["Tarif"])
async def bulk_delete_tarif(ids: list[int], database: Session = Depends(get_db)) -> dict:
    """Delete multiple Tarif entities at once"""
    deleted_count = 0
    not_found = []

    for item_id in ids:
        db_tarif = database.query(Tarif).filter(Tarif.id == item_id).first()
        if db_tarif:
            database.delete(db_tarif)
            deleted_count += 1
        else:
            not_found.append(item_id)

    database.commit()

    return {
        "deleted_count": deleted_count,
        "not_found": not_found,
        "message": f"Successfully deleted {deleted_count} Tarif entities"
    }

@app.put("/tarif/{tarif_id}/", response_model=None, tags=["Tarif"])
async def update_tarif(tarif_id: int, tarif_data: TarifCreate, database: Session = Depends(get_db)) -> Tarif:
    db_tarif = database.query(Tarif).filter(Tarif.id == tarif_id).first()
    if db_tarif is None:
        raise HTTPException(status_code=404, detail="Tarif not found")

    setattr(db_tarif, 'dateFin', tarif_data.dateFin)
    setattr(db_tarif, 'dateDebut', tarif_data.dateDebut)
    setattr(db_tarif, 'prixDemiJournee', tarif_data.prixDemiJournee)
    setattr(db_tarif, 'prixJournalier', tarif_data.prixJournalier)
    if tarif_data.elementcentre_1 is not None:
        db_elementcentre_1 = database.query(ElementCentre).filter(ElementCentre.id == tarif_data.elementcentre_1).first()
        if not db_elementcentre_1:
            raise HTTPException(status_code=400, detail="ElementCentre not found")
        setattr(db_tarif, 'elementcentre_1_id', tarif_data.elementcentre_1)
    database.commit()
    database.refresh(db_tarif)

    return db_tarif


@app.delete("/tarif/{tarif_id}/", response_model=None, tags=["Tarif"])
async def delete_tarif(tarif_id: int, database: Session = Depends(get_db)):
    db_tarif = database.query(Tarif).filter(Tarif.id == tarif_id).first()
    if db_tarif is None:
        raise HTTPException(status_code=404, detail="Tarif not found")
    database.delete(db_tarif)
    database.commit()
    return db_tarif



############################################
#   Tarif Method Endpoints
############################################




@app.post("/tarif/methods/calculerMontant/", response_model=None, tags=["Tarif Methods"])
async def tarif_calculerMontant(
    params: dict = Body(default=None, embed=True),
    database: Session = Depends(get_db)
):
    """
    Execute the calculerMontant class method on Tarif.
    This method operates on all Tarif entities or performs class-level operations.

    Parameters (pass as JSON body):
    - debut: Any    - fin: Any    """
    try:
        # Capture stdout to include print outputs in the response
        import io
        import sys
        captured_output = io.StringIO()
        sys.stdout = captured_output

        # Extract parameters from request body
        params = params or {}
        debut = params.get('debut')
        fin = params.get('fin')

        # Method body not defined
        result = None

        # Restore stdout
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()

        # Handle result serialization
        if hasattr(result, '__iter__') and not isinstance(result, (str, dict)):
            # It's a list of entities
            result_data = []
            for item in result:
                if hasattr(item, '__dict__'):
                    item_dict = {k: v for k, v in item.__dict__.items() if not k.startswith('_')}
                    result_data.append(item_dict)
                else:
                    result_data.append(str(item))
            result = result_data
        elif hasattr(result, '__dict__'):
            result = {k: v for k, v in result.__dict__.items() if not k.startswith('_')}

        return {
            "class": "Tarif",
            "method": "calculerMontant",
            "status": "executed",
            "result": result,
            "output": output if output else None
        }
    except Exception as e:
        sys.stdout = sys.__stdout__
        raise HTTPException(status_code=500, detail=f"Method execution failed: {str(e)}")




############################################
#
#   ElementCentre functions
#
############################################

@app.get("/elementcentre/", response_model=None, tags=["ElementCentre"])
def get_all_elementcentre(detailed: bool = False, database: Session = Depends(get_db)) -> list:
    from sqlalchemy.orm import joinedload

    # Use detailed=true to get entities with eagerly loaded relationships (for tables with lookup columns)
    if detailed:
        # Eagerly load all relationships to avoid N+1 queries
        query = database.query(ElementCentre)
        query = query.options(joinedload(ElementCentre.centredecongres_1))
        elementcentre_list = query.all()

        # Serialize with relationships included
        result = []
        for elementcentre_item in elementcentre_list:
            item_dict = elementcentre_item.__dict__.copy()
            item_dict.pop('_sa_instance_state', None)

            # Add many-to-one relationships (foreign keys for lookup columns)
            if elementcentre_item.centredecongres_1:
                related_obj = elementcentre_item.centredecongres_1
                related_dict = related_obj.__dict__.copy()
                related_dict.pop('_sa_instance_state', None)
                item_dict['centredecongres_1'] = related_dict
            else:
                item_dict['centredecongres_1'] = None

            # Add many-to-many and one-to-many relationship objects (full details)
            reservation_list = database.query(Reservation).join(elementcentre_reservation, Reservation.id == elementcentre_reservation.c.reservation).filter(elementcentre_reservation.c.elementcentre_3 == elementcentre_item.id).all()
            item_dict['reservation'] = []
            for reservation_obj in reservation_list:
                reservation_dict = reservation_obj.__dict__.copy()
                reservation_dict.pop('_sa_instance_state', None)
                item_dict['reservation'].append(reservation_dict)
            indisponibilite_list = database.query(Indisponibilite).filter(Indisponibilite.elementcentre_2_id == elementcentre_item.id).all()
            item_dict['indisponibilite'] = []
            for indisponibilite_obj in indisponibilite_list:
                indisponibilite_dict = indisponibilite_obj.__dict__.copy()
                indisponibilite_dict.pop('_sa_instance_state', None)
                item_dict['indisponibilite'].append(indisponibilite_dict)
            tarif_list = database.query(Tarif).filter(Tarif.elementcentre_1_id == elementcentre_item.id).all()
            item_dict['tarif'] = []
            for tarif_obj in tarif_list:
                tarif_dict = tarif_obj.__dict__.copy()
                tarif_dict.pop('_sa_instance_state', None)
                item_dict['tarif'].append(tarif_dict)

            result.append(item_dict)
        return result
    else:
        # Default: return flat entities (faster for charts/widgets without lookup columns)
        return database.query(ElementCentre).all()


@app.get("/elementcentre/count/", response_model=None, tags=["ElementCentre"])
def get_count_elementcentre(database: Session = Depends(get_db)) -> dict:
    """Get the total count of ElementCentre entities"""
    count = database.query(ElementCentre).count()
    return {"count": count}


@app.get("/elementcentre/paginated/", response_model=None, tags=["ElementCentre"])
def get_paginated_elementcentre(skip: int = 0, limit: int = 100, detailed: bool = False, database: Session = Depends(get_db)) -> dict:
    """Get paginated list of ElementCentre entities"""
    total = database.query(ElementCentre).count()
    elementcentre_list = database.query(ElementCentre).offset(skip).limit(limit).all()
    # By default, return flat entities (for charts/widgets)
    # Use detailed=true to get entities with relationships
    if not detailed:
        return {
            "total": total,
            "skip": skip,
            "limit": limit,
            "data": elementcentre_list
        }

    result = []
    for elementcentre_item in elementcentre_list:
        reservation_ids = database.query(elementcentre_reservation.c.reservation).filter(elementcentre_reservation.c.elementcentre_3 == elementcentre_item.id).all()
        indisponibilite_ids = database.query(Indisponibilite.id).filter(Indisponibilite.elementcentre_2_id == elementcentre_item.id).all()
        tarif_ids = database.query(Tarif.id).filter(Tarif.elementcentre_1_id == elementcentre_item.id).all()
        item_data = {
            "elementcentre": elementcentre_item,
            "reservation_ids": [x[0] for x in reservation_ids],
            "indisponibilite_ids": [x[0] for x in indisponibilite_ids],            "tarif_ids": [x[0] for x in tarif_ids]        }
        result.append(item_data)
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "data": result
    }


@app.get("/elementcentre/search/", response_model=None, tags=["ElementCentre"])
def search_elementcentre(
    database: Session = Depends(get_db)
) -> list:
    """Search ElementCentre entities by attributes"""
    query = database.query(ElementCentre)


    results = query.all()
    return results


@app.get("/elementcentre/{elementcentre_id}/", response_model=None, tags=["ElementCentre"])
async def get_elementcentre(elementcentre_id: int, database: Session = Depends(get_db)) -> ElementCentre:
    db_elementcentre = database.query(ElementCentre).filter(ElementCentre.id == elementcentre_id).first()
    if db_elementcentre is None:
        raise HTTPException(status_code=404, detail="ElementCentre not found")

    reservation_ids = database.query(elementcentre_reservation.c.reservation).filter(elementcentre_reservation.c.elementcentre_3 == db_elementcentre.id).all()
    indisponibilite_ids = database.query(Indisponibilite.id).filter(Indisponibilite.elementcentre_2_id == db_elementcentre.id).all()
    tarif_ids = database.query(Tarif.id).filter(Tarif.elementcentre_1_id == db_elementcentre.id).all()
    response_data = {
        "elementcentre": db_elementcentre,
        "reservation_ids": [x[0] for x in reservation_ids],
        "indisponibilite_ids": [x[0] for x in indisponibilite_ids],        "tarif_ids": [x[0] for x in tarif_ids]}
    return response_data



@app.post("/elementcentre/", response_model=None, tags=["ElementCentre"])
async def create_elementcentre(elementcentre_data: ElementCentreCreate, database: Session = Depends(get_db)) -> ElementCentre:

    if elementcentre_data.centredecongres_1 is not None:
        db_centredecongres_1 = database.query(CentreDeCongres).filter(CentreDeCongres.id == elementcentre_data.centredecongres_1).first()
        if not db_centredecongres_1:
            raise HTTPException(status_code=400, detail="CentreDeCongres not found")
    else:
        raise HTTPException(status_code=400, detail="CentreDeCongres ID is required")
    if elementcentre_data.reservation:
        for id in elementcentre_data.reservation:
            # Entity already validated before creation
            db_reservation = database.query(Reservation).filter(Reservation.id == id).first()
            if not db_reservation:
                raise HTTPException(status_code=404, detail=f"Reservation with ID {id} not found")

    db_elementcentre = ElementCentre(
        capaciteMax=elementcentre_data.capaciteMax,        id=elementcentre_data.id,        nom=elementcentre_data.nom,        dureeMiniLocation=elementcentre_data.dureeMiniLocation,        description=elementcentre_data.description,        actif=elementcentre_data.actif,        centredecongres_1_id=elementcentre_data.centredecongres_1        )

    database.add(db_elementcentre)
    database.commit()
    database.refresh(db_elementcentre)

    if elementcentre_data.indisponibilite:
        # Validate that all Indisponibilite IDs exist
        for indisponibilite_id in elementcentre_data.indisponibilite:
            db_indisponibilite = database.query(Indisponibilite).filter(Indisponibilite.id == indisponibilite_id).first()
            if not db_indisponibilite:
                raise HTTPException(status_code=400, detail=f"Indisponibilite with id {indisponibilite_id} not found")

        # Update the related entities with the new foreign key
        database.query(Indisponibilite).filter(Indisponibilite.id.in_(elementcentre_data.indisponibilite)).update(
            {Indisponibilite.elementcentre_2_id: db_elementcentre.id}, synchronize_session=False
        )
        database.commit()
    if elementcentre_data.tarif:
        # Validate that all Tarif IDs exist
        for tarif_id in elementcentre_data.tarif:
            db_tarif = database.query(Tarif).filter(Tarif.id == tarif_id).first()
            if not db_tarif:
                raise HTTPException(status_code=400, detail=f"Tarif with id {tarif_id} not found")

        # Update the related entities with the new foreign key
        database.query(Tarif).filter(Tarif.id.in_(elementcentre_data.tarif)).update(
            {Tarif.elementcentre_1_id: db_elementcentre.id}, synchronize_session=False
        )
        database.commit()

    if elementcentre_data.reservation:
        for id in elementcentre_data.reservation:
            # Entity already validated before creation
            db_reservation = database.query(Reservation).filter(Reservation.id == id).first()
            # Create the association
            association = elementcentre_reservation.insert().values(elementcentre_3=db_elementcentre.id, reservation=db_reservation.id)
            database.execute(association)
            database.commit()


    reservation_ids = database.query(elementcentre_reservation.c.reservation).filter(elementcentre_reservation.c.elementcentre_3 == db_elementcentre.id).all()
    indisponibilite_ids = database.query(Indisponibilite.id).filter(Indisponibilite.elementcentre_2_id == db_elementcentre.id).all()
    tarif_ids = database.query(Tarif.id).filter(Tarif.elementcentre_1_id == db_elementcentre.id).all()
    response_data = {
        "elementcentre": db_elementcentre,
        "reservation_ids": [x[0] for x in reservation_ids],
        "indisponibilite_ids": [x[0] for x in indisponibilite_ids],        "tarif_ids": [x[0] for x in tarif_ids]    }
    return response_data


@app.post("/elementcentre/bulk/", response_model=None, tags=["ElementCentre"])
async def bulk_create_elementcentre(items: list[ElementCentreCreate], database: Session = Depends(get_db)) -> dict:
    """Create multiple ElementCentre entities at once"""
    created_items = []
    errors = []

    for idx, item_data in enumerate(items):
        try:
            # Basic validation for each item
            if not item_data.centredecongres_1:
                raise ValueError("CentreDeCongres ID is required")

            db_elementcentre = ElementCentre(
                capaciteMax=item_data.capaciteMax,                id=item_data.id,                nom=item_data.nom,                dureeMiniLocation=item_data.dureeMiniLocation,                description=item_data.description,                actif=item_data.actif,                centredecongres_1_id=item_data.centredecongres_1            )
            database.add(db_elementcentre)
            database.flush()  # Get ID without committing
            created_items.append(db_elementcentre.id)
        except Exception as e:
            errors.append({"index": idx, "error": str(e)})

    if errors:
        database.rollback()
        raise HTTPException(status_code=400, detail={"message": "Bulk creation failed", "errors": errors})

    database.commit()
    return {
        "created_count": len(created_items),
        "created_ids": created_items,
        "message": f"Successfully created {len(created_items)} ElementCentre entities"
    }


@app.delete("/elementcentre/bulk/", response_model=None, tags=["ElementCentre"])
async def bulk_delete_elementcentre(ids: list[int], database: Session = Depends(get_db)) -> dict:
    """Delete multiple ElementCentre entities at once"""
    deleted_count = 0
    not_found = []

    for item_id in ids:
        db_elementcentre = database.query(ElementCentre).filter(ElementCentre.id == item_id).first()
        if db_elementcentre:
            database.delete(db_elementcentre)
            deleted_count += 1
        else:
            not_found.append(item_id)

    database.commit()

    return {
        "deleted_count": deleted_count,
        "not_found": not_found,
        "message": f"Successfully deleted {deleted_count} ElementCentre entities"
    }

@app.put("/elementcentre/{elementcentre_id}/", response_model=None, tags=["ElementCentre"])
async def update_elementcentre(elementcentre_id: int, elementcentre_data: ElementCentreCreate, database: Session = Depends(get_db)) -> ElementCentre:
    db_elementcentre = database.query(ElementCentre).filter(ElementCentre.id == elementcentre_id).first()
    if db_elementcentre is None:
        raise HTTPException(status_code=404, detail="ElementCentre not found")

    setattr(db_elementcentre, 'capaciteMax', elementcentre_data.capaciteMax)
    setattr(db_elementcentre, 'id', elementcentre_data.id)
    setattr(db_elementcentre, 'nom', elementcentre_data.nom)
    setattr(db_elementcentre, 'dureeMiniLocation', elementcentre_data.dureeMiniLocation)
    setattr(db_elementcentre, 'description', elementcentre_data.description)
    setattr(db_elementcentre, 'actif', elementcentre_data.actif)
    if elementcentre_data.centredecongres_1 is not None:
        db_centredecongres_1 = database.query(CentreDeCongres).filter(CentreDeCongres.id == elementcentre_data.centredecongres_1).first()
        if not db_centredecongres_1:
            raise HTTPException(status_code=400, detail="CentreDeCongres not found")
        setattr(db_elementcentre, 'centredecongres_1_id', elementcentre_data.centredecongres_1)
    if elementcentre_data.indisponibilite is not None:
        # Clear all existing relationships (set foreign key to NULL)
        database.query(Indisponibilite).filter(Indisponibilite.elementcentre_2_id == db_elementcentre.id).update(
            {Indisponibilite.elementcentre_2_id: None}, synchronize_session=False
        )

        # Set new relationships if list is not empty
        if elementcentre_data.indisponibilite:
            # Validate that all IDs exist
            for indisponibilite_id in elementcentre_data.indisponibilite:
                db_indisponibilite = database.query(Indisponibilite).filter(Indisponibilite.id == indisponibilite_id).first()
                if not db_indisponibilite:
                    raise HTTPException(status_code=400, detail=f"Indisponibilite with id {indisponibilite_id} not found")

            # Update the related entities with the new foreign key
            database.query(Indisponibilite).filter(Indisponibilite.id.in_(elementcentre_data.indisponibilite)).update(
                {Indisponibilite.elementcentre_2_id: db_elementcentre.id}, synchronize_session=False
            )
    if elementcentre_data.tarif is not None:
        # Clear all existing relationships (set foreign key to NULL)
        database.query(Tarif).filter(Tarif.elementcentre_1_id == db_elementcentre.id).update(
            {Tarif.elementcentre_1_id: None}, synchronize_session=False
        )

        # Set new relationships if list is not empty
        if elementcentre_data.tarif:
            # Validate that all IDs exist
            for tarif_id in elementcentre_data.tarif:
                db_tarif = database.query(Tarif).filter(Tarif.id == tarif_id).first()
                if not db_tarif:
                    raise HTTPException(status_code=400, detail=f"Tarif with id {tarif_id} not found")

            # Update the related entities with the new foreign key
            database.query(Tarif).filter(Tarif.id.in_(elementcentre_data.tarif)).update(
                {Tarif.elementcentre_1_id: db_elementcentre.id}, synchronize_session=False
            )
    existing_reservation_ids = [assoc.reservation for assoc in database.execute(
        elementcentre_reservation.select().where(elementcentre_reservation.c.elementcentre_3 == db_elementcentre.id))]

    reservations_to_remove = set(existing_reservation_ids) - set(elementcentre_data.reservation)
    for reservation_id in reservations_to_remove:
        association = elementcentre_reservation.delete().where(
            (elementcentre_reservation.c.elementcentre_3 == db_elementcentre.id) & (elementcentre_reservation.c.reservation == reservation_id))
        database.execute(association)

    new_reservation_ids = set(elementcentre_data.reservation) - set(existing_reservation_ids)
    for reservation_id in new_reservation_ids:
        db_reservation = database.query(Reservation).filter(Reservation.id == reservation_id).first()
        if db_reservation is None:
            raise HTTPException(status_code=404, detail=f"Reservation with ID {reservation_id} not found")
        association = elementcentre_reservation.insert().values(reservation=db_reservation.id, elementcentre_3=db_elementcentre.id)
        database.execute(association)
    database.commit()
    database.refresh(db_elementcentre)

    reservation_ids = database.query(elementcentre_reservation.c.reservation).filter(elementcentre_reservation.c.elementcentre_3 == db_elementcentre.id).all()
    indisponibilite_ids = database.query(Indisponibilite.id).filter(Indisponibilite.elementcentre_2_id == db_elementcentre.id).all()
    tarif_ids = database.query(Tarif.id).filter(Tarif.elementcentre_1_id == db_elementcentre.id).all()
    response_data = {
        "elementcentre": db_elementcentre,
        "reservation_ids": [x[0] for x in reservation_ids],
        "indisponibilite_ids": [x[0] for x in indisponibilite_ids],        "tarif_ids": [x[0] for x in tarif_ids]    }
    return response_data


@app.delete("/elementcentre/{elementcentre_id}/", response_model=None, tags=["ElementCentre"])
async def delete_elementcentre(elementcentre_id: int, database: Session = Depends(get_db)):
    db_elementcentre = database.query(ElementCentre).filter(ElementCentre.id == elementcentre_id).first()
    if db_elementcentre is None:
        raise HTTPException(status_code=404, detail="ElementCentre not found")
    database.delete(db_elementcentre)
    database.commit()
    return db_elementcentre

@app.post("/elementcentre/{elementcentre_id}/reservation/{reservation_id}/", response_model=None, tags=["ElementCentre Relationships"])
async def add_reservation_to_elementcentre(elementcentre_id: int, reservation_id: int, database: Session = Depends(get_db)):
    """Add a Reservation to this ElementCentre's reservation relationship"""
    db_elementcentre = database.query(ElementCentre).filter(ElementCentre.id == elementcentre_id).first()
    if db_elementcentre is None:
        raise HTTPException(status_code=404, detail="ElementCentre not found")

    db_reservation = database.query(Reservation).filter(Reservation.id == reservation_id).first()
    if db_reservation is None:
        raise HTTPException(status_code=404, detail="Reservation not found")

    # Check if relationship already exists
    existing = database.query(elementcentre_reservation).filter(
        (elementcentre_reservation.c.elementcentre_3 == elementcentre_id) &
        (elementcentre_reservation.c.reservation == reservation_id)
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="Relationship already exists")

    # Create the association
    association = elementcentre_reservation.insert().values(elementcentre_3=elementcentre_id, reservation=reservation_id)
    database.execute(association)
    database.commit()

    return {"message": "Reservation added to reservation successfully"}


@app.delete("/elementcentre/{elementcentre_id}/reservation/{reservation_id}/", response_model=None, tags=["ElementCentre Relationships"])
async def remove_reservation_from_elementcentre(elementcentre_id: int, reservation_id: int, database: Session = Depends(get_db)):
    """Remove a Reservation from this ElementCentre's reservation relationship"""
    db_elementcentre = database.query(ElementCentre).filter(ElementCentre.id == elementcentre_id).first()
    if db_elementcentre is None:
        raise HTTPException(status_code=404, detail="ElementCentre not found")

    # Check if relationship exists
    existing = database.query(elementcentre_reservation).filter(
        (elementcentre_reservation.c.elementcentre_3 == elementcentre_id) &
        (elementcentre_reservation.c.reservation == reservation_id)
    ).first()

    if not existing:
        raise HTTPException(status_code=404, detail="Relationship not found")

    # Delete the association
    association = elementcentre_reservation.delete().where(
        (elementcentre_reservation.c.elementcentre_3 == elementcentre_id) &
        (elementcentre_reservation.c.reservation == reservation_id)
    )
    database.execute(association)
    database.commit()

    return {"message": "Reservation removed from reservation successfully"}


@app.get("/elementcentre/{elementcentre_id}/reservation/", response_model=None, tags=["ElementCentre Relationships"])
async def get_reservation_of_elementcentre(elementcentre_id: int, database: Session = Depends(get_db)):
    """Get all Reservation entities related to this ElementCentre through reservation"""
    db_elementcentre = database.query(ElementCentre).filter(ElementCentre.id == elementcentre_id).first()
    if db_elementcentre is None:
        raise HTTPException(status_code=404, detail="ElementCentre not found")

    reservation_ids = database.query(elementcentre_reservation.c.reservation).filter(elementcentre_reservation.c.elementcentre_3 == elementcentre_id).all()
    reservation_list = database.query(Reservation).filter(Reservation.id.in_([id[0] for id in reservation_ids])).all()

    return {
        "elementcentre_id": elementcentre_id,
        "reservation_count": len(reservation_list),
        "reservation": reservation_list
    }



############################################
#   ElementCentre Method Endpoints
############################################




@app.post("/elementcentre/methods/estDisponible/", response_model=None, tags=["ElementCentre Methods"])
async def elementcentre_estDisponible(
    params: dict = Body(default=None, embed=True),
    database: Session = Depends(get_db)
):
    """
    Execute the estDisponible class method on ElementCentre.
    This method operates on all ElementCentre entities or performs class-level operations.

    Parameters (pass as JSON body):
    - debut: Any    - fin: Any    """
    try:
        # Capture stdout to include print outputs in the response
        import io
        import sys
        captured_output = io.StringIO()
        sys.stdout = captured_output

        # Extract parameters from request body
        params = params or {}
        debut = params.get('debut')
        fin = params.get('fin')

        # Method body not defined
        result = None

        # Restore stdout
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()

        # Handle result serialization
        if hasattr(result, '__iter__') and not isinstance(result, (str, dict)):
            # It's a list of entities
            result_data = []
            for item in result:
                if hasattr(item, '__dict__'):
                    item_dict = {k: v for k, v in item.__dict__.items() if not k.startswith('_')}
                    result_data.append(item_dict)
                else:
                    result_data.append(str(item))
            result = result_data
        elif hasattr(result, '__dict__'):
            result = {k: v for k, v in result.__dict__.items() if not k.startswith('_')}

        return {
            "class": "ElementCentre",
            "method": "estDisponible",
            "status": "executed",
            "result": result,
            "output": output if output else None
        }
    except Exception as e:
        sys.stdout = sys.__stdout__
        raise HTTPException(status_code=500, detail=f"Method execution failed: {str(e)}")






@app.post("/elementcentre/methods/getTarifPour/", response_model=None, tags=["ElementCentre Methods"])
async def elementcentre_getTarifPour(
    params: dict = Body(default=None, embed=True),
    database: Session = Depends(get_db)
):
    """
    Execute the getTarifPour class method on ElementCentre.
    This method operates on all ElementCentre entities or performs class-level operations.

    Parameters (pass as JSON body):
    - date: Any    """
    try:
        # Capture stdout to include print outputs in the response
        import io
        import sys
        captured_output = io.StringIO()
        sys.stdout = captured_output

        # Extract parameters from request body
        params = params or {}
        date = params.get('date')

        # Method body not defined
        result = None

        # Restore stdout
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()

        # Handle result serialization
        if hasattr(result, '__iter__') and not isinstance(result, (str, dict)):
            # It's a list of entities
            result_data = []
            for item in result:
                if hasattr(item, '__dict__'):
                    item_dict = {k: v for k, v in item.__dict__.items() if not k.startswith('_')}
                    result_data.append(item_dict)
                else:
                    result_data.append(str(item))
            result = result_data
        elif hasattr(result, '__dict__'):
            result = {k: v for k, v in result.__dict__.items() if not k.startswith('_')}

        return {
            "class": "ElementCentre",
            "method": "getTarifPour",
            "status": "executed",
            "result": result,
            "output": output if output else None
        }
    except Exception as e:
        sys.stdout = sys.__stdout__
        raise HTTPException(status_code=500, detail=f"Method execution failed: {str(e)}")




############################################
#
#   Gestionnaire functions
#
############################################

@app.get("/gestionnaire/", response_model=None, tags=["Gestionnaire"])
def get_all_gestionnaire(detailed: bool = False, database: Session = Depends(get_db)) -> list:
    from sqlalchemy.orm import joinedload

    return database.query(Gestionnaire).all()


@app.get("/gestionnaire/count/", response_model=None, tags=["Gestionnaire"])
def get_count_gestionnaire(database: Session = Depends(get_db)) -> dict:
    """Get the total count of Gestionnaire entities"""
    count = database.query(Gestionnaire).count()
    return {"count": count}


@app.get("/gestionnaire/paginated/", response_model=None, tags=["Gestionnaire"])
def get_paginated_gestionnaire(skip: int = 0, limit: int = 100, detailed: bool = False, database: Session = Depends(get_db)) -> dict:
    """Get paginated list of Gestionnaire entities"""
    total = database.query(Gestionnaire).count()
    gestionnaire_list = database.query(Gestionnaire).offset(skip).limit(limit).all()
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "data": gestionnaire_list
    }


@app.get("/gestionnaire/search/", response_model=None, tags=["Gestionnaire"])
def search_gestionnaire(
    database: Session = Depends(get_db)
) -> list:
    """Search Gestionnaire entities by attributes"""
    query = database.query(Gestionnaire)


    results = query.all()
    return results


@app.get("/gestionnaire/{gestionnaire_id}/", response_model=None, tags=["Gestionnaire"])
async def get_gestionnaire(gestionnaire_id: int, database: Session = Depends(get_db)) -> Gestionnaire:
    db_gestionnaire = database.query(Gestionnaire).filter(Gestionnaire.id == gestionnaire_id).first()
    if db_gestionnaire is None:
        raise HTTPException(status_code=404, detail="Gestionnaire not found")

    response_data = {
        "gestionnaire": db_gestionnaire,
}
    return response_data



@app.post("/gestionnaire/", response_model=None, tags=["Gestionnaire"])
async def create_gestionnaire(gestionnaire_data: GestionnaireCreate, database: Session = Depends(get_db)) -> Gestionnaire:


    db_gestionnaire = Gestionnaire(
        nom=gestionnaire_data.nom,        id=gestionnaire_data.id,        prenom=gestionnaire_data.prenom,        email=gestionnaire_data.email,        emailReferent=gestionnaire_data.emailReferent        )

    database.add(db_gestionnaire)
    database.commit()
    database.refresh(db_gestionnaire)




    return db_gestionnaire


@app.post("/gestionnaire/bulk/", response_model=None, tags=["Gestionnaire"])
async def bulk_create_gestionnaire(items: list[GestionnaireCreate], database: Session = Depends(get_db)) -> dict:
    """Create multiple Gestionnaire entities at once"""
    created_items = []
    errors = []

    for idx, item_data in enumerate(items):
        try:
            # Basic validation for each item

            db_gestionnaire = Gestionnaire(
                nom=item_data.nom,                id=item_data.id,                prenom=item_data.prenom,                email=item_data.email,                emailReferent=item_data.emailReferent            )
            database.add(db_gestionnaire)
            database.flush()  # Get ID without committing
            created_items.append(db_gestionnaire.id)
        except Exception as e:
            errors.append({"index": idx, "error": str(e)})

    if errors:
        database.rollback()
        raise HTTPException(status_code=400, detail={"message": "Bulk creation failed", "errors": errors})

    database.commit()
    return {
        "created_count": len(created_items),
        "created_ids": created_items,
        "message": f"Successfully created {len(created_items)} Gestionnaire entities"
    }


@app.delete("/gestionnaire/bulk/", response_model=None, tags=["Gestionnaire"])
async def bulk_delete_gestionnaire(ids: list[int], database: Session = Depends(get_db)) -> dict:
    """Delete multiple Gestionnaire entities at once"""
    deleted_count = 0
    not_found = []

    for item_id in ids:
        db_gestionnaire = database.query(Gestionnaire).filter(Gestionnaire.id == item_id).first()
        if db_gestionnaire:
            database.delete(db_gestionnaire)
            deleted_count += 1
        else:
            not_found.append(item_id)

    database.commit()

    return {
        "deleted_count": deleted_count,
        "not_found": not_found,
        "message": f"Successfully deleted {deleted_count} Gestionnaire entities"
    }

@app.put("/gestionnaire/{gestionnaire_id}/", response_model=None, tags=["Gestionnaire"])
async def update_gestionnaire(gestionnaire_id: int, gestionnaire_data: GestionnaireCreate, database: Session = Depends(get_db)) -> Gestionnaire:
    db_gestionnaire = database.query(Gestionnaire).filter(Gestionnaire.id == gestionnaire_id).first()
    if db_gestionnaire is None:
        raise HTTPException(status_code=404, detail="Gestionnaire not found")

    setattr(db_gestionnaire, 'nom', gestionnaire_data.nom)
    setattr(db_gestionnaire, 'id', gestionnaire_data.id)
    setattr(db_gestionnaire, 'prenom', gestionnaire_data.prenom)
    setattr(db_gestionnaire, 'email', gestionnaire_data.email)
    setattr(db_gestionnaire, 'emailReferent', gestionnaire_data.emailReferent)
    database.commit()
    database.refresh(db_gestionnaire)

    return db_gestionnaire


@app.delete("/gestionnaire/{gestionnaire_id}/", response_model=None, tags=["Gestionnaire"])
async def delete_gestionnaire(gestionnaire_id: int, database: Session = Depends(get_db)):
    db_gestionnaire = database.query(Gestionnaire).filter(Gestionnaire.id == gestionnaire_id).first()
    if db_gestionnaire is None:
        raise HTTPException(status_code=404, detail="Gestionnaire not found")
    database.delete(db_gestionnaire)
    database.commit()
    return db_gestionnaire



############################################
#   Gestionnaire Method Endpoints
############################################




@app.post("/gestionnaire/methods/creerReservation/", response_model=None, tags=["Gestionnaire Methods"])
async def gestionnaire_creerReservation(
    params: dict = Body(default=None, embed=True),
    database: Session = Depends(get_db)
):
    """
    Execute the creerReservation class method on Gestionnaire.
    This method operates on all Gestionnaire entities or performs class-level operations.

    Parameters (pass as JSON body):
    - event: Any    - element: Any    """
    try:
        # Capture stdout to include print outputs in the response
        import io
        import sys
        captured_output = io.StringIO()
        sys.stdout = captured_output

        # Extract parameters from request body
        params = params or {}
        event = params.get('event')
        element = params.get('element')

        # Method body not defined
        result = None

        # Restore stdout
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()

        # Handle result serialization
        if hasattr(result, '__iter__') and not isinstance(result, (str, dict)):
            # It's a list of entities
            result_data = []
            for item in result:
                if hasattr(item, '__dict__'):
                    item_dict = {k: v for k, v in item.__dict__.items() if not k.startswith('_')}
                    result_data.append(item_dict)
                else:
                    result_data.append(str(item))
            result = result_data
        elif hasattr(result, '__dict__'):
            result = {k: v for k, v in result.__dict__.items() if not k.startswith('_')}

        return {
            "class": "Gestionnaire",
            "method": "creerReservation",
            "status": "executed",
            "result": result,
            "output": output if output else None
        }
    except Exception as e:
        sys.stdout = sys.__stdout__
        raise HTTPException(status_code=500, detail=f"Method execution failed: {str(e)}")




############################################
#
#   CentreDeCongres functions
#
############################################

@app.get("/centredecongres/", response_model=None, tags=["CentreDeCongres"])
def get_all_centredecongres(detailed: bool = False, database: Session = Depends(get_db)) -> list:
    from sqlalchemy.orm import joinedload

    # Use detailed=true to get entities with eagerly loaded relationships (for tables with lookup columns)
    if detailed:
        # Eagerly load all relationships to avoid N+1 queries
        query = database.query(CentreDeCongres)
        query = query.options(joinedload(CentreDeCongres.gestionnaire))
        centredecongres_list = query.all()

        # Serialize with relationships included
        result = []
        for centredecongres_item in centredecongres_list:
            item_dict = centredecongres_item.__dict__.copy()
            item_dict.pop('_sa_instance_state', None)

            # Add many-to-one relationships (foreign keys for lookup columns)
            if centredecongres_item.gestionnaire:
                related_obj = centredecongres_item.gestionnaire
                related_dict = related_obj.__dict__.copy()
                related_dict.pop('_sa_instance_state', None)
                item_dict['gestionnaire'] = related_dict
            else:
                item_dict['gestionnaire'] = None

            # Add many-to-many and one-to-many relationship objects (full details)
            elementcentre_list = database.query(ElementCentre).filter(ElementCentre.centredecongres_1_id == centredecongres_item.id).all()
            item_dict['elementcentre'] = []
            for elementcentre_obj in elementcentre_list:
                elementcentre_dict = elementcentre_obj.__dict__.copy()
                elementcentre_dict.pop('_sa_instance_state', None)
                item_dict['elementcentre'].append(elementcentre_dict)

            result.append(item_dict)
        return result
    else:
        # Default: return flat entities (faster for charts/widgets without lookup columns)
        return database.query(CentreDeCongres).all()


@app.get("/centredecongres/count/", response_model=None, tags=["CentreDeCongres"])
def get_count_centredecongres(database: Session = Depends(get_db)) -> dict:
    """Get the total count of CentreDeCongres entities"""
    count = database.query(CentreDeCongres).count()
    return {"count": count}


@app.get("/centredecongres/paginated/", response_model=None, tags=["CentreDeCongres"])
def get_paginated_centredecongres(skip: int = 0, limit: int = 100, detailed: bool = False, database: Session = Depends(get_db)) -> dict:
    """Get paginated list of CentreDeCongres entities"""
    total = database.query(CentreDeCongres).count()
    centredecongres_list = database.query(CentreDeCongres).offset(skip).limit(limit).all()
    # By default, return flat entities (for charts/widgets)
    # Use detailed=true to get entities with relationships
    if not detailed:
        return {
            "total": total,
            "skip": skip,
            "limit": limit,
            "data": centredecongres_list
        }

    result = []
    for centredecongres_item in centredecongres_list:
        elementcentre_ids = database.query(ElementCentre.id).filter(ElementCentre.centredecongres_1_id == centredecongres_item.id).all()
        item_data = {
            "centredecongres": centredecongres_item,
            "elementcentre_ids": [x[0] for x in elementcentre_ids]        }
        result.append(item_data)
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "data": result
    }


@app.get("/centredecongres/search/", response_model=None, tags=["CentreDeCongres"])
def search_centredecongres(
    database: Session = Depends(get_db)
) -> list:
    """Search CentreDeCongres entities by attributes"""
    query = database.query(CentreDeCongres)


    results = query.all()
    return results


@app.get("/centredecongres/{centredecongres_id}/", response_model=None, tags=["CentreDeCongres"])
async def get_centredecongres(centredecongres_id: int, database: Session = Depends(get_db)) -> CentreDeCongres:
    db_centredecongres = database.query(CentreDeCongres).filter(CentreDeCongres.id == centredecongres_id).first()
    if db_centredecongres is None:
        raise HTTPException(status_code=404, detail="CentreDeCongres not found")

    elementcentre_ids = database.query(ElementCentre.id).filter(ElementCentre.centredecongres_1_id == db_centredecongres.id).all()
    response_data = {
        "centredecongres": db_centredecongres,
        "elementcentre_ids": [x[0] for x in elementcentre_ids]}
    return response_data



@app.post("/centredecongres/", response_model=None, tags=["CentreDeCongres"])
async def create_centredecongres(centredecongres_data: CentreDeCongresCreate, database: Session = Depends(get_db)) -> CentreDeCongres:

    if centredecongres_data.gestionnaire is not None:
        db_gestionnaire = database.query(Gestionnaire).filter(Gestionnaire.id == centredecongres_data.gestionnaire).first()
        if not db_gestionnaire:
            raise HTTPException(status_code=400, detail="Gestionnaire not found")
    else:
        raise HTTPException(status_code=400, detail="Gestionnaire ID is required")

    db_centredecongres = CentreDeCongres(
        nom=centredecongres_data.nom,        email=centredecongres_data.email,        delaiConfirmationDefaut=centredecongres_data.delaiConfirmationDefaut,        id=centredecongres_data.id,        telephone=centredecongres_data.telephone,        adresse=centredecongres_data.adresse,        gestionnaire_id=centredecongres_data.gestionnaire        )

    database.add(db_centredecongres)
    database.commit()
    database.refresh(db_centredecongres)

    if centredecongres_data.elementcentre:
        # Validate that all ElementCentre IDs exist
        for elementcentre_id in centredecongres_data.elementcentre:
            db_elementcentre = database.query(ElementCentre).filter(ElementCentre.id == elementcentre_id).first()
            if not db_elementcentre:
                raise HTTPException(status_code=400, detail=f"ElementCentre with id {elementcentre_id} not found")

        # Update the related entities with the new foreign key
        database.query(ElementCentre).filter(ElementCentre.id.in_(centredecongres_data.elementcentre)).update(
            {ElementCentre.centredecongres_1_id: db_centredecongres.id}, synchronize_session=False
        )
        database.commit()



    elementcentre_ids = database.query(ElementCentre.id).filter(ElementCentre.centredecongres_1_id == db_centredecongres.id).all()
    response_data = {
        "centredecongres": db_centredecongres,
        "elementcentre_ids": [x[0] for x in elementcentre_ids]    }
    return response_data


@app.post("/centredecongres/bulk/", response_model=None, tags=["CentreDeCongres"])
async def bulk_create_centredecongres(items: list[CentreDeCongresCreate], database: Session = Depends(get_db)) -> dict:
    """Create multiple CentreDeCongres entities at once"""
    created_items = []
    errors = []

    for idx, item_data in enumerate(items):
        try:
            # Basic validation for each item
            if not item_data.gestionnaire:
                raise ValueError("Gestionnaire ID is required")

            db_centredecongres = CentreDeCongres(
                nom=item_data.nom,                email=item_data.email,                delaiConfirmationDefaut=item_data.delaiConfirmationDefaut,                id=item_data.id,                telephone=item_data.telephone,                adresse=item_data.adresse,                gestionnaire_id=item_data.gestionnaire            )
            database.add(db_centredecongres)
            database.flush()  # Get ID without committing
            created_items.append(db_centredecongres.id)
        except Exception as e:
            errors.append({"index": idx, "error": str(e)})

    if errors:
        database.rollback()
        raise HTTPException(status_code=400, detail={"message": "Bulk creation failed", "errors": errors})

    database.commit()
    return {
        "created_count": len(created_items),
        "created_ids": created_items,
        "message": f"Successfully created {len(created_items)} CentreDeCongres entities"
    }


@app.delete("/centredecongres/bulk/", response_model=None, tags=["CentreDeCongres"])
async def bulk_delete_centredecongres(ids: list[int], database: Session = Depends(get_db)) -> dict:
    """Delete multiple CentreDeCongres entities at once"""
    deleted_count = 0
    not_found = []

    for item_id in ids:
        db_centredecongres = database.query(CentreDeCongres).filter(CentreDeCongres.id == item_id).first()
        if db_centredecongres:
            database.delete(db_centredecongres)
            deleted_count += 1
        else:
            not_found.append(item_id)

    database.commit()

    return {
        "deleted_count": deleted_count,
        "not_found": not_found,
        "message": f"Successfully deleted {deleted_count} CentreDeCongres entities"
    }

@app.put("/centredecongres/{centredecongres_id}/", response_model=None, tags=["CentreDeCongres"])
async def update_centredecongres(centredecongres_id: int, centredecongres_data: CentreDeCongresCreate, database: Session = Depends(get_db)) -> CentreDeCongres:
    db_centredecongres = database.query(CentreDeCongres).filter(CentreDeCongres.id == centredecongres_id).first()
    if db_centredecongres is None:
        raise HTTPException(status_code=404, detail="CentreDeCongres not found")

    setattr(db_centredecongres, 'nom', centredecongres_data.nom)
    setattr(db_centredecongres, 'email', centredecongres_data.email)
    setattr(db_centredecongres, 'delaiConfirmationDefaut', centredecongres_data.delaiConfirmationDefaut)
    setattr(db_centredecongres, 'id', centredecongres_data.id)
    setattr(db_centredecongres, 'telephone', centredecongres_data.telephone)
    setattr(db_centredecongres, 'adresse', centredecongres_data.adresse)
    if centredecongres_data.gestionnaire is not None:
        db_gestionnaire = database.query(Gestionnaire).filter(Gestionnaire.id == centredecongres_data.gestionnaire).first()
        if not db_gestionnaire:
            raise HTTPException(status_code=400, detail="Gestionnaire not found")
        setattr(db_centredecongres, 'gestionnaire_id', centredecongres_data.gestionnaire)
    if centredecongres_data.elementcentre is not None:
        # Clear all existing relationships (set foreign key to NULL)
        database.query(ElementCentre).filter(ElementCentre.centredecongres_1_id == db_centredecongres.id).update(
            {ElementCentre.centredecongres_1_id: None}, synchronize_session=False
        )

        # Set new relationships if list is not empty
        if centredecongres_data.elementcentre:
            # Validate that all IDs exist
            for elementcentre_id in centredecongres_data.elementcentre:
                db_elementcentre = database.query(ElementCentre).filter(ElementCentre.id == elementcentre_id).first()
                if not db_elementcentre:
                    raise HTTPException(status_code=400, detail=f"ElementCentre with id {elementcentre_id} not found")

            # Update the related entities with the new foreign key
            database.query(ElementCentre).filter(ElementCentre.id.in_(centredecongres_data.elementcentre)).update(
                {ElementCentre.centredecongres_1_id: db_centredecongres.id}, synchronize_session=False
            )
    database.commit()
    database.refresh(db_centredecongres)

    elementcentre_ids = database.query(ElementCentre.id).filter(ElementCentre.centredecongres_1_id == db_centredecongres.id).all()
    response_data = {
        "centredecongres": db_centredecongres,
        "elementcentre_ids": [x[0] for x in elementcentre_ids]    }
    return response_data


@app.delete("/centredecongres/{centredecongres_id}/", response_model=None, tags=["CentreDeCongres"])
async def delete_centredecongres(centredecongres_id: int, database: Session = Depends(get_db)):
    db_centredecongres = database.query(CentreDeCongres).filter(CentreDeCongres.id == centredecongres_id).first()
    if db_centredecongres is None:
        raise HTTPException(status_code=404, detail="CentreDeCongres not found")
    database.delete(db_centredecongres)
    database.commit()
    return db_centredecongres



############################################
#   CentreDeCongres Method Endpoints
############################################




@app.post("/centredecongres/methods/getStatistiques/", response_model=None, tags=["CentreDeCongres Methods"])
async def centredecongres_getStatistiques(
    params: dict = Body(default=None, embed=True),
    database: Session = Depends(get_db)
):
    """
    Execute the getStatistiques class method on CentreDeCongres.
    This method operates on all CentreDeCongres entities or performs class-level operations.

    Parameters (pass as JSON body):
    - periode: Any    """
    try:
        # Capture stdout to include print outputs in the response
        import io
        import sys
        captured_output = io.StringIO()
        sys.stdout = captured_output

        # Extract parameters from request body
        params = params or {}
        periode = params.get('periode')

        # Method body not defined
        result = None

        # Restore stdout
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()

        # Handle result serialization
        if hasattr(result, '__iter__') and not isinstance(result, (str, dict)):
            # It's a list of entities
            result_data = []
            for item in result:
                if hasattr(item, '__dict__'):
                    item_dict = {k: v for k, v in item.__dict__.items() if not k.startswith('_')}
                    result_data.append(item_dict)
                else:
                    result_data.append(str(item))
            result = result_data
        elif hasattr(result, '__dict__'):
            result = {k: v for k, v in result.__dict__.items() if not k.startswith('_')}

        return {
            "class": "CentreDeCongres",
            "method": "getStatistiques",
            "status": "executed",
            "result": result,
            "output": output if output else None
        }
    except Exception as e:
        sys.stdout = sys.__stdout__
        raise HTTPException(status_code=500, detail=f"Method execution failed: {str(e)}")






@app.post("/centredecongres/methods/getDisponibilites/", response_model=None, tags=["CentreDeCongres Methods"])
async def centredecongres_getDisponibilites(
    params: dict = Body(default=None, embed=True),
    database: Session = Depends(get_db)
):
    """
    Execute the getDisponibilites class method on CentreDeCongres.
    This method operates on all CentreDeCongres entities or performs class-level operations.

    Parameters (pass as JSON body):
    - debut: Any    - fin: Any    """
    try:
        # Capture stdout to include print outputs in the response
        import io
        import sys
        captured_output = io.StringIO()
        sys.stdout = captured_output

        # Extract parameters from request body
        params = params or {}
        debut = params.get('debut')
        fin = params.get('fin')

        # Method body not defined
        result = None

        # Restore stdout
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()

        # Handle result serialization
        if hasattr(result, '__iter__') and not isinstance(result, (str, dict)):
            # It's a list of entities
            result_data = []
            for item in result:
                if hasattr(item, '__dict__'):
                    item_dict = {k: v for k, v in item.__dict__.items() if not k.startswith('_')}
                    result_data.append(item_dict)
                else:
                    result_data.append(str(item))
            result = result_data
        elif hasattr(result, '__dict__'):
            result = {k: v for k, v in result.__dict__.items() if not k.startswith('_')}

        return {
            "class": "CentreDeCongres",
            "method": "getDisponibilites",
            "status": "executed",
            "result": result,
            "output": output if output else None
        }
    except Exception as e:
        sys.stdout = sys.__stdout__
        raise HTTPException(status_code=500, detail=f"Method execution failed: {str(e)}")




############################################
#
#   Prestation functions
#
############################################

@app.get("/prestation/", response_model=None, tags=["Prestation"])
def get_all_prestation(detailed: bool = False, database: Session = Depends(get_db)) -> list:
    from sqlalchemy.orm import joinedload

    # Use detailed=true to get entities with eagerly loaded relationships (for tables with lookup columns)
    if detailed:
        # Eagerly load all relationships to avoid N+1 queries
        query = database.query(Prestation)
        query = query.options(joinedload(Prestation.lignereservation_1))
        prestation_list = query.all()

        # Serialize with relationships included
        result = []
        for prestation_item in prestation_list:
            item_dict = prestation_item.__dict__.copy()
            item_dict.pop('_sa_instance_state', None)

            # Add many-to-one relationships (foreign keys for lookup columns)
            if prestation_item.lignereservation_1:
                related_obj = prestation_item.lignereservation_1
                related_dict = related_obj.__dict__.copy()
                related_dict.pop('_sa_instance_state', None)
                item_dict['lignereservation_1'] = related_dict
            else:
                item_dict['lignereservation_1'] = None


            result.append(item_dict)
        return result
    else:
        # Default: return flat entities (faster for charts/widgets without lookup columns)
        return database.query(Prestation).all()


@app.get("/prestation/count/", response_model=None, tags=["Prestation"])
def get_count_prestation(database: Session = Depends(get_db)) -> dict:
    """Get the total count of Prestation entities"""
    count = database.query(Prestation).count()
    return {"count": count}


@app.get("/prestation/paginated/", response_model=None, tags=["Prestation"])
def get_paginated_prestation(skip: int = 0, limit: int = 100, detailed: bool = False, database: Session = Depends(get_db)) -> dict:
    """Get paginated list of Prestation entities"""
    total = database.query(Prestation).count()
    prestation_list = database.query(Prestation).offset(skip).limit(limit).all()
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "data": prestation_list
    }


@app.get("/prestation/search/", response_model=None, tags=["Prestation"])
def search_prestation(
    database: Session = Depends(get_db)
) -> list:
    """Search Prestation entities by attributes"""
    query = database.query(Prestation)


    results = query.all()
    return results


@app.get("/prestation/{prestation_id}/", response_model=None, tags=["Prestation"])
async def get_prestation(prestation_id: int, database: Session = Depends(get_db)) -> Prestation:
    db_prestation = database.query(Prestation).filter(Prestation.id == prestation_id).first()
    if db_prestation is None:
        raise HTTPException(status_code=404, detail="Prestation not found")

    response_data = {
        "prestation": db_prestation,
}
    return response_data



@app.post("/prestation/", response_model=None, tags=["Prestation"])
async def create_prestation(prestation_data: PrestationCreate, database: Session = Depends(get_db)) -> Prestation:

    if prestation_data.lignereservation_1 is not None:
        db_lignereservation_1 = database.query(LigneReservation).filter(LigneReservation.id == prestation_data.lignereservation_1).first()
        if not db_lignereservation_1:
            raise HTTPException(status_code=400, detail="LigneReservation not found")
    else:
        raise HTTPException(status_code=400, detail="LigneReservation ID is required")

    db_prestation = Prestation(
        nom=prestation_data.nom,        id=prestation_data.id,        description=prestation_data.description,        prixUnitaire=prestation_data.prixUnitaire,        lignereservation_1_id=prestation_data.lignereservation_1        )

    database.add(db_prestation)
    database.commit()
    database.refresh(db_prestation)




    return db_prestation


@app.post("/prestation/bulk/", response_model=None, tags=["Prestation"])
async def bulk_create_prestation(items: list[PrestationCreate], database: Session = Depends(get_db)) -> dict:
    """Create multiple Prestation entities at once"""
    created_items = []
    errors = []

    for idx, item_data in enumerate(items):
        try:
            # Basic validation for each item
            if not item_data.lignereservation_1:
                raise ValueError("LigneReservation ID is required")

            db_prestation = Prestation(
                nom=item_data.nom,                id=item_data.id,                description=item_data.description,                prixUnitaire=item_data.prixUnitaire,                lignereservation_1_id=item_data.lignereservation_1            )
            database.add(db_prestation)
            database.flush()  # Get ID without committing
            created_items.append(db_prestation.id)
        except Exception as e:
            errors.append({"index": idx, "error": str(e)})

    if errors:
        database.rollback()
        raise HTTPException(status_code=400, detail={"message": "Bulk creation failed", "errors": errors})

    database.commit()
    return {
        "created_count": len(created_items),
        "created_ids": created_items,
        "message": f"Successfully created {len(created_items)} Prestation entities"
    }


@app.delete("/prestation/bulk/", response_model=None, tags=["Prestation"])
async def bulk_delete_prestation(ids: list[int], database: Session = Depends(get_db)) -> dict:
    """Delete multiple Prestation entities at once"""
    deleted_count = 0
    not_found = []

    for item_id in ids:
        db_prestation = database.query(Prestation).filter(Prestation.id == item_id).first()
        if db_prestation:
            database.delete(db_prestation)
            deleted_count += 1
        else:
            not_found.append(item_id)

    database.commit()

    return {
        "deleted_count": deleted_count,
        "not_found": not_found,
        "message": f"Successfully deleted {deleted_count} Prestation entities"
    }

@app.put("/prestation/{prestation_id}/", response_model=None, tags=["Prestation"])
async def update_prestation(prestation_id: int, prestation_data: PrestationCreate, database: Session = Depends(get_db)) -> Prestation:
    db_prestation = database.query(Prestation).filter(Prestation.id == prestation_id).first()
    if db_prestation is None:
        raise HTTPException(status_code=404, detail="Prestation not found")

    setattr(db_prestation, 'nom', prestation_data.nom)
    setattr(db_prestation, 'id', prestation_data.id)
    setattr(db_prestation, 'description', prestation_data.description)
    setattr(db_prestation, 'prixUnitaire', prestation_data.prixUnitaire)
    if prestation_data.lignereservation_1 is not None:
        db_lignereservation_1 = database.query(LigneReservation).filter(LigneReservation.id == prestation_data.lignereservation_1).first()
        if not db_lignereservation_1:
            raise HTTPException(status_code=400, detail="LigneReservation not found")
        setattr(db_prestation, 'lignereservation_1_id', prestation_data.lignereservation_1)
    database.commit()
    database.refresh(db_prestation)

    return db_prestation


@app.delete("/prestation/{prestation_id}/", response_model=None, tags=["Prestation"])
async def delete_prestation(prestation_id: int, database: Session = Depends(get_db)):
    db_prestation = database.query(Prestation).filter(Prestation.id == prestation_id).first()
    if db_prestation is None:
        raise HTTPException(status_code=404, detail="Prestation not found")
    database.delete(db_prestation)
    database.commit()
    return db_prestation



############################################
#   Prestation Method Endpoints
############################################




@app.post("/prestation/methods/calculerCout/", response_model=None, tags=["Prestation Methods"])
async def prestation_calculerCout(
    params: dict = Body(default=None, embed=True),
    database: Session = Depends(get_db)
):
    """
    Execute the calculerCout class method on Prestation.
    This method operates on all Prestation entities or performs class-level operations.

    Parameters (pass as JSON body):
    - params: Any    """
    try:
        # Capture stdout to include print outputs in the response
        import io
        import sys
        captured_output = io.StringIO()
        sys.stdout = captured_output

        # Extract parameters from request body
        params = params or {}
        params = params.get('params')

        # Method body not defined
        result = None

        # Restore stdout
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()

        # Handle result serialization
        if hasattr(result, '__iter__') and not isinstance(result, (str, dict)):
            # It's a list of entities
            result_data = []
            for item in result:
                if hasattr(item, '__dict__'):
                    item_dict = {k: v for k, v in item.__dict__.items() if not k.startswith('_')}
                    result_data.append(item_dict)
                else:
                    result_data.append(str(item))
            result = result_data
        elif hasattr(result, '__dict__'):
            result = {k: v for k, v in result.__dict__.items() if not k.startswith('_')}

        return {
            "class": "Prestation",
            "method": "calculerCout",
            "status": "executed",
            "result": result,
            "output": output if output else None
        }
    except Exception as e:
        sys.stdout = sys.__stdout__
        raise HTTPException(status_code=500, detail=f"Method execution failed: {str(e)}")




############################################
#
#   PrestationGlobale functions
#
############################################

@app.get("/prestationglobale/", response_model=None, tags=["PrestationGlobale"])
def get_all_prestationglobale(detailed: bool = False, database: Session = Depends(get_db)) -> list:
    from sqlalchemy.orm import joinedload

    # Use detailed=true to get entities with eagerly loaded relationships (for tables with lookup columns)
    if detailed:
        # Eagerly load all relationships to avoid N+1 queries
        query = database.query(PrestationGlobale)
        query = query.options(joinedload(PrestationGlobale.lignereservation_1))
        prestationglobale_list = query.all()

        # Serialize with relationships included
        result = []
        for prestationglobale_item in prestationglobale_list:
            item_dict = prestationglobale_item.__dict__.copy()
            item_dict.pop('_sa_instance_state', None)

            # Add many-to-one relationships (foreign keys for lookup columns)
            if prestationglobale_item.lignereservation_1:
                related_obj = prestationglobale_item.lignereservation_1
                related_dict = related_obj.__dict__.copy()
                related_dict.pop('_sa_instance_state', None)
                item_dict['lignereservation_1'] = related_dict
            else:
                item_dict['lignereservation_1'] = None


            result.append(item_dict)
        return result
    else:
        # Default: return flat entities (faster for charts/widgets without lookup columns)
        return database.query(PrestationGlobale).all()


@app.get("/prestationglobale/count/", response_model=None, tags=["PrestationGlobale"])
def get_count_prestationglobale(database: Session = Depends(get_db)) -> dict:
    """Get the total count of PrestationGlobale entities"""
    count = database.query(PrestationGlobale).count()
    return {"count": count}


@app.get("/prestationglobale/paginated/", response_model=None, tags=["PrestationGlobale"])
def get_paginated_prestationglobale(skip: int = 0, limit: int = 100, detailed: bool = False, database: Session = Depends(get_db)) -> dict:
    """Get paginated list of PrestationGlobale entities"""
    total = database.query(PrestationGlobale).count()
    prestationglobale_list = database.query(PrestationGlobale).offset(skip).limit(limit).all()
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "data": prestationglobale_list
    }


@app.get("/prestationglobale/search/", response_model=None, tags=["PrestationGlobale"])
def search_prestationglobale(
    database: Session = Depends(get_db)
) -> list:
    """Search PrestationGlobale entities by attributes"""
    query = database.query(PrestationGlobale)


    results = query.all()
    return results


@app.get("/prestationglobale/{prestationglobale_id}/", response_model=None, tags=["PrestationGlobale"])
async def get_prestationglobale(prestationglobale_id: int, database: Session = Depends(get_db)) -> PrestationGlobale:
    db_prestationglobale = database.query(PrestationGlobale).filter(PrestationGlobale.id == prestationglobale_id).first()
    if db_prestationglobale is None:
        raise HTTPException(status_code=404, detail="PrestationGlobale not found")

    response_data = {
        "prestationglobale": db_prestationglobale,
}
    return response_data



@app.post("/prestationglobale/", response_model=None, tags=["PrestationGlobale"])
async def create_prestationglobale(prestationglobale_data: PrestationGlobaleCreate, database: Session = Depends(get_db)) -> PrestationGlobale:

    if prestationglobale_data.lignereservation_1 is not None:
        db_lignereservation_1 = database.query(LigneReservation).filter(LigneReservation.id == prestationglobale_data.lignereservation_1).first()
        if not db_lignereservation_1:
            raise HTTPException(status_code=400, detail="LigneReservation not found")
    else:
        raise HTTPException(status_code=400, detail="LigneReservation ID is required")

    db_prestationglobale = PrestationGlobale(
        nom=prestationglobale_data.nom,        id=prestationglobale_data.id,        description=prestationglobale_data.description,        prixUnitaire=prestationglobale_data.prixUnitaire,        unite=prestationglobale_data.unite,        quantiteMin=prestationglobale_data.quantiteMin,        lignereservation_1_id=prestationglobale_data.lignereservation_1        )

    database.add(db_prestationglobale)
    database.commit()
    database.refresh(db_prestationglobale)




    return db_prestationglobale


@app.post("/prestationglobale/bulk/", response_model=None, tags=["PrestationGlobale"])
async def bulk_create_prestationglobale(items: list[PrestationGlobaleCreate], database: Session = Depends(get_db)) -> dict:
    """Create multiple PrestationGlobale entities at once"""
    created_items = []
    errors = []

    for idx, item_data in enumerate(items):
        try:
            # Basic validation for each item
            if not item_data.lignereservation_1:
                raise ValueError("LigneReservation ID is required")

            db_prestationglobale = PrestationGlobale(
                nom=item_data.nom,                id=item_data.id,                description=item_data.description,                prixUnitaire=item_data.prixUnitaire,                unite=item_data.unite,                quantiteMin=item_data.quantiteMin,                lignereservation_1_id=item_data.lignereservation_1            )
            database.add(db_prestationglobale)
            database.flush()  # Get ID without committing
            created_items.append(db_prestationglobale.id)
        except Exception as e:
            errors.append({"index": idx, "error": str(e)})

    if errors:
        database.rollback()
        raise HTTPException(status_code=400, detail={"message": "Bulk creation failed", "errors": errors})

    database.commit()
    return {
        "created_count": len(created_items),
        "created_ids": created_items,
        "message": f"Successfully created {len(created_items)} PrestationGlobale entities"
    }


@app.delete("/prestationglobale/bulk/", response_model=None, tags=["PrestationGlobale"])
async def bulk_delete_prestationglobale(ids: list[int], database: Session = Depends(get_db)) -> dict:
    """Delete multiple PrestationGlobale entities at once"""
    deleted_count = 0
    not_found = []

    for item_id in ids:
        db_prestationglobale = database.query(PrestationGlobale).filter(PrestationGlobale.id == item_id).first()
        if db_prestationglobale:
            database.delete(db_prestationglobale)
            deleted_count += 1
        else:
            not_found.append(item_id)

    database.commit()

    return {
        "deleted_count": deleted_count,
        "not_found": not_found,
        "message": f"Successfully deleted {deleted_count} PrestationGlobale entities"
    }

@app.put("/prestationglobale/{prestationglobale_id}/", response_model=None, tags=["PrestationGlobale"])
async def update_prestationglobale(prestationglobale_id: int, prestationglobale_data: PrestationGlobaleCreate, database: Session = Depends(get_db)) -> PrestationGlobale:
    db_prestationglobale = database.query(PrestationGlobale).filter(PrestationGlobale.id == prestationglobale_id).first()
    if db_prestationglobale is None:
        raise HTTPException(status_code=404, detail="PrestationGlobale not found")

    setattr(db_prestationglobale, 'unite', prestationglobale_data.unite)
    setattr(db_prestationglobale, 'quantiteMin', prestationglobale_data.quantiteMin)
    database.commit()
    database.refresh(db_prestationglobale)

    return db_prestationglobale


@app.delete("/prestationglobale/{prestationglobale_id}/", response_model=None, tags=["PrestationGlobale"])
async def delete_prestationglobale(prestationglobale_id: int, database: Session = Depends(get_db)):
    db_prestationglobale = database.query(PrestationGlobale).filter(PrestationGlobale.id == prestationglobale_id).first()
    if db_prestationglobale is None:
        raise HTTPException(status_code=404, detail="PrestationGlobale not found")
    database.delete(db_prestationglobale)
    database.commit()
    return db_prestationglobale



############################################
#   PrestationGlobale Method Endpoints
############################################




@app.post("/prestationglobale/methods/calculerCout/", response_model=None, tags=["PrestationGlobale Methods"])
async def prestationglobale_calculerCout(
    params: dict = Body(default=None, embed=True),
    database: Session = Depends(get_db)
):
    """
    Execute the calculerCout class method on PrestationGlobale.
    This method operates on all PrestationGlobale entities or performs class-level operations.

    Parameters (pass as JSON body):
    - quantite: Any    """
    try:
        # Capture stdout to include print outputs in the response
        import io
        import sys
        captured_output = io.StringIO()
        sys.stdout = captured_output

        # Extract parameters from request body
        params = params or {}
        quantite = params.get('quantite')

        # Method body not defined
        result = None

        # Restore stdout
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()

        # Handle result serialization
        if hasattr(result, '__iter__') and not isinstance(result, (str, dict)):
            # It's a list of entities
            result_data = []
            for item in result:
                if hasattr(item, '__dict__'):
                    item_dict = {k: v for k, v in item.__dict__.items() if not k.startswith('_')}
                    result_data.append(item_dict)
                else:
                    result_data.append(str(item))
            result = result_data
        elif hasattr(result, '__dict__'):
            result = {k: v for k, v in result.__dict__.items() if not k.startswith('_')}

        return {
            "class": "PrestationGlobale",
            "method": "calculerCout",
            "status": "executed",
            "result": result,
            "output": output if output else None
        }
    except Exception as e:
        sys.stdout = sys.__stdout__
        raise HTTPException(status_code=500, detail=f"Method execution failed: {str(e)}")




############################################
#
#   PrestationDimensionnee functions
#
############################################

@app.get("/prestationdimensionnee/", response_model=None, tags=["PrestationDimensionnee"])
def get_all_prestationdimensionnee(detailed: bool = False, database: Session = Depends(get_db)) -> list:
    from sqlalchemy.orm import joinedload

    # Use detailed=true to get entities with eagerly loaded relationships (for tables with lookup columns)
    if detailed:
        # Eagerly load all relationships to avoid N+1 queries
        query = database.query(PrestationDimensionnee)
        query = query.options(joinedload(PrestationDimensionnee.lignereservation_1))
        prestationdimensionnee_list = query.all()

        # Serialize with relationships included
        result = []
        for prestationdimensionnee_item in prestationdimensionnee_list:
            item_dict = prestationdimensionnee_item.__dict__.copy()
            item_dict.pop('_sa_instance_state', None)

            # Add many-to-one relationships (foreign keys for lookup columns)
            if prestationdimensionnee_item.lignereservation_1:
                related_obj = prestationdimensionnee_item.lignereservation_1
                related_dict = related_obj.__dict__.copy()
                related_dict.pop('_sa_instance_state', None)
                item_dict['lignereservation_1'] = related_dict
            else:
                item_dict['lignereservation_1'] = None


            result.append(item_dict)
        return result
    else:
        # Default: return flat entities (faster for charts/widgets without lookup columns)
        return database.query(PrestationDimensionnee).all()


@app.get("/prestationdimensionnee/count/", response_model=None, tags=["PrestationDimensionnee"])
def get_count_prestationdimensionnee(database: Session = Depends(get_db)) -> dict:
    """Get the total count of PrestationDimensionnee entities"""
    count = database.query(PrestationDimensionnee).count()
    return {"count": count}


@app.get("/prestationdimensionnee/paginated/", response_model=None, tags=["PrestationDimensionnee"])
def get_paginated_prestationdimensionnee(skip: int = 0, limit: int = 100, detailed: bool = False, database: Session = Depends(get_db)) -> dict:
    """Get paginated list of PrestationDimensionnee entities"""
    total = database.query(PrestationDimensionnee).count()
    prestationdimensionnee_list = database.query(PrestationDimensionnee).offset(skip).limit(limit).all()
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "data": prestationdimensionnee_list
    }


@app.get("/prestationdimensionnee/search/", response_model=None, tags=["PrestationDimensionnee"])
def search_prestationdimensionnee(
    database: Session = Depends(get_db)
) -> list:
    """Search PrestationDimensionnee entities by attributes"""
    query = database.query(PrestationDimensionnee)


    results = query.all()
    return results


@app.get("/prestationdimensionnee/{prestationdimensionnee_id}/", response_model=None, tags=["PrestationDimensionnee"])
async def get_prestationdimensionnee(prestationdimensionnee_id: int, database: Session = Depends(get_db)) -> PrestationDimensionnee:
    db_prestationdimensionnee = database.query(PrestationDimensionnee).filter(PrestationDimensionnee.id == prestationdimensionnee_id).first()
    if db_prestationdimensionnee is None:
        raise HTTPException(status_code=404, detail="PrestationDimensionnee not found")

    response_data = {
        "prestationdimensionnee": db_prestationdimensionnee,
}
    return response_data



@app.post("/prestationdimensionnee/", response_model=None, tags=["PrestationDimensionnee"])
async def create_prestationdimensionnee(prestationdimensionnee_data: PrestationDimensionneeCreate, database: Session = Depends(get_db)) -> PrestationDimensionnee:

    if prestationdimensionnee_data.lignereservation_1 is not None:
        db_lignereservation_1 = database.query(LigneReservation).filter(LigneReservation.id == prestationdimensionnee_data.lignereservation_1).first()
        if not db_lignereservation_1:
            raise HTTPException(status_code=400, detail="LigneReservation not found")
    else:
        raise HTTPException(status_code=400, detail="LigneReservation ID is required")

    db_prestationdimensionnee = PrestationDimensionnee(
        nom=prestationdimensionnee_data.nom,        id=prestationdimensionnee_data.id,        description=prestationdimensionnee_data.description,        prixUnitaire=prestationdimensionnee_data.prixUnitaire,        nbParticipantsMax=prestationdimensionnee_data.nbParticipantsMax,        nbParticipantsMin=prestationdimensionnee_data.nbParticipantsMin,        lignereservation_1_id=prestationdimensionnee_data.lignereservation_1        )

    database.add(db_prestationdimensionnee)
    database.commit()
    database.refresh(db_prestationdimensionnee)




    return db_prestationdimensionnee


@app.post("/prestationdimensionnee/bulk/", response_model=None, tags=["PrestationDimensionnee"])
async def bulk_create_prestationdimensionnee(items: list[PrestationDimensionneeCreate], database: Session = Depends(get_db)) -> dict:
    """Create multiple PrestationDimensionnee entities at once"""
    created_items = []
    errors = []

    for idx, item_data in enumerate(items):
        try:
            # Basic validation for each item
            if not item_data.lignereservation_1:
                raise ValueError("LigneReservation ID is required")

            db_prestationdimensionnee = PrestationDimensionnee(
                nom=item_data.nom,                id=item_data.id,                description=item_data.description,                prixUnitaire=item_data.prixUnitaire,                nbParticipantsMax=item_data.nbParticipantsMax,                nbParticipantsMin=item_data.nbParticipantsMin,                lignereservation_1_id=item_data.lignereservation_1            )
            database.add(db_prestationdimensionnee)
            database.flush()  # Get ID without committing
            created_items.append(db_prestationdimensionnee.id)
        except Exception as e:
            errors.append({"index": idx, "error": str(e)})

    if errors:
        database.rollback()
        raise HTTPException(status_code=400, detail={"message": "Bulk creation failed", "errors": errors})

    database.commit()
    return {
        "created_count": len(created_items),
        "created_ids": created_items,
        "message": f"Successfully created {len(created_items)} PrestationDimensionnee entities"
    }


@app.delete("/prestationdimensionnee/bulk/", response_model=None, tags=["PrestationDimensionnee"])
async def bulk_delete_prestationdimensionnee(ids: list[int], database: Session = Depends(get_db)) -> dict:
    """Delete multiple PrestationDimensionnee entities at once"""
    deleted_count = 0
    not_found = []

    for item_id in ids:
        db_prestationdimensionnee = database.query(PrestationDimensionnee).filter(PrestationDimensionnee.id == item_id).first()
        if db_prestationdimensionnee:
            database.delete(db_prestationdimensionnee)
            deleted_count += 1
        else:
            not_found.append(item_id)

    database.commit()

    return {
        "deleted_count": deleted_count,
        "not_found": not_found,
        "message": f"Successfully deleted {deleted_count} PrestationDimensionnee entities"
    }

@app.put("/prestationdimensionnee/{prestationdimensionnee_id}/", response_model=None, tags=["PrestationDimensionnee"])
async def update_prestationdimensionnee(prestationdimensionnee_id: int, prestationdimensionnee_data: PrestationDimensionneeCreate, database: Session = Depends(get_db)) -> PrestationDimensionnee:
    db_prestationdimensionnee = database.query(PrestationDimensionnee).filter(PrestationDimensionnee.id == prestationdimensionnee_id).first()
    if db_prestationdimensionnee is None:
        raise HTTPException(status_code=404, detail="PrestationDimensionnee not found")

    setattr(db_prestationdimensionnee, 'nbParticipantsMax', prestationdimensionnee_data.nbParticipantsMax)
    setattr(db_prestationdimensionnee, 'nbParticipantsMin', prestationdimensionnee_data.nbParticipantsMin)
    database.commit()
    database.refresh(db_prestationdimensionnee)

    return db_prestationdimensionnee


@app.delete("/prestationdimensionnee/{prestationdimensionnee_id}/", response_model=None, tags=["PrestationDimensionnee"])
async def delete_prestationdimensionnee(prestationdimensionnee_id: int, database: Session = Depends(get_db)):
    db_prestationdimensionnee = database.query(PrestationDimensionnee).filter(PrestationDimensionnee.id == prestationdimensionnee_id).first()
    if db_prestationdimensionnee is None:
        raise HTTPException(status_code=404, detail="PrestationDimensionnee not found")
    database.delete(db_prestationdimensionnee)
    database.commit()
    return db_prestationdimensionnee



############################################
#   PrestationDimensionnee Method Endpoints
############################################




@app.post("/prestationdimensionnee/methods/calculerCout/", response_model=None, tags=["PrestationDimensionnee Methods"])
async def prestationdimensionnee_calculerCout(
    params: dict = Body(default=None, embed=True),
    database: Session = Depends(get_db)
):
    """
    Execute the calculerCout class method on PrestationDimensionnee.
    This method operates on all PrestationDimensionnee entities or performs class-level operations.

    Parameters (pass as JSON body):
    - nbParticipants: Any    """
    try:
        # Capture stdout to include print outputs in the response
        import io
        import sys
        captured_output = io.StringIO()
        sys.stdout = captured_output

        # Extract parameters from request body
        params = params or {}
        nbParticipants = params.get('nbParticipants')

        # Method body not defined
        result = None

        # Restore stdout
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()

        # Handle result serialization
        if hasattr(result, '__iter__') and not isinstance(result, (str, dict)):
            # It's a list of entities
            result_data = []
            for item in result:
                if hasattr(item, '__dict__'):
                    item_dict = {k: v for k, v in item.__dict__.items() if not k.startswith('_')}
                    result_data.append(item_dict)
                else:
                    result_data.append(str(item))
            result = result_data
        elif hasattr(result, '__dict__'):
            result = {k: v for k, v in result.__dict__.items() if not k.startswith('_')}

        return {
            "class": "PrestationDimensionnee",
            "method": "calculerCout",
            "status": "executed",
            "result": result,
            "output": output if output else None
        }
    except Exception as e:
        sys.stdout = sys.__stdout__
        raise HTTPException(status_code=500, detail=f"Method execution failed: {str(e)}")




############################################
#
#   StockMateriel functions
#
############################################

@app.get("/stockmateriel/", response_model=None, tags=["StockMateriel"])
def get_all_stockmateriel(detailed: bool = False, database: Session = Depends(get_db)) -> list:
    from sqlalchemy.orm import joinedload

    # Use detailed=true to get entities with eagerly loaded relationships (for tables with lookup columns)
    if detailed:
        # Eagerly load all relationships to avoid N+1 queries
        query = database.query(StockMateriel)
        query = query.options(joinedload(StockMateriel.materiel))
        stockmateriel_list = query.all()

        # Serialize with relationships included
        result = []
        for stockmateriel_item in stockmateriel_list:
            item_dict = stockmateriel_item.__dict__.copy()
            item_dict.pop('_sa_instance_state', None)

            # Add many-to-one relationships (foreign keys for lookup columns)
            if stockmateriel_item.materiel:
                related_obj = stockmateriel_item.materiel
                related_dict = related_obj.__dict__.copy()
                related_dict.pop('_sa_instance_state', None)
                item_dict['materiel'] = related_dict
            else:
                item_dict['materiel'] = None


            result.append(item_dict)
        return result
    else:
        # Default: return flat entities (faster for charts/widgets without lookup columns)
        return database.query(StockMateriel).all()


@app.get("/stockmateriel/count/", response_model=None, tags=["StockMateriel"])
def get_count_stockmateriel(database: Session = Depends(get_db)) -> dict:
    """Get the total count of StockMateriel entities"""
    count = database.query(StockMateriel).count()
    return {"count": count}


@app.get("/stockmateriel/paginated/", response_model=None, tags=["StockMateriel"])
def get_paginated_stockmateriel(skip: int = 0, limit: int = 100, detailed: bool = False, database: Session = Depends(get_db)) -> dict:
    """Get paginated list of StockMateriel entities"""
    total = database.query(StockMateriel).count()
    stockmateriel_list = database.query(StockMateriel).offset(skip).limit(limit).all()
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "data": stockmateriel_list
    }


@app.get("/stockmateriel/search/", response_model=None, tags=["StockMateriel"])
def search_stockmateriel(
    database: Session = Depends(get_db)
) -> list:
    """Search StockMateriel entities by attributes"""
    query = database.query(StockMateriel)


    results = query.all()
    return results


@app.get("/stockmateriel/{stockmateriel_id}/", response_model=None, tags=["StockMateriel"])
async def get_stockmateriel(stockmateriel_id: int, database: Session = Depends(get_db)) -> StockMateriel:
    db_stockmateriel = database.query(StockMateriel).filter(StockMateriel.id == stockmateriel_id).first()
    if db_stockmateriel is None:
        raise HTTPException(status_code=404, detail="StockMateriel not found")

    response_data = {
        "stockmateriel": db_stockmateriel,
}
    return response_data



@app.post("/stockmateriel/", response_model=None, tags=["StockMateriel"])
async def create_stockmateriel(stockmateriel_data: StockMaterielCreate, database: Session = Depends(get_db)) -> StockMateriel:

    if stockmateriel_data.materiel is not None:
        db_materiel = database.query(Materiel).filter(Materiel.id == stockmateriel_data.materiel).first()
        if not db_materiel:
            raise HTTPException(status_code=400, detail="Materiel not found")
    else:
        raise HTTPException(status_code=400, detail="Materiel ID is required")

    db_stockmateriel = StockMateriel(
        quantiteEnPanne=stockmateriel_data.quantiteEnPanne,        quantiteTotale=stockmateriel_data.quantiteTotale,        dateMaj=stockmateriel_data.dateMaj,        materiel_id=stockmateriel_data.materiel        )

    database.add(db_stockmateriel)
    database.commit()
    database.refresh(db_stockmateriel)




    return db_stockmateriel


@app.post("/stockmateriel/bulk/", response_model=None, tags=["StockMateriel"])
async def bulk_create_stockmateriel(items: list[StockMaterielCreate], database: Session = Depends(get_db)) -> dict:
    """Create multiple StockMateriel entities at once"""
    created_items = []
    errors = []

    for idx, item_data in enumerate(items):
        try:
            # Basic validation for each item
            if not item_data.materiel:
                raise ValueError("Materiel ID is required")

            db_stockmateriel = StockMateriel(
                quantiteEnPanne=item_data.quantiteEnPanne,                quantiteTotale=item_data.quantiteTotale,                dateMaj=item_data.dateMaj,                materiel_id=item_data.materiel            )
            database.add(db_stockmateriel)
            database.flush()  # Get ID without committing
            created_items.append(db_stockmateriel.id)
        except Exception as e:
            errors.append({"index": idx, "error": str(e)})

    if errors:
        database.rollback()
        raise HTTPException(status_code=400, detail={"message": "Bulk creation failed", "errors": errors})

    database.commit()
    return {
        "created_count": len(created_items),
        "created_ids": created_items,
        "message": f"Successfully created {len(created_items)} StockMateriel entities"
    }


@app.delete("/stockmateriel/bulk/", response_model=None, tags=["StockMateriel"])
async def bulk_delete_stockmateriel(ids: list[int], database: Session = Depends(get_db)) -> dict:
    """Delete multiple StockMateriel entities at once"""
    deleted_count = 0
    not_found = []

    for item_id in ids:
        db_stockmateriel = database.query(StockMateriel).filter(StockMateriel.id == item_id).first()
        if db_stockmateriel:
            database.delete(db_stockmateriel)
            deleted_count += 1
        else:
            not_found.append(item_id)

    database.commit()

    return {
        "deleted_count": deleted_count,
        "not_found": not_found,
        "message": f"Successfully deleted {deleted_count} StockMateriel entities"
    }

@app.put("/stockmateriel/{stockmateriel_id}/", response_model=None, tags=["StockMateriel"])
async def update_stockmateriel(stockmateriel_id: int, stockmateriel_data: StockMaterielCreate, database: Session = Depends(get_db)) -> StockMateriel:
    db_stockmateriel = database.query(StockMateriel).filter(StockMateriel.id == stockmateriel_id).first()
    if db_stockmateriel is None:
        raise HTTPException(status_code=404, detail="StockMateriel not found")

    setattr(db_stockmateriel, 'quantiteEnPanne', stockmateriel_data.quantiteEnPanne)
    setattr(db_stockmateriel, 'quantiteTotale', stockmateriel_data.quantiteTotale)
    setattr(db_stockmateriel, 'dateMaj', stockmateriel_data.dateMaj)
    if stockmateriel_data.materiel is not None:
        db_materiel = database.query(Materiel).filter(Materiel.id == stockmateriel_data.materiel).first()
        if not db_materiel:
            raise HTTPException(status_code=400, detail="Materiel not found")
        setattr(db_stockmateriel, 'materiel_id', stockmateriel_data.materiel)
    database.commit()
    database.refresh(db_stockmateriel)

    return db_stockmateriel


@app.delete("/stockmateriel/{stockmateriel_id}/", response_model=None, tags=["StockMateriel"])
async def delete_stockmateriel(stockmateriel_id: int, database: Session = Depends(get_db)):
    db_stockmateriel = database.query(StockMateriel).filter(StockMateriel.id == stockmateriel_id).first()
    if db_stockmateriel is None:
        raise HTTPException(status_code=404, detail="StockMateriel not found")
    database.delete(db_stockmateriel)
    database.commit()
    return db_stockmateriel



############################################
#   StockMateriel Method Endpoints
############################################




@app.post("/stockmateriel/methods/getQuantiteDisponible/", response_model=None, tags=["StockMateriel Methods"])
async def stockmateriel_getQuantiteDisponible(
    database: Session = Depends(get_db)
):
    """
    Execute the getQuantiteDisponible class method on StockMateriel.
    This method operates on all StockMateriel entities or performs class-level operations.
    """
    try:
        # Capture stdout to include print outputs in the response
        import io
        import sys
        captured_output = io.StringIO()
        sys.stdout = captured_output


        # Method body not defined
        result = None

        # Restore stdout
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()

        # Handle result serialization
        if hasattr(result, '__iter__') and not isinstance(result, (str, dict)):
            # It's a list of entities
            result_data = []
            for item in result:
                if hasattr(item, '__dict__'):
                    item_dict = {k: v for k, v in item.__dict__.items() if not k.startswith('_')}
                    result_data.append(item_dict)
                else:
                    result_data.append(str(item))
            result = result_data
        elif hasattr(result, '__dict__'):
            result = {k: v for k, v in result.__dict__.items() if not k.startswith('_')}

        return {
            "class": "StockMateriel",
            "method": "getQuantiteDisponible",
            "status": "executed",
            "result": result,
            "output": output if output else None
        }
    except Exception as e:
        sys.stdout = sys.__stdout__
        raise HTTPException(status_code=500, detail=f"Method execution failed: {str(e)}")




############################################
#
#   Materiel functions
#
############################################

@app.get("/materiel/", response_model=None, tags=["Materiel"])
def get_all_materiel(detailed: bool = False, database: Session = Depends(get_db)) -> list:
    from sqlalchemy.orm import joinedload

    # Use detailed=true to get entities with eagerly loaded relationships (for tables with lookup columns)
    if detailed:
        # Eagerly load all relationships to avoid N+1 queries
        query = database.query(Materiel)
        query = query.options(joinedload(Materiel.lignereservation_2))
        materiel_list = query.all()

        # Serialize with relationships included
        result = []
        for materiel_item in materiel_list:
            item_dict = materiel_item.__dict__.copy()
            item_dict.pop('_sa_instance_state', None)

            # Add many-to-one relationships (foreign keys for lookup columns)
            if materiel_item.lignereservation_2:
                related_obj = materiel_item.lignereservation_2
                related_dict = related_obj.__dict__.copy()
                related_dict.pop('_sa_instance_state', None)
                item_dict['lignereservation_2'] = related_dict
            else:
                item_dict['lignereservation_2'] = None

            # Add many-to-many and one-to-many relationship objects (full details)
            stockmateriel_list = database.query(StockMateriel).filter(StockMateriel.materiel_id == materiel_item.id).all()
            item_dict['stockmateriel'] = []
            for stockmateriel_obj in stockmateriel_list:
                stockmateriel_dict = stockmateriel_obj.__dict__.copy()
                stockmateriel_dict.pop('_sa_instance_state', None)
                item_dict['stockmateriel'].append(stockmateriel_dict)

            result.append(item_dict)
        return result
    else:
        # Default: return flat entities (faster for charts/widgets without lookup columns)
        return database.query(Materiel).all()


@app.get("/materiel/count/", response_model=None, tags=["Materiel"])
def get_count_materiel(database: Session = Depends(get_db)) -> dict:
    """Get the total count of Materiel entities"""
    count = database.query(Materiel).count()
    return {"count": count}


@app.get("/materiel/paginated/", response_model=None, tags=["Materiel"])
def get_paginated_materiel(skip: int = 0, limit: int = 100, detailed: bool = False, database: Session = Depends(get_db)) -> dict:
    """Get paginated list of Materiel entities"""
    total = database.query(Materiel).count()
    materiel_list = database.query(Materiel).offset(skip).limit(limit).all()
    # By default, return flat entities (for charts/widgets)
    # Use detailed=true to get entities with relationships
    if not detailed:
        return {
            "total": total,
            "skip": skip,
            "limit": limit,
            "data": materiel_list
        }

    result = []
    for materiel_item in materiel_list:
        stockmateriel_ids = database.query(StockMateriel.id).filter(StockMateriel.materiel_id == materiel_item.id).all()
        item_data = {
            "materiel": materiel_item,
            "stockmateriel_ids": [x[0] for x in stockmateriel_ids]        }
        result.append(item_data)
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "data": result
    }


@app.get("/materiel/search/", response_model=None, tags=["Materiel"])
def search_materiel(
    database: Session = Depends(get_db)
) -> list:
    """Search Materiel entities by attributes"""
    query = database.query(Materiel)


    results = query.all()
    return results


@app.get("/materiel/{materiel_id}/", response_model=None, tags=["Materiel"])
async def get_materiel(materiel_id: int, database: Session = Depends(get_db)) -> Materiel:
    db_materiel = database.query(Materiel).filter(Materiel.id == materiel_id).first()
    if db_materiel is None:
        raise HTTPException(status_code=404, detail="Materiel not found")

    stockmateriel_ids = database.query(StockMateriel.id).filter(StockMateriel.materiel_id == db_materiel.id).all()
    response_data = {
        "materiel": db_materiel,
        "stockmateriel_ids": [x[0] for x in stockmateriel_ids]}
    return response_data



@app.post("/materiel/", response_model=None, tags=["Materiel"])
async def create_materiel(materiel_data: MaterielCreate, database: Session = Depends(get_db)) -> Materiel:


    db_materiel = Materiel(
        nom=materiel_data.nom,        description=materiel_data.description,        id=materiel_data.id,        prixUnitaire=materiel_data.prixUnitaire,        quantiteMinimale=materiel_data.quantiteMinimale        )

    database.add(db_materiel)
    database.commit()
    database.refresh(db_materiel)

    if materiel_data.stockmateriel:
        # Validate that all StockMateriel IDs exist
        for stockmateriel_id in materiel_data.stockmateriel:
            db_stockmateriel = database.query(StockMateriel).filter(StockMateriel.id == stockmateriel_id).first()
            if not db_stockmateriel:
                raise HTTPException(status_code=400, detail=f"StockMateriel with id {stockmateriel_id} not found")

        # Update the related entities with the new foreign key
        database.query(StockMateriel).filter(StockMateriel.id.in_(materiel_data.stockmateriel)).update(
            {StockMateriel.materiel_id: db_materiel.id}, synchronize_session=False
        )
        database.commit()



    stockmateriel_ids = database.query(StockMateriel.id).filter(StockMateriel.materiel_id == db_materiel.id).all()
    response_data = {
        "materiel": db_materiel,
        "stockmateriel_ids": [x[0] for x in stockmateriel_ids]    }
    return response_data


@app.post("/materiel/bulk/", response_model=None, tags=["Materiel"])
async def bulk_create_materiel(items: list[MaterielCreate], database: Session = Depends(get_db)) -> dict:
    """Create multiple Materiel entities at once"""
    created_items = []
    errors = []

    for idx, item_data in enumerate(items):
        try:
            # Basic validation for each item

            db_materiel = Materiel(
                nom=item_data.nom,                description=item_data.description,                id=item_data.id,                prixUnitaire=item_data.prixUnitaire,                quantiteMinimale=item_data.quantiteMinimale            )
            database.add(db_materiel)
            database.flush()  # Get ID without committing
            created_items.append(db_materiel.id)
        except Exception as e:
            errors.append({"index": idx, "error": str(e)})

    if errors:
        database.rollback()
        raise HTTPException(status_code=400, detail={"message": "Bulk creation failed", "errors": errors})

    database.commit()
    return {
        "created_count": len(created_items),
        "created_ids": created_items,
        "message": f"Successfully created {len(created_items)} Materiel entities"
    }


@app.delete("/materiel/bulk/", response_model=None, tags=["Materiel"])
async def bulk_delete_materiel(ids: list[int], database: Session = Depends(get_db)) -> dict:
    """Delete multiple Materiel entities at once"""
    deleted_count = 0
    not_found = []

    for item_id in ids:
        db_materiel = database.query(Materiel).filter(Materiel.id == item_id).first()
        if db_materiel:
            database.delete(db_materiel)
            deleted_count += 1
        else:
            not_found.append(item_id)

    database.commit()

    return {
        "deleted_count": deleted_count,
        "not_found": not_found,
        "message": f"Successfully deleted {deleted_count} Materiel entities"
    }

@app.put("/materiel/{materiel_id}/", response_model=None, tags=["Materiel"])
async def update_materiel(materiel_id: int, materiel_data: MaterielCreate, database: Session = Depends(get_db)) -> Materiel:
    db_materiel = database.query(Materiel).filter(Materiel.id == materiel_id).first()
    if db_materiel is None:
        raise HTTPException(status_code=404, detail="Materiel not found")

    setattr(db_materiel, 'nom', materiel_data.nom)
    setattr(db_materiel, 'description', materiel_data.description)
    setattr(db_materiel, 'id', materiel_data.id)
    setattr(db_materiel, 'prixUnitaire', materiel_data.prixUnitaire)
    setattr(db_materiel, 'quantiteMinimale', materiel_data.quantiteMinimale)
    if materiel_data.stockmateriel is not None:
        # Clear all existing relationships (set foreign key to NULL)
        database.query(StockMateriel).filter(StockMateriel.materiel_id == db_materiel.id).update(
            {StockMateriel.materiel_id: None}, synchronize_session=False
        )

        # Set new relationships if list is not empty
        if materiel_data.stockmateriel:
            # Validate that all IDs exist
            for stockmateriel_id in materiel_data.stockmateriel:
                db_stockmateriel = database.query(StockMateriel).filter(StockMateriel.id == stockmateriel_id).first()
                if not db_stockmateriel:
                    raise HTTPException(status_code=400, detail=f"StockMateriel with id {stockmateriel_id} not found")

            # Update the related entities with the new foreign key
            database.query(StockMateriel).filter(StockMateriel.id.in_(materiel_data.stockmateriel)).update(
                {StockMateriel.materiel_id: db_materiel.id}, synchronize_session=False
            )
    database.commit()
    database.refresh(db_materiel)

    stockmateriel_ids = database.query(StockMateriel.id).filter(StockMateriel.materiel_id == db_materiel.id).all()
    response_data = {
        "materiel": db_materiel,
        "stockmateriel_ids": [x[0] for x in stockmateriel_ids]    }
    return response_data


@app.delete("/materiel/{materiel_id}/", response_model=None, tags=["Materiel"])
async def delete_materiel(materiel_id: int, database: Session = Depends(get_db)):
    db_materiel = database.query(Materiel).filter(Materiel.id == materiel_id).first()
    if db_materiel is None:
        raise HTTPException(status_code=404, detail="Materiel not found")
    database.delete(db_materiel)
    database.commit()
    return db_materiel



############################################
#   Materiel Method Endpoints
############################################




@app.post("/materiel/methods/getStockDisponible/", response_model=None, tags=["Materiel Methods"])
async def materiel_getStockDisponible(
    database: Session = Depends(get_db)
):
    """
    Execute the getStockDisponible class method on Materiel.
    This method operates on all Materiel entities or performs class-level operations.
    """
    try:
        # Capture stdout to include print outputs in the response
        import io
        import sys
        captured_output = io.StringIO()
        sys.stdout = captured_output


        # Method body not defined
        result = None

        # Restore stdout
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()

        # Handle result serialization
        if hasattr(result, '__iter__') and not isinstance(result, (str, dict)):
            # It's a list of entities
            result_data = []
            for item in result:
                if hasattr(item, '__dict__'):
                    item_dict = {k: v for k, v in item.__dict__.items() if not k.startswith('_')}
                    result_data.append(item_dict)
                else:
                    result_data.append(str(item))
            result = result_data
        elif hasattr(result, '__dict__'):
            result = {k: v for k, v in result.__dict__.items() if not k.startswith('_')}

        return {
            "class": "Materiel",
            "method": "getStockDisponible",
            "status": "executed",
            "result": result,
            "output": output if output else None
        }
    except Exception as e:
        sys.stdout = sys.__stdout__
        raise HTTPException(status_code=500, detail=f"Method execution failed: {str(e)}")




############################################
#
#   Evenement functions
#
############################################

@app.get("/evenement/", response_model=None, tags=["Evenement"])
def get_all_evenement(detailed: bool = False, database: Session = Depends(get_db)) -> list:
    from sqlalchemy.orm import joinedload

    # Use detailed=true to get entities with eagerly loaded relationships (for tables with lookup columns)
    if detailed:
        # Eagerly load all relationships to avoid N+1 queries
        query = database.query(Evenement)
        query = query.options(joinedload(Evenement.reservation_2))
        evenement_list = query.all()

        # Serialize with relationships included
        result = []
        for evenement_item in evenement_list:
            item_dict = evenement_item.__dict__.copy()
            item_dict.pop('_sa_instance_state', None)

            # Add many-to-one relationships (foreign keys for lookup columns)
            if evenement_item.reservation_2:
                related_obj = evenement_item.reservation_2
                related_dict = related_obj.__dict__.copy()
                related_dict.pop('_sa_instance_state', None)
                item_dict['reservation_2'] = related_dict
            else:
                item_dict['reservation_2'] = None


            result.append(item_dict)
        return result
    else:
        # Default: return flat entities (faster for charts/widgets without lookup columns)
        return database.query(Evenement).all()


@app.get("/evenement/count/", response_model=None, tags=["Evenement"])
def get_count_evenement(database: Session = Depends(get_db)) -> dict:
    """Get the total count of Evenement entities"""
    count = database.query(Evenement).count()
    return {"count": count}


@app.get("/evenement/paginated/", response_model=None, tags=["Evenement"])
def get_paginated_evenement(skip: int = 0, limit: int = 100, detailed: bool = False, database: Session = Depends(get_db)) -> dict:
    """Get paginated list of Evenement entities"""
    total = database.query(Evenement).count()
    evenement_list = database.query(Evenement).offset(skip).limit(limit).all()
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "data": evenement_list
    }


@app.get("/evenement/search/", response_model=None, tags=["Evenement"])
def search_evenement(
    database: Session = Depends(get_db)
) -> list:
    """Search Evenement entities by attributes"""
    query = database.query(Evenement)


    results = query.all()
    return results


@app.get("/evenement/{evenement_id}/", response_model=None, tags=["Evenement"])
async def get_evenement(evenement_id: int, database: Session = Depends(get_db)) -> Evenement:
    db_evenement = database.query(Evenement).filter(Evenement.id == evenement_id).first()
    if db_evenement is None:
        raise HTTPException(status_code=404, detail="Evenement not found")

    response_data = {
        "evenement": db_evenement,
}
    return response_data



@app.post("/evenement/", response_model=None, tags=["Evenement"])
async def create_evenement(evenement_data: EvenementCreate, database: Session = Depends(get_db)) -> Evenement:

    if evenement_data.reservation_2 is not None:
        db_reservation_2 = database.query(Reservation).filter(Reservation.id == evenement_data.reservation_2).first()
        if not db_reservation_2:
            raise HTTPException(status_code=400, detail="Reservation not found")
    else:
        raise HTTPException(status_code=400, detail="Reservation ID is required")

    db_evenement = Evenement(
        dateFin=evenement_data.dateFin,        description=evenement_data.description,        dateDebut=evenement_data.dateDebut,        id=evenement_data.id,        nom=evenement_data.nom,        nbParticipantsPrevus=evenement_data.nbParticipantsPrevus,        reservation_2_id=evenement_data.reservation_2        )

    database.add(db_evenement)
    database.commit()
    database.refresh(db_evenement)




    return db_evenement


@app.post("/evenement/bulk/", response_model=None, tags=["Evenement"])
async def bulk_create_evenement(items: list[EvenementCreate], database: Session = Depends(get_db)) -> dict:
    """Create multiple Evenement entities at once"""
    created_items = []
    errors = []

    for idx, item_data in enumerate(items):
        try:
            # Basic validation for each item
            if not item_data.reservation_2:
                raise ValueError("Reservation ID is required")

            db_evenement = Evenement(
                dateFin=item_data.dateFin,                description=item_data.description,                dateDebut=item_data.dateDebut,                id=item_data.id,                nom=item_data.nom,                nbParticipantsPrevus=item_data.nbParticipantsPrevus,                reservation_2_id=item_data.reservation_2            )
            database.add(db_evenement)
            database.flush()  # Get ID without committing
            created_items.append(db_evenement.id)
        except Exception as e:
            errors.append({"index": idx, "error": str(e)})

    if errors:
        database.rollback()
        raise HTTPException(status_code=400, detail={"message": "Bulk creation failed", "errors": errors})

    database.commit()
    return {
        "created_count": len(created_items),
        "created_ids": created_items,
        "message": f"Successfully created {len(created_items)} Evenement entities"
    }


@app.delete("/evenement/bulk/", response_model=None, tags=["Evenement"])
async def bulk_delete_evenement(ids: list[int], database: Session = Depends(get_db)) -> dict:
    """Delete multiple Evenement entities at once"""
    deleted_count = 0
    not_found = []

    for item_id in ids:
        db_evenement = database.query(Evenement).filter(Evenement.id == item_id).first()
        if db_evenement:
            database.delete(db_evenement)
            deleted_count += 1
        else:
            not_found.append(item_id)

    database.commit()

    return {
        "deleted_count": deleted_count,
        "not_found": not_found,
        "message": f"Successfully deleted {deleted_count} Evenement entities"
    }

@app.put("/evenement/{evenement_id}/", response_model=None, tags=["Evenement"])
async def update_evenement(evenement_id: int, evenement_data: EvenementCreate, database: Session = Depends(get_db)) -> Evenement:
    db_evenement = database.query(Evenement).filter(Evenement.id == evenement_id).first()
    if db_evenement is None:
        raise HTTPException(status_code=404, detail="Evenement not found")

    setattr(db_evenement, 'dateFin', evenement_data.dateFin)
    setattr(db_evenement, 'description', evenement_data.description)
    setattr(db_evenement, 'dateDebut', evenement_data.dateDebut)
    setattr(db_evenement, 'id', evenement_data.id)
    setattr(db_evenement, 'nom', evenement_data.nom)
    setattr(db_evenement, 'nbParticipantsPrevus', evenement_data.nbParticipantsPrevus)
    if evenement_data.reservation_2 is not None:
        db_reservation_2 = database.query(Reservation).filter(Reservation.id == evenement_data.reservation_2).first()
        if not db_reservation_2:
            raise HTTPException(status_code=400, detail="Reservation not found")
        setattr(db_evenement, 'reservation_2_id', evenement_data.reservation_2)
    database.commit()
    database.refresh(db_evenement)

    return db_evenement


@app.delete("/evenement/{evenement_id}/", response_model=None, tags=["Evenement"])
async def delete_evenement(evenement_id: int, database: Session = Depends(get_db)):
    db_evenement = database.query(Evenement).filter(Evenement.id == evenement_id).first()
    if db_evenement is None:
        raise HTTPException(status_code=404, detail="Evenement not found")
    database.delete(db_evenement)
    database.commit()
    return db_evenement



############################################
#   Evenement Method Endpoints
############################################




@app.post("/evenement/methods/aCommencer/", response_model=None, tags=["Evenement Methods"])
async def evenement_aCommencer(
    database: Session = Depends(get_db)
):
    """
    Execute the aCommencer class method on Evenement.
    This method operates on all Evenement entities or performs class-level operations.
    """
    try:
        # Capture stdout to include print outputs in the response
        import io
        import sys
        captured_output = io.StringIO()
        sys.stdout = captured_output


        # Method body not defined
        result = None

        # Restore stdout
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()

        # Handle result serialization
        if hasattr(result, '__iter__') and not isinstance(result, (str, dict)):
            # It's a list of entities
            result_data = []
            for item in result:
                if hasattr(item, '__dict__'):
                    item_dict = {k: v for k, v in item.__dict__.items() if not k.startswith('_')}
                    result_data.append(item_dict)
                else:
                    result_data.append(str(item))
            result = result_data
        elif hasattr(result, '__dict__'):
            result = {k: v for k, v in result.__dict__.items() if not k.startswith('_')}

        return {
            "class": "Evenement",
            "method": "aCommencer",
            "status": "executed",
            "result": result,
            "output": output if output else None
        }
    except Exception as e:
        sys.stdout = sys.__stdout__
        raise HTTPException(status_code=500, detail=f"Method execution failed: {str(e)}")




############################################
#
#   LigneReservation functions
#
############################################

@app.get("/lignereservation/", response_model=None, tags=["LigneReservation"])
def get_all_lignereservation(detailed: bool = False, database: Session = Depends(get_db)) -> list:
    from sqlalchemy.orm import joinedload

    # Use detailed=true to get entities with eagerly loaded relationships (for tables with lookup columns)
    if detailed:
        # Eagerly load all relationships to avoid N+1 queries
        query = database.query(LigneReservation)
        query = query.options(joinedload(LigneReservation.materiel_1))
        query = query.options(joinedload(LigneReservation.reservation_1))
        lignereservation_list = query.all()

        # Serialize with relationships included
        result = []
        for lignereservation_item in lignereservation_list:
            item_dict = lignereservation_item.__dict__.copy()
            item_dict.pop('_sa_instance_state', None)

            # Add many-to-one relationships (foreign keys for lookup columns)
            if lignereservation_item.materiel_1:
                related_obj = lignereservation_item.materiel_1
                related_dict = related_obj.__dict__.copy()
                related_dict.pop('_sa_instance_state', None)
                item_dict['materiel_1'] = related_dict
            else:
                item_dict['materiel_1'] = None
            if lignereservation_item.reservation_1:
                related_obj = lignereservation_item.reservation_1
                related_dict = related_obj.__dict__.copy()
                related_dict.pop('_sa_instance_state', None)
                item_dict['reservation_1'] = related_dict
            else:
                item_dict['reservation_1'] = None

            # Add many-to-many and one-to-many relationship objects (full details)
            prestation_list = database.query(Prestation).filter(Prestation.lignereservation_1_id == lignereservation_item.id).all()
            item_dict['prestation'] = []
            for prestation_obj in prestation_list:
                prestation_dict = prestation_obj.__dict__.copy()
                prestation_dict.pop('_sa_instance_state', None)
                item_dict['prestation'].append(prestation_dict)

            result.append(item_dict)
        return result
    else:
        # Default: return flat entities (faster for charts/widgets without lookup columns)
        return database.query(LigneReservation).all()


@app.get("/lignereservation/count/", response_model=None, tags=["LigneReservation"])
def get_count_lignereservation(database: Session = Depends(get_db)) -> dict:
    """Get the total count of LigneReservation entities"""
    count = database.query(LigneReservation).count()
    return {"count": count}


@app.get("/lignereservation/paginated/", response_model=None, tags=["LigneReservation"])
def get_paginated_lignereservation(skip: int = 0, limit: int = 100, detailed: bool = False, database: Session = Depends(get_db)) -> dict:
    """Get paginated list of LigneReservation entities"""
    total = database.query(LigneReservation).count()
    lignereservation_list = database.query(LigneReservation).offset(skip).limit(limit).all()
    # By default, return flat entities (for charts/widgets)
    # Use detailed=true to get entities with relationships
    if not detailed:
        return {
            "total": total,
            "skip": skip,
            "limit": limit,
            "data": lignereservation_list
        }

    result = []
    for lignereservation_item in lignereservation_list:
        prestation_ids = database.query(Prestation.id).filter(Prestation.lignereservation_1_id == lignereservation_item.id).all()
        item_data = {
            "lignereservation": lignereservation_item,
            "prestation_ids": [x[0] for x in prestation_ids]        }
        result.append(item_data)
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "data": result
    }


@app.get("/lignereservation/search/", response_model=None, tags=["LigneReservation"])
def search_lignereservation(
    database: Session = Depends(get_db)
) -> list:
    """Search LigneReservation entities by attributes"""
    query = database.query(LigneReservation)


    results = query.all()
    return results


@app.get("/lignereservation/{lignereservation_id}/", response_model=None, tags=["LigneReservation"])
async def get_lignereservation(lignereservation_id: int, database: Session = Depends(get_db)) -> LigneReservation:
    db_lignereservation = database.query(LigneReservation).filter(LigneReservation.id == lignereservation_id).first()
    if db_lignereservation is None:
        raise HTTPException(status_code=404, detail="LigneReservation not found")

    prestation_ids = database.query(Prestation.id).filter(Prestation.lignereservation_1_id == db_lignereservation.id).all()
    response_data = {
        "lignereservation": db_lignereservation,
        "prestation_ids": [x[0] for x in prestation_ids]}
    return response_data



@app.post("/lignereservation/", response_model=None, tags=["LigneReservation"])
async def create_lignereservation(lignereservation_data: LigneReservationCreate, database: Session = Depends(get_db)) -> LigneReservation:

    if lignereservation_data.materiel_1 is not None:
        db_materiel_1 = database.query(Materiel).filter(Materiel.id == lignereservation_data.materiel_1).first()
        if not db_materiel_1:
            raise HTTPException(status_code=400, detail="Materiel not found")
    else:
        raise HTTPException(status_code=400, detail="Materiel ID is required")
    if lignereservation_data.reservation_1 is not None:
        db_reservation_1 = database.query(Reservation).filter(Reservation.id == lignereservation_data.reservation_1).first()
        if not db_reservation_1:
            raise HTTPException(status_code=400, detail="Reservation not found")
    else:
        raise HTTPException(status_code=400, detail="Reservation ID is required")

    db_lignereservation = LigneReservation(
        dateDebut=lignereservation_data.dateDebut,        quantite=lignereservation_data.quantite,        sousTotal=lignereservation_data.sousTotal,        dateFin=lignereservation_data.dateFin,        materiel_1_id=lignereservation_data.materiel_1,        reservation_1_id=lignereservation_data.reservation_1        )

    database.add(db_lignereservation)
    database.commit()
    database.refresh(db_lignereservation)

    if lignereservation_data.prestation:
        # Validate that all Prestation IDs exist
        for prestation_id in lignereservation_data.prestation:
            db_prestation = database.query(Prestation).filter(Prestation.id == prestation_id).first()
            if not db_prestation:
                raise HTTPException(status_code=400, detail=f"Prestation with id {prestation_id} not found")

        # Update the related entities with the new foreign key
        database.query(Prestation).filter(Prestation.id.in_(lignereservation_data.prestation)).update(
            {Prestation.lignereservation_1_id: db_lignereservation.id}, synchronize_session=False
        )
        database.commit()



    prestation_ids = database.query(Prestation.id).filter(Prestation.lignereservation_1_id == db_lignereservation.id).all()
    response_data = {
        "lignereservation": db_lignereservation,
        "prestation_ids": [x[0] for x in prestation_ids]    }
    return response_data


@app.post("/lignereservation/bulk/", response_model=None, tags=["LigneReservation"])
async def bulk_create_lignereservation(items: list[LigneReservationCreate], database: Session = Depends(get_db)) -> dict:
    """Create multiple LigneReservation entities at once"""
    created_items = []
    errors = []

    for idx, item_data in enumerate(items):
        try:
            # Basic validation for each item
            if not item_data.materiel_1:
                raise ValueError("Materiel ID is required")
            if not item_data.reservation_1:
                raise ValueError("Reservation ID is required")

            db_lignereservation = LigneReservation(
                dateDebut=item_data.dateDebut,                quantite=item_data.quantite,                sousTotal=item_data.sousTotal,                dateFin=item_data.dateFin,                materiel_1_id=item_data.materiel_1,                reservation_1_id=item_data.reservation_1            )
            database.add(db_lignereservation)
            database.flush()  # Get ID without committing
            created_items.append(db_lignereservation.id)
        except Exception as e:
            errors.append({"index": idx, "error": str(e)})

    if errors:
        database.rollback()
        raise HTTPException(status_code=400, detail={"message": "Bulk creation failed", "errors": errors})

    database.commit()
    return {
        "created_count": len(created_items),
        "created_ids": created_items,
        "message": f"Successfully created {len(created_items)} LigneReservation entities"
    }


@app.delete("/lignereservation/bulk/", response_model=None, tags=["LigneReservation"])
async def bulk_delete_lignereservation(ids: list[int], database: Session = Depends(get_db)) -> dict:
    """Delete multiple LigneReservation entities at once"""
    deleted_count = 0
    not_found = []

    for item_id in ids:
        db_lignereservation = database.query(LigneReservation).filter(LigneReservation.id == item_id).first()
        if db_lignereservation:
            database.delete(db_lignereservation)
            deleted_count += 1
        else:
            not_found.append(item_id)

    database.commit()

    return {
        "deleted_count": deleted_count,
        "not_found": not_found,
        "message": f"Successfully deleted {deleted_count} LigneReservation entities"
    }

@app.put("/lignereservation/{lignereservation_id}/", response_model=None, tags=["LigneReservation"])
async def update_lignereservation(lignereservation_id: int, lignereservation_data: LigneReservationCreate, database: Session = Depends(get_db)) -> LigneReservation:
    db_lignereservation = database.query(LigneReservation).filter(LigneReservation.id == lignereservation_id).first()
    if db_lignereservation is None:
        raise HTTPException(status_code=404, detail="LigneReservation not found")

    setattr(db_lignereservation, 'dateDebut', lignereservation_data.dateDebut)
    setattr(db_lignereservation, 'quantite', lignereservation_data.quantite)
    setattr(db_lignereservation, 'sousTotal', lignereservation_data.sousTotal)
    setattr(db_lignereservation, 'dateFin', lignereservation_data.dateFin)
    if lignereservation_data.materiel_1 is not None:
        db_materiel_1 = database.query(Materiel).filter(Materiel.id == lignereservation_data.materiel_1).first()
        if not db_materiel_1:
            raise HTTPException(status_code=400, detail="Materiel not found")
        setattr(db_lignereservation, 'materiel_1_id', lignereservation_data.materiel_1)
    if lignereservation_data.reservation_1 is not None:
        db_reservation_1 = database.query(Reservation).filter(Reservation.id == lignereservation_data.reservation_1).first()
        if not db_reservation_1:
            raise HTTPException(status_code=400, detail="Reservation not found")
        setattr(db_lignereservation, 'reservation_1_id', lignereservation_data.reservation_1)
    if lignereservation_data.prestation is not None:
        # Clear all existing relationships (set foreign key to NULL)
        database.query(Prestation).filter(Prestation.lignereservation_1_id == db_lignereservation.id).update(
            {Prestation.lignereservation_1_id: None}, synchronize_session=False
        )

        # Set new relationships if list is not empty
        if lignereservation_data.prestation:
            # Validate that all IDs exist
            for prestation_id in lignereservation_data.prestation:
                db_prestation = database.query(Prestation).filter(Prestation.id == prestation_id).first()
                if not db_prestation:
                    raise HTTPException(status_code=400, detail=f"Prestation with id {prestation_id} not found")

            # Update the related entities with the new foreign key
            database.query(Prestation).filter(Prestation.id.in_(lignereservation_data.prestation)).update(
                {Prestation.lignereservation_1_id: db_lignereservation.id}, synchronize_session=False
            )
    database.commit()
    database.refresh(db_lignereservation)

    prestation_ids = database.query(Prestation.id).filter(Prestation.lignereservation_1_id == db_lignereservation.id).all()
    response_data = {
        "lignereservation": db_lignereservation,
        "prestation_ids": [x[0] for x in prestation_ids]    }
    return response_data


@app.delete("/lignereservation/{lignereservation_id}/", response_model=None, tags=["LigneReservation"])
async def delete_lignereservation(lignereservation_id: int, database: Session = Depends(get_db)):
    db_lignereservation = database.query(LigneReservation).filter(LigneReservation.id == lignereservation_id).first()
    if db_lignereservation is None:
        raise HTTPException(status_code=404, detail="LigneReservation not found")
    database.delete(db_lignereservation)
    database.commit()
    return db_lignereservation



############################################
#   LigneReservation Method Endpoints
############################################




@app.post("/lignereservation/methods/verifierDisponibilite/", response_model=None, tags=["LigneReservation Methods"])
async def lignereservation_verifierDisponibilite(
    database: Session = Depends(get_db)
):
    """
    Execute the verifierDisponibilite class method on LigneReservation.
    This method operates on all LigneReservation entities or performs class-level operations.
    """
    try:
        # Capture stdout to include print outputs in the response
        import io
        import sys
        captured_output = io.StringIO()
        sys.stdout = captured_output


        # Method body not defined
        result = None

        # Restore stdout
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()

        # Handle result serialization
        if hasattr(result, '__iter__') and not isinstance(result, (str, dict)):
            # It's a list of entities
            result_data = []
            for item in result:
                if hasattr(item, '__dict__'):
                    item_dict = {k: v for k, v in item.__dict__.items() if not k.startswith('_')}
                    result_data.append(item_dict)
                else:
                    result_data.append(str(item))
            result = result_data
        elif hasattr(result, '__dict__'):
            result = {k: v for k, v in result.__dict__.items() if not k.startswith('_')}

        return {
            "class": "LigneReservation",
            "method": "verifierDisponibilite",
            "status": "executed",
            "result": result,
            "output": output if output else None
        }
    except Exception as e:
        sys.stdout = sys.__stdout__
        raise HTTPException(status_code=500, detail=f"Method execution failed: {str(e)}")






@app.post("/lignereservation/methods/calculerSousTotal/", response_model=None, tags=["LigneReservation Methods"])
async def lignereservation_calculerSousTotal(
    database: Session = Depends(get_db)
):
    """
    Execute the calculerSousTotal class method on LigneReservation.
    This method operates on all LigneReservation entities or performs class-level operations.
    """
    try:
        # Capture stdout to include print outputs in the response
        import io
        import sys
        captured_output = io.StringIO()
        sys.stdout = captured_output


        # Method body not defined
        result = None

        # Restore stdout
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()

        # Handle result serialization
        if hasattr(result, '__iter__') and not isinstance(result, (str, dict)):
            # It's a list of entities
            result_data = []
            for item in result:
                if hasattr(item, '__dict__'):
                    item_dict = {k: v for k, v in item.__dict__.items() if not k.startswith('_')}
                    result_data.append(item_dict)
                else:
                    result_data.append(str(item))
            result = result_data
        elif hasattr(result, '__dict__'):
            result = {k: v for k, v in result.__dict__.items() if not k.startswith('_')}

        return {
            "class": "LigneReservation",
            "method": "calculerSousTotal",
            "status": "executed",
            "result": result,
            "output": output if output else None
        }
    except Exception as e:
        sys.stdout = sys.__stdout__
        raise HTTPException(status_code=500, detail=f"Method execution failed: {str(e)}")






############################################
# Maintaining the server
############################################
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)



