const AWS = require('aws-sdk');
const uuid = require('uuid');

const dynamoDb = new AWS.DynamoDB.DocumentClient();

module.exports.postHabilitacion = (event, context, callback) => {

    const params = {
        TableName: 'Habilitacion',
        Item: {
            idHabilitacion: uuid.v1(), //id_maker(?)
            idMaker: event.queryStringParameters.idMaker,
            tipoDeMaquina: event.queryStringParameters.tipoDeMaquina, //tipo_maquina(?)
            Habilitado: event.queryStringParameters.Habilitado, //habilitado_o_no (?)
        }
    };

    dynamoDb.put(params, (error, data) => {
        if(error) {
            console.error(error);
            callback(new Error(error));
            return;
        }

        const response = {
            statusCode: 201,
            body: JSON.stringify({"message": "OK"})
        };

        callback(null, response);
    });
}