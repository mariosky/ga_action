var openwhisk = require('openwhisk');
var request = require('request');


/**
  *
  * main() will be run when you invoke this action
  *
  * @param Cloud Functions actions accept a single parameter, which must be a JSON object.
  *
  * @return The output of this action, which must be a JSON object.
  *
  */
function main(params){

    return new Promise(function(resolve, reject) {

        console.log("Found", params.messages.length, "messages");

        var tasks = params.messages.map(function(message) {
            console.log("Found", message.value.experiment.owner);
            actionName = "testPromise";
            params = message.value;

            return new Promise(function (actionName, params, resolve, reject) {
                console.log("Calling", actionName);
                var wsk = openwhisk();
                return new Promise(function (resolve, reject) {
                    wsk.actions.invoke(actionName, kwargs).then(
                        function (activation) {
                            console.log(actionName, "[activation]", activation);
                            resolve(activation);
                        }).catch(
                        function (error) {
                            console.log(actionName, "[error]", error);
                            reject(error);
                        });

                });

            });
        });

        return Promises.All(tasks, function(err, result) {
                if (err) {
                    console.log("Error", err);
                    reject(err);
                } else {
                    resolve({
                    status: "Success"
                    });
            }}).then(function(values) {
                      console.log(values);
                    });

});

}



