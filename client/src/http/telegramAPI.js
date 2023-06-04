import { $host } from "./index"

export const createTelegramProfile = async (profile) => {
    const { data } = await $host.post("telegram_profile", {
        params: profile,
    })
    return data
}

export const changeTelegramProfile = async (profile) => {
    console.log(profile)
    const { data } = await $host.post("change_telegram_profile/" + profile.id, {
        params: profile,
    })
    return data
}