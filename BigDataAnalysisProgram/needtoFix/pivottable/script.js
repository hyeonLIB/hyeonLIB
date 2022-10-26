const draggables = document.querySelectorAll('.draggable')
const containers = document.querySelectorAll('.container')

// var arr1 = ["age", "incm","sex"]
// var arr2 = ["1", "2", "3"]


// // create nodes and put them all in the each container
// containers.forEach(container => {
//     const a = checkEmptyContainer(container, arr1)
//     if (a == false) {
//         console.log(false)
//         const newItem = document.createElement("draggable")
//         container.appendChild(newItem)
//     } else {
//         console.log(true)
//         const newItem = document.createElement("draggable")
//         container.appendChild(newItem)
//     }
// })
console.log(containers.length)

draggables.forEach(draggable => {
    draggable.addEventListener('dragstart', () => {
      draggable.classList.add('dragging')
    })
  
    draggable.addEventListener('dragend', () => {
      draggable.classList.remove('dragging')
    })
})
  
containers.forEach(container => {
    container.addEventListener('dragover', e => {
      e.preventDefault()
      const afterElement = getDragAfterElement(container, e.clientY)
      const draggable = document.querySelector('.dragging')
      const newItem = document.createElement("draggable")
      container.appendChild(newItem)
      if (afterElement == null) {
        container.appendChild(draggable)
      } else {
        container.insertBefore(draggable, afterElement)
      }
    })
})
  
// function checkEmptyContainer(container, arr) {
//     if(document.querySelector('.container:empty')) {
//         return true
//     } else{
//         // container.appendChild(arr[1])
//         return false
//     }
// }


function getDragAfterElement(container, y) {
  const draggableElements = [...container.querySelectorAll('.draggable:not(.dragging)')]

  return draggableElements.reduce((closest, child) => {
    const box = child.getBoundingClientRect()
    const offset = y - box.top - box.height / 2
    if (offset < 0 && offset > closest.offset) {
      return { offset: offset, element: child }
    } else {
      return closest
    }
  }, { offset: Number.NEGATIVE_INFINITY }).element
}