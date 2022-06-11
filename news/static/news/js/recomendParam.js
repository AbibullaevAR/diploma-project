import getCookie from "../../../../static/base/js/get_cookie.js";
(function (){
    const sliders = document.querySelectorAll('.checkbox')

    for(let slider of sliders){
        slider.addEventListener('change', function(event){
            changeRecomendParam(event)
        })
    }

}())

async function changeRecomendParam(event){
    const {checked} = event.target
    const {tag_id} = event.target.dataset
    let choice_url = `http://127.0.0.1:8000/news/api/update_choice/?pk=${tag_id}`

    const dataSend = {
        tag: tag_id,
        choice: checked
    }
    const XToken = getCookie('csrftoken')
    const options = {
        method: 'PUT',
        headers: {
            'mode': 'no-cors',
            'Content-Type': 'application/json',
            'X-CSRFToken': XToken
        },
        body: JSON.stringify(dataSend),
    }


    const data = await fetch(choice_url, options)
}

