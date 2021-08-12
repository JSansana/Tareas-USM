const AWS = require('aws-sdk');
const dynamoDb = new AWS.DynamoDB.DocumentClient();

module.exports.getUrls = (event,context,callback) => {
    
    const params = {
        TableName : 'Recurso',
        FilterExpression : 'tipoDeMaquina = :tdm',
        ExpressionAttributeValues : {':tdm' : event.pathParameters.tipoDeMaquina}
      };

    dynamoDb.scan(params, (error,data) => {
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
            body: JSON.stringify(data.Items)
        };

        callback(null, response);
    });
}