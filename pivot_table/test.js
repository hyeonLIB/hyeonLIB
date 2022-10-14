const row1 = document.querySelector(".row1")

function createDropDownItem(element, id) {
    const dpdn_item = document.createElement("a")
    dpdn_item.href = "#"
    dpdn_item.textContent=element
    
    const dropdown = document.querySelector("#"+id+"-content")
    dropdown.appendChild(dpdn_item)
}

function createDropDown(id) {
    // gelements outside of this function
    const elements = ["Box Plot", "Scatter Plot", "Histogram", "Line Plot"]
    
    // dropdown component
    const dropdown = document.createElement("div")
    dropdown.classList.add("dropdown")
    dropdown.classList.add("dropdown-"+id)
    dropdown.id = id
    row1.appendChild(dropdown)

    // dropdown button
    const dpdn_button = document.createElement("button")
    dpdn_button.id = id
    dpdn_button.textContent= id+" selection"
    dpdn_button.classList.add("dpdn-button")
    dpdn_button.classList.add("dpdn-button-"+id)
    dpdn_button.onclick = "clickDropDown"
    dropdown.appendChild(dpdn_button)

    dpdn_content = document.createElement("div")
    dpdn_content.classList.add("dropdown-content")
    dpdn_content.classList.add("dropdown-content-"+id)
    dpdn_content.id = id + "-content"
    dropdown.appendChild(dpdn_content)
    for (var i = 0; i < elements.length; i++) {
        createDropDownItem(elements[i], id)
    }

    return dropdown
}

function myFunction() {
    // document.querySelector(".dropdown-content").classList.toggle("show");
    document.getElementById("graph-content").classList.toggle("show");
    console.log("hey")
}
  
// Close the dropdown menu if the user clicks outside of it
window.onclick = function(event) {
    if (!event.target.matches('.dpdn-button')) {
        var dropdowns = document.getElementsByClassName("dropdown-content");
        var i;
        for (i = 0; i < dropdowns.length; i++) {
            var openDropdown = dropdowns[i];
            if (openDropdown.classList.contains('show')) {
            openDropdown.classList.remove('show');
            }
        }
    }
}

createDropDown("graph")