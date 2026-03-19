import React from "react";
import { TableBlock } from "../components/runtime/TableBlock";

const Indisponibilite: React.FC = () => {
  return (
    <div id="page-indisponibilite-5">
    <div id="i1d995" style={{"display": "flex", "height": "100vh", "fontFamily": "Arial, sans-serif", "--chart-color-palette": "default"}}>
      <nav id="ij6duq" style={{"width": "250px", "background": "linear-gradient(135deg, #4b3c82 0%, #5a3d91 100%)", "color": "white", "padding": "20px", "overflowY": "auto", "display": "flex", "flexDirection": "column", "--chart-color-palette": "default"}}>
        <h2 id="i32cqg" style={{"marginTop": "0", "fontSize": "24px", "marginBottom": "30px", "fontWeight": "bold", "--chart-color-palette": "default"}}>{"BESSER"}</h2>
        <div id="iggulb" style={{"display": "flex", "flexDirection": "column", "flex": "1", "--chart-color-palette": "default"}}>
          <a id="i0g8kd" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/centredecongres">{"CentreDeCongres"}</a>
          <a id="i51keh" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/gestionnaire">{"Gestionnaire"}</a>
          <a id="id28cl" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/elementcentre">{"ElementCentre"}</a>
          <a id="imqgqb" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/tarif">{"Tarif"}</a>
          <a id="ilxvlt" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/reservation">{"Reservation"}</a>
          <a id="i9enkj" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "rgba(255,255,255,0.2)", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/indisponibilite">{"Indisponibilite"}</a>
          <a id="it305i" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/lignereservation">{"LigneReservation"}</a>
          <a id="iiw1lt" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/evenement">{"Evenement"}</a>
          <a id="itb9c3" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/materiel">{"Materiel"}</a>
          <a id="ib5gxr" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/stockmateriel">{"StockMateriel"}</a>
          <a id="i4gmeo" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/prestation">{"Prestation"}</a>
          <a id="ikfhlp" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/prestationglobale">{"PrestationGlobale"}</a>
          <a id="ihdax3" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/prestationdimensionnee">{"PrestationDimensionnee"}</a>
        </div>
        <p id="izpnas" style={{"marginTop": "auto", "paddingTop": "20px", "borderTop": "1px solid rgba(255,255,255,0.2)", "fontSize": "11px", "opacity": "0.8", "textAlign": "center", "--chart-color-palette": "default"}}>{"© 2026 BESSER. All rights reserved."}</p>
      </nav>
      <main id="i2es6p" style={{"flex": "1", "padding": "40px", "overflowY": "auto", "background": "#f5f5f5", "--chart-color-palette": "default"}}>
        <h1 id="i37rms" style={{"marginTop": "0", "color": "#333", "fontSize": "32px", "marginBottom": "10px", "--chart-color-palette": "default"}}>{"Indisponibilite"}</h1>
        <p id="i23yi8" style={{"color": "#666", "marginBottom": "30px", "--chart-color-palette": "default"}}>{"Manage Indisponibilite data"}</p>
        <TableBlock id="table-indisponibilite-5" styles={{"width": "100%", "minHeight": "400px", "--chart-color-palette": "default"}} title="Indisponibilite List" options={{"showHeader": true, "stripedRows": false, "showPagination": true, "rowsPerPage": 5, "actionButtons": true, "columns": [{"label": "DateDebut", "column_type": "field", "field": "dateDebut", "type": "datetime", "required": true}, {"label": "DateFin", "column_type": "field", "field": "dateFin", "type": "datetime", "required": true}, {"label": "Motif", "column_type": "field", "field": "motif", "type": "str", "required": true}, {"label": "Type", "column_type": "field", "field": "type", "type": "str", "required": true}], "formColumns": [{"column_type": "field", "field": "dateDebut", "label": "dateDebut", "type": "datetime", "required": true, "defaultValue": null}, {"column_type": "field", "field": "dateFin", "label": "dateFin", "type": "datetime", "required": true, "defaultValue": null}, {"column_type": "field", "field": "motif", "label": "motif", "type": "str", "required": true, "defaultValue": null}, {"column_type": "field", "field": "type", "label": "type", "type": "str", "required": true, "defaultValue": null}]}} dataBinding={{"entity": "Indisponibilite", "endpoint": "/indisponibilite/"}} />
      </main>
    </div>    </div>
  );
};

export default Indisponibilite;
