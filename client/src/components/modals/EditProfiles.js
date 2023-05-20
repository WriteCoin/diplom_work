import React, { useEffect, useState } from "react"
import {Modal, Row, Col, Button} from 'react-bootstrap'
import { fetchEmailProfiles } from "../../http/emailAPI"
import FormEmailProfile from "../FormEmailProfile"

const EditProfiles = ({show, onHide, email_service_id}) => {
    const [emailProfiles, setEmailProfiles] = useState([])

    const updateProfiles = () => fetchEmailProfiles().then(data => {
        console.log("email_service_id", email_service_id)
        const resultData = data.filter(item => item.email_id === email_service_id)
        console.log('resultData', resultData)
        setEmailProfiles(resultData)
    })

    // useEffect(() => {
    //     updateProfiles()
    // }, [])

    // console.log("email_service_id", email_service_id)

    return (
        <Modal
            show={show}
            onHide={onHide}
            centered
        >
            <Modal.Header closeButton>
                <Modal.Title id="contained-modal-title-vcenter">
                    Изменить профили
                </Modal.Title>
            </Modal.Header>
            <Modal.Body>
                <Row className="mt-2">
                    <Col>Ваши профили:</Col>
                </Row>
                {emailProfiles.map((item) => {
                    return (
                        <div key={item.id}>
                            <FormEmailProfile emailProfile={item} updateProfiles={updateProfiles} emailProfiles={emailProfiles} setEmailProfiles={setEmailProfiles}></FormEmailProfile>
                        </div>
                    )
                })}
                <Row className="mt-2">
                    <Col>Добавить профиль:</Col>
                </Row>
                <FormEmailProfile email_id={email_service_id} updateProfiles={updateProfiles} emailProfiles={emailProfiles} setEmailProfiles={setEmailProfiles}></FormEmailProfile>
            </Modal.Body>
            <Modal.Footer>
                <Button variant="outline-danger" onClick={onHide}>Закрыть</Button>
            </Modal.Footer>
        </Modal>
    )
}

export default EditProfiles