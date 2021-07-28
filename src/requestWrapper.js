import axios from 'axios'

export async function secureRequest(conf, successHandler, errorHandler, tokenSetter=token=>null, attemptRefresh=true){
    const refreshInstance = axios.create({withCredentials: true, validateStatus: function (status){return (status>=200 && status<300) || status===401}})
    try {
        const res = await refreshInstance(conf)
        console.log(res)
        if (res.status===401){
            if (attemptRefresh===true){
                console.log("Attempting Refresh...")
                const refreshRes = await refreshInstance.get('http://dev.localhost:5000/api/refresh')
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
    } catch(err){
        errorHandler(err)
    }
}
