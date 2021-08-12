'use strict'

const AWS = require('aws-sdk');
const uuid = require('uuid');
const dynamoDb = new AWS.DynamoDB.DocumentClient();

module.exports.getNoHabilitados = (event,context,callback) => {
    //Filtro para hacer el escaneo utilizando los query params
    const params = {
        TableName: 'Habilitacion',
        FilterExpression : 'tipoDeMaquina = :this_tipo and Habilitado = :this_bool',
        ExpressionAttributeValues : {':this_tipo' : event.queryStringParameters.tipoDeMaquina, ':this_bool' : "false"}
    };

    dynamoDb.scan(params, (error,data) => {
        if(error){
            console.error(error);
            callback(new Error(error));
            return;
        }
        var arr_habilitados = [];
        data.Items.forEach(function(itemdata) {
            arr_habilitados.push(itemdata.idMaker);
         });

        const response = {
            statusCode: 200,
            body: JSON.stringify({"Habilitados" : arr_habilitados})
        };

        callback(null, response);
    });
}