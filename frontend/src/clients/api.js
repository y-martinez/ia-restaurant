class ApiClient {
    constructor() {
        this.baseUrl = process.env.REACT_APP_API_URL;
    }

    async run(endpoint, options={}) {
        options.headers = {
            'Content-Type': 'application/json',
            Accept: 'application/json',
        };

        try {
            const response = await fetch(this.baseUrl + endpoint, options);
            if(response.ok) {
                return {
                    statusCode: response.status,
                    connectionOk: response.ok,
                    data: await response.json()
                };
            }

            return {
                statusCode: response.status,
                connectionOk: response.ok,
                error: this.defaultErrorMessage
            };
            
        } catch(error) {
            console.log(error);
            return { 
                statusCode: 500,
                connectionOk: false,
                error: error.message 
            };
        }
    }
};

export default ApiClient;