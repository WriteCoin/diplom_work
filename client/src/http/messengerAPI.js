import { $host } from "./index"

export const fetchMessengers = async () => {
    const { data } = await $host.get("messengers")
    return data
}

export const updateMessenger = async (id, enabled, limit, msUpdate) => {
    const { data } = await $host.post("messenger/" + id, {
        params: {
            enabled,
            limit,
            ms_update: msUpdate
        },
    })
    return data
}