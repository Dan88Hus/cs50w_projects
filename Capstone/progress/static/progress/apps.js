const addBtns = document.querySelectorAll('.add-btn:not(.solid)');
const saveItemBtns = document.querySelectorAll('.solid');
const addItemContainers = document.querySelectorAll('.add-container');
const addItems = document.querySelectorAll('.add-item');
// Item Lists
const listColumns = document.querySelectorAll('.drag-item-list');
const startedList = document.getElementById('started-list');
const proceedingList = document.getElementById('proceeding-list');
const completedList = document.getElementById('completed-list');
const cancelledList = document.getElementById('cancelled-list');
// Drag Functionality
let draggedItem;
let currentColumn;
let startedArray = {};
let proceedingArray = {};
let completedArray = {};
let cancelledArray = {};
let stfnew_value = false;
let ptfnew_value =false;
let cotfnew_value = false;
let catfnew_value = false;
let itemText = '';




//calling load_stage which is getting data from db
load_stage_started();
load_stage_proceeding();
load_stage_completed();
load_stage_cancelled();

//getting stages as json array from db
async function load_stage_started(){
  try{
    const response = await fetch("/load_stage");
    const data = await response.json();
    // console.log(data.cancelled);
    const started = await data.started.forEach(starteditem => {
      const liEl = document.createElement('li');
      liEl.className = 'drag-item';
      liEl.draggable = true;
      liEl.textContent = starteditem.started;
      liEl.setAttribute('ondragstart', 'drag(event)');
      startedList.appendChild(liEl);
    });
  }catch (error){
    console.log('whoops, error by fetching',error)
  }
}

//getting proceeding stages as json array from db
async function load_stage_proceeding(){
  try{
    const response = await fetch("/load_stage");
    const data = await response.json();
    // console.log(data.cancelled);
    const proceeding = await data.proceeding.forEach(proceedingitem => {
      const liEl = document.createElement('li');
      liEl.className = 'drag-item';
      liEl.draggable = true;
      liEl.textContent = proceedingitem.proceeding;
      liEl.setAttribute('ondragstart', 'drag(event)');
      proceedingList.appendChild(liEl);
    });
  }catch (error){
    console.log('whoops, error by fetching',error)
  }
}

//getting completed stages as json array from db
async function load_stage_completed(){
  try{
    const response = await fetch("/load_stage");
    const data = await response.json();
    // console.log(data.cancelled);
    const completed = await data.completed.forEach(completeditem => {
      const liEl = document.createElement('li');
      liEl.className = 'drag-item';
      liEl.draggable = true;
      liEl.textContent = completeditem.completed;
      liEl.setAttribute('ondragstart', 'drag(event)');
      completedList.appendChild(liEl);
    });
  }catch (error){
    console.log('whoops, error by fetching',error)
  }
}

//getting cancelled stages as json array from db
async function load_stage_cancelled(){
  try{
    const response = await fetch("/load_stage");
    const data = await response.json();
    // console.log(data.cancelled);
    const cancelled = await data.cancelled.forEach(cancelleditem => {
      const liEl = document.createElement('li');
      liEl.className = 'drag-item';
      liEl.draggable = true;
      liEl.textContent = cancelleditem.cancelled;
      liEl.setAttribute('ondragstart', 'drag(event)');
      cancelledList.appendChild(liEl);

    });
  }catch (error){
    console.log('whoops, error by fetching',error)
  }
}

// when Item starts Dragging
function drag(e){
  draggedItem = e.target;
  // console.log('draggedItem:',draggedItem)
}

// Column Allows for Item to Drop
function allowDrop(e){
  e.preventDefault();

}
//when Item Enters Column Area
function dragEnter(column){
  listColumns[column].classList.add('over');
  currentColumn = column;
}
// Dropping Item in Column
function drop(e){
  e.preventDefault();
  // Remove Background Color/Padding
  listColumns.forEach((column) => {
    column.classList.remove('over');
  });
  // Add Item to Column
  const parent = listColumns[currentColumn];
  parent.appendChild(draggedItem);
  rebuildArrays();
}
// Column Allow for Item to Drop
function rebuildArrays(){
  // for started array
  for (let i=0; i< startedList.children.length; i++){
    stfnew_value = false;
    fetch(`/startedNew_stage`, {
      method:'PUT',
      headers: {
        'X-CSRFToken': getCookie("csrftoken")
        }, body: body = JSON.stringify({
          started: startedList.children[i].textContent,
          slength: startedList.children.length,
          stfnew_value: true,
        })
      })  
      // .then(response => response.json())
      // .then(response => console.log(response))
      // console.log('body', body)
  }
  // for proceeding Array
  for (let i=0; i< proceedingList.children.length; i++){
    ptfnew_value = false;
    fetch(`/proceedingNew_stage`, {
      method:'PUT',
      headers: {
        'X-CSRFToken': getCookie("csrftoken")
        }, body: body = JSON.stringify({
          proceeding: proceedingList.children[i].textContent,
          plength: proceedingList.children.length,
          ptfnew_value: true,
        })
      })  
      // .then(response => response.json())
      // .then(response => console.log(response))
      // console.log('body', body)
  }
  
  // for completed Array
  for (let i=0; i< completedList.children.length; i++){
    cotfnew_value = false;
    fetch(`/completedNew_stage`, {
      method:'PUT',
      headers: {
        'X-CSRFToken': getCookie("csrftoken")
        }, body: body = JSON.stringify({
          completed: completedList.children[i].textContent,
          colength: completedList.children.length,
          cotfnew_value: true,
        })
      })  
      // .then(response => response.json())
      // .then(response => console.log(response))
      // console.log('body', body)
  }

  // for cancelled Array
  for (let i=0; i< cancelledList.children.length; i++){
    catfnew_value = false;
    fetch(`/cancelledNew_stage`, {
      method:'PUT',
      headers: {
        'X-CSRFToken': getCookie("csrftoken")
        }, body: body = JSON.stringify({
          cancelled: cancelledList.children[i].textContent,
          calength: cancelledList.children.length,
          catfnew_value: true,
        })
      })  
      // .then(response => response.json())
      // .then(response => console.log(response))
      // console.log('body', body)
  }

}

function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(';').shift();
}

  // to save new Item fecth
function saveitemfetch(column){
  // console.log(itemobject);
    fetch(`/new_item_save`, {
      method:'PUT',
      headers: {
        'X-CSRFToken': getCookie("csrftoken")
        }, body: body = JSON.stringify({
          data: addItems[column].textContent,
          column: column,
          // itemtfnew_value: true,
          // itemobject: itemobject,
          // itemfield: itemfield,
          // itemnew_value: itemnew_value,
        })
      })  
      .then(response => response.json())
      .then(response => console.log(response))
      addItems[column].textContent = ""
      location.reload()
      // console.log('body', body)
}

//Add to Column List, reset TextBox
function addToColumn(column){
  
  switch (column) {
    case 0:
      // itemobject = "Started";
      // itemfield = "started";
      // itemnew_value = "stfnew_value";
      saveitemfetch(column);
      // console.log("started");
      break;
    case 1:
      // itemobject = "Proceeding";
      // itemfield = "proceeding";
      // itemnew_value = "ptfnew_value";
      saveitemfetch(column);
      // console.log("proceeding");
      break;
    case 2:
      // itemobject = "Completed";
      // itemfield = "completed";
      // itemnew_valuev = "cotfnew_value";
      saveitemfetch(column);
      // console.log("completed");
      break;
    case 3:
      // itemobject = "Cancelled";
      // itemfield = "cancelled";
      // itemnew_value = "catfnew_value";
      saveitemfetch(column);
      // console.log("cancelled");
      break;
    default:
      console.log("whoops, look at switch");
      break;
  }
}
// Add functionality
function showInputBox(column) {
  addBtns[column].style.visibility = 'hidden';
  saveItemBtns[column].style.display = 'flex';
  addItemContainers[column].style.display = 'flex';


}

// Hide Item Input Box
function  hideInputBox(column){
  addBtns[column].style.visibility = 'visible';
  saveItemBtns[column].style.display = 'none';
  addItemContainers[column].style.display = 'none';
  // function to save item in the column
  addToColumn(column);

}