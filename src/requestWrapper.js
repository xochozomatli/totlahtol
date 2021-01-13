import axios from 'axios'

export async function secureRequest(conf, successHandler, errorHandler, tokenSetter=token=>null, attemptRefresh=true){
    console.log(arguments);
    const refreshInstance = axios.create({withCredentials: true, validateStatus: function (status){return (status>=200 && status<300) || status===401}})
    try {
        console.log("made it into the try block")
        const res = await refreshInstance(conf)
        console.log(res)
        if (res.status===401){
            console.log("res.status===401 block entered; attemptRefresh==="+attemptRefresh.toString())  
            if (attemptRefresh===true){
                console.log("Attempting Refresh...")
                const refreshRes = await refreshInstance.get('http://localhost:5000/api/refresh')
                const newToken = refreshRes.data
                console.log(newToken)
                tokenSetter(newToken)
                conf.headers.Authorization="Bearer "+newToken.token
                secureRequest(conf, successHandler, errorHandler, tokenSetter, false)
                return null
            }
            throw new Error(res)//attemptRefresh false, reject promise=>401 error=>login page
        }
        successHandler(res)
        console.log("Success Handler Called!")
    } catch(err){
        errorHandler(err)
        console.log("Error Handler Called! Attempt Refresh: "+attemptRefresh)
    }
}