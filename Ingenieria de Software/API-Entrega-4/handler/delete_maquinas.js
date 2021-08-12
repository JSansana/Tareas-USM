const AWS = require('aws-sdk');
const dynamoDb = new AWS.DynamoDB.DocumentClient();

module.exports.deleteMaquinas = (event,context,callback) => {

    
    const params = {
        TableName : 'Maquina',
        Key: {
          idMaquina: event.queryStringParameters.idMaquina
        }
      };

    dynamoDb.delete(params, (error,data) => {
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
            body: JSON.stringify({"message": "Maquina borrada!"})
        };

        callback(null, response);
    });
}
