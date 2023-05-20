import React, { useEffect, useState } from "react"
// import { Row, Col } from "react-bootstrap";
import {
    MDBContainer,
    MDBCol,
    MDBTreeview,
    MDBTreeviewList,
    MDBTreeviewItem,
} from "mdbreact"
import { fetchEmailServices } from "../http/emailAPI"
// import EmailMessages from "./EmailMessages"
// import MessengerMessages from "./MessengerMessages"
import { io } from "socket.io-client"

class TreeNode extends React.Component {
    constructor(props) {
        super(props)
        this.state = {
            isExpanded: true,
        }
        this.handleExpand = this.handleExpand.bind(this)
    }

    handleExpand() {
        // this.setState((prevState) => ({ isExpanded: !prevState.isExpanded }))
        this.setState({ isExpanded: !this.state.isExpanded })
    }

    render() {
        // console.log(this.props)
        // const [label, info] = this.props
        const { label, children } = this.props
        const { isExpanded } = this.state

        const image = this.props.image && <img alt="" src={this.props.image} />
        const treeElClass = image ? "tree-el-with-image" : "tree-el"

        const renderChildren = (children) => {
            if (isExpanded && Array.isArray(children)) {
                return <Tree data={children}></Tree>
            }
        }

        return (
            <div className="tree-node">
                <li
                    className={`fa fa-${isExpanded ? "minus" : "plus"}`}
                    key={label}
                    onClick={this.handleExpand}
                >
                    <div className={treeElClass}>
                        {image}
                        {/* <p>{label}</p> */}
                        {label}
                    </div>
                </li>

                <div className="tree-children">{renderChildren(children)}</div>
            </div>
        )
    }
}

class Tree extends React.Component {
    constructor(props) {
        super(props)
    }

    render() {
        const { data, name } = this.props
        return (
            <div className="tree">
                <h3>{name}</h3>
                <ul>
                    {/* {data &&
                        Object.entries(data).map((node) => {
                            return <TreeNode {...node} />
                        })} */}
                    {Array.isArray(data) &&
                        data.map((node) => {
                            return <TreeNode {...node} />
                        })}
                </ul>
            </div>
        )
    }
}

const AgregatorMessages = ({ header }) => {
    const [messages, setMessages] = useState([])
    const [newMessage, setNewMessage] = useState("")

    useEffect(() => {
        const socket = io(process.env.SOCKET_URL)

        console.log(socket)

        socket.on('connect', function() {
            console.log('Socket connected:', socket.connected); // true
        })

        return (() => {
            socket.disconnect()
        })
    })

    // Клиентское соединение с сервером Flask
    // console.log('Клиентское соединение с сервером Flask')
    // const socket = io(process.env.SOCKET_URL)

    // console.log('socket', socket)

    // // Обработчик для получения сообщений от сервера
    // socket.on("message", (message) => {
    //     setMessages((messages) => [...messages, message])
    // })

    // // Обработчик для отправки сообщения на сервер
    // const sendMessage = () => {
    //     socket.emit("message", newMessage)
    //     setNewMessage("")
    // }

    // socket.emit('Новое сообщение')
    // console.log('Сообщение отправлено')

    return <></>

    // return (

    //     // <MDBTreeview header="Заголовок" className="w-20">
    //     //     <MDBTreeviewList
    //     //         icon="envelope-open"
    //     //         title="Почты"
    //     //         far
    //     //         open
    //     //     ></MDBTreeviewList>
    //     //     <MDBTreeviewList
    //     //         icon="comment"
    //     //         title="Мессенджеры"
    //     //         far
    //     //     ></MDBTreeviewList>
    //     // </MDBTreeview>
    // )
}

export default AgregatorMessages
