function sendNotification(type, text) {
    let notificationBox = document.querySelector(".notification-box");
    const alerts = {
        info: {
            icon: `<svg class="notif-ico" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
  </svg>`,
            color: "blue-500"
        },
        error: {
            icon: `<svg xmlns="http://www.w3.org/2000/svg" class="notif-ico" fill="none" viewBox="0 0 24 24" stroke="currentColor">
    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
  </svg>`,
            color: "red-500"
        },
        warning: {
            icon: `<svg xmlns="http://www.w3.org/2000/svg" class="notif-ico" fill="none" viewBox="0 0 24 24" stroke="currentColor">
    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
  </svg>`,
            color: "yellow-500"
        },
        success: {
            icon: `<svg xmlns="http://www.w3.org/2000/svg" class="notif-ico" fill="none" viewBox="0 0 24 24" stroke="currentColor">
    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
  </svg>`,
            color: "green-500"
        }
    };
    let component = document.createElement("div");
    component.className = `notif-txt opacity-0 bg-${alerts[type].color}`;
    component.innerHTML = `${alerts[type].icon}<p class='p-notif'>${text}</p>`;



    notificationBox.appendChild(component);
    setTimeout(() => {
        component.classList.remove("opacity-0");
        component.classList.add("opacity-1");
    }, 1); //1ms For fixing opacity on new element
    setTimeout(() => {
        component.classList.remove("opacity-1");
        component.classList.add("opacity-0");
        //component.classList.add("-translate-y-80"); //it's a little bit buggy when send multiple alerts
        component.style.margin = 0;
        component.style.padding = 0;
    }, 5000);
    setTimeout(() => {
        component.style.setProperty("height", "0", "important");
    }, 5100);
    setTimeout(() => {
        notificationBox.removeChild(component);
    }, 5700);
    //If you can do something more elegant than timeouts, please do, but i can't
}


function validateAddForm() {
    var x = document.forms["AddForm"]["name"].value;
    if (x == null || x == "") {
        sendNotification('error', 'Name must be filled out.');
        return false;
    }

    var x = document.forms["AddForm"]["username"].value;
    if (x == null || x == "") {
        sendNotification('error', 'Username must be filled out.');
        return false;
    }

    var x = document.forms["AddForm"]["password"].value;
    if (x == null || x == "") {
        sendNotification('error', 'Password must be filled out.');
        return false;
    }
}

function deletePass() {
    var x = document.getElementsByClassName("checkmark");
    const r = [];
    for (let i = 0; i < x.length; i++) {
      if (x[i].checked) {
        r.push(x[i].id);
      }
    }
    if (r === undefined || r.length == 0) {
      sendNotification('error','Please select at least one record to be deleted.')
    }
    else{
      document.getElementById("delete-form-input").value = "['" + r.join("','") + "']";
      document.getElementById("delete-form").submit();
    }
  }
  function openNav() {
    document.getElementById("mySidenav").style.width = "250px";
    document.getElementById("main").style.marginLeft = "250px";
  }
  function closeNav() {
    document.getElementById("mySidenav").style.width = "0";
    document.getElementById("main").style.marginLeft = "0";
  }
  function CopyText(inp) {
    navigator.clipboard.writeText(inp);
  }
  function showPass(id) {
    var x = document.getElementById(id);
    var y = document.getElementById(id + "_b");
    if (x.type == "password") {
      x.type = "text";
      y.classList.remove("fa-eye");
      y.classList.add("fa-eye-slash");

    } else {
      x.type = "password";
      y.classList.remove("fa-eye-slash");
      y.classList.add("fa-eye");
    }
  }