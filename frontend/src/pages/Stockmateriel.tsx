import React from "react";
import { TableBlock } from "../components/runtime/TableBlock";
import { MethodButton } from "../components/MethodButton";

const Stockmateriel: React.FC = () => {
  return (
    <div id="page-stockmateriel-9">
    <div id="ixit6i" style={{"display": "flex", "height": "100vh", "fontFamily": "Arial, sans-serif", "--chart-color-palette": "default"}}>
      <nav id="ixuzoe" style={{"width": "250px", "background": "linear-gradient(135deg, #4b3c82 0%, #5a3d91 100%)", "color": "white", "padding": "20px", "overflowY": "auto", "display": "flex", "flexDirection": "column", "--chart-color-palette": "default"}}>
        <h2 id="ic570g" style={{"marginTop": "0", "fontSize": "24px", "marginBottom": "30px", "fontWeight": "bold", "--chart-color-palette": "default"}}>{"BESSER"}</h2>
        <div id="i8huti" style={{"display": "flex", "flexDirection": "column", "flex": "1", "--chart-color-palette": "default"}}>
          <a id="iedu1h" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/centredecongres">{"CentreDeCongres"}</a>
          <a id="ig33pj" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/gestionnaire">{"Gestionnaire"}</a>
          <a id="iqg9bi" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/elementcentre">{"ElementCentre"}</a>
          <a id="ivzmvj" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/tarif">{"Tarif"}</a>
          <a id="it7nz5" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/reservation">{"Reservation"}</a>
          <a id="i4qb7y" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/indisponibilite">{"Indisponibilite"}</a>
          <a id="ilvi3i" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/lignereservation">{"LigneReservation"}</a>
          <a id="itg8a9" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/evenement">{"Evenement"}</a>
          <a id="ioxiqs" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/materiel">{"Materiel"}</a>
          <a id="i4fto9" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "rgba(255,255,255,0.2)", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/stockmateriel">{"StockMateriel"}</a>
          <a id="i332rl" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/prestation">{"Prestation"}</a>
          <a id="ic106k" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/prestationglobale">{"PrestationGlobale"}</a>
          <a id="ikepwg" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/prestationdimensionnee">{"PrestationDimensionnee"}</a>
        </div>
        <p id="igimeq" style={{"marginTop": "auto", "paddingTop": "20px", "borderTop": "1px solid rgba(255,255,255,0.2)", "fontSize": "11px", "opacity": "0.8", "textAlign": "center", "--chart-color-palette": "default"}}>{"© 2026 BESSER. All rights reserved."}</p>
      </nav>
      <main id="ikfz1i" style={{"flex": "1", "padding": "40px", "overflowY": "auto", "background": "#f5f5f5", "--chart-color-palette": "default"}}>
        <h1 id="i3r3h3" style={{"marginTop": "0", "color": "#333", "fontSize": "32px", "marginBottom": "10px", "--chart-color-palette": "default"}}>{"StockMateriel"}</h1>
        <p id="iuhzwn" style={{"color": "#666", "marginBottom": "30px", "--chart-color-palette": "default"}}>{"Manage StockMateriel data"}</p>
        <TableBlock id="table-stockmateriel-9" styles={{"width": "100%", "minHeight": "400px", "--chart-color-palette": "default"}} title="StockMateriel List" options={{"showHeader": true, "stripedRows": false, "showPagination": true, "rowsPerPage": 5, "actionButtons": true, "columns": [{"label": "QuantiteTotale", "column_type": "field", "field": "quantiteTotale", "type": "int", "required": true}, {"label": "QuantiteEnPanne", "column_type": "field", "field": "quantiteEnPanne", "type": "int", "required": true}, {"label": "DateMaj", "column_type": "field", "field": "dateMaj", "type": "datetime", "required": true}], "formColumns": [{"column_type": "field", "field": "quantiteTotale", "label": "quantiteTotale", "type": "int", "required": true, "defaultValue": null}, {"column_type": "field", "field": "quantiteEnPanne", "label": "quantiteEnPanne", "type": "int", "required": true, "defaultValue": null}, {"column_type": "field", "field": "dateMaj", "label": "dateMaj", "type": "datetime", "required": true, "defaultValue": null}, {"column_type": "lookup", "path": "materiel", "field": "materiel", "lookup_field": "id", "entity": "Materiel", "type": "str", "required": true}]}} dataBinding={{"entity": "StockMateriel", "endpoint": "/stockmateriel/"}} />
        <div id="iox3jf" style={{"marginTop": "20px", "display": "flex", "gap": "10px", "flexWrap": "wrap", "--chart-color-palette": "default"}}>
          <MethodButton id="i40ahe" className="action-button-component" style={{"display": "inline-flex", "alignItems": "center", "padding": "6px 14px", "background": "linear-gradient(90deg, #2563eb 0%, #1e40af 100%)", "color": "#fff", "textDecoration": "none", "borderRadius": "4px", "fontSize": "13px", "fontWeight": "600", "letterSpacing": "0.01em", "cursor": "pointer", "border": "none", "boxShadow": "0 1px 4px rgba(37,99,235,0.10)", "transition": "background 0.2s", "--chart-color-palette": "default"}} endpoint="/stockmateriel/{stockmateriel_id}/methods/getQuantiteDisponible/" label="+ getQuantiteDisponible" isInstanceMethod={true} instanceSourceTableId="table-stockmateriel-9" />
        </div>
      </main>
    </div>    </div>
  );
};

export default Stockmateriel;
