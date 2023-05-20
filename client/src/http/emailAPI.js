import { $host } from "./index";

export const fetchEmailServices = async () => {
    const {data} = await $host.get('email_services')
    return data
}

export const updateEmailService = async (id, enabled) => {
    const {data} = await $host.post('email_service/' + id, { params: {
        enabled
    }})
    return data
}

export const fetchEmailProfiles = async () => {
    const {data} = await $host.get('email_profiles')
    return data
}

export const createEmailProfile = async (profile) => {
    const {data} = await $host.post('email_profile', {
        params: profile
    })
    return data
}

export const changeEmailProfile = async (profile) => {
    console.log(profile)
    const {data} = await $host.post('change_email_profile/' + profile.id, {
        params: profile
    })
    return data
}

export const fetchOneEmailProfile = async (id) => {
    const {data} = await $host.get('email_profile/' + id)
    return data
}