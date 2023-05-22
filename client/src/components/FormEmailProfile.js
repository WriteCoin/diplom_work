import React, { useEffect, useState } from "react"
import { Form, Row, Col, Button } from "react-bootstrap"
import { changeEmailProfile, createEmailProfile } from "../http/emailAPI"

const FormEmailProfile = ({
    emailProfile,
    email_id,
    updateProfiles,
    emailProfiles,
    setEmailProfiles,
}) => {
    const [username, setUsername] = useState(
        (emailProfile && emailProfile.username) || ""
    )
    const [password, setPassword] = useState(
        (emailProfile && emailProfile.password) || ""
    )
    const [isActive, setIsActive] = useState(
        (emailProfile && emailProfile.is_active) || false
    )
    const [buttonVisible, setButtonVisible] = useState(false)

    useEffect(() => {
        updateProfiles()
    }, [])

    const onChangeUsername = (event) => {
        setUsername(event.target.value)
        setButtonVisible(true)
    }

    const onChangePassword = (event) => {
        setPassword(event.target.value)
        setButtonVisible(true)
    }

    const onChangeIsActive = (event) => {
        setIsActive(true)
        setButtonVisible(true)
    }

    const onOffActive = (event) => {
        setIsActive(false)
        console.log("Отключение всех профилей")
        setEmailProfiles(
            emailProfiles.map(async (emailProfile) => {
                console.log("emailProfile", emailProfile)
                try {
                    const data = await changeEmailProfile({
                        ...emailProfile,
                        id: emailProfile.email_profile_id,
                        isActive: false,
                    })
                    return data
                } catch (error) {
                    return console.error(error)
                }
            })
        )
    }
    // for (let index = 0; index < emailProfiles.length; index++) {
    //     const emailProfile = emailProfiles[index];
    //     const newEmailProfile = {...emailProfile, isActive: false}
    //     try {
    //         const data = await changeEmailProfile(newEmailProfile)
    //         if (data.error) {
    //             throw data
    //         }
    //     }
    // }

    const editEmailProfile = async () => {
        try {
            if (!emailProfile) {
                console.log("Добавление данных")
                console.log(username, password, email_id)
                const data = await createEmailProfile({
                    username,
                    password,
                    email_id,
                })
                if (data.error) {
                    throw data
                }
                console.log(data)
                setUsername("")
                setPassword("")
                setEmailProfiles([...emailProfiles, data])
            } else {
                console.log("Изменение данных")
                const newProfile = {
                    username,
                    password,
                    isActive,
                    id: emailProfile.email_profile_id,
                }
                console.log("Новый профиль", newProfile)
                const data = await changeEmailProfile(newProfile)
                if (data.error) {
                    throw data
                }
                // alert("Запись сохранена")
                setEmailProfiles(
                    emailProfiles.map((item) => {
                        return item.email_profile_id ===
                            emailProfile.email_profile_id
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

    const buttonText = emailProfile ? "Сохранить" : "Добавить"

    const button = buttonVisible ? (
        <Button
            className="mt-2 md-2"
            variant="outline-success"
            onClick={editEmailProfile}
        >
            {buttonText}
        </Button>
    ) : (
        <></>
    )

    console.log("username", username)
    console.log("isActive", isActive)

    // кнопка активации профиля
    const radio = !email_id ? (
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
    const radioOff = !email_id ? (
        <></>
    ) : (
        <Row className="mt-5">
            <Col md="8"></Col>
            <Col md="3">
                <Form.Check
                    type="radio"
                    checked={
                        !emailProfiles.find(
                            (emailProfile) => emailProfile.is_active
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
                        value={username}
                        type="email"
                        onChange={onChangeUsername}
                        placeholder={"Введите email"}
                    />
                </Col>
                <Col>
                    <Form.Control
                        value={password}
                        type="password"
                        onChange={onChangePassword}
                        placeholder={"Введите пароль"}
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

export default FormEmailProfile
