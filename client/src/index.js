import React from "react"
import ReactDOM from "react-dom/client"
// import { Telegram } from "./telegram"
import {viewPanel, viewTree} from './agregator'
// import { Game } from "./game"

const root = ReactDOM.createRoot(document.getElementById("root"))
root.render(
    <React.Fragment>
        <div className="panel-and-game">
            {viewPanel()}
            {/* <Game /> */}
        </div>
        <div className="view">
            {viewTree("Все сообщения")}
            {viewTree("Новые сообщения")}
        </div>

        {/* <Telegram /> */}
        
    </React.Fragment>
)