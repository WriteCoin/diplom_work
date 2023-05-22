import React, { useEffect, useState } from "react"
import { Row, Col } from "react-bootstrap"
// import {
//     MDBContainer,
//     MDBCol,
//     MDBTreeview,
//     MDBTreeviewList,
//     MDBTreeviewItem,
// } from "mdbreact"
import {
    fetchEmailMessages,
    fetchEmailProfiles,
    fetchEmailServices,
} from "../http/emailAPI"
import { $url } from "../http"
import {
    MDBCard,
    MDBCardBody,
    MDBCardText,
    MDBCardTitle,
    MDBCol,
} from "mdbreact"
// import EmailMessages from "./EmailMessages"
// import MessengerMessages from "./MessengerMessages"
// import { io } from "socket.io-client"
// import { Client } from "pg"
// import createSubscriber from "pg-listen"
// import { pgClient } from "../db";
// import worker from 'workerize-loader!../updateMessages';

const data = [
    {
        label: "Мессенджеры",
        image: undefined,
        children: [
            {
                label: "Вконтакте",
                image: "/favicon-vk-32x32.png",
                enabled: true,
                limit: 100,
            },
            {
                label: "Telegram",
                image: "/favicon-telegram-32x32.png",
                enabled: true,
                limit: 50,
            },
        ],
    },
    {
        label: "Почты",
        image: undefined,
        children: [
            {
                label: "Gmail",
                image: "/favicon-gmail-32x32.png",
                enabled: true,
                limit: 100,
            },
            {
                label: "Yandex",
                image: "/favicon-yandex-32x32.png",
                enabled: true,
                limit: 100,
            },
        ],
    },
]

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
                        {/* <p>{label}</p> */}
                        {image}
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
                {/* <h3>{name}</h3> */}
                <ul>
                    {Array.isArray(data) &&
                        data.map((node, index) => {
                            return <TreeNode key={index} {...node} />
                        })}
                </ul>
            </div>
        )
    }
}

const AgregatorMessages = ({ header }) => {
    const [allEmailMessages, setAllEmailMessages] = useState({})
    const [newEmailMessages, setNewEmailMessages] = useState({})

    useEffect(() => {
        setInterval(async () => {
            const profilesData = await fetchEmailProfiles(true)

            console.log("profilesData", profilesData)

            if (!profilesData) {
                return
            }

            for (let index = 0; index < profilesData.length; index++) {
                const profileData = profilesData[index]

                const setNewMessages = (
                    newMessages,
                    emailMessages,
                    setEmailMessages
                ) => {
                    console.log("newMessages", newMessages)
                    const newEmailMessages = emailMessages
                    for (let index = 0; index < newMessages.length; index++) {
                        const newMessage = newMessages[index]
                        const email_id = profileData.email_id
                        const message_id = newMessage.id
                        newEmailMessages[email_id] =
                            newEmailMessages[email_id] || {}
                        newEmailMessages[email_id][message_id] = newMessage
                    }
                    setEmailMessages(newEmailMessages)
                }

                fetchEmailMessages(profileData).then((newMessages) => {
                    setNewMessages(
                        newMessages.all_email_messages,
                        allEmailMessages,
                        setAllEmailMessages
                    )
                    setNewMessages(
                        newMessages.new_email_messages,
                        newEmailMessages,
                        setNewEmailMessages
                    )
                })
            }
        }, 5000)
    })

    const getEmailNodes = (emailMessages) =>
        Object.entries(allEmailMessages).map((_, thisEmailMessages) => {
            const firstMessage =
                thisEmailMessages[Object.keys(thisEmailMessages)[0]]

            return {
                label: firstMessage.name,
                image: $url + firstMessage.logo,
                children: Object.entries(thisEmailMessages).map(
                    (_, thisMessage) => {
                        return {
                            label: `${thisMessage.sender} - ${thisMessage.subject}; ${thisMessage.date}`,
                            image: undefined,
                            children: [
                                {
                                    label: `${thisMessage.text}`,
                                    image: undefined,
                                },
                            ],
                        }
                    }
                ),
            }
        })

    const allData = [
        {
            label: "Мессенджеры",
            image: undefined,
            children: [
                {
                    label: "Вконтакте",
                    image: "/favicon-vk-32x32.png",
                },
                {
                    label: "Telegram",
                    image: "/favicon-telegram-32x32.png",
                },
            ],
        },
        {
            label: "Почты",
            image: undefined,
            children: getEmailNodes(allEmailMessages),
        },
    ]

    const newData = [
        {
            label: "Мессенджеры",
            image: undefined,
            children: [
                {
                    label: "Вконтакте",
                    image: "/favicon-vk-32x32.png",
                },
                {
                    label: "Telegram",
                    image: "/favicon-telegram-32x32.png",
                },
            ],
        },
        {
            label: "Почты",
            image: undefined,
            children: getEmailNodes(newEmailMessages),
        },
    ]

    return (
        <>
            <MDBCol md="6">
                <MDBCard className="text-dark">
                    <MDBCardBody>
                        <MDBCardTitle>{header}</MDBCardTitle>
                        <MDBCardText className="text-dark">
                            <Tree data={allData} name="Все сообщения"></Tree>
                        </MDBCardText>
                    </MDBCardBody>
                </MDBCard>
            </MDBCol>
            <MDBCol md="6">
                <MDBCard className="text-dark">
                    <MDBCardBody>
                        <MDBCardTitle>{header}</MDBCardTitle>
                        <MDBCardText className="text-dark">
                            <Tree data={newData} name="Новые сообщения"></Tree>
                        </MDBCardText>
                    </MDBCardBody>
                </MDBCard>
            </MDBCol>
            {/* <MDBCol md="6"></MDBCol> */}
        </>

        // <div className="first-tree">
        //     <Tree data={data} name={header}></Tree>
        // </div>
    )

    // const worker = new Worker('../updateMessages.js')

    // // Обработка сообщения от воркера в основном потоке
    // worker.onmessage = (event) => {
    //     setMessages(event.data.messages)
    // };

    // // Передача сообщения в воркер
    // worker.postMessage({message: 'Hello World!'});

    // const workerInstance = worker(); // Создание экземпляра воркера
    // workerInstance.updateMessages() // Вызов функции воркера
    //     .then(messages => {
    //         console.log(messages)
    //         setMessages(messages)
    //     }) // Получение результата

    // console.log('SOCKET_URL', process.env.SOCKET_URL)
    // const socket = new WebSocket(process.env.REACT_APP_SOCKET_URL);

    // function onOpen(event) {
    //     console.log('WebSocket opened!');
    // }

    // function onClose(event) {
    //     console.log('WebSocket closed!');
    // }

    // function onMessage(event) {
    //     console.log(`Message received: ${event.data}`);
    // }

    // function onError(event) {
    //     console.error('WebSocket error:', event);
    // }

    // socket.addEventListener('open', onOpen);
    // socket.addEventListener('close', onClose);
    // socket.addEventListener('message', onMessage);
    // socket.addEventListener('error', onError);
    // console.log(pgClient)

    // const socket = io()
    // const socket = io(process.env.REACT_APP_SOCKET_URL)

    // console.log(socket)

    // socket.on('connect', function() {
    //     console.log('Socket connected:', socket.connected); // true
    // })

    // return (() => {
    //     socket.disconnect()
    // })
    // const pgClient = new Client({
    //     ...
    // })

    // pgClient()
    // })

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

    // return <></>

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
