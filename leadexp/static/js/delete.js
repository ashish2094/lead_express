let groupCheck = Array.from(document.getElementsByName("delitem"));
let sepCheck = document.getElementById("del-all");
let frm_get = document.getElementById("formget");
let frm_post = document.getElementById("formpost");
let filter = document.getElementById("filter");
let del = document.getElementById("delete");

sepCheck.onchange = () => {
  if (sepCheck.checked) {
    groupCheck.forEach((element) => {
      element.checked = true;
    });
  } else {
    groupCheck.forEach((element) => {
      element.checked = false;
    });
  }
};
