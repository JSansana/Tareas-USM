const AWS = require('aws-sdk');
const dynamoDb = new AWS.DynamoDB.DocumentClient();

module.exports.deleteRecursos = (event,context,callback) => {

    const data = JSON.parse(event.body);

    const params = {
        TableName : 'Recurso',
        Key: {
          idRecurso: event.queryStringParameters.idRecurso
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
            body: JSON.stringify({"message": "Recurso borrada!"})
        };

        callback(null, response);
    });
}
