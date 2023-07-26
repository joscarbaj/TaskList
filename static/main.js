document.addEventListener("DOMContentLoaded", function() {
  var text = document.querySelector(".div__list-form-task");
  var containerDiv = document.querySelector(".section");
  var submit = document.querySelector(".submit").addEventListener("click", (e) => {
    e.preventDefault();
    let newValue = text.value;
    text.value = "";
    fetch("/add-task", {
      method: "POST",
      headers: { 'Content-type': 'application/x-www-form-urlencoded' },
      body: `nuevo_contenido=${encodeURIComponent(newValue)}`
    })
      .then(obtenerContent);
  });

  function obtenerContent() {
    fetch("/get-content")
      .then((data) => data.json())
      .then((result) => {
        innerContent = ``
        result.forEach((x, i) => {
          innerContent += `<section class="section__flex">
         <div class="div__info-container">
             <h2  class="grid-items">N°</h2>
             <h2 class="grid-items">Task</h2>
             <h2 class="grid-items">State</h2>
       
                 <p class="grid-items "> ${x[0]} -</p>
                 <p class="grid-items ">  ${x[1]} </p>
                 <p  data-id="${x[0]}" class="grid-items div__info-container-state"> ${x[2]} </p>
     
         </div>
     </section>`
        });
        containerDiv.innerHTML = innerContent; // Agrega los elementos generados dentro del div

        var stateButtons = document.querySelectorAll(".div__info-container-state");
        stateButtons.forEach(function(button) {
          var stateValue = button.textContent.trim();

          if (stateValue == "PENDING") {
            button.classList.add("PENDING");
          } else if (stateValue == "DONE") {
            button.classList.add("DONE");
          }

          button.addEventListener("click", function() {
            var id = button.getAttribute("data-id");
          
            let data = {
              id: id
            };

            fetch("/change-state/" + id, {
              method: "POST",
              headers: {
                "Content-Type": "application/json"
              },
              body: JSON.stringify(data)
            })
              .then(response => response.json())
              .then(responseData => {
                console.log(responseData);
                // Aquí puedes hacer algo con la respuesta del servidor, si es necesario
              })
              .catch(error => {
                console.error("Error en la solicitud fetch:", error);
              });

              obtenerContent()
          });
        });
      });
  }

  obtenerContent();
  setInterval(obtenerContent, 1000);
});
