const AWS = require('aws-sdk');
const uuid = require('uuid');

const dynamoDb = new AWS.DynamoDB.DocumentClient();

module.exports.postRecursos = (event, context, callback) => {

    const data = JSON.parse(event.body);

    const params = {
        TableName: 'Recurso',
        Item: {
            idRecurso: uuid.v1(),
            tipoDeMaquina: event.queryStringParameters.tipoDeMaquina,
            url: event.queryStringParameters.url,
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
            body: JSON.stringify({"message": "Recurso Creado!"})
        };

        callback(null, response);
    });
}