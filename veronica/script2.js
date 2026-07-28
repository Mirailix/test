class Timer {
  constructor() {
      this.hoursInput = document.getElementById('hours');
      this.minutesInput = document.getElementById('minutes');
      this.secondsInput = document.getElementById('seconds');
      this.display = document.getElementById('timer-display');
      this.alarmSound = document.getElementById('alarm-sound');
      this.startButton = document.getElementById('start-button');
      this.intervalId = null;

      this.startButton.addEventListener('click', () => this.startTimer());
  }

  startTimer() {
      let totalSeconds = 
          parseInt(this.hoursInput.value || 0) * 3600 +
          parseInt(this.minutesInput.value || 0) * 60 +
          parseInt(this.secondsInput.value || 0);

      if (totalSeconds <= 0) {
          alert("Please set a time greater than 0 seconds.");
          return;
      }

      this.updateDisplay(totalSeconds);

      this.intervalId = setInterval(() => {
          totalSeconds--;
          this.updateDisplay(totalSeconds);

          if (totalSeconds <= 0) {
              clearInterval(this.intervalId);
              this.alarmSound.play();
          }
      }, 1000);
  }

  updateDisplay(totalSeconds) {
      const hours = Math.floor(totalSeconds / 3600);
      const minutes = Math.floor((totalSeconds % 3600) / 60);
      const seconds = totalSeconds % 60;

      this.display.textContent = 
          String(hours).padStart(2, '0') + ':' +
          String(minutes).padStart(2, '0') + ':' +
          String(seconds).padStart(2, '0');
  }
}

document.addEventListener('DOMContentLoaded', () => {
  new Timer();
});
