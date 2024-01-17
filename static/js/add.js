var x = 0;
var y = 1;


function addInput() {
	if (x < 15) {
    var str = '<div class="row justify-content-center"><div class="mb-3 col-12"><label for="exampleInputEmail1" class="form-label">Symptom '+ (y + 1) +'</label><input class="form-control form-control-lg" type="text" placeholder="Write down your symptom" aria-label="Пример .form-control-lg" data-bs-theme="light" name="field'+ (y+1)+'" autocomplete="off"></div></div><div id="input' + (x + 1) + '"></div>';
    document.getElementById('input' + x).innerHTML = str;
    x++;
    y++;
  } else
  {
    document.getElementById("addbutton").classList.add('d-none');
  }
}