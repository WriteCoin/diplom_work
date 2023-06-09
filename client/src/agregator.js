import React, { useEffect, useState } from "react"
import { fetchEmailServices } from "../http/emailAPI"

const data = [
    {
        label: "Мессенджеры",
        image: undefined,
        children: [
            {
                label: "Вконтакте",
                image: "/favicon-vk-32x32.png",
                enabled: true,
                limit: 100
            },
            {
                label: "Telegram",
                image: "/favicon-telegram-32x32.png",
                enabled: true,
                limit: 50
            },
        ],
    },
    {
        label: "Почты",
        image: undefined,
        children: [
            {
                label: "Gmail",
                image: "/favicon-gmail-32x32.png",
                enabled: true,
                limit: 100
            },
            {
                label: "Yandex",
                image: "/favicon-yandex-32x32.png",
                enabled: true,
                limit: 100
            },
        ],
    },
]

const data2 = {
    Мессенджеры: {
        image: undefined,
        children: {
            Вконтакте: {
                image: "/favicon-vk-32x32.png",
            },
            Telegram: {
                image: "/favicon-telegram-32x32.png",
            },
        },
    },
    Почты: {
        image: undefined,
        children: {
            Gmail: {
                image: "/favicon-gmail-32x32.png",
            },
            Yandex: {
                image: "/favicon-yandex-32x32.png",
            },
        },
    },
}

class TreeNode extends React.Component {
    constructor(props) {
        super(props)
        this.state = {
            isExpanded: true,
        }
        this.handleExpand = this.handleExpand.bind(this)
    }

    handleExpand() {
        // this.setState((prevState) => ({ isExpanded: !prevState.isExpanded }))
        this.setState({ isExpanded: !this.state.isExpanded })
    }

    render() {
        // console.log(this.props)
        // const [label, info] = this.props
        const { label, children } = this.props
        const { isExpanded } = this.state

        const image = this.props.image && <img alt="" src={this.props.image} />
        const treeElClass = image ? 'tree-el-with-image' : 'tree-el'
        
        const renderChildren = (children) => {
            if (isExpanded && Array.isArray(children)) {
                return <Tree data={children}></Tree>
            }
        }

        return (
            <div className="tree-node">
                <li
                    className={`fa fa-${isExpanded ? "minus" : "plus"}`}
                    key={label}
                    onClick={this.handleExpand}
                >
                    <div className={treeElClass}>
                        {image}
                        {/* <p>{label}</p> */}
                        {label}
                    </div>
                </li>

                <div className="tree-children">
                    {renderChildren(children)}
                </div>
            </div>
        )
    }
}

class Tree extends React.Component {
    constructor(props) {
        super(props)
    }

    render() {
        const { data, name } = this.props
        return (
            <div className="tree">
                <h3>{name}</h3>
                <ul>
                    {/* {data &&
                        Object.entries(data).map((node) => {
                            return <TreeNode {...node} />
                        })} */}
                    {Array.isArray(data) && data.map((node) => {
                        return <TreeNode {...node} />
                    })}
                </ul>
            </div>
        )
    }
}

// export function viewPanel() {
//     return <Panel data={data}></Panel>
// }

export function viewTree(name) {
    return (
        <div className="first-tree">
            <Tree data={data} name={name}></Tree>
        </div>
    )
}

// export class AgregatorApp extends React.Component {
//     constructor(props) {
//         super(props)
//         this.state = {
//             ...data2,
//         }

//     }

//     render() {
//         return (
//             <div></div>
//         )
//     }
// }
