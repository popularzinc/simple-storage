function upload(files){
  document.getElementById("msg").innerHTML = "<b>Uploading..</b>";
  var ajax = new XMLHttpRequest;
  var formData = new FormData;
  for (let i = 0; i < files.length; i++) {
    formData.append('files', files[i]);
  }
  ajax.onreadystatechange = function() {
      if (this.readyState == 4 && this.status == 200) {
          done(this.responseText);
     }
  };
  ajax.open('POST', '', true);
  ajax.send(formData);
}
function done(response){
  document.getElementById("msg").innerHTML = "<b>Drag here</b> or click to browse";
  window.location.reload();
}
function browsed(e){
  var files = document.getElementById("in").files;
  upload(files);
}

function handleClick(){
  document.getElementById("in").click();
}
function toggle(e){
  if(document.getElementById("blur-section").style.pointerEvents == "none"){
    document.getElementById("blur-section").style.filter = "none";
    document.getElementById("blur-section").style.pointerEvents = "all";
    document.getElementById("focused").style.visibility = "hidden";
  }else{
    //opening
    var link = e.attributes.link.value;
    document.getElementById("blur-section").style.filter = "blur(3px)";
    document.getElementById("blur-section").style.pointerEvents = "none";
    document.getElementById("focused").style.visibility = "visible";
    document.getElementById("image").style.background = "url('"+link+"')";
    document.getElementById("image").style.backgroundSize = "contain";
    document.getElementById("image").style.backgroundRepeat = "no-repeat";
    document.getElementById("image").style.backgroundPosition = "center";
  }
}
function clicked(e){
  var checkedBoxes = document.querySelectorAll('input[name=checkboxes]:checked');
  if(checkedBoxes.length > 0){
    document.getElementById("down").className = "bottom-buttons";
    document.getElementById("del").className = "bottom-buttons-red";
  }else{
    document.getElementById("down").className = "bottom-buttons-disabled";
    document.getElementById("del").className = "bottom-buttons-disabled";
  }
//  if(!e.querySelector('.info').style.visibility = "visible"){
//    if(e.querySelector('.selector').checked == true){
//      e.querySelector('.selector').checked = false;
//    }else{
//      e.querySelector('.selector').checked = true;
//    }
//  }
}
function remove(){
  var checkedBoxes = document.querySelectorAll('input[name=checkboxes]:checked');
  if(checkedBoxes.length > 0){
    if(confirm('Are you sure you want to delete these files?')){

      var ajax = new XMLHttpRequest;
      var formData = new FormData;
      var files = [];
      for (let i = 0; i < checkedBoxes.length; i++) {
        console.log(checkedBoxes[i].value);
        formData.append('files',checkedBoxes[i].value)
      }
      ajax.onreadystatechange = function() {
          if (this.readyState == 4 && this.status == 200) {
            window.location.reload();
         }
      };
      ajax.open('POST', '/delete');
      ajax.send(formData);

    }
  }
}
function download(){
  var checkedBoxes = document.querySelectorAll('input[name=checkboxes]:checked');
  if(checkedBoxes.length > 0){
    var ajax = new XMLHttpRequest;
    var formData = new FormData;
    var files = [];
    for (let i = 0; i < checkedBoxes.length; i++) {
      console.log(checkedBoxes[i].value);
      formData.append('files',checkedBoxes[i].value)
    }
    ajax.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            //window.location.reload();
            //console.log(this.responseText);
            window.location = this.responseText;
       }
    };
    ajax.open('POST', '/downloads');
    ajax.send(formData);
  }
}
function dropHandler(e){
  e.stopPropagation();
  e.preventDefault();
  var files = e.dataTransfer.files;
  document.getElementById("dropzone").style.backgroundColor = "#191922";
  upload(files);
}

function dragleaveHandler(e){
  e.stopPropagation();
  e.preventDefault();
  document.getElementById("dropzone").style.backgroundColor = "#191922";
}

function dragoverHandler(e){
  e.stopPropagation();
  e.preventDefault();
  document.getElementById("dropzone").style.backgroundColor = "white";
}
