var x = 0;

function myFunction1() {
  const prorgess = document.querySelector('.mark1');
  document.getElementById("m1").innerHTML = "Chosen";
  document.getElementById("m2").innerHTML = "";
  document.getElementById("m3").innerHTML = "";
  x = 1;
  //alert(prorgess.dataset.userid + " + " + prorgess.dataset.cardid);
  fetch("/progress/" + prorgess.dataset.userid + "/" + prorgess.dataset.cardid + "/" + prorgess.dataset.mark).then(
    response => console.log(response)
  ).catch(
    err => console.log(err)
  )
}

function myFunction2() {
  const prorgess = document.querySelector('.mark2');
  document.getElementById("m2").innerHTML = "Chosen";
  document.getElementById("m1").innerHTML = "";
  document.getElementById("m3").innerHTML = "";
  x = 1;
  //alert(prorgess.dataset.userid + " + " + prorgess.dataset.cardid);
  fetch("/progress/" + prorgess.dataset.userid + "/" + prorgess.dataset.cardid + "/" + prorgess.dataset.mark).then(
    response => console.log(response)
  ).catch(
    err => console.log(err)
  )
}

function myFunction3() {
  const prorgess = document.querySelector('.mark3');
  document.getElementById("m3").innerHTML = "Chosen";
  document.getElementById("m1").innerHTML = "";
  document.getElementById("m2").innerHTML = "";
  x = 1;
  //alert(prorgess.dataset.userid + " + " + prorgess.dataset.cardid);
  fetch("/progress/" + prorgess.dataset.userid + "/" + prorgess.dataset.cardid + "/" + prorgess.dataset.mark).then(
    response => console.log(response)
  ).catch(
    err => console.log(err)
  )
}

function clickfunction(){
  
}

