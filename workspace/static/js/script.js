$(window).load(function() {
	$(".loading").fadeOut("slow");
});
$(document).ready(function() {
	$(".presenta").find("img").on("click", function() {
		$(".presenta").fadeOut('slow');
	});
	$("#panell_esquerre_boto").on("click", function() {
		if (!$(this).hasClass("boto_desactivat")) {
			$(".panell_esquerre").toggleClass("panell_esquerre_tancat");
			desactivaMenus("panell_esquerre_boto");
		}
	});
	$("#panell_dret_boto").on("click", function() {
		if (!$(this).hasClass("boto_desactivat")) {
			$(".panell_dret").toggleClass("panell_dret_tancat");
			desactivaMenus("panell_dret_boto");
		}
	});
	$("#panell_inferior_boto").on("click", function() {
		if (!$(this).hasClass("boto_desactivat")) {
			$(".panell_inferior").toggleClass("panell_inferior_tancat");
			desactivaMenus("panell_inferior_boto");
		}
	});

	function desactivaMenus(menu) {
		if (menu != "panell_inferior_boto") {
			$("#panell_inferior_boto").toggleClass("boto_desactivat");
		}
		if (menu != "panell_dret_boto") {
			$("#panell_dret_boto").toggleClass("boto_desactivat");
		}
		if (menu != "panell_esquerre_boto") {
			$("#panell_esquerre_boto").toggleClass("boto_desactivat");
		}
	};
});

$("#msjError2:empty").hide();
$("#msjError:empty").hide();
function validarRegistre() {
	$("#msjError2").slideUp();
	if ($("#username").val() != "") {
		if ($("#password").val() != "" && ($("#password").val() == $("#password2").val())) {
			return true;
		}
		else {
			$("#msjError").text("Les contrasenyes no coincideixen");
			$("#password").val("");
			$("#password2").val("");
			$("#msjError").slideDown("slow");
			return false;
		}
	}
	else {
		$("#msjError").text("Error amb l'usuari");
	}

}