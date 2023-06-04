import React, { useEffect, useState } from "react"
import { fetchEmailServices, updateEmailService } from "../http/emailAPI"
import { $url } from "../http"
import EditProfiles from "./modals/EditProfiles"
import {
    MDBCard,
    MDBCardBody,
    MDBCardTitle,
    MDBCardText,
    MDBCol,
    MDBTable,
    MDBTableHead,
    MDBTableBody,
} from "mdbreact"
import { fetchMessengers, updateMessenger } from "../http/messengerAPI"
import EditTelegramProfiles from "./modals/EditTelegramProfiles"
// import { Row } from 'react-bootstrap'

export const Panel = () => {
    const [emailServices, setEmailServices] = useState([])
    const [messengers, setMessengers] = useState([])
    // const [enabled, setEnabled] = useState('')
    const [profilesVisible, setProfilesVisible] = useState(false)
    const [modalMessengerProfiles, setModalMessengerProfiles] = useState(<></>)
    const [messengerProfilesVisible, setMessengerProfilesVisible] =
        useState(false)
    const [emailServiceId, setEmailServiceId] = useState(0)
    const [emailServiceName, setEmailServiceName] = useState("")
    const [messengerName, setMessengerName] = useState("")
    // const [radioEnabled, setRadioEnabled] = useState(false)
    // const [limit, setLimit] = useState(100)
    // const [msUpdate, setMsUpdate] = useState(5000)
    // const [buttonSaveVisible, buttonSaveSetVisible] = useState(false)

    useEffect(() => {
        fetchEmailServices().then((data) => {
            setEmailServices(
                data.map((service) => {
                    return {
                        ...service,
                        changed: false,
                    }
                })
            )
            // console.log(data)
        })
        fetchMessengers().then((data) => {
            setMessengers(
                data.map((service) => {
                    return {
                        ...service,
                        changed: false,
                    }
                })
            )
        })
    }, [])

    const onChangeService = async (
        id,
        services,
        setServices,
        updateService
    ) => {
        // console.log(event.target.value, id)
        try {
            const changedService = services.find((service) => service.id === id)

            const data = await updateService(
                id,
                changedService.enabled,
                changedService.limit,
                changedService.ms_update
            )

            setServices(
                services.map((service) => {
                    return service.id === id
                        ? { ...data, changed: false }
                        : service
                })
            )

            console.log("Данные измененного сервиса:", data)
        } catch (e) {
            console.error(e)
            alert(e.message)
        }
    }

    const onChangeRadio = (enabled, id, services, setServices) => {
        console.log("Изменение переключателя, новое значение", enabled)
        setServices(
            services.map((service) => {
                return service.id === id
                    ? { ...service, enabled, changed: true }
                    : service
            })
        )
    }

    const onChangeLimit = (event, id, services, setServices) => {
        console.log("Изменение лимита, новое значение", event.target.value)
        setServices(
            services.map((service) => {
                return service.id === id
                    ? { ...service, limit: event.target.value, changed: true }
                    : service
            })
        )
    }

    const onChangeMsUpdate = (event, id, services, setServices) => {
        console.log(
            "Изменение интервала обновления, новое значение",
            event.target.value
        )
        setServices(
            services.map((service) => {
                return service.id === id
                    ? {
                          ...service,
                          ms_update: event.target.value,
                          changed: true,
                      }
                    : service
            })
        )
    }

    const onEmailProfileClick = (email_service_id, name) => {
        setEmailServiceId(email_service_id)
        setEmailServiceName(name)
        setProfilesVisible(true)
    }

    const onMessengerProfileClick = (name) => {
        setMessengerName(name)
        setMessengerProfilesVisible(true)
        if (name === "Telegram") {
            setModalMessengerProfiles(
                <EditTelegramProfiles
                    show={messengerProfilesVisible}
                    onHide={() => setMessengerProfilesVisible(false)}
                ></EditTelegramProfiles>
            )
        }
    }

    const getTableRow = (
        name,
        services,
        setServices,
        updateService,
        item,
        onProfileClick
    ) => {
        const image = <img alt="" src={$url + item.logo} />
        const serverInfo = (
            <>
                {item.imap_server && <td>{item.imap_server}</td>}
                {item.pop_server && <td>{item.pop_server}</td>}
                {item.smtp_server && <td>{item.smtp_server}</td>}
            </>
        )
        return (
            <tr key={item.id}>
                <td>
                    {image} {item.name}
                </td>
                <td>
                    <input
                        type="radio"
                        value="1"
                        onChange={(e) =>
                            onChangeRadio(true, item.id, services, setServices)
                        }
                        name={item.id + `${name}_enabled`}
                        checked={item.enabled}
                    ></input>
                    Да
                    <span> </span>
                    <input
                        type="radio"
                        value="0"
                        onChange={(e) =>
                            onChangeRadio(false, item.id, services, setServices)
                        }
                        name={item.id + `${name}_enabled`}
                        checked={!item.enabled}
                    ></input>
                    Нет
                </td>
                <td>
                    <input
                        type="number"
                        step="1"
                        min="1"
                        max="500"
                        value={item.limit}
                        style={{
                            width: "100%",
                            textAlign: "center",
                        }}
                        onChange={(e) =>
                            onChangeLimit(e, item.id, services, setServices)
                        }
                    ></input>
                </td>
                <td>
                    <input
                        type="number"
                        step="1"
                        min="250"
                        value={item.ms_update}
                        style={{
                            width: "100%",
                            textAlign: "center",
                        }}
                        onChange={(e) =>
                            onChangeMsUpdate(e, item.id, services, setServices)
                        }
                    ></input>
                </td>
                {serverInfo}
                <td>
                    <button onClick={() => onProfileClick(item.name)}>
                        Профили
                    </button>
                </td>
                <td>
                    <button
                        hidden={!item.changed}
                        onClick={(e) =>
                            onChangeService(
                                item.id,
                                services,
                                setServices,
                                updateService
                            )
                        }
                    >
                        Сохранить
                    </button>
                </td>
            </tr>
        )
    }

    return (
        <>
            <MDBCol>
                <MDBCard>
                    {/* <MDBCardImage
                            className="img-fluid"
                            src="https://mdbootstrap.com/img/Photos/Others/images/43.webp"
                            waves
                        /> */}
                    <MDBCardBody>
                        <MDBCardTitle>Настройки</MDBCardTitle>
                        <MDBCardText>
                            <MDBTable small>
                                <MDBTableHead>
                                    <tr>
                                        <th>Почты</th>
                                        <th>Включен</th>
                                        <th>Лимит сообщений</th>
                                        <th>Интервал обновления, мс</th>
                                        <th>Протокол IMAP</th>
                                        <th>Протокол POP</th>
                                        <th>Протокол SMTP</th>
                                    </tr>
                                </MDBTableHead>
                                <MDBTableBody>
                                    {emailServices.map((item) =>
                                        getTableRow(
                                            "email",
                                            emailServices,
                                            setEmailServices,
                                            updateEmailService,
                                            item,
                                            (name) =>
                                                onEmailProfileClick(
                                                    item.id,
                                                    name
                                                )
                                        )
                                    )}
                                </MDBTableBody>
                            </MDBTable>
                            <MDBTable small>
                                <MDBTableHead>
                                    <tr>
                                        <th>Мессенджеры</th>
                                        <th>Включен</th>
                                        <th>Лимит сообщений</th>
                                        <th>Интервал обновления, мс</th>
                                    </tr>
                                </MDBTableHead>
                                <MDBTableBody>
                                    {messengers.map((item) =>
                                        getTableRow(
                                            "messenger",
                                            messengers,
                                            setMessengers,
                                            updateMessenger,
                                            item,
                                            onMessengerProfileClick
                                        )
                                    )}
                                </MDBTableBody>
                            </MDBTable>
                        </MDBCardText>
                        {/* <MDBBtn href="#">MDBBtn</MDBBtn> */}
                    </MDBCardBody>
                </MDBCard>
            </MDBCol>
            <EditProfiles
                show={profilesVisible}
                onHide={() => setProfilesVisible(false)}
                email_service_id={emailServiceId}
                email_name={emailServiceName}
            ></EditProfiles>
            {modalMessengerProfiles}
        </>
    )
}

export default Panel
