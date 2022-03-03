var myTimeout = null;

function createInvoice(description, price) {

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
      createLightningInvoice(res['invoice_id']);
    }
  }

}

function createLightningInvoice(invoice_id) {

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
      document.getElementById('buy-button').style.display = 'none'

      document.querySelector('#Modal' + ' .qr-content').style.display = 'block'
      document.getElementById('invoice_id').innerHTML = 'id: ' + invoice_id;
      document.getElementById('ln_invoice_qr').src = res['ln_invoice_qr'];
      document.getElementById('ln_invoice').innerHTML = res['ln_invoice'];
      document.getElementById('ln_timer').innerHTML = res['expiration_in_sec'];
      checkInvoice(invoice_id);

    }
  }

}

function getInvoice(invoice_id) {

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

function checkInvoice(invoice_id) {

  getInvoice(invoice_id);
  myTimeout = setTimeout(function(){
    checkInvoice(invoice_id);
  }, 5000);

}



function closeModal() {
  clearInvoice()
  // update button
  document.getElementById('buy-button').style.display = 'inline-block'
  document.querySelector('#Modal' + ' .qr-content').style.display = 'none'
}

function clearInvoice() {
  document.getElementById('invoice_id').innerHTML = '';
  document.getElementById('ln_invoice_qr').src = '';
  document.getElementById('ln_invoice').innerHTML = '';
  document.getElementById('ln_timer').innerHTML = '';

  clearTimeout(myTimeout);
  myTimeout = null;
}
