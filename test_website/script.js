// Inicialitzar el comptador a 23:59:59
let countdownTime = 23 * 3600 + 59 * 60 + 59; // 23 hores, 59 minuts i 59 segons

function updateCountdown() {
  let hours = Math.floor(countdownTime / 3600);
  let minutes = Math.floor((countdownTime % 3600) / 60);
  let seconds = countdownTime % 60;

  // Mostrar el comptador
  document.getElementById("countdown").textContent = `${hours}:${minutes}:${seconds}`;

  // Descomptar cada segon
  if (countdownTime > 0) {
    countdownTime--;
  } else {
    document.getElementById("countdown").textContent = "Time's up!";
  }
}

// Actualitzar el comptador cada segon
setInterval(updateCountdown, 1000);

// Funció per copiar el text al portapapers
document.getElementById('bank-account').addEventListener('click', function() {
    // Creem un element temporal per copiar el text
    const tempInput = document.createElement('input');
    tempInput.value = this.textContent; // Assignem el valor del codi bancari
    document.body.appendChild(tempInput); // Afegim l'element temporal al cos del document
    tempInput.select(); // Seleccionem el text
    document.execCommand('copy'); // Copiem el text al portapapers
    document.body.removeChild(tempInput); // Eliminem l'element temporal
  
    // Mostrem el missatge de la broma
    const prankMessage = document.getElementById('prank-message');
    prankMessage.style.display = 'block';
    
    // Opcionalment, es pot ocultar el missatge després de 3 segons
    setTimeout(() => {
      prankMessage.style.display = 'none';
    }, 3000);
  });