const app = document.querySelector(".app")
const row1 = document.querySelector(".row1")
const row2 = document.querySelector(".row2")

function NewItem(column) {
    const newItem = document.createElement("p")
    newItem.classList.add("item")
    newItem.draggable = true
    newItem.id = column
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
    horizontal_container.classList.add("container")
    horizontal_container.classList.add("hcontainer")
    col_selector.classList.add("container")
    col_selector.classList.add("scontainer")
    vertical_container.classList.add("container")
    vertical_container.classList.add("vcontainer")
    graph_container.classList.add("gcontainer")

    emptyspace.id="empty"
    dpdnComponent.id="dropdown"
    horizontal_container.id="hcontainer"
    col_selector.id="scontainer"
    vertical_container.id="vcontainer"
    graph_container.id="gcontainer"
    
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

const items = document.querySelectorAll('.item')
const containers = document.querySelectorAll('.container')

items.forEach(item => {
    item.addEventListener('dragstart', () =>{
        item.classList.add('dragging')
    })
    item.addEventListener('dragend', () =>{
        item.classList.remove('dragging')
    })
})

containers.forEach(container => {
    container.addEventListener('dragover', e => {
        e.preventDefault()
        const afterElement = getDragAfterElement(container, e.clientY)
        const dragging = document.querySelector('.dragging')
        const newItem = document.createElement('item')
        if (container.id == 'hcontainer' && dragging.classList.length == 2) {
            dragging.classList.add('horizontal')
        } else if (container.id != 'hcontainer' && dragging.classList.length==3) {
            dragging.classList.remove('horizontal')
        }

        container.appendChild(newItem)
        if (afterElement == null) {
            container.appendChild(dragging)
        } else {
            container.insertBefore(dragging, afterElement)
        }
    })
})

function getDragAfterElement(container,y) {
    const draggableElements = [...container.querySelectorAll('.item:not(.dragging)')]

    return draggableElements.reduce((closest, child) => {
        const box = child.getBoundingClientRect()
        const offset = y - box.top - box.height / 2
        if (offset<0 && offset > closest.offset) {
            return { offset: offset, element: child }
        } else {
            return closest
        }
    }, { offset: Number.NEGATIVE_INFINITY }).element
}