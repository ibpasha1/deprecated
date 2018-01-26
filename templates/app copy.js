$(document).ready(function () {
    var url = "/voo";
    //flask url

	$("#get_info").click(function () {
		var date = $("#date").val();
		var dataString = "date=" + date + "&get_info=";
		if ($.trim(date).length > 0 ) {
			$.ajax({
				type: "POST",
				url: url,
				data: dataString,
				crossDomain: true,
				cache: false,
				beforeSend: function () {
					$("#get_info").val('Connecting...');
				},
				success: function (data) {
					var obj = JSON.parse(data);
					var current_status = obj.status;
					if ($.trim(current_status) == "success") {
						window.location.href = "pending_account.html";
					} else {
						$('#key').html(data);
						$('#status').html(data);
					}

				}
			});
		}
		return false;
	});

	window.onload = function () {
		document.addEventListener("deviceready", init, false);
	}


	$("#login").click(function () {
		var email = $("#email").val();
		var password = $("#password").val();
		var dataString = "email=" + email + "&password=" + password + "&login=";
		if ($.trim(email).length > 0 & $.trim(password).length > 0) {
			$.ajax({
				type: "POST",
				url: url,
				data: dataString,
				crossDomain: true,
				cache: false,
				beforeSend: function () {
					$("#login").val('Connecting...');
				},
				success: function (data) {
					var obj = JSON.parse(data);
					var current_status = obj.status;
					var id = obj.id;
					var active = obj.active;
					var account_type = obj.account_type;
					var ig_user = obj.insta_username;
					var ver_code = obj.verification_code;
					var firstname = obj.first_name;
					var lastname = obj.last_name;
					var streetaddress = obj.street_address;
					var city = obj.city;
					var state = obj.state;
					var zip = obj.zip;
					var gender = obj.gender;
					var booler = 'your account is not activated';
					var age = obj.age;
					//----------Business elements-----------//
					var position = obj.position;
					var business_type = obj.business_type;
					var business_name = obj.business_name;


					if ($.trim(current_status) == "success" && $.trim(active) == "1" && $.trim(account_type) == "0") {
						$('#key').html(id);
						$('#igu').html(ig_user);
						$('#vcode').html(ver_code);
						$('#firstname').html(firstname);
						$('#lastname').html(lastname);
						$('#streetaddress').html(streetaddress);
						$('#city').html(city);
						$('#state').html(state);
						$('#zip').html(zip);
						$('#gender').html(gender);
						$('#active').html(active);
						$('#age').html(age);
						//----------Business elements-----------//
						$('#position').html(position);
						$('#business_type').html(business_type);
						$('#business_name').html(business_name);

						console.log(id);
						console.log(ig_user);
						window.localStorage.setItem("status", current_status);
						window.localStorage.setItem("key", id);
						window.localStorage.setItem("igu", ig_user);
						window.localStorage.setItem("vcode", ver_code);
						window.localStorage.setItem("firstname", firstname);
						window.localStorage.setItem("lastname", lastname);
						window.localStorage.setItem("streetaddress", streetaddress);
						window.localStorage.setItem("city", city);
						window.localStorage.setItem("state", state);
						window.localStorage.setItem("zip", zip);
						window.localStorage.setItem("gender", gender);
						window.localStorage.setItem("age", age);
						//redirection
						window.location.href = "app.in.html";

					} else if ($.trim(current_status) == "success" && $.trim(active) == "1" && $.trim(account_type) == "1") {
						$('#key').html(id);
						$('#igu').html(ig_user);
						$('#vcode').html(ver_code);
						$('#firstname').html(firstname);
						$('#lastname').html(lastname);
						$('#streetaddress').html(streetaddress);
						$('#city').html(city);
						$('#state').html(state);
						$('#zip').html(zip);
						$('#gender').html(gender);
						$('#active').html(active);
						console.log(id);
						console.log(ig_user);
						window.localStorage.setItem("status", current_status);
						window.localStorage.setItem("key", id);
						window.localStorage.setItem("igu", ig_user);
						window.localStorage.setItem("vcode", ver_code);
						window.localStorage.setItem("firstname", firstname);
						window.localStorage.setItem("lastname", lastname);
						window.localStorage.setItem("streetaddress", streetaddress);
						window.localStorage.setItem("city", city);
						window.localStorage.setItem("state", state);
						window.localStorage.setItem("zip", zip);
						window.localStorage.setItem("gender", gender);
						window.localStorage.setItem("age", age);
						//----------Business elements-----------//
						window.localStorage.setItem("position", position);
						window.localStorage.setItem("business_type", business_type);
						window.localStorage.setItem("business_name", business_name);
						//redirection
						window.location.href = "app.bs.html";
					} else if ($.trim(current_status) == "mismatch") {
						window.location.href = "login.html";
						$('#status').html('wrong password or email');
					} else if ($.trim(active) == "0") {
						$('#status').html(booler);
						window.location.href = "pending_account.html";
					}

				}
			});
		}
		return false;
	});


	$("#update_account_in").click(function () {
		var id = $("#id").val();
		var insta_username = $("#insta_username").val();
		var verification_code = $("#verification_code").val();
		var first_name = $("#first_name").val();
		var last_name = $("#last_name").val();
		var street_address = $("#street_address").val();
		var city = $("#city").val();
		var state = $("#state").val();
		var zip = $("#zip").val();
		var gender = $("#gender").val();
		var dataString = 'id=' + id + '&insta_username=' + insta_username + '&verification_code=' + verification_code + '&first_name=' + first_name +
			'&last_name=' + last_name + '&street_address=' + street_address + '&city=' + city + '&state=' + state + '&zip=' + zip + '&gender=' + gender + "&update_account_in=";
		if ($.trim(id).length > 0 & $.trim(first_name).length > 0 & $.trim(insta_username).length > 0) {
			$.ajax({
				type: "POST",
				url: url,
				data: dataString,
				crossDomain: true,
				cache: false,
				beforeSend: function () {
					$("#update_account_in").val('Connecting...');
				},
				success: function (data) {
					var obj2 = JSON.parse(data);
					var insta = obj2.insta_username;
					var ver_code = obj2.verification_code;
					$('#insta_var').html(insta);
					$('#ver').html(ver_code);
					window.localStorage.setItem("insta_var", insta);
					window.localStorage.setItem("ver", ver_code);
					if ($.trim(data) == "error") {
						alert("push fill in all fields");
					}

				}
			});
		}
		return false;
	});


	$("#update_account_bs").click(function () {
		var id = $("#id").val();
		var first_name = $("#first_name").val();
		var last_name = $("#last_name").val();
		var street_address = $("#street_address").val();
		var city = $("#city").val();
		var state = $("#state").val();
		var zip = $("#zip").val();
		var gender = $("#gender").val();
		var position = $("#position").val();
		var business_type = $("#business_type").val();
		var business_name = $("#business_name").val();
		var dataString = 'id=' + id + '&first_name=' +
			first_name + '&last_name=' + last_name + '&street_address=' + street_address + '&city=' + city + '&state=' + state + '&zip=' +
			zip + '&gender=' + gender + '&position=' + position + '&business_type=' + business_type + '&business_name=' + business_name + "&update_account_bs=";
		if ($.trim(id).length > 0 & $.trim(first_name).length > 0) {
			$.ajax({
				type: "POST",
				url: url,
				data: dataString,
				crossDomain: true,
				cache: false,
				beforeSend: function () {
					$("#update_account_bs").val('Connecting...');
				},
				success: function (data) {
					var obj = JSON.parse(data);
					var current_status = obj.status;
					if ($.trim(current_status) == "success") {
						$('#key').html(data);
						$('#status').html(data);
					} else {

					}

				}
			});
		}
		return false;
	});


	


	$("#logout").click(function () {
		localStorage.login = "false";
		localStorage.clear();
		//window.localstorage.setItem("status",current_status);
		//window.localstorage.setItem("key",id);
		window.location.href = "login.html";
	});


});