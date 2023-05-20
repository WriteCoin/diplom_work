import React from "react"
import ReactDOM from "react-dom/client"
// import { Telegram } from "./telegram"
// import {viewTree} from './agregator'
// import { Game } from "./game"
import "@fortawesome/fontawesome-free/css/all.min.css"
import "bootstrap-css-only/css/bootstrap.min.css"
import "mdbreact/dist/css/mdb.css"
// import "./styles/agregator.css"
import {
    MDBCol,
    MDBContainer,
    MDBRow,
    MDBTreeview,
    MDBTreeviewList,
    MDBTreeviewItem,
} from "mdbreact"
import Panel from "./components/Panel"
import AgregatorMessages from "./components/AgregatorMessages"

const root = ReactDOM.createRoot(document.getElementById("root"))
root.render(
    <MDBContainer className="m-5 p-0">
        <MDBRow>
            <Panel></Panel>
        </MDBRow>
        <MDBRow>
            <MDBCol md="2">
                <AgregatorMessages header={"Все сообщения"}></AgregatorMessages>
            </MDBCol>
            <MDBCol md="2">
                {/* <AgregatorMessages
                    header={"Новые сообщения"}
                ></AgregatorMessages> */}
            </MDBCol>
            <MDBCol md="6">
            </MDBCol>
        </MDBRow>
    </MDBContainer>
)
