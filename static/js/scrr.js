
var x = document.getElementById("latt");
var x2 = document.getElementById("longg");

function getLocation() {
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(showPosition, showError);
  } else { 
    x.innerHTML = "Geolocation is not supported by this browser.";
    x2.innerHTML = "Geolocation is not supported by this browser.";

  }
}

function showPosition(position) {
  x.value =  position.coords.latitude;
  x2.value =  position.coords.longitude;

}

function showError(error) {
  switch(error.code) {
    case error.PERMISSION_DENIED:
      x.innerHTML = "User denied the request for Geolocation."
      x2.innerHTML = "User denied the request for Geolocation."
      break;
    case error.POSITION_UNAVAILABLE:
      x.innerHTML = "Location information is unavailable."
      x2.innerHTML = "Location information is unavailable."
      break;
    case error.TIMEOUT:
      x.innerHTML = "The request to get user location timed out."
      x2.innerHTML = "The request to get user location timed out."
      break;
    case error.UNKNOWN_ERROR:
      x.innerHTML = "An unknown error occurred."
      x2.innerHTML = "An unknown error occurred."
      break;
  }
}



  
