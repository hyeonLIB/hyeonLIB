// frame
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

function createDropDownItem(dropdown_content, element, component) {
    const dropdown_item = document.createElement("a")
    dropdown_item.href = "#"
    dropdown_item.id = "dropdown-item-"+component+"-"+element
    dropdown_item.textContent=element
    
    dropdown_content.appendChild(dropdown_item)
}

function createDropDown(component) {
    // gelements outside of this function
    const elements = ["Box Plot", "Scatter Plot", "Histogram", "Line Plot"]
    
    // dropdown component
    const dropdown = document.createElement("div")
    dropdown.classList.add("dropdown")
    dropdown.id = "dropdown-"+component
    // row1.appendChild(dropdown) //

    // dropdown button
    const dropdown_button = document.createElement("button")
    dropdown_button.classList.add("dropdown")
    dropdown_button.classList.add("button")
    dropdown_button.id = "dropdown-button-"+component
    dropdown_button.textContent= component+" selection"
    
    const dropdown_content = document.createElement("div")
    dropdown_content.classList.add("dropdown")
    dropdown_content.classList.add("content")
    dropdown_content.id = "dropdown-content-"+component
    for (var i = 0; i < elements.length; i++) {
        createDropDownItem(dropdown_content, elements[i], component)
    }

    dropdown.appendChild(dropdown_button)
    dropdown.appendChild(dropdown_content)

    return dropdown
}

function Frame() {
    const emptyspace = document.createElement("span")
    const graphDropDown = createDropDown("graph")
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
    emptyspace.appendChild(graphDropDown)
    row1.appendChild(dpdnComponent)
    row1.appendChild(horizontal_container)
    row2.appendChild(col_selector)
    row2.appendChild(vertical_container)
    row2.appendChild(graph_container)
    
    app.appendChild(row1)
    app.appendChild(row2)
}

Frame()

// columns input
function CheckEmptyContainer(arr) {
    if (document.querySelector('.scontainer:empty')) {
        for (i=0; i<arr.length; i++) {
            NewItem(arr[i])
        }
    } else {
        console.log("false")
    }
}


var arr1 = ["age", "incm","sex","age", "incm","sex","age", "incm","sex"] // from json

CheckEmptyContainer(arr1)


// dropdown function
const buttonDropDowns = document.querySelectorAll(".dropdown.button")
buttonDropDowns.forEach(buttonDropDown => {
    buttonDropDown.addEventListener('click', () => {
        const content_dropdown = document.getElementById("dropdown-content-graph")
        content_dropdown.classList.toggle("show")
        const DropDownitems = document.querySelectorAll(".dropdown.content a")
        DropDownitems.forEach(DropDownItem => {
            DropDownItem.addEventListener('click', () => {
                console.log(DropDownItem.textContent)
                buttonDropDown.textContent = DropDownItem.textContent // to json + if condition
            })
        })
    })
})

window.onclick = function(event) {
    if (!event.target.matches('.dropdown.button')) {
        var dropdowns = document.querySelectorAll(".dropdown.content");
        dropdowns.forEach(dropdown => {
            if (dropdown.classList.contains('show')){
                dropdown.classList.remove('show')
            }
        })
    }
}


// Drag and drop function
const items = document.querySelectorAll('.item')
const containers = document.querySelectorAll('.container')

items.forEach(item => {
    item.addEventListener('dragstart', () =>{
        item.classList.add('dragging')
    })
    item.addEventListener('dragend', () =>{
        item.classList.remove('dragging')
        var Xelements = document.getElementById("hcontainer").getElementsByTagName("p");
        var Yelements = document.getElementById("vcontainer").getElementsByTagName("p");
        var Xarr = []
        var Yarr = []
        for (var i = 0; i < Xelements.length; i++) {
            Xarr.push(Xelements[i].id)
        }
        for (var i = 0; i < Yelements.length; i++) {
            Yarr.push(Yelements[i].id)
        }
        console.log(Xarr, Yarr) // to json
        // func for graphic
    })
})

containers.forEach(container => {
    container.addEventListener('dragover', e => {
        e.preventDefault()
        const afterElement = getDragAfterElement(container ,e.clientX, e.clientY)
        const dragging = document.querySelector('.dragging')
        if (container.id == 'hcontainer' && dragging.classList.length == 2) {
            dragging.classList.add('horizontal')
        } else if (container.id != 'hcontainer' && dragging.classList.length==3) {
            dragging.classList.remove('horizontal')
        }
        if (afterElement == null) {
            container.appendChild(dragging)
        } else {
            container.insertBefore(dragging, afterElement)
        }
    })
})

function getDragAfterElement(container,x,y) {
    const draggableElements = [...container.querySelectorAll('.item:not(.dragging)')]
    if (container.id =='hcontainer') {
        return draggableElements.reduce((closest, child) => {
            const box = child.getBoundingClientRect()
            const offset = x - box.left - box.right / 2
            if (offset<0 && offset > closest.offset) {
                return { offset: offset, element: child }
            } else {
                return closest
            }
        }, { offset: Number.NEGATIVE_INFINITY }).element
    } else {
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
}