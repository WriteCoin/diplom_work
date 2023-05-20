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
// import { Row } from 'react-bootstrap'

export const Panel = () => {
    const [emailServices, setEmailServices] = useState([])
    // const [enabled, setEnabled] = useState('')
    const [profilesVisible, setProfilesVisible] = useState(false)
    const [emailServiceId, setEmailServiceId] = useState(0)

    useEffect(() => {
        fetchEmailServices().then((data) => {
            setEmailServices(data)
            // console.log(data)
        })
    }, [])

    const enabledHandler = async (event, id) => {
        // console.log(event.target.value, id)
        await updateEmailService(id, event.target.value)
        const data = await fetchEmailServices()
        setEmailServices(data)
    }

    const onProfileClick = (email_service_id) => {
        setEmailServiceId(email_service_id)
        setProfilesVisible(true)
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
                                        <th>Протокол IMAP</th>
                                        <th>Протокол POP</th>
                                        <th>Протокол SMTP</th>
                                    </tr>
                                </MDBTableHead>
                                <MDBTableBody>
                                    {emailServices.map((item) => {
                                        const image = (
                                            <img
                                                alt=""
                                                src={$url + item.logo}
                                            />
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
                                                            enabledHandler(
                                                                e,
                                                                item.id
                                                            )
                                                        }
                                                        name={
                                                            item.id + "_enabled"
                                                        }
                                                        checked={item.enabled}
                                                    ></input>
                                                    Да
                                                    <span> </span>
                                                    <input
                                                        type="radio"
                                                        value="0"
                                                        onChange={(e) =>
                                                            enabledHandler(
                                                                e,
                                                                item.id
                                                            )
                                                        }
                                                        name={
                                                            item.id + "_enabled"
                                                        }
                                                        checked={!item.enabled}
                                                    ></input>
                                                    Нет
                                                    {/* <span>
                                            <input
                                                type='radio'
                                                value='1'
                                                
                                                name="enabled"
                                            ></input>
                                            Да
                                        </span> */}
                                                    {/* <input
                                            type='radio'
                                            value='0'
                                            checked={item.enabled ? 'true' : 'false'}
                                            name="enabled"
                                        >
                                            Нет
                                        </input> */}
                                                </td>
                                                <td>{item.limit}</td>
                                                <td>{item.imap_server}</td>
                                                <td>{item.pop_server}</td>
                                                <td>{item.smtp_server}</td>
                                                <td>
                                                    <button
                                                        onClick={() =>
                                                            onProfileClick(
                                                                item.id
                                                            )
                                                        }
                                                    >
                                                        Профили
                                                    </button>
                                                </td>
                                                {/* <td>
                                        <button className="filter-options-settings-button">Настройки</button>
                                    </td> */}
                                            </tr>
                                        )
                                    })}
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
            ></EditProfiles>
        </>
    )
}

export default Panel
