let circularProgress = document.querySelector(".circular-progress"),
    progressValue = document.querySelector(".progress-value");

let progressStartValue = 0,

    speed = 20;

function progressbar(progressEndValue) {
    let progress = setInterval(() => {
        progressStartValue += (progressEndValue > progressStartValue) ? 1 : (progressEndValue < progressStartValue) ? -1 : 0;

        progressValue.textContent = `${progressStartValue}%`
        circularProgress.style.background = `conic-gradient(#7d2ae8 ${progressStartValue * 3.6}deg, #ededed 0deg)`

        if (progressStartValue == progressEndValue) {
            clearInterval(progress);
        }
    }, speed);
}


