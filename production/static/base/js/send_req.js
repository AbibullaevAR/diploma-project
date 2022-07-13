import getCookie from "./get_cookie.js";

export default async function send_req(url, method, dataSend) {
        const XToken = getCookie('csrftoken');
            const options = {
                method: method,
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': XToken
                },
                body: JSON.stringify(dataSend),
            };
            return await fetch(url, options);
    }