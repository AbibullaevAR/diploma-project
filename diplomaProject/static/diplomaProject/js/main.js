import send_req from "../../../../static/base/js/send_req.js";

(function () {
    const addUserBtn = document.querySelector('.main__members .main__news__addNews')
    const addUser = document.querySelector('.main__add-user')
    const formButtonElem = document.querySelector('.form__button')
    const addUserEmailElem = document.querySelector('.addUserEmail')


    addUserBtn.addEventListener('click', function (event) {
        if (addUser.classList.contains('main__add-user_open')) {
            closeElemAddUser()
            return
        }
        openElemAddUser()
    })
    function openElemAddUser() {
        addUser.classList.add('main__add-user_open')
    }
    function closeElemAddUser() {
        addUser.classList.remove('main__add-user_open')
    }

    formButtonElem.addEventListener('click', async function (event) {
        const url = '/accounts/api/create_student/'
        const dataSend = {
                email: addUserEmailElem.value
            }
        await send_req(url, "POST", dataSend)

        closeElemAddUser()
    })
})()