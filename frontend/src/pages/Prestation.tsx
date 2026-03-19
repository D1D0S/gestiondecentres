import React from "react";
import { TableBlock } from "../components/runtime/TableBlock";
import { MethodButton } from "../components/MethodButton";

const Prestation: React.FC = () => {
  return (
    <div id="page-prestation-10">
    <div id="it7mvk" style={{"display": "flex", "height": "100vh", "fontFamily": "Arial, sans-serif", "--chart-color-palette": "default"}}>
      <nav id="isaj59" style={{"width": "250px", "background": "linear-gradient(135deg, #4b3c82 0%, #5a3d91 100%)", "color": "white", "padding": "20px", "overflowY": "auto", "display": "flex", "flexDirection": "column", "--chart-color-palette": "default"}}>
        <h2 id="i3osr5" style={{"marginTop": "0", "fontSize": "24px", "marginBottom": "30px", "fontWeight": "bold", "--chart-color-palette": "default"}}>{"BESSER"}</h2>
        <div id="ixnciw" style={{"display": "flex", "flexDirection": "column", "flex": "1", "--chart-color-palette": "default"}}>
          <a id="iu23y1" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/centredecongres">{"CentreDeCongres"}</a>
          <a id="iols53" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/gestionnaire">{"Gestionnaire"}</a>
          <a id="isyjsx" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/elementcentre">{"ElementCentre"}</a>
          <a id="ipcg83" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/tarif">{"Tarif"}</a>
          <a id="ivl0qy" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/reservation">{"Reservation"}</a>
          <a id="izj7vv" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/indisponibilite">{"Indisponibilite"}</a>
          <a id="i2okf5" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/lignereservation">{"LigneReservation"}</a>
          <a id="itb1vq" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/evenement">{"Evenement"}</a>
          <a id="ihrnnh" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/materiel">{"Materiel"}</a>
          <a id="i1qk6v" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/stockmateriel">{"StockMateriel"}</a>
          <a id="iwm949" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "rgba(255,255,255,0.2)", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/prestation">{"Prestation"}</a>
          <a id="i9g7fg" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/prestationglobale">{"PrestationGlobale"}</a>
          <a id="isr8wg" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/prestationdimensionnee">{"PrestationDimensionnee"}</a>
        </div>
        <p id="i1pmu6" style={{"marginTop": "auto", "paddingTop": "20px", "borderTop": "1px solid rgba(255,255,255,0.2)", "fontSize": "11px", "opacity": "0.8", "textAlign": "center", "--chart-color-palette": "default"}}>{"© 2026 BESSER. All rights reserved."}</p>
      </nav>
      <main id="isb0b2" style={{"flex": "1", "padding": "40px", "overflowY": "auto", "background": "#f5f5f5", "--chart-color-palette": "default"}}>
        <h1 id="iu56f6" style={{"marginTop": "0", "color": "#333", "fontSize": "32px", "marginBottom": "10px", "--chart-color-palette": "default"}}>{"Prestation"}</h1>
        <p id="ia5gmy" style={{"color": "#666", "marginBottom": "30px", "--chart-color-palette": "default"}}>{"Manage Prestation data"}</p>
        <TableBlock id="table-prestation-10" styles={{"width": "100%", "minHeight": "400px", "--chart-color-palette": "default"}} title="Prestation List" options={{"showHeader": true, "stripedRows": false, "showPagination": true, "rowsPerPage": 5, "actionButtons": true, "columns": [{"label": "Id", "column_type": "field", "field": "id", "type": "str", "required": true}, {"label": "Nom", "column_type": "field", "field": "nom", "type": "str", "required": true}, {"label": "Description", "column_type": "field", "field": "description", "type": "str", "required": true}, {"label": "PrixUnitaire", "column_type": "field", "field": "prixUnitaire", "type": "float", "required": true}], "formColumns": [{"column_type": "field", "field": "nom", "label": "nom", "type": "str", "required": true, "defaultValue": null}, {"column_type": "field", "field": "description", "label": "description", "type": "str", "required": true, "defaultValue": null}, {"column_type": "field", "field": "prixUnitaire", "label": "prixUnitaire", "type": "float", "required": true, "defaultValue": null}, {"column_type": "field", "field": "id", "label": "id", "type": "str", "required": true, "defaultValue": null}, {"column_type": "lookup", "path": "lignereservation_1", "field": "lignereservation_1", "lookup_field": "quantite", "entity": "LigneReservation", "type": "str", "required": true}]}} dataBinding={{"entity": "Prestation", "endpoint": "/prestation/"}} />
        <div id="ioyce6" style={{"marginTop": "20px", "display": "flex", "gap": "10px", "flexWrap": "wrap", "--chart-color-palette": "default"}}>
          <MethodButton id="ih0m08" className="action-button-component" style={{"display": "inline-flex", "alignItems": "center", "padding": "6px 14px", "background": "linear-gradient(90deg, #2563eb 0%, #1e40af 100%)", "color": "#fff", "textDecoration": "none", "borderRadius": "4px", "fontSize": "13px", "fontWeight": "600", "letterSpacing": "0.01em", "cursor": "pointer", "border": "none", "boxShadow": "0 1px 4px rgba(37,99,235,0.10)", "transition": "background 0.2s", "--chart-color-palette": "default"}} endpoint="/prestation/{prestation_id}/methods/calculerCout/" label="+ calculerCout" parameters={[{"name": "params", "type": "any", "required": true}]} isInstanceMethod={true} instanceSourceTableId="table-prestation-10" />
        </div>
      </main>
    </div>    </div>
  );
};

export default Prestation;
