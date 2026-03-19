import React from "react";
import { TableBlock } from "../components/runtime/TableBlock";
import { MethodButton } from "../components/MethodButton";

const Tarif: React.FC = () => {
  return (
    <div id="page-tarif-3">
    <div id="imonfh" style={{"display": "flex", "height": "100vh", "fontFamily": "Arial, sans-serif", "--chart-color-palette": "default"}}>
      <nav id="iylfpk" style={{"width": "250px", "background": "linear-gradient(135deg, #4b3c82 0%, #5a3d91 100%)", "color": "white", "padding": "20px", "overflowY": "auto", "display": "flex", "flexDirection": "column", "--chart-color-palette": "default"}}>
        <h2 id="ilqszn" style={{"marginTop": "0", "fontSize": "24px", "marginBottom": "30px", "fontWeight": "bold", "--chart-color-palette": "default"}}>{"BESSER"}</h2>
        <div id="im5vrn" style={{"display": "flex", "flexDirection": "column", "flex": "1", "--chart-color-palette": "default"}}>
          <a id="i8a1ye" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/centredecongres">{"CentreDeCongres"}</a>
          <a id="is8kdx" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/gestionnaire">{"Gestionnaire"}</a>
          <a id="icdld9" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/elementcentre">{"ElementCentre"}</a>
          <a id="iean7s" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "rgba(255,255,255,0.2)", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/tarif">{"Tarif"}</a>
          <a id="i5ab8h" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/reservation">{"Reservation"}</a>
          <a id="ipitpa" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/indisponibilite">{"Indisponibilite"}</a>
          <a id="icd3c5" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/lignereservation">{"LigneReservation"}</a>
          <a id="i0pnrg" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/evenement">{"Evenement"}</a>
          <a id="iqhw0v" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/materiel">{"Materiel"}</a>
          <a id="i68jph" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/stockmateriel">{"StockMateriel"}</a>
          <a id="ii3uu7" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/prestation">{"Prestation"}</a>
          <a id="izxxmg" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/prestationglobale">{"PrestationGlobale"}</a>
          <a id="iy1dma" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/prestationdimensionnee">{"PrestationDimensionnee"}</a>
        </div>
        <p id="ile6xj" style={{"marginTop": "auto", "paddingTop": "20px", "borderTop": "1px solid rgba(255,255,255,0.2)", "fontSize": "11px", "opacity": "0.8", "textAlign": "center", "--chart-color-palette": "default"}}>{"© 2026 BESSER. All rights reserved."}</p>
      </nav>
      <main id="i9zzlg" style={{"flex": "1", "padding": "40px", "overflowY": "auto", "background": "#f5f5f5", "--chart-color-palette": "default"}}>
        <h1 id="iiklg3" style={{"marginTop": "0", "color": "#333", "fontSize": "32px", "marginBottom": "10px", "--chart-color-palette": "default"}}>{"Tarif"}</h1>
        <p id="i95ble" style={{"color": "#666", "marginBottom": "30px", "--chart-color-palette": "default"}}>{"Manage Tarif data"}</p>
        <TableBlock id="table-tarif-3" styles={{"width": "100%", "minHeight": "400px", "--chart-color-palette": "default"}} title="Tarif List" options={{"showHeader": true, "stripedRows": false, "showPagination": true, "rowsPerPage": 5, "actionButtons": true, "columns": [{"label": "PrixJournalier", "column_type": "field", "field": "prixJournalier", "type": "float", "required": true}, {"label": "PrixDemiJournee", "column_type": "field", "field": "prixDemiJournee", "type": "float", "required": true}, {"label": "DateDebut", "column_type": "field", "field": "dateDebut", "type": "datetime", "required": true}, {"label": "DateFin", "column_type": "field", "field": "dateFin", "type": "datetime", "required": true}], "formColumns": [{"column_type": "field", "field": "prixJournalier", "label": "prixJournalier", "type": "float", "required": true, "defaultValue": null}, {"column_type": "field", "field": "prixDemiJournee", "label": "prixDemiJournee", "type": "float", "required": true, "defaultValue": null}, {"column_type": "field", "field": "dateDebut", "label": "dateDebut", "type": "datetime", "required": true, "defaultValue": null}, {"column_type": "field", "field": "dateFin", "label": "dateFin", "type": "datetime", "required": true, "defaultValue": null}, {"column_type": "lookup", "path": "elementcentre_1", "field": "elementcentre_1", "lookup_field": "id", "entity": "ElementCentre", "type": "str", "required": true}]}} dataBinding={{"entity": "Tarif", "endpoint": "/tarif/"}} />
        <div id="ier488" style={{"marginTop": "20px", "display": "flex", "gap": "10px", "flexWrap": "wrap", "--chart-color-palette": "default"}}>
          <MethodButton id="ix961f" className="action-button-component" style={{"display": "inline-flex", "alignItems": "center", "padding": "6px 14px", "background": "linear-gradient(90deg, #2563eb 0%, #1e40af 100%)", "color": "#fff", "textDecoration": "none", "borderRadius": "4px", "fontSize": "13px", "fontWeight": "600", "letterSpacing": "0.01em", "cursor": "pointer", "border": "none", "boxShadow": "0 1px 4px rgba(37,99,235,0.10)", "transition": "background 0.2s", "--chart-color-palette": "default"}} endpoint="/tarif/{tarif_id}/methods/calculerMontant/" label="+ calculerMontant" parameters={[{"name": "debut", "type": "any", "required": true}, {"name": "fin", "type": "any", "required": true}]} isInstanceMethod={true} instanceSourceTableId="table-tarif-3" />
        </div>
      </main>
    </div>    </div>
  );
};

export default Tarif;
