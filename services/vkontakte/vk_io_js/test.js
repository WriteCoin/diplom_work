let { VK } = require("vk-io")
let fs = require("fs")

const vk = new VK({
    token: process.env.TOKEN,
})

async function run() {
    // let response = await vk.api.wall.get({
    //     owner_id: 1,
    // })

    // let response = await vk.api.messages.getConversations({count: 5 })

    let response = await vk.api.account.getProfileInfo()

    // console.log(response)

    fs.writeFileSync("output.json", JSON.stringify(response), {
        encoding: "utf-8",
    })
}

run().catch(console.log)
