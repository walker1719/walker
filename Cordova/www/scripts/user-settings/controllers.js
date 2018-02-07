'use strict';

var geotrekUserSettings = angular.module('geotrekUserSettings');

geotrekUserSettings.controller('UserSettingsController',
    ['$ionicPlatform', '$rootScope', '$state', '$scope', 'settings', '$q', '$ionicPopup', 'utils', 'globalSettings', '$cordovaFile', '$translate','localeSettings', 'userSettingsService', 'networkSettings', 'globalizationService', 'mapFactory', 'treksFactory', 'logging',
    function ($ionicPlatform, $rootScope, $state, $scope, settings, $q, $ionicPopup, utils, globalSettings, $cordovaFile, $translate, localeSettings, userSettingsService, networkSettings, globalizationService, mapFactory, treksFactory, logging) {

    // To have a correct 2-ways binding, localeSettings and networkSettings are used for
    // 1/ select markup initialization
    function getAvailableLanguages() {
        var availableLanguages = {},
            langLength = 0;
        angular.forEach(localeSettings, function (language, languageCode) {
            if (globalSettings.AVAILABLE_LANGUAGES.indexOf(languageCode) > -1) {
                availableLanguages[languageCode] = language;
                langLength ++;
            }
        });
        $scope.languages = availableLanguages;
        $scope.langLength = langLength;
    }
    getAvailableLanguages();
    $scope.connections = networkSettings;

    function somethingToDelete () {
        if (window.cordova) {
            $cordovaFile.listDir(settings.device.RELATIVE_TILES_ROOT)
                .then(function(listFiles) {
                    var detailedTilesArePresent = false;
                    for (var i = listFiles.length - 1; i >= 0; i--) {
                        var currentFile = listFiles[i];
                        if (currentFile.isDirectory && parseInt(currentFile.name, 10) > 12) {
                            detailedTilesArePresent = true;
                        }
                    }
                    $scope.cleanIsDisabled = !detailedTilesArePresent;
                });
        } else {
            $scope.cleanIsDisabled = false;
        }
    }

    somethingToDelete();

    // AND
    // 2/ initialize select with saved user settings
    userSettingsService.getUserSettings().then(function(userSettings){
            var scopeUserSettings = {
                currentLanguage: localeSettings[userSettings.currentLanguage],
                synchronizationMode: networkSettings[userSettings.synchronizationMode],
                alertOnPois: userSettings.alertOnPois
            };
            $scope.userSettings = scopeUserSettings;
        }
    );

    // If current language is modified, translating text
    $scope.$watch('userSettings.currentLanguage', function() {
        var chosenLanguage = $scope.userSettings.currentLanguage.locale;
        globalizationService.translateTo(chosenLanguage);
    });

    // If user settings are modified, saving them
    $scope.$watch('userSettings', function() {
        userSettingsService.saveUserSettings($scope.userSettings);
    }, true);

    $scope.cleanFiles = function() {
        $translate([
            'usersettings_controller_cleanmaps_confirm_title',
            'usersettings_controller_cleanmaps_confirm_label',
            'user_parameters.cancel'
        ]).then(function(translations) {
            var confirmPopup = $ionicPopup.confirm({
                title: translations.usersettings_controller_cleanmaps_confirm_title,
                template: translations.usersettings_controller_cleanmaps_confirm_label,
                cancelText: translations['user_parameters.cancel']
            });

            confirmPopup.then(function(confirmed) {
                if(confirmed) {
                    utils.showSpinner();
                    $q.all([
                        mapFactory.cleanDownloadedLayers()
                        .then(
                            function(result) {
                            }, function(error) {
                                logging.error(error);
                            }
                        ),
                        treksFactory.removeDownloadedImages()
                        .then(
                            function() {
                            }, function(error) {
                                console.error(error);
                            }
                        )
                    ])
                    .then(
                        function(result) {
                            // Disabling delete button to inform user that delete is done
                            $scope.cleanIsDisabled = true;
                            utils.hideSpinner();
                        }, function(error) {
                            console.error(error);
                        }
                    );
                }
            });
        });
    };

    $scope.exitApp = function() {
        ionic.Platform.exitApp()
    };

    $scope.contacts = [];

    $scope.contacts=JSON.parse(localStorage.getItem("numeros"));


    $scope.addContact = function () {
          var data = document.getElementById("inputtext").value;

          var numeropresent=0;
          for(var i=0; i<$scope.contacts.length; i++){
              if(data === $scope.contacts[i]){
                numeropresent = numeropresent + 1;
              }
          }

          if(numeropresent === 0){
            if(data.length==10){
              $scope.contacts.push(data);
              $scope.formTodoText = '';
              localStorage.setItem("numeros", JSON.stringify($scope.contacts));
            }
            else{
              alert('pas assez de chiffre');
            }
          }
          else{
            alert('Le numéro est déjà présent dans la liste');
          }
    };

    $scope.removeContact = function () {
          // remove an item
          $scope.contacts.splice(this.$index, 1);
          localStorage.setItem("numeros", JSON.stringify($scope.contacts));

    };
    // onSuccess Callback
  // This method accepts a Position object, which contains the
  // current GPS coordinates
  //
  /*function getPosition (){
    var onSuccess = function(position) {
      var coordonnees = [ position.coords.latitude,position.coords.longitude ];
      return coordonnees;
        alert('Latitude: '          + position.coords.latitude          + '\n' +
              'Longitude: '         + position.coords.longitude         + '\n' +);

    };

    // onError Callback receives a PositionError object
    //
    function onError(error) {
        alert('code: '    + error.code    + '\n' +
              'message: ' + error.message + '\n');
    }

    geotrekGeolocation.getCurrentPosition(onSuccess, onError);
  };*/
  // current GPS coordinates

    var ok=0;
    $scope.positioncoord = function(){

    };



   $scope.send_from_phone = function(n){
     var message;
     var ok=0;
          var numero =  (JSON.parse(localStorage.getItem("numeros")));

          if(n===1 ){
            alert("Avez-vous bien activé votre GPS ?")
            var onSuccess = function(position) {
                  var latitude=JSON.stringify(position.coords.latitude);
                  var longitude= JSON.stringify(position.coords.longitude);

                  message = "SOS: Votre proche vous a défini comme contact d'urgence. Une chute a été détecté.\n\nVoici sa position:\n"+ "Latitude: " + latitude + "\nLongitude: " +longitude+"\n\nCliquez ici pour voir dans Google Maps:\n"+"http://maps.google.com/maps?q=loc:"+latitude+","+longitude+"\n-- WALKER";
                  for (var i=0; i<numero.length; i++) {
                    sms.send(numero[i],message,{}, function(message) {
                      ionicPopup.alert(
                          'Message to ' + numero[i] + ' has been sent.',
                          null,
                          'Message Sent',
                          'Done'
                      );

                    }, function(error) {
                      navigator.notification.alert(
                        'Sorry, message not sent: ' + error.message,
                        null,
                        'Error',
                        'Done'
                      );
                    });
                  }
              };
            // onError Callback receives a PositionError object
            //
            function onError(error) {
                alert('code: '    + error.code    + '\n' +
                      'message: ' + error.message + '\n');
            }

             navigator.geolocation.getCurrentPosition(onSuccess, onError);

          }
          if(n===2){
             message = "Votre proche est bien arrivé à destination pour sa randonnée !\n-- WALKER";
             for (var i=0; i<numero.length; i++) {
               sms.send(numero[i],message,{}, function(message) {
                 ionicPopup.alert(
                     'Message to ' + numero[i] + ' has been sent.',
                     null,
                     'Message Sent',
                     'Done'
                 );

               }, function(error) {
                 navigator.notification.alert(
                   'Sorry, message not sent: ' + error.message,
                   null,
                   'Error',
                   'Done'
                 );
               });
             }
          }


    };

    $scope.transfert = function(){
        localStorage.setItem("numeros", JSON.stringify($scope.contacts));

        bluetoothSerial.isEnabled(
            function() {
                //disconnect if already connected, connect if not already connected
                bluetoothSerial.isConnected(disconnect, connect);
            },
            function() {
                $ionicPopup.alert({
                    title: 'Bluetooth désactivé',
                    template: 'Vous devez activer le bluetooth de votre téléphone avant de continuer.'
                });
            }
        );
    };

    function connect() {
        var macAddress = "B8:27:EB:B3:1B:FA";
        // if not connected, do this:
        display("Connexion en cours");
        // attempt to connect:
        bluetoothSerial.connect(
            macAddress,  // device to connect to
            openPort,    // start listening if you succeed
            function() { // show message if failure
                $ionicPopup.alert({
                    title: 'Bracelet non appairé',
                    template: 'Vous devez vous appairer au bracelet avant de continuer.'
                });
            }
        );
    }

    function disconnect() {
        bluetoothSerial.write("3;\n",display("Déconnexion en cours"),display("Déconnexion en cours"));
        // if connected, do this:
        bluetoothSerial.disconnect(
            closePort,     // stop listening to the port
            showError      // show the error if you fail
        );
    }

    function send(){
      //GO FIND the datas stocked in the local storage of the phone
      var storedNames = (JSON.parse(localStorage.getItem("numeros")));
      var success = function (){
          display("Envoyé");
          //ON attend 1seconde avant l'appel de la fonction disconnect
          setTimeout(function() {   disconnect(); }, 4000);
      }
      var failure = function (){
          display("Non envoyé");
      }
      bluetoothSerial.write("2;"+storedNames+"\n", success, failure);
    }



    /*
        subscribes to a Bluetooth serial listener for newline
        and changes the button:
    */
    function openPort() {
        var macAddress = "B8:27:EB:B3:1B:FA";
        // if you get a good Bluetooth serial connection:
        display("Connecté à: " + macAddress);
        // set up a listener to listen for newlines
        // and display any new data that's come in since
        // the last newline:
        bluetoothSerial.subscribe('\n', function (data) {
            clear();
            display(data);
        });
        setTimeout(function() {   send(); }, 2000);

    }

    /*
        unsubscribes from any Bluetooth serial listener and changes the button:
    */
    function closePort() {
        var macAddress = "B8:27:EB:B3:1B:FA";
        // if you get a good Bluetooth serial connection:
        display("Déconnecté de: " + macAddress);
        // unsubscribe from listening:
        bluetoothSerial.unsubscribe(
                function (data) {
                    display("Déconnecté");
                    clear();
                },
                showError
        );
    }
    /*
        appends @error to the message div:
    */
    function showError(error) {
        display(error);
    }

    /*
        appends @message to the message div:
    */
    function display(message) {
        document.getElementById("connectButton").style.display = "none";
        document.getElementById("message").innerHTML = message;
    }
    /*
        clears the message div:
    */
    function clear() {
        document.getElementById("connectButton").style.display = "block";
        document.getElementById("message").innerHTML = "";
    }

}]);
