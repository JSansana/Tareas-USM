const AWS = require('aws-sdk');
const uuid = require('uuid');

const dynamoDb = new AWS.DynamoDB.DocumentClient();

module.exports.postMaquinas = (event, context, callback) => {


    const params = {
        TableName: 'Maquina',
        Item: {
            idMaquina: uuid.v1(),
            nombre: event.queryStringParameters.nombre,
            ubicacion: event.queryStringParameters.ubicacion,
            tipoDeMaquina: event.queryStringParameters.tipoDeMaquina,
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
            body: JSON.stringify({"message": "Maquina Creada!"})
        };

        callback(null, response);
    });
}