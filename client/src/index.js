// import * as dotenv from 'dotenv';
import React from "react"
import ReactDOM from "react-dom/client"
import "@fortawesome/fontawesome-free/css/all.min.css"
import "bootstrap-css-only/css/bootstrap.min.css"
import "mdbreact/dist/css/mdb.css"
import {
    MDBBtn,
    MDBCard,
    MDBCardBody,
    MDBCardText,
    MDBCardTitle,
    MDBCol,
    MDBContainer,
    MDBRow,
} from "mdbreact"
// import { Telegram } from "./telegram"
// import {viewTree} from './agregator'
// import { Game } from "./game"
import "./styles/agregator.css"
import Panel from "./components/Panel"
import AgregatorMessages from "./components/AgregatorMessages"
// import { pgClient } from "./db";

// dotenv.config()

// console.log(process.env)
// console.log('SOCKET_URL', process.env.SOCKET_URL)

const root = ReactDOM.createRoot(document.getElementById("root"))
root.render(
    <>
        <MDBContainer className="m-5 p-3 bg-warning" fluid>
            <MDBRow>
                <Panel></Panel>
                {/* <MDBCol>
                    <MDBCard>
                        <MDBCardBody>
                            <MDBCardTitle>Card title</MDBCardTitle>
                            <MDBCardText>
                                Some quick example text to build on the card
                                title and make up the bulk of the card's
                                content.
                            </MDBCardText>
                        </MDBCardBody>
                    </MDBCard>
                </MDBCol> */}
            </MDBRow>
            <MDBRow className="mt-5">
                <AgregatorMessages></AgregatorMessages>
            </MDBRow>
        </MDBContainer>

        {/* <div className="view">
            <AgregatorMessages header={"Все сообщения"}></AgregatorMessages>
            <AgregatorMessages header={"Новые сообщения"}></AgregatorMessages>
        </div> */}
    </>
)
