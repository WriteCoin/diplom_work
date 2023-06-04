import React, { useEffect, useState } from "react"
import { Modal, Row, Col, Button } from "react-bootstrap"
// import { fetchEmailProfiles } from "../../http/emailAPI"
// import FormEmailProfile from "../FormEmailProfile"
import FormTelegramProfile from "../FormTelegramProfile"

const EditTelegramProfiles = ({ show, onHide }) => {
    const [telegramProfiles, setTelegramProfiles] = useState([])

    // const updateProfiles = () =>
    //     fetchEmailProfiles().then((data) => {
    //         console.log("email_service_id", email_service_id)
    //         const resultData = data.filter(
    //             (item) => item.email_id === email_service_id
    //         )
    //         console.log("resultData", resultData)
    //         setEmailProfiles(resultData)
    //     })
    const updateProfiles = () => {}

    return (
        <Modal size="lg" show={show} onHide={onHide} centered>
            <Modal.Header closeButton>
                <Modal.Title id="contained-modal-title-vcenter">
                    Изменить профили мессенджера Telegram
                </Modal.Title>
            </Modal.Header>
            <Modal.Body>
                <Row className="mt-2">
                    <Col>Ваши профили:</Col>
                </Row>
                {telegramProfiles.length > 0 ? (
                    telegramProfiles.map((item) => {
                        return (
                            <FormTelegramProfile
                                key={item.id}
                                telegramProfile={item}
                                isAdd={false}
                                updateProfiles={updateProfiles}
                                telegramProfiles={telegramProfiles}
                                setTelegramProfiles={setTelegramProfiles}
                            ></FormTelegramProfile>
                        )
                    })
                ) : (
                    <Row className="mt-2">
                        <Col>
                            <i>
                                <b>Профили отсутствуют</b>
                            </i>
                        </Col>
                    </Row>
                )}
                <Row className="mt-2">
                    <Col>Добавить профиль:</Col>
                </Row>
                <FormTelegramProfile
                    isAdd={true}
                    updateProfiles={updateProfiles}
                    telegramProfiles={telegramProfiles}
                    setTelegramProfiles={setTelegramProfiles}
                ></FormTelegramProfile>
            </Modal.Body>
            <Modal.Footer>
                <Button variant="outline-danger" onClick={onHide}>
                    Закрыть
                </Button>
            </Modal.Footer>
        </Modal>
    )
}

export default EditTelegramProfiles
