import getCookie from "../../../../static/base/js/get_cookie.js";
(function(){
    let objResultSelected = {}
    if (window.objResultSelected) {
        objResultSelected = window.objResultSelected
    }
    const massivItemSelect = document.querySelectorAll('.tags__item-select')
    const containerDeteteItem = document.querySelector('.tags__container-add-tags')
    const heading = document.querySelector('.tags__heading-selected')
    const send_btn = document.querySelector('.send-button')
    const bodyElem = document.querySelector('.news__descrption')
    const titleElem = document.querySelector('#title')
    const addTagBtn = document.querySelector('#addTagBtn')
    const tagTextElem = document.querySelector('#tagText')

    addTagBtn.addEventListener('click', async function (event){
        await addTag()
    })

    send_btn.addEventListener('click', async function (event) {
        await saveNews()
    })


    heading.addEventListener('click', function (event){
        const className = 'tags__container-selects_open'
        const container = document.querySelector('.tags__container-selects')
        if (container.classList.contains(className)){
            close()
            return
        }
        open(className,container)

    })

    containerDeteteItem.addEventListener('click', function (event){
        const {className} = event.target
        if (className === 'tags__delete'){
            deleteSelected(event.target.dataset)
            renderRezult()
        }
    })

    for (const select of massivItemSelect) {
        select.addEventListener('click', function (event){
            addNewSelected(event.target.dataset)
            renderRezult()
            addHeading(event.target.dataset.tag_name)
            close()
        })
    }


    function addNewSelected (element){
        const {tag_id, tag_name} = element;
        objResultSelected[tag_id] = tag_name
    }
    function deleteSelected (element) {
        const {tag_id, tag_name} = element;
        delete objResultSelected[tag_id]
    }
    function renderRezult (){
        const container = document.querySelector('.tags__container-add-tags')
        let result = ''
        for (const id in objResultSelected){
            const structureHTML = createResultItemStructure({tag_id:id, tag_name: objResultSelected[id]})
            result += structureHTML
        }
        container.innerHTML = result
    }
    function createResultItemStructure (dataRezult){
        const {tag_id, tag_name} = dataRezult
        return `<div class="tags__edit">
        <p class="tags__text">${tag_name}</p>
        <div class="tags__delete" data-tag_id="${tag_id}">
            X
        </div>
    </div>`
    }
    function addHeading (name){
        const heading = document.querySelector('.tags__heading-selected')
        heading.innerHTML = name
    }
    function open (className, container){
        container.classList.add(className)
    }
    function close(){
        const className = 'tags__container-selects_open'
        const container = document.querySelector('.tags__container-selects')
        container.classList.remove(className)
    }

    async function saveNews() {
            let url = ''
            if (window.news_id){
                url = `/news/api/update_news/?pk=${window.news_id}`;
            }else {
                url = '/news/api/update_news/';
            }

            let tags = ''

            if (Object.keys(objResultSelected).length !== 0){
                tags = Object.keys(objResultSelected)
            }else {
                alert('Нужно выбрать хотя-бы один тег')
                return
            }


            const dataSend = {
                title: titleElem.value,
                body: bodyElem.value,
                tags: tags
            }

            await send_req(url, "PUT", dataSend)
            window.location.href = '/diplomaProject/main_page'
    }
    async function addTag(){

        const url = '/news/api/tags/'
        const tagName = tagTextElem.value

        const dataSend = {
                name: tagName
            }

        const data = await send_req(url, "POST", dataSend)
        const tagId = data.headers.get('create_obj_pk')
        objResultSelected[tagId] = tagName
        renderRezult()
    }

    async function send_req(url, method, dataSend) {
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

    renderRezult()
}())