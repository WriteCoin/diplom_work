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
        setIsActive(event.target.value)
        setButtonVisible(true)
    }

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

    const radio = !email_id ? (
        <Col>
            <Form.Check 
                type="radio"
                value={isActive ? '1' : '0'}
                id="is_active"
                label="Активировать"
                onChange={onChangeIsActive}
            />
        </Col>
    ) : (
        <></>
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
                <Col md="7"></Col>
                <Col md="2">{button}</Col>
            </Row>
        </Form>
    )
}

export default FormEmailProfile
