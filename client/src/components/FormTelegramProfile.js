import React, { useEffect, useState } from "react"
import { Form, Row, Col, Button } from "react-bootstrap"
import { changeTelegramProfile, createTelegramProfile } from "../http/telegramAPI"

const FormTelegramProfile = ({
    telegramProfile,
    isAdd,
    updateProfiles,
    telegramProfiles,
    setTelegramProfiles,
}) => {
    const [phone, setPhone] = useState(
        (telegramProfile && telegramProfile.phone) || ""
    )
    const [sessionName, setSessionName] = useState(
        (telegramProfile && telegramProfile.session_name) || ""
    )
    const [apiId, setApiId] = useState(
        (telegramProfile && telegramProfile.api_id) || ""
    )
    const [apiHash, setApiHash] = useState(
        (telegramProfile && telegramProfile.api_hash) || ""
    )
    const [isActive, setIsActive] = useState(
        (telegramProfile && telegramProfile.is_active) || false
    )
    const [buttonVisible, setButtonVisible] = useState(false)

    useEffect(() => {
        updateProfiles()
    }, [])

    const onChangePhone = (event) => {
        setPhone(event.target.value)
        setButtonVisible(true)
    }

    const onChangeSessionName = (event) => {
        setSessionName(event.target.value)
        setButtonVisible(true)
    }

    const onChangeApiId = (event) => {
        setApiId(event.target.value)
        setButtonVisible(true)
    }

    const onChangeApiHash = (event) => {
        setApiHash(event.target.value)
        setButtonVisible(true)
    }

    const onChangeIsActive = (event) => {
        setIsActive(true)
        setButtonVisible(true)
    }

    const onOffActive = (event) => {
        setIsActive(false)
        console.log("Отключение всех профилей")
        setTelegramProfiles(
            telegramProfiles.map(async (telegramProfile) => {
                console.log("telegramProfile", telegramProfile)
                try {
                    const data = await changeTelegramProfile({
                        ...telegramProfile,
                        isActive: false,
                    })
                    return data
                } catch (error) {
                    return console.error(error)
                }
            })
        )
    }

    const editTelegramProfile = async () => {
        try {
            if (!telegramProfile) {
                console.log("Добавление данных")
                console.log(phone, sessionName, apiId, apiHash)
                let inputApiId
                try {
                    inputApiId = parseInt(apiId)
                } catch {
                    throw { message: "Идентификатор приложения должен состоять из цифр"}
                }
                const data = await createTelegramProfile({
                    phone: phone,
                    sessionName: sessionName,
                    apiId: inputApiId,
                    apiHash: apiHash,
                })
                if (data.error) {
                    throw data
                }
                console.log(data)
                setPhone("")
                setSessionName("")
                setApiId("")
                setApiHash("")
                setTelegramProfiles([...telegramProfiles, data.map(d => {
                    return {
                        ...d,
                        apiId: d.api_id.toString()
                    }
                })])
            } else {
                console.log("Изменение данных")
                let inputApiId
                try {
                    inputApiId = parseInt(apiId)
                } catch {
                    throw { message: "Идентификатор приложения должен состоять из цифр"}
                }
                const newProfile = {
                    id: telegramProfile.id,
                    phone: phone,
                    sessionName: sessionName,
                    apiId: inputApiId,
                    isActive,
                }
                console.log("Новый профиль", newProfile)
                const data = await changeTelegramProfile(newProfile)
                if (data.error) {
                    throw data
                }
                // alert("Запись сохранена")
                setTelegramProfiles(
                    telegramProfiles.map((item) => {
                        return item.id ===
                            telegramProfile.id
                            ? newProfile
                            : item
                    })
                )
            }
        } catch (e) {
            console.error(e)
            alert(e.message)
        }
    }

    const buttonText = telegramProfile ? "Сохранить" : "Добавить"

    const button = buttonVisible ? (
        <Button
            className="mt-2 md-2"
            variant="outline-success"
            onClick={editTelegramProfile}
        >
            {buttonText}
        </Button>
    ) : (
        <></>
    )

    console.log("sessionName", sessionName)
    console.log("isActive", isActive)

    // кнопка активации профиля
    const radio = !isAdd ? (
        // для изменяемых профилей
        <Col>
            <Form.Check
                type="radio"
                checked={isActive}
                id="is_active"
                name="is_active"
                label="Активировать"
                onChange={onChangeIsActive}
            />
        </Col>
    ) : (
        // для добавляемого профиля
        <></>
    )

    // кнопка отключения профилей почты
    const radioOff = isAdd ? (
        <></>
    ) : (
        <Row className="mt-5">
            <Col md="8"></Col>
            <Col md="3">
                <Form.Check
                    type="radio"
                    checked={
                        !telegramProfiles.find(
                            (telegramProfile) => telegramProfile.is_active
                        )
                    }
                    id="is_active"
                    name="is_active"
                    label="Отключить все"
                    onChange={onOffActive}
                />
            </Col>
        </Row>
    )

    return (
        <Form>
            <Row>
                <Col>
                    <Form.Control
                        value={sessionName}
                        type="email"
                        onChange={onChangeSessionName}
                        placeholder={"Введите имя сессии"}
                    />
                </Col>
                <Col>
                    <Form.Control
                        value={apiId}
                        type="password"
                        onChange={onChangeApiId}
                        placeholder={"Введите идентификатор приложения"}
                    />
                </Col>
                <Col>
                    <Form.Control
                        value={apiHash}
                        type="password"
                        onChange={onChangeApiHash}
                        placeholder={"Введите хэш-ключ приложения"}
                    />
                </Col>
                {radio}
            </Row>
            <Row className="mt-1">
                <Col md="8"></Col>
                <Col md="3">{button}</Col>
            </Row>
            {radioOff}
        </Form>
    )
}

export default FormTelegramProfile
