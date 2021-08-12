const AWS = require('aws-sdk');

const dynamoDB = new AWS.DynamoDB.DocumentClient();

module.exports.putPersonaH = (event,context,callback) => {
    

    const params = {
        TableName: 'Habilitacion',
        Key: {
            idHabilitacion: event.queryStringParameters.idHabilitacion
        },
        UpdateExpression: 'set idMaker=:i, tipoDeMaquina=:tdm, Habilitado=:h',
        ExpressionAttributeValues: {
            ':i' : event.queryStringParameters.idMaker,
            ':tdm':  event.queryStringParameters.tipoDeMaquina,
            ':h': event.queryStringParameters.Habilitado
        },
        ReturnValues:"UPDATED_NEW"
    };

    dynamoDB.update(params, (error,data) => {
        if(error){
            console.error(error);
            callback(new Error(error));
            return;
        }

        const response = {
            statusCode: 200,
            headers: {
                "Access-Control-Allow-Origin": "*"
            },
            body: JSON.stringify({"message": "Data actualizada"})
        };
        callback(null,response);
    });
}