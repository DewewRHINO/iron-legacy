document.addEventListener("DOMContentLoaded", function () {
  var endDate = new Date("2026-04-13T00:00:00Z");
  function updateCountdown() {
    var now = new Date();
    var diff = endDate - now;
    if (diff < 0) diff = 0;
    var days = Math.floor(diff / (1000 * 60 * 60 * 24));
    var hours = Math.floor((diff / (1000 * 60 * 60)) % 24);
    var minutes = Math.floor((diff / (1000 * 60)) % 60);
    var seconds = Math.floor((diff / 1000) % 60);
    document.getElementById("countdown-days").textContent = days;
    document.getElementById("countdown-hours").textContent = hours;
    document.getElementById("countdown-minutes").textContent = minutes;
    document.getElementById("countdown-seconds").textContent = seconds;
  }
  updateCountdown();
  setInterval(updateCountdown, 1000);
});
