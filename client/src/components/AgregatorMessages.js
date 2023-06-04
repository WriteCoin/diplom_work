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
    fetchOneEmailProfile,
} from "../http/emailAPI"
import { $url } from "../http"
import {
    MDBCard,
    MDBCardBody,
    MDBCardText,
    MDBCardTitle,
    MDBCol,
} from "mdbreact"

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
    const [emailServices, setEmailServices] = useState([])
    const [allEmailMessages, setAllEmailMessages] = useState({})
    const [newEmailMessages, setNewEmailMessages] = useState({})
    const [emailTimerIds, setEmailTimerIds] = useState({})
    const [allTelegramMessages, setAllTelegramMessages] = useState({})
    const [newTelegramMessages, setNewTelegramMessages] = useState({})
    const [telegramTimerId, setTelegramTimerId] = useState(0)

    const setNewProfileMessages = (
        newMessages,
        emailMessages,
        setEmailMessages,
        email_id
    ) => {
        const newEmailMessages = emailMessages
        for (let index = 0; index < newMessages.length; index++) {
            const newMessage = newMessages[index]
            const message_id = newMessage.id
            newEmailMessages[email_id] = newEmailMessages[email_id] || {}
            newEmailMessages[email_id][message_id] = newMessage
        }
        setEmailMessages(newEmailMessages)
    }

    useEffect(() => {
        const startTimer = (profileId) => {
            fetchOneEmailProfile(profileId)
                .then((profileData) => {
                    if (!profileData.enabled || !profileData.is_active) {
                        clearTimeout(
                            emailTimerIds[profileData.email_profile_id]
                        )
                        setEmailTimerIds({
                            ...emailTimerIds,
                            [profileData.email_profile_id]: null,
                        })
                    } else {
                        const timerId = setTimeout(
                            fetchProfileMessages,
                            profileData.ms_update
                        )
                        setEmailTimerIds({
                            ...emailTimerIds,
                            [profileData.email_profile_id]: timerId,
                        })
                    }
                })
                .catch((e) => {
                    console.error(e)
                    alert(e.message)
                })
        }

        const fetchProfileMessages = (profileData) => {
            fetchEmailMessages(profileData)
                .then((newMessages) => {
                    if (newMessages.error) {
                        // startTimer(profileData.email_profile_id)
                        console.error(newMessages)
                        return
                    }
                    console.log("new messages", newMessages)
                    const emailAllMessagesId = newMessages.all_email_messages
                        .length
                        ? newMessages.all_email_messages[0].email_id
                        : 0
                    setNewProfileMessages(
                        newMessages.all_email_messages,
                        allEmailMessages,
                        setAllEmailMessages,
                        emailAllMessagesId
                    )
                    const emailNewMessagesId = newMessages.new_email_messages
                        .length
                        ? newMessages.new_email_messages[0].email_id
                        : 0
                    setNewProfileMessages(
                        newMessages.new_email_messages,
                        newEmailMessages,
                        setNewEmailMessages,
                        emailNewMessagesId
                    )
                    // startTimer(profileData.email_profile_id)
                    // const timerId = setTimeout(fetchProfileMessages, profileData.ms_update)
                    // setEmailTimerIds({...emailTimerIds, [profileData.email_profile_id]: timerId})
                })
                .catch((e) => {
                    console.error(e)
                    // startTimer(profileData.email_profile_id)
                })
        }

        const timeRefetch = 10000

        let allFetchTimerId

        console.log("ЕДИНОКРАТНЫЙ АЛГОРИТМ - НАЧАЛО ПОЛУЧЕНИЯ СООБЩЕНИЙ")

        const fetchData = async () => {
            const emailServicesData = await fetchEmailServices()

            setEmailServices(emailServicesData.filter((data) => data.enabled))

            const profilesData = await fetchEmailProfiles(true)

            console.log("profilesData", profilesData)

            if (!profilesData.length) {
                console.log(
                    "Таймер ожидания получения хоть одного активированного профиля"
                )
                allFetchTimerId = setTimeout(fetchData, timeRefetch)
                return
            }

            profilesData.forEach((profileData) => {
                console.log("Получение сообщений для профиля:", profileData)

                fetchProfileMessages(profileData)
                startTimer(profileData.email_profile_id)
            })

            console.log("Таймер ожидания изменения активированных профилей")
            allFetchTimerId = setInterval(async () => {
                const newProfilesData = await fetchEmailProfiles(true)
                if (
                    JSON.stringify(newProfilesData) !==
                    JSON.stringify(profilesData)
                ) {
                    console.log("ПРОФИЛИ ИЗМЕНИЛИСЬ")
                    console.log("Новые профили", newProfilesData)
                    console.log("Остановка таймеров профилей")
                    Object.entries(emailTimerIds).forEach(([_, timerId]) => {
                        clearTimeout(timerId)
                    })
                    console.log("Перезапуск получений сообщений и таймеров")
                    newProfilesData.forEach((profileData) => {
                        console.log(
                            "Получение сообщений для профиля:",
                            profileData
                        )

                        fetchProfileMessages(profileData)
                        startTimer(profileData.email_profile_id)
                    })
                }
                // if (profilesData.length - count !== newProfilesData.filter(profileData => profileData.enabled).length) {

                // }
            }, timeRefetch)

            // console.log("Цикл по profilesData")

            // let count = 0

            // for (let index = 0; index < profilesData.length; index++) {
            //     const profileData = profilesData[index]

            // if (!profileData.enabled) {
            //     count++
            //     fetchActivateTimerIds[profileData.email_profile_id] = setTimeout(fetchOneProfileData, timeRefetch)
            //     return
            // }

            // console.log("Получение сообщений для профиля:", profileData)

            // fetchProfileMessages(profileData)

            // const fetchOneProfileData = () => {
            //     if (!profileData.enabled) {
            //         count++
            //         console.log("Таймер ожидания профиля", profileData)
            //         fetchActivateTimerIds[profileData.email_profile_id] = setTimeout(fetchOneProfileData, timeRefetch)
            //         return
            //     }

            //     console.log("Включен профиль:", profileData)

            //     fetchProfileMessages(profileData)
            // }
            // }

            // if (count == profilesData.length) {
            //     console.log("Таймер ожидания активации профилей")
            //     allFetchTimerId = setTimeout(fetchData, timeRefetch)
            //     return
            // } else {
            //     console.log("Таймер ожидания активации новых профилей")
            //     allFetchTimerId = setInterval(async () => {
            //         const newProfilesData = await fetchEmailProfiles(true)
            //         if (JSON.stringify(newProfilesData) !== JSON.stringify(profilesData)) {

            //         }

            //         if (profilesData.length - count !== newProfilesData.filter(profileData => profileData.enabled).length) {

            //         }
            //     }, timeRefetch)
            // }
        }
        fetchData()
        return () => {
            console.log("ОТМОНТИРОВАНИЕ КОМПОНЕНТА")
            console.log("Остановка всех таймеров")
            Object.entries(emailTimerIds).forEach(([_, timerId]) => {
                clearTimeout(timerId)
            })
            clearTimeout(allFetchTimerId)
        }
    }, [])

    const getEmailNodes = (emailMessages) =>
        Object.keys(emailMessages).length
            ? Object.entries(emailMessages).map((_, thisEmailMessages) => {
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
            : emailServices.map((data) => {
                  return {
                      label: data.name,
                      image: $url + data.logo,
                      children: [
                          { label: <b><i>{"Сообщения отсутствуют"}</i></b>, image: undefined },
                      ],
                  }
              })

    const vkChild = {
        label: "Вконтакте",
        image: "/favicon-vk-32x32.png",
    }
    const telegramChild = {
        label: "Telegram",
        image: "/favicon-telegram-32x32.png",
    }

    const allData = [
        {
            label: "Мессенджеры",
            image: undefined,
            children: [telegramChild],
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
            children: [telegramChild],
        },
        {
            label: "Почты",
            image: undefined,
            children: getEmailNodes(newEmailMessages),
        },
    ]

    console.log("newData", newData)

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
