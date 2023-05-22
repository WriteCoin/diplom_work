// import { fetchEmailProfiles } from "./http/emailAPI";
// const {fetchEmailProfiles} = require('./http/emailAPI')

// Обработка сообщения от основного потока в веб воркере
export function updateMessages() {
    // const { message } = event.data;
    // console.log('Received in worker:', message);

    // цикличное обновление
    // setInterval(async () => {
    //     // try {
    //     //     const profilesData = await fetchEmailProfiles(true)

    //     //     console.log(profilesData)

    //     //     if (profilesData.enabled) {

    //     //     }
    //     // } catch (e) {
    //     //     console.error(e.message)
    //     // }

    //     postMessage({messages: "Результат"})

    // }, 5000)

    // const result = heavyOperation(message);

    // // Отправка результата в основной поток
    // postMessage({result});

    return "Messages"
}
