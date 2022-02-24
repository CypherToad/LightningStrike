var myTimeout = null;

function createInvoice(loop_index, description, price) {

  var http = new XMLHttpRequest();
  var url = '/invoice/';
  var params = 'description=' + description + '&price=' + price;

  http.open('POST', url , true);
  http.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
  http.send(params);

  http.onreadystatechange = function() {
    if (this.status === 200 && this.readyState === 4) {
      var res = JSON.parse(http.response);
      console.log(res);
      createLightningInvoice(loop_index, res['invoice_id']);
    }
  }

}

function createLightningInvoice(loop_index, invoice_id) {

  var http = new XMLHttpRequest();
  var url = '/ln_invoice/';
  var params = 'invoice_id=' + invoice_id;

  http.open('POST', url , true);
  http.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
  http.send(params);

  http.onreadystatechange = function() {
    if (this.status === 200 && this.readyState === 4) {
      var res = JSON.parse(http.response);
      console.log(res);

      // update button
      document.getElementById('buy-button' + loop_index).style.display = 'none'

      document.querySelector('#Modal' + loop_index + ' .qr-content').style.display = 'block'
      document.getElementById('invoice_id' + loop_index).innerHTML = 'id: ' + invoice_id;
      document.getElementById('ln_invoice_qr' + loop_index).src = res['ln_invoice_qr'];
      document.getElementById('ln_invoice' + loop_index).innerHTML = res['ln_invoice'];
      checkInvoice(loop_index, invoice_id);

    }
  }

}

function getInvoice(loop_index, invoice_id) {

  var http = new XMLHttpRequest();
  var url = '/invoice/' + invoice_id;

  http.open('GET', url , true);
  http.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
  http.send();

  http.onreadystatechange = function() {
    if (this.status === 200 && this.readyState === 4) {
      var res = JSON.parse(http.response);
      console.log(res);

      if (res['state'] == 'PAID') {
        window.location.replace("/receipt/" + invoice_id);
      }
    }
  }

}

function checkInvoice(loop_index, invoice_id) {

  getInvoice(loop_index, invoice_id);
  myTimeout = setTimeout(function(){
    checkInvoice(loop_index, invoice_id);
  }, 5000);

}



function closeModal(loop_index) {
  clearInvoice(loop_index)
  // update button
  document.getElementById('buy-button' + loop_index).style.display = 'inline-block'
  document.querySelector('#Modal' + loop_index + ' .qr-content').style.display = 'none'
}

function clearInvoice(loop_index) {
  document.getElementById('invoice_id' + loop_index).innerHTML = '';
  document.getElementById('ln_invoice_qr' + loop_index).src = '';
  document.getElementById('ln_invoice' + loop_index).innerHTML = '';
  document.getElementById('ln_invoice_text' + loop_index).innerHTML = '';

  clearTimeout(myTimeout);
  myTimeout = null;
}
