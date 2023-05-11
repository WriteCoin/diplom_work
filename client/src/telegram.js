import React from "react"
import "./telegram.css"

const data = [
    {
        label: "Мессенджеры",
        image: undefined,
        children: [
            {
                label: "Вконтакте",
                image: "/favicon-vk-32x32.png",
            },
            {
                label: "Telegram",
                image: "/favicon-telegram-32x32.png",
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
            },
            {
                label: "Yandex",
                image: "/favicon-yandex-32x32.png",
            },
        ],
    },
]

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
        console.log(this.props)
        const { label, children } = this.props
        const { isExpanded } = this.state

        const image = this.props.image && <img alt="" src={this.props.image} />

        const renderChildren = (children) => {
            if (isExpanded) {
                return <Tree data={children}></Tree>
            }
        }

        return (
            <li
                className={`fa fa-${isExpanded ? "minus" : "plus"}`}
                key={label}
                onClick={this.handleExpand}
            >
                <div>
                    {image}
                    <span>{label}</span>
                    {renderChildren(children)}
                </div>
            </li>

            // <div
            //     className={`fa fa-${isExpanded ? "minus" : "plus"}`}
            //     onClick={this.handleExpand}
            // >
            //     {image}
            //     <span>{label}</span>
            //     {/* {isExpanded && children} */}
            // </div>
        )
        // return <p>Узел</p>
    }
}

class Tree extends React.Component {
    render() {
        const { data } = this.props
        console.log("Tree", data)
        const renderChildren = (nodes) => {
            return (
                <ul>
                    {nodes.map((node) => {
                        return (
                            <TreeNode {...node} />
                            // <li key={node.label}>
                            //     <TreeNode {...node} />
                            //     {node.children && renderChildren(node.children)}
                            // </li>
                        )
                    })}
                </ul>
            )
        }
        return renderChildren(data)
    }
}

export class Telegram extends React.Component {
    render() {
        return (
            <Tree data={data}></Tree>
            // <h2>Это Telegram</h2>
            // <MyClass></MyClass>
        )
    }
}
// class MyClass extends React.Component {
//     constructor(props) {
//         super(props)
//         this.state = { count: 0 }
//         this.handleClick = this.handleClick.bind(this)
//     }

//     handleClick() {
//         this.setState({ count: this.state.count + 1 })
//     }

//     render() {
//         return (
//             <div>
//                 <p>Count: {this.state.count}</p>
//                 <button onClick={this.handleClick}>Increment</button>
//             </div>
//         )
//     }
// }

