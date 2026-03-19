import React from "react";
import { Routes, Route, Navigate } from "react-router-dom";
import { TableProvider } from "./contexts/TableContext";
import Centredecongres from "./pages/Centredecongres";
import Stockmateriel from "./pages/Stockmateriel";
import Prestation from "./pages/Prestation";
import Prestationglobale from "./pages/Prestationglobale";
import Prestationdimensionnee from "./pages/Prestationdimensionnee";
import Gestionnaire from "./pages/Gestionnaire";
import Elementcentre from "./pages/Elementcentre";
import Tarif from "./pages/Tarif";
import Reservation from "./pages/Reservation";
import Indisponibilite from "./pages/Indisponibilite";
import Lignereservation from "./pages/Lignereservation";
import Evenement from "./pages/Evenement";
import Materiel from "./pages/Materiel";

function App() {
  return (
    <TableProvider>
      <div className="app-container">
        <main className="app-main">
          <Routes>
            <Route path="/centredecongres" element={<Centredecongres />} />
            <Route path="/stockmateriel" element={<Stockmateriel />} />
            <Route path="/prestation" element={<Prestation />} />
            <Route path="/prestationglobale" element={<Prestationglobale />} />
            <Route path="/prestationdimensionnee" element={<Prestationdimensionnee />} />
            <Route path="/gestionnaire" element={<Gestionnaire />} />
            <Route path="/elementcentre" element={<Elementcentre />} />
            <Route path="/tarif" element={<Tarif />} />
            <Route path="/reservation" element={<Reservation />} />
            <Route path="/indisponibilite" element={<Indisponibilite />} />
            <Route path="/lignereservation" element={<Lignereservation />} />
            <Route path="/evenement" element={<Evenement />} />
            <Route path="/materiel" element={<Materiel />} />
            <Route path="/" element={<Navigate to="/centredecongres" replace />} />
            <Route path="*" element={<Navigate to="/centredecongres" replace />} />
          </Routes>
        </main>
      </div>
    </TableProvider>
  );
}
export default App;
