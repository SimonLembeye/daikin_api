document.addEventListener("DOMContentLoaded", function (event) {
    fetchData();
    switchButtons();
    console.log(document.getElementById("tank-power-state").textContent === "True");
});

const fetchData = () => {
    axios.get('/data')
        .then(function (response) {
            console.log(response);
        })
        .catch(function (error) {
            console.log(error);
        })
}

const switchButtons = () => {
    if (document.getElementById("tank-power-state").textContent === "True") {
        document.getElementById("start-tank-btn").style.display = 'none';
        document.getElementById("stop-tank-btn").style.display = 'block';
    } else {
        document.getElementById("start-tank-btn").style.display = 'block';
        document.getElementById("stop-tank-btn").style.display = 'none';
    }

    if (document.getElementById("tank-powerfull-state").textContent === "True") {
        document.getElementById("start-tank-powerfull-btn").style.display = 'none';
        document.getElementById("stop-tank-powerfull-btn").style.display = 'block';
    } else {
        document.getElementById("start-tank-powerfull-btn").style.display = 'block';
        document.getElementById("stop-tank-powerfull-btn").style.display = 'none';
    }

    if (document.getElementById("heater-state").textContent === "True") {
        document.getElementById("start-heater-btn").style.display = 'none';
        document.getElementById("stop-heater-btn").style.display = 'block';
    } else {
        document.getElementById("start-heater-btn").style.display = 'block';
        document.getElementById("stop-heater-btn").style.display = 'none';
    }

}

document.getElementById("stop-tank-btn").onclick = () => {
    axios.get('/startstoptank/false')
        .then(function (response) {
            console.log(response);
            location.reload();
        })
        .catch(function (error) {
            console.log(error);
        })
}

document.getElementById("start-tank-btn").onclick = () => {
    axios.get('/startstoptank/true')
        .then(function (response) {
            console.log(response);
            location.reload();
        })
        .catch(function (error) {
            console.log(error);
        })
}


document.getElementById("stop-tank-powerfull-btn").onclick = () => {
    axios.get('/startstoptankpowerfull/false')
        .then(function (response) {
            console.log(response);
            location.reload();
        })
        .catch(function (error) {
            console.log(error);
        })
}

document.getElementById("start-tank-powerfull-btn").onclick = () => {
    axios.get('/startstoptankpowerfull/true')
        .then(function (response) {
            console.log(response);
            location.reload();
        })
        .catch(function (error) {
            console.log(error);
        })
}

document.getElementById("stop-heater-btn").onclick = () => {
    axios.get('/startstopheater/false')
        .then(function (response) {
            console.log(response);
            location.reload();
        })
        .catch(function (error) {
            console.log(error);
        })
}

document.getElementById("start-heater-btn").onclick = () => {
    axios.get('/startstopheater/true')
        .then(function (response) {
            console.log(response);
            location.reload();
        })
        .catch(function (error) {
            console.log(error);
        })
}