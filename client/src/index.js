// import * as dotenv from 'dotenv';
import React from "react"
import ReactDOM from "react-dom/client"
import "@fortawesome/fontawesome-free/css/all.min.css"
import "bootstrap-css-only/css/bootstrap.min.css"
import "mdbreact/dist/css/mdb.css"
import { MDBCol, MDBContainer, MDBRow } from "mdbreact"
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
        <MDBContainer fluid className="container m-5 p-0 ">
            <MDBRow>
                <Panel></Panel>
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
