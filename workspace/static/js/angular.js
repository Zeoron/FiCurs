var app = angular.module("appLearn", ['ngCookies', 'ngDragDrop', 'ngAnimate']);

app.config(function($interpolateProvider) {
    $interpolateProvider.startSymbol('{[{');
    $interpolateProvider.endSymbol('}]}');
});

app.run(['$http', '$cookies',
    function($http, $cookies) {
        $http.defaults.xsrfCookieName = 'csrftoken';
        $http.defaults.xsrfHeaderName = 'X-CSRFToken';
    }
]);

app.factory('Missatges', function() {
    var missatgeSistema = "";
    return missatgeSistema;
});

app.factory('EnCofre', function() {
    var peixosCofre = []
    return peixosCofre;
});

app.factory('ForaCofre', function() {
    var peixosFora = []
    return peixosFora;
});

app.directive("repeatEnd", function() {
    return {
        restrict: "A",
        link: function(scope, element, attrs) {
            if (scope.$last) {
                scope.$eval(attrs.repeatEnd);
            }
        }
    };
});

//var peixosActius = [];
var mouseX;
var mouseY;
var missatges = $("#panellMissatges");

$(document).on("mousemove", function(event) {
    mouseX = event.pageX;
    mouseY = event.pageY;
});

$("#panell_usuari").hide();
$("#alerta_compra").hide();
$("#obrePerfil").on("click", function() {
    $("#panell_usuari").fadeIn();
});
$("#tancarPerfil").on("click", function() {
    $("#panell_usuari").fadeOut();
});
$("#mesDades").on("click", function() {
    alert("Sergio Rovira Gómez - Institut Cendrassos - 2016")
})

var idGeneralPeixos = 1;
app.controller("Peixera", function($http, $scope, $timeout, ForaCofre, EnCofre, Missatges) {
    //INFORMACIÓ DE L'USUARI
    $scope.infoUsuari = []
    $scope.missatgeSistema = Missatges;

    $scope.monedesPendents = 0;
    $scope.llistaMonedesPendents = [];
    $http.get("https://fi-curs-cloned-srovira.c9users.io/elements/infoUsuari/")
        .success(function(dades) {
            $scope.infoUsuari = dades.resposta;
            missatges.text("Benvingut " + $scope.infoUsuari.nom + " a la teva peixera!");

        });
    var a;
    var timeRebreMonedes;
    $scope.peixosForaCofre = ForaCofre;
    $scope.peixosEnCofre = EnCofre;
    //DROP A LA PEIXERA
    $scope.peixosANedar = function(data, event) {
        if ($scope.peixArrosegant.idDom == null) {
            $http.post("https://fi-curs-cloned-srovira.c9users.io/elements/treurePeix/", {
                idPeix: $scope.peixArrosegant.nom_peix,
            }).success(function(dades) {
                if (dades.resposta == "true") {
                    $scope.peixArrosegant.quantitatpeixera++;
                    var copiedObject = angular.copy($scope.peixArrosegant);
                    copiedObject.x = mouseX - 50;
                    copiedObject.y = mouseY - 20;
                    copiedObject.idGeneral = idGeneralPeixos;
                    $scope.peixosForaCofre.push(copiedObject);
                    idGeneralPeixos += 1;
                    missatgeCorrecte("Peix fora!");
                }
                else {
                    missatgeInCorrecte("No pots treure més peixos!");

                }
            });

        }
    }
    $scope.startMovement = function(event, ui, peix) {
        $scope.peixArrosegant = peix;
    }

    $scope.posaId = function(index, peix) {
        peix.idDom = (index * peix.idGeneral);
    }
    $scope.onEnd = function() {
        $timeout(function() {
            for (var peix = 0; peix < $scope.peixosForaCofre.length; peix++) {
                if ($scope.peixosForaCofre[peix].dom == null) {
                    $scope.peixosForaCofre[peix].dom = $("#" + $scope.peixosForaCofre[peix].idDom);
                }

                if ($scope.peixosForaCofre[peix].x == null) {
                    $scope.peixosForaCofre[peix].x = (Math.floor(Math.random() * (document.body.clientWidth - 0) + 0));
                    $scope.peixosForaCofre[peix].y = (Math.floor(Math.random() * (document.body.clientHeight - 120) + 30));
                }
                $scope.peixosForaCofre[peix].dom.css("left", $scope.peixosForaCofre[peix].x + "px");
                $scope.peixosForaCofre[peix].dom.css("top", $scope.peixosForaCofre[peix].y + "px");

                calcularPosicions($scope.peixosForaCofre[peix]);

            }


        }, 1);
    };


    function calcularPosicions(peix) {
        var tempX = (Math.floor(Math.random() * 801) - 400);
        var tempY = (Math.floor(Math.random() * 401) - 200);
        var tempMov = (Math.floor(Math.random() * (10 - 5) + 5));
        /*while (tempX>=-200 && tempX<=200) {
            tempX = (Math.floor(Math.random() * 500 - 300));
        }*/
        if ((peix.dom.position().left + tempX) < 10) {
            tempX = 50;
        }
        if ((peix.dom.position().left + tempX) > document.body.clientWidth - 100) {
            tempX = -100;
        }

        if ((peix.dom.position().top + tempY) < 100) {
            tempY = 100;
        }
        if ((peix.dom.position().top + tempY) > document.body.clientHeight - 75) {
            tempY = -100;

        }
        if (tempX < 0) {
            if (tempY < 0) {
                TweenMax.to(peix.dom, 2, {
                    rotation: 5,
                });
            }
            if (tempY > 0) {
                TweenMax.to(peix.dom, 2, {
                    rotation: -5,
                });
            }
            TweenMax.to(peix.dom, 0.8, {
                rotationY: 180,
                ease: Power0.easeNone,
            });

            TweenMax.to(peix.dom, tempMov, {
                x: "+=" + tempX,
                y: "+=" + tempY,
                ease: Power0.easeNone,
                onComplete: calcularPosicions,
                onCompleteParams: [peix]
            });
        }
        if (tempX >= 0) {
            if (tempY < 0) {
                TweenMax.to(peix.dom, 2, {
                    rotation: -5,
                });
            }
            if (tempY > 0) {
                TweenMax.to(peix.dom, 2, {
                    rotation: 5,
                });
            }
            TweenMax.to(peix.dom, 0.8, {
                rotationY: 0,
            });
            TweenMax.to(peix.dom, tempMov, {
                x: "+=" + tempX,
                y: "+=" + tempY,
                ease: Power0.easeNone,
                onComplete: calcularPosicions,
                onCompleteParams: [peix]
            });
        }
    }




    timeRebreMonedes = setInterval(rebreMonedes, 20000);
    rebreMonedes();
    var i = 0;

    function rebreMonedes() {
        var tempMonedesPendents = $scope.llistaMonedesPendents.length;
        /*if (tempMonedesPendents <200) {
            tempMonedesPendents = 200;
            alert(tempMonedesPendents);
        }*/
        $http.get("https://fi-curs-cloned-srovira.c9users.io/elements/tiraMonedes/").success(function(dades) {
            var monedesAGenerar = dades.resposta;
            if (dades.resposta > 500) {
                monedesAGenerar = 150;
            }
            for (var a = 0; a < (monedesAGenerar - tempMonedesPendents); a++) {
                var tempMoneda = {
                    'id': i,
                    'x': null,
                    'y': null,
                };
                i++;
                $scope.llistaMonedesPendents.push(tempMoneda);
            }
            $scope.monedesPendents = dades.resposta - $scope.monedesPendents;
        });
    };

    $scope.onEndMonedes = function() {
        $timeout(function() {
            for (var moneda in $scope.llistaMonedesPendents) {
                var selector = $scope.llistaMonedesPendents[moneda];
                selector.dom = $("#moneda" + selector.id);
                selector.dom = $("#moneda" + selector.id);
                if (selector.y == null) {
                    var tempy = (Math.floor(Math.random() * (document.body.clientHeight - 400) + 100));
                    selector.dom.css("top", -(tempy) + "px");
                    selector.y = tempy;
                    var tempx = (Math.floor(Math.random() * (document.body.clientWidth - 200) + 100));
                    selector.dom.css("left", tempx + "px");
                    selector.x = tempx;
                    var caiguda = (Math.floor(Math.random() * (16 - 8) + 8));
                    var final = (Math.floor(Math.random() * (90 - 85) + 85));
                    $("#moneda" + selector.id).animate({
                        top: final + "vh",
                        ease: Power0.easeIn
                    }, caiguda * 1000);
                }
            }
        }, 1);
    }
    $scope.recollirMoneda = function(moneda) {
        var mon = $scope.llistaMonedesPendents.indexOf(moneda);
        $scope.llistaMonedesPendents.splice(mon, 1);
        $scope.infoUsuari.monedes++;
        $http.post("https://fi-curs-cloned-srovira.c9users.io/elements/recollirMoneda/").success(function(dades) {})
    }


});

app.controller("CofreController", function($scope, $http, ForaCofre, EnCofre, Missatges) {
    $scope.missatgeSistema = Missatges;
    $scope.peixosEnCofre = EnCofre;
    $scope.peixosForaCofre = ForaCofre;
    $http.get("https://fi-curs-cloned-srovira.c9users.io/elements/getCofre/")
        .success(function(dades) {
            $scope.peixos = dades.posesions.peixos;
            for (p in $scope.peixos) {
                var peixactual = $scope.peixos[p];
                var total = peixactual.quantitat - peixactual.quantitatpeixera;
                if (total == 0) {
                    $scope.peixosEnCofre.push(peixactual);
                    for (var i = 0; i < peixactual.quantitat; i++) {
                        var copiedObject = jQuery.extend({}, peixactual)
                        copiedObject.idGeneral = idGeneralPeixos;
                        $scope.peixosForaCofre.push(copiedObject);
                        idGeneralPeixos += 1;
                    }
                }
                else {
                    $scope.peixosEnCofre.push(peixactual);
                    for (var i = total; i < peixactual.quantitat; i++) {
                        var copiedObject = jQuery.extend({}, peixactual)
                        copiedObject.idGeneral = idGeneralPeixos;
                        $scope.peixosForaCofre.push(copiedObject);
                        idGeneralPeixos += 1;
                    }
                }
            }
            $scope.deco = dades.deco;
        })
        .error(function(err) {
            alert(err);
        });

    $scope.guardarPeix = function(data, $event) {
        var pees = $scope.peixosForaCofre.indexOf($scope.peixArrosegant);
        $scope.peixosForaCofre.splice(pees, 1);
        $http.post("https://fi-curs-cloned-srovira.c9users.io/elements/guardarPeix/", {
            idPeix: $scope.peixArrosegant.nom_peix,
        }).success(function(dades) {
            missatgeCorrecte("Peix desat correctament!")
        });
        for (peix in $scope.peixosEnCofre) {
            if ($scope.peixosEnCofre[peix].nom_peix == $scope.peixArrosegant.nom_peix) {
                $scope.peixosEnCofre[peix].quantitatpeixera--;
            }
        }
    }
    $scope.aplicaClass = function() {
        $(".temp").addClass("overDrop");
    }
    $scope.removeClass = function() {
        $(".temp").removeClass("overDrop");
    }
});

app.controller("BotigaController", function($scope, $http, EnCofre, Missatges) {
    $scope.missatgeSistema = Missatges;
    $http.get("https://fi-curs-cloned-srovira.c9users.io/elements/totsElements/")
        .success(function(dades) {
            $scope.peixos = dades.elements.peixos;
            $scope.decoracio = dades.elements.deco;
        })
    $scope.comprarPeix = function(peix) {
        $http.post("https://fi-curs-cloned-srovira.c9users.io/elements/compraPeix/", {
            idPeix: peix.nom,
        }).success(function(dades) {
            var temp = EnCofre;
            if (($scope.infoUsuari.monedes - peix.preu) >= 0) {
                $scope.infoUsuari.monedes -= peix.preu;
                $scope.infoUsuari.peixosComprats += 1;
                var trobat = true;
                for (var llistaPeix in temp) {
                    if (peix.nom == temp[llistaPeix].nom_peix) {
                        temp[llistaPeix].quantitat += 1;
                        trobat = false;
                        break;
                    }
                }
                if (trobat) {
                    $("#alerta_compra").fadeIn();
                }
                missatgeCorrecte("Peix afegit al cofre!");
                
            }else {
                missatgeInCorrecte("No tens prous diners!");
                
            }
        });
    }
});

function missatgeCorrecte(text) {
    missatges.text(text);
    missatges.addClass("missatge_correcte");
    setTimeout(function() {
        missatges.text("");
        missatges.removeClass("missatge_correcte")
    }, 1500);
}
function missatgeInCorrecte(text) {
    missatges.text(text);
    missatges.addClass("missatge_incorrecte");
    setTimeout(function() {
        missatges.text("");
        missatges.removeClass("missatge_incorrecte")
    }, 1500);
}