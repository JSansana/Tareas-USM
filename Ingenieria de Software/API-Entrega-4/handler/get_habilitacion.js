'use strict'

const AWS = require('aws-sdk');
const uuid = require('uuid');
const dynamoDb = new AWS.DynamoDB.DocumentClient();

module.exports.getHabilitacion = (event,context,callback) => {
    //Filtro para hacer el escaneo utilizando los query params
    const params = {
        TableName: 'Habilitacion',
        FilterExpression : 'idMaker = :this_id and tipoDeMaquina = :this_tipo',
        ExpressionAttributeValues : {':this_id' : parseInt(event.queryStringParameters.idMaker), ':this_tipo' : event.queryStringParameters.tipoDeMaquina}
    };

    dynamoDb.scan(params, (error,data) => {
        if(error){
            console.error(error);
            callback(new Error(error));
            return;
        }

        //Retorno del metodo utilizando el dato entregado por el escaneo
        const response = {
            statusCode: 200,
            body: JSON.stringify({"Habilitado" : data.Items[0].Habilitado})
        };

        callback(null, response);
    });
}