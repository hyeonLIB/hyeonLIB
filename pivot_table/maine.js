const app = document.querySelector(".app")
const row1 = document.querySelector(".row1")
const row2 = document.querySelector(".row2")

function NewItem(column) {
    const newItem = document.createElement("div")
    newItem.classList.add("item")
    newItem.textContent = column
    const col_selector = document.querySelector(".scontainer")
    col_selector.appendChild(newItem)
}

function Frame() {
    const emptyspace = document.createElement("span")
    const dpdnComponent = document.createElement("span")
    const horizontal_container = document.createElement("span")
    const col_selector = document.createElement("span")
    const vertical_container = document.createElement("span")
    const graph_container = document.createElement("span")
    
    emptyspace.classList.add("empty")
    dpdnComponent.classList.add("dropdown")
    horizontal_container.classList.add("hcontainer")
    col_selector.classList.add("scontainer")
    vertical_container.classList.add("vcontainer")
    graph_container.classList.add("gcontainer")
    
    row1.appendChild(emptyspace)
    row1.appendChild(dpdnComponent)
    row1.appendChild(horizontal_container)
    row2.appendChild(col_selector)
    row2.appendChild(vertical_container)
    row2.appendChild(graph_container)
    
    app.appendChild(row1)
    app.appendChild(row2)
}

function CheckEmptyContainer(arr) {
    if (document.querySelector('.scontainer:empty')) {
        for (i=0; i<arr.length; i++) {
            NewItem(arr[i])
        }
    } else {
        console.log("false")
    }
}

Frame()
var arr1 = ["age", "incm","sex","age", "incm","sex","age", "incm","sex"]

CheckEmptyContainer(arr1)